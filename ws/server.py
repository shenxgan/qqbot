import importlib
import json
import os

from functools import wraps

from sanic import Sanic
from sanic import response
from sanic import exceptions
from sanic.log import logger

from message import group_msg
from notice import notice
from cron import cron_job

app = Sanic('qqbot')
app.static('/webqq/static/', './static/')


@app.before_server_start
async def init(app):
    """初始化"""
    app.ctx.msgs = {}               # 所有群组消息
    app.ctx.msg_maxlen = 100        # 每个群组保存的历史消息条数
    app.ctx.sign = None             # 网页qq鉴权sign
    app.ctx.group_id_name = {}      # 群组id与名称对应关系
    app.ctx.delete_groups = set()   # 当前过滤不查看的群组


@app.before_server_start
async def load_plugins(app):
    """加载所有插件，并初始化"""
    app.ctx.plugins = []
    for de in os.scandir('plugins'):
        if not de.is_dir():
            continue
        if de.name == '__pycache__':
            continue
        try:
            logger.info(f'加载插件 {de.name}')
            x = importlib.import_module(f'plugins.{de.name}.main')
            app.ctx.plugins.append(x.Plugin())
        except Exception as e:
            logger.error(f'插件 {de.name} 加载失败：{e}')


@app.websocket('/qqbot')
async def qqbot(request, ws):
    """QQ机器人"""
    app.ctx.ws = ws
    app.add_task(cron_job())
    await ws.send(json.dumps({'action': 'get_group_list'}))

    while True:
        data = await ws.recv()
        data = json.loads(data)
        logger.debug(json.dumps(data, indent=4, ensure_ascii=False))

        post_type = data.get('post_type')
        # 根据消息类型、内容来进行分别处理
        if post_type == 'message' or post_type == 'message_sent':
            if data.get('message_type') == 'group' and data.get('raw_message'):
                await group_msg(ws, data)
        elif post_type == 'notice':
            await notice(ws, data)
        elif isinstance(data.get('data'), list):
            app.ctx.group_id_name = {
                g['group_id']: g['group_name'] for g in data['data']}
        else:
            if data.get('meta_event_type') == 'heartbeat':
                continue
            logger.info(json.dumps(data, indent=4, ensure_ascii=False))


def authorized():
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


@app.get('/webqq/')
@authorized()
async def index(request):
    with open('index.html') as f:
        html = f.read()
    return response.html(html)


@app.post('/webqq/msgs')
@authorized()
async def post_msgs(request):
    data = request.json
    if 'msg' in data:
        msg = data['msg']
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


@app.get('/webqq/groups')
@authorized()
async def get_group_list(request):
    request.app.ctx.delete_groups.clear()
    return response.json(request.app.ctx.group_id_name)


@app.delete('/webqq/group/<group_id:int>')
@authorized()
async def delete_group(request, group_id):
    del request.app.ctx.msgs[group_id]
    request.app.ctx.delete_groups.add(group_id)
    return response.empty()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, auto_reload=True, workers=1)
