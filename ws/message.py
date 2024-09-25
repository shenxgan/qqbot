import json
import re

from collections import deque

from sanic import Sanic
from sanic.log import logger


def init_message(data):
    """初始处理消息体"""
    raw_message = data['raw_message']
    re_s = r'(\[CQ:.*?\])'
    cqs = re.findall(re_s, raw_message)
    message = raw_message
    ats = set()
    for cq in cqs:
        if cq[1:6] == 'CQ:at':
            if cq != f'[CQ:at,qq={data["self_id"]}]':  # 不@自己
                ats.add(cq)
        message = message.replace(cq, '')
    message = message.strip()
    return message, ats


async def group_msg(ws, data, is_me):
    """群消息处理"""
    app = Sanic.get_app()

    message, ats = init_message(data)
    # who = data['sender']['user_id']
    who = data['user_id']
    msg = None
    if data['group_id'] not in app.ctx.msgs:
        app.ctx.msgs[data['group_id']] = deque(maxlen=app.ctx.msg_maxlen)
    app.ctx.msgs[data['group_id']].append(data)

    for plugin in app.ctx.plugins:
        if plugin.type != 'message':
            continue
        try:
            for attr in {'ws', 'data', 'ats'}:
                if hasattr(plugin, attr):
                    setattr(plugin, attr, locals()[attr])
            msg = await plugin.run(message)
            if msg:
                if plugin.is_at:
                    ats.add(f'[CQ:at,qq={who}]')
                break
        except Exception as e:
            logger.error(f'插件 {plugin} 运行报错：{e}')

    if msg:
        if ats:
            msg = ' '.join(ats) + '\n' + msg
        ret = {
            'action': 'send_group_msg',
            'params': {
                'group_id': data['group_id'],
                'message': msg,
            }
        }
        await ws.send(json.dumps(ret))
