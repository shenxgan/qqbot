import os
import json
import time
import importlib
import mimetypes
import shutil
import zipfile

from functools import wraps
from pathlib import Path

from sanic import Blueprint
from sanic import exceptions
from sanic import response
from sanic.log import logger

from utils import get_files_hash

webqq = Blueprint('webqq', url_prefix='/webqq')

webqq.static('/static/', './static/')


def authorized():
    """鉴权"""
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            sign = request.args.get('sign')
            is_authorized = sign and sign == request.app.ctx.sign
            if is_authorized or os.environ.get('ENV') == 'test':
                response = await f(request, *args, **kwargs)
                return response
            else:
                raise exceptions.Unauthorized()
        return decorated_function
    return decorator


@webqq.get('/')
@authorized()
async def index(request):
    with open('index.html') as f:
        html = f.read()
    return response.html(html)


def save_private_msg(request):
    """存储主动发送的私聊消息
    机器人发送的群聊消息，会自动获取一遍
    私聊消息，需要主动在发送的时候存储一遍
    """
    data = request.json
    msg = data['msg']
    user_id = int(data['group_id'][2:])
    self_id = 123456  # 机器人的qq号，没有获取，随机指定一个值
    _time = int(time.time())
    _data = {
        "message_type": "private",
        "message_id": _time,
        "user_id": self_id,
        "message": [
            {
                "type": "text",
                "data": {
                    "text": msg
                }
            }
        ],
        "raw_message": msg,
        "font": 0,
        "sender": {
            "user_id": self_id,
            "nickname": "我",  # 机器人昵称，随意
            "sex": "unknown"
        },
        "target_id": user_id,
        "time": _time,
        "self_id": self_id,
        "post_type": "message",
        "group_id": data['group_id']
    }
    request.app.ctx.msgs[data['group_id']].append(_data)


@webqq.post('/msgs')
@authorized()
async def post_msgs(request):
    """获取、发送消息"""
    data = request.json
    if 'msg' in data:
        msg = data['msg']
        if data['group_id'][:2] == 'qq':  # 私聊消息
            ret = {
                'action': 'send_private_msg',
                'params': {
                    'user_id': int(data['group_id'][2:]),
                    'message': msg,
                }
            }
            save_private_msg(request)
        else:  # 群组消息
            ret = {
                'action': 'send_group_msg',
                'params': {
                    'group_id': int(data['group_id']),
                    'message': msg,
                }
            }
        await request.app.ctx.ws.send(json.dumps(ret))
        return response.empty()
    else:  # get msg data
        last_msg_ids = data['last_msg_ids']
        msgs = {}
        for k, v in request.app.ctx.msgs.items():
            k = str(k)
            if k not in last_msg_ids:
                msgs[k] = list(v)
                continue
            for i, msg in enumerate(v):
                if msg['message_id'] == last_msg_ids[k]:
                    vv = list(v)[i+1:]
                    if vv:
                        msgs[k] = vv
                    break
        return response.json(msgs)


@webqq.get('/groups')
@authorized()
async def get_group_list(request):
    """获取群组列表信息"""
    request.app.ctx.delete_groups.clear()
    return response.json(request.app.ctx.group_id_name)


@webqq.delete('/groups/<group_id>')
@authorized()
async def delete_group(request, group_id):
    """删除本地群组记录"""
    if group_id[:2] != 'qq':
        group_id = int(group_id)
    del request.app.ctx.msgs[group_id]
    request.app.ctx.delete_groups.add(group_id)
    return response.empty()


@webqq.post('/action')
@authorized()
async def post_action(request):
    """一些动作"""
    data = request.json
    action = data['action']
    if action == 'delete_msg':  # 撤回消息
        params = {
            'message_id': data['message_id'],
        }
    elif action == 'set_group_ban':  # 群组单人禁言
        params = {
            'group_id': data['group_id'],
            'user_id': data['user_id'],
            'duration': data.get('duration', 150),
        }
    ret = {
        'action': action,
        'params': params,
    }
    await request.app.ctx.ws.send(json.dumps(ret))
    return response.empty()


def generate_tree(directory, prefix, tree):
    """获取与 `tree` 命令类似的目录结构"""
    entries = sorted(directory.iterdir(), key=lambda e: e.name)
    entries_count = len(entries)

    for index, entry in enumerate(entries):
        if entry.name == '__pycache__':
            continue
        connector = '├── ' if index < entries_count - 1 else '└── '  # 选择连接符
        line = prefix + connector + entry.name
        tree.append(line)

        if entry.is_dir():  # 递归处理子目录
            new_prefix = prefix + (
                '│   ' if index < entries_count - 1 else '    ')
            generate_tree(entry, new_prefix, tree)


def is_text_file(file_path):
    text_extensions = {
        '.txt', '.md', '.json', '.csv', '.xml', '.html', '.css', '.js',
        '.py', '.java', '.c', '.cpp', '.h', '.sh'}  # 常见文本文件扩展名
    if file_path.suffix in text_extensions:
        return True
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type is not None and mime_type.startswith('text')


