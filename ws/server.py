import os
import importlib
import json

from sanic import Sanic
from sanic.log import logger

from message import group_msg, private_msg
from notice import notice
from cron import cron_job
from utils import get_files_hash

from webqq import webqq

app = Sanic('qqbot')
app.blueprint(webqq)


@app.before_server_start
async def init(app):
    """初始化"""
    app.ctx.msgs = {}               # 所有群组消息
    app.ctx.msg_maxlen = 50         # 每个群组保存的历史消息条数
    app.ctx.sign = None             # 网页qq鉴权sign
    app.ctx.group_info = {}         # 群组id与群信息的对应关系
    app.ctx.myfaces = []            # 机器人的收藏表情列表
    app.ctx.delete_groups = set()   # 当前过滤不查看的群组
    app.ctx.user_last_ts = {}       # 用户频率限制，记录触发的时间戳
    app.ctx.user_id_name = {}       # QQ号与昵称对应关系


@app.before_server_start
async def load_plugins(app):
    """加载所有插件，并初始化"""
    app.ctx.plugins = {}
    for de in os.scandir('plugins'):
        if not de.is_dir():
            continue
        if de.name == '__pycache__':
            continue
        try:
            logger.info(f'加载插件 {de.name}')
            x = importlib.import_module(f'plugins.{de.name}.main')
            app.ctx.plugins[de.name] = {
                'instance': x.Plugin(),
                'hash': get_files_hash(f'plugins/{de.name}'),
            }
        except Exception as e:
            logger.error(f'插件 {de.name} 加载失败：{e}')


@app.websocket('/qqbot')
async def qqbot(request, ws):
    """QQ机器人"""
    app.ctx.ws = ws
    app.add_task(cron_job())
    await ws.send(json.dumps({'action': 'get_group_list'}))
    await ws.send(json.dumps({
        'action': 'fetch_custom_face',
        'params': {
            'count': 120,
        }
    }))

    while True:
        data = await ws.recv()
        data = json.loads(data)
        logger.debug(json.dumps(data, indent=4, ensure_ascii=False))

        post_type = data.get('post_type')
        # 根据消息类型、内容来进行分别处理
        if post_type == 'message' or post_type == 'message_sent':
            if data.get('message_type') == 'group' and data.get('raw_message'):
                await group_msg(ws, data)
            elif data.get('message_type') == 'private':
                await private_msg(ws, data)
        elif post_type == 'notice':
            await notice(ws, data)
        elif isinstance(data.get('data'), list):
            logger.info(json.dumps(data, indent=4, ensure_ascii=False))
            if isinstance(data['data'][0], dict) \
                    and 'group_id' in data['data'][0]:  # 获取群列表
                app.ctx.group_info = {g['group_id']: g for g in data['data']}
            elif isinstance(data['data'][0], str) \
                    and data['data'][0].startswith('http'):
                app.ctx.myfaces = data['data']
        else:
            if data.get('meta_event_type') == 'heartbeat':
                continue
            logger.info(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, auto_reload=True, workers=1)
