import json
import os
import importlib

from sanic import Sanic
from sanic.log import logger

from group_msg import group_msg

app = Sanic('qqbot')


@app.before_server_start
async def load_plugins(app):
    """加载所有插件，并初始化"""
    app.ctx.plugins = []
    for de in os.scandir('plugins'):
        if not de.is_dir():
            continue
        logger.info(f'加载插件 {de.name}')
        x = importlib.import_module(f'plugins.{de.name}.main')
        app.ctx.plugins.append(x.Plugin())


@app.websocket('/qqbot')
async def qqbot(request, ws):
    """QQ机器人"""
    while True:
        data = await ws.recv()
        data = json.loads(data)
        logger.debug(json.dumps(data, indent=4, ensure_ascii=False))

        # 记录是否是自己发送的消息
        is_me = False
        if 'user_id' in data and 'self_id' in data:
            is_me = data['user_id'] == data['self_id']

        # 根据消息类型、内容来进行分别处理
        if data.get('message_type') == 'group' and data.get('raw_message'):
            await group_msg(ws, data, is_me)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, auto_reload=False, workers=1)