def dir_to_json(path):
    """获取目录的层次结构"""
    base_path = Path(path)

    def traverse(directory):
        result = {
            'id': str(directory.relative_to(base_path)),
            'label': directory.name,
            'children': [],
        }
        try:
            entries = sorted(directory.iterdir(), key=lambda e: e.name)
            for entry in entries:
                if entry.name == '__pycache__':
                    continue
                if entry.is_dir():
                    result['children'].append(traverse(entry))
                elif is_text_file(entry):
                    result['children'].append({
                        'id': str(entry.relative_to(base_path)),
                        'label': entry.name,
                    })
        except PermissionError:
            pass  # 忽略无权限访问的目录
        return result
    return traverse(Path(path))


@webqq.get('/plugins')
@authorized()
async def get_plugin_list(request):
    """获取插件列表"""
    plugins = []
    for k, v in request.app.ctx.plugins.items():
        instance = v['instance']
        path = f'plugins/{k}'
        tree = [f'ws/{path}']
        generate_tree(Path(path), '', tree)
        plugin = {
            'name': k,
            'type': instance.type,
            'is_open': instance.is_open,
            'desc': instance.__doc__ or '',
            'last_run': instance.last_run,
            'run_times': instance.run_times,
            'tree': '\n'.join(tree),
        }
        plugin['desc'] = plugin['desc'].split('\n')[0]
        plugins.append(plugin)
    return response.json(plugins)


@webqq.post('/plugins')
@authorized()
async def post_plugins(request):
    """添加插件"""
    data = request.json
    logger.info(data)
    fpath = data['fpath']
    name = fpath.rsplit('/', 1)[1].split('.')[0]

    with zipfile.ZipFile(fpath, 'r') as zip_ref:
        file_list = zip_ref.namelist()

        # 检查 ZIP 是否所有文件都在一个相同的根目录下
        top_dirs = {f.split('/')[0] for f in file_list if '/' in f}

        if len(top_dirs) == 1:
            extract_to = os.path.join('plugins')  # 直接解压到 output
        else:
            extract_to = os.path.join('plugins', name)

        os.makedirs(extract_to, exist_ok=True)
        zip_ref.extractall(extract_to)
    # 加载插件 load_plugin
    try:
        if name in request.app.ctx.plugins:
            raise Exception('存在同名插件，跳过')
        logger.info(f'加载插件 {name}')
        x = importlib.import_module(f'plugins.{name}.main')
        request.app.ctx.plugins[name] = {
            'instance': x.Plugin(),
            'hash': get_files_hash(f'plugins/{name}'),
        }
    except Exception as e:
        logger.error(f'插件 {name} 加载失败：{e}')
    return response.empty()


@webqq.get('/plugins/<name>')
@authorized()
async def get_plugin(request, name):
    """获取插件详情"""
    fpath = request.args.get('fpath')
    data = {}
    if fpath:
        fpath = f'plugins/{name}/{fpath}'
        with open(fpath) as f:
            fdata = f.read()
        data = {
            'fdata': fdata,
            'dir_tree': [dir_to_json(f'plugins/{name}')],
        }
    return response.json(data)


@webqq.put('/plugins/<name>')
@authorized()
async def put_plugin(request, name):
    """更新插件"""
    data = request.json
    logger.info(data)
    action = data['action']
    plugin = request.app.ctx.plugins[name]
    if action == 'is_open':
        x = importlib.import_module(f'plugins.{name}.main')
        plugin['instance'].is_open = not plugin['instance'].is_open
        plugin['instance'].save_config()
        plugin['instance'] = x.Plugin()
    elif action == 'reload':
        x = importlib.import_module(f'plugins.{name}.main')
        plugin['instance'] = x.Plugin()
    elif action == 'code':
        fpath = data['fpath']
        fpath = f'plugins/{name}/{fpath}'
        with open(fpath, 'w') as f:
            f.write(data['code'])
    return response.empty()


@webqq.delete('/plugins/<name>')
@authorized()
async def delete_plugin(request, name):
    """删除插件"""
    del request.app.ctx.plugins[name]
    path = Path(f'plugins/{name}')
    shutil.rmtree(path)  # 递归删除目录及其内容
    return response.empty()


@webqq.get('/plugins/store')
@authorized()
async def get_plugin_store_list(request):
    """获取插件市场中的插件列表"""
    plugins = []
    with open('/tmp/store.data.js') as f:
        data = f.read()
    name = None
    fpath = None
    for line in data.split('\n'):
        line = line.strip()
        if line.startswith('name'):
            name = line.split("'")[1]
        if line.startswith('downloadUrl') and line.endswith(".zip',"):
            fpath = line.split("'")[1]
            fpath = fpath.replace('/qqbot/static/file', '/tmp/store')
            plugins.append({
                'name': name,
                'fpath': fpath,
            })
    return response.json(plugins)
