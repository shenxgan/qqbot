import json
import random
import re
import requests
import time

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


def key_msg(message):
    """根据关键字触发回复"""
    app = Sanic.get_app()

    key = message.lower().replace('()', '').strip()
    msg = app.ctx.botmsg.get(key)
    return msg


def run_code(message):
    """运行代码"""
    code = message[3:].strip()
    replace_kv = {
        '&#91;': '[',
        '&#93;': ']',
        '&amp;': '&',
        '\r\n': '\n',
    }
    for k, v in replace_kv.items():
        code = code.replace(k, v)

    url = 'http://python:8001/code'  # python 为 python 容器的名称
    r = requests.post(url, json={'code': code})
    msg = r.text
    if msg:
        emojis = '🏄✨🚀⚡⚽🧐'  # 添加一个emoji是为了防止代码输出会触发关键字
        msg = random.choice(emojis) + msg
    else:
        msg = '😶无输出😲'
    return msg


async def group_msg(ws, data, is_me):
    """群消息处理"""
    app = Sanic.get_app()

    message, ats = init_message(data)
    # who = data['sender']['user_id']
    who = data['user_id']
    msg = None

    # 限制每个人触发频率
    now = time.time()
    if not is_me:
        if now - app.ctx.db['trigger']['last_ts'].get(who, 0) \
                < app.ctx.db['trigger']['cd']:
            return

    # 判断是否是执行代码
    if message[:3] == '###':
        if app.ctx.db['flag']['code'] is False:
            if not is_me:
                return
        try:
            msg = run_code(message)
        except Exception as e:
            logger.error(e)
        if not is_me:  # 同时@触发的人
            ats.add(f'[CQ:at,qq={who}]')
    else:
        msg = key_msg(message)

    # 未触发任何回复、且是自己时，进一步判断是否是管理指令
    if (not msg) and is_me:
        msg = app.ctx.admin.run(message)

    if msg:
        if not is_me:
            app.ctx.db['trigger']['last_ts'][who] = now
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
