import json

from sanic import Sanic
from sanic.log import logger


async def notice(ws, data):
    """群通知事件处理"""
    app = Sanic.get_app()
    msg = None

    for plugin in app.ctx.plugins:
        if plugin.type != 'notice':
            continue
        try:
            msg = plugin.run(data)
            if msg:
                break
        except Exception as e:
            logger.error(f'插件 {plugin} 运行报错：{e}')

    if msg:
        ret = {
            'action': 'send_group_msg',
            'params': {
                'group_id': data['group_id'],
                'message': msg,
            }
        }
        await ws.send(json.dumps(ret))
