import json
import re
import time
import traceback

from collections import deque

from sanic import Sanic
from sanic.log import logger


def init_message(data):
    """初始处理消息体"""
    is_at_me = False
    raw_message = data['raw_message']
    re_s = r'(\[CQ:.*?\])'
    cqs = re.findall(re_s, raw_message)
    message = raw_message
    ats = set()
    for cq in cqs:
        if cq[1:6] == 'CQ:at':
            # if cq != f'[CQ:at,qq={data["self_id"]}]':  # 不@自己
            if str(data['self_id']) not in cq:
                ats.add(cq)
            else:
                is_at_me = True
        message = message.replace(cq, '')
    message = message.strip()
    data['is_at_me'] = is_at_me
    return message, ats


async def group_msg(ws, data):
    """群消息处理"""
    app = Sanic.get_app()

    message, ats = init_message(data)
    # who = data['sender']['user_id']
    who = data['user_id']

    # 弥补 napcat 中 at 信息不带昵称的问题
    if who not in app.ctx.user_id_name:
        app.ctx.user_id_name[who] = data['sender']['nickname']
    for item in data['message']:
        if item['type'] == 'at':
            if 'name' not in item['data']:
                _qq = item['data']['qq']
                if _qq == 'all':
                    _nickname = '全体成员'
                else:
                    _nickname = app.ctx.user_id_name.get(int(_qq), _qq)
                item['data']['name'] = f'@{_nickname}'

    msg = None
    group_id = data['group_id']
    if group_id not in app.ctx.delete_groups:
        if group_id not in app.ctx.msgs:
            app.ctx.msgs[group_id] = deque(maxlen=app.ctx.msg_maxlen)
        app.ctx.msgs[group_id].append(data)

    # if '[CQ:json' in data['raw_message']:
    #     with open('raw_message_json.txt', 'a') as f:
    #         f.write(data['raw_message'])

    for plugin in app.ctx.plugins:
        if plugin.type != 'message':
            continue
        try:
            plugin_id = id(plugin)
            if plugin_id not in app.ctx.user_last_ts:
                app.ctx.user_last_ts[plugin_id] = {}
            for attr in {'ws', 'data', 'ats'}:
                if hasattr(plugin, attr):
                    setattr(plugin, attr, locals()[attr])
            if hasattr(plugin, 'db'):
                setattr(plugin, 'data', data)
            msg = await plugin.run(message)
            if msg:
                if who == data['self_id'] \
                        or data['sender']['role'] in {'owner', 'admin'}:
                    pass
                else:
                    now = time.time()
                    if now - app.ctx.user_last_ts[plugin_id].get(who, 0) \
                            > plugin.user_cd:
                        app.ctx.user_last_ts[plugin_id][who] = now
                    else:
                        msg = f'🚫不要刷屏，此功能频率限制为 {plugin.user_cd} 秒'
                if plugin.is_at and who != data['self_id']:
                    ats.add(f'[CQ:at,qq={who}]')
                break
        except Exception as e:
            logger.error(f'插件 {plugin} 运行报错：{e}')
            logger.error(traceback.format_exc())

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


async def private_msg(ws, data):
    """私有消息处理"""
    app = Sanic.get_app()

    qq = data['user_id']
    group_id = f'qq{qq}'
    data['group_id'] = group_id

    if group_id not in app.ctx.delete_groups:
        if group_id not in app.ctx.msgs:
            app.ctx.msgs[group_id] = deque(maxlen=app.ctx.msg_maxlen)
        app.ctx.msgs[group_id].append(data)
