import json
import random
import re
import requests
import time

from sanic import Sanic
from sanic.log import logger

app = Sanic('qqbot')
app.ctx.last_ts = {}  # 记录每个人上次触发的时间戳


@app.before_server_start
async def load_botmsg(app):
    """加载机器人回复内容到本地内存"""
    with open('botmsg.txt') as f:
        res = f.read()

    botmsg = {}
    for r in res.split('\n'):
        if not r.strip():
            continue
        keys, value = r.split('###', 1)
        value = value.replace('\\n', '\n')
        for key in keys.split(';'):
            if key in botmsg:
                logger.error(f'key {key} 重复')
            botmsg[key] = value
    logger.info(f'botmsg 关键字加载完毕，共 {len(botmsg)} 条数据')
    app.ctx.botmsg = botmsg


@app.before_server_start
async def init_flag(app):
    """初始化开关"""
    app.ctx.flag = {
        '机器人': True,
        '回复': True,
        '代码': True,
    }


def init_message(data):
    """初始处理消息体"""
    raw_message = data['raw_message']
    re_s = r'(\[CQ:.*?\])'
    cqs = re.findall(re_s, raw_message)
    message = raw_message
    ats = set()
    for cq in cqs:
        if cq[1:6] == 'CQ:at':
            ats.add(cq)
        message = message.replace(cq, '')
    message = message.strip()
    return message, ats


def group_msg(message):
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
        emojis = '🏄✨🚀⚡⚽🧐🥶'
        msg = random.choice(emojis) + msg
    else:
        msg = '😶无输出😲'
    return msg


def admin_action(message):
    """机器人管理命令"""
    app = Sanic.get_app()
    all_actions = []
    for flag, _ in app.ctx.flag.items():
        all_actions.append(f'开启{flag}')
        all_actions.append(f'关闭{flag}')
    msg = None
    if message == '机器人指令':
        msg = '\n'.join(all_actions)
    elif message == '机器人状态':
        msg = json.dumps(app.ctx.flag, indent=4, ensure_ascii=False)
    elif message in all_actions:
        action = message[:2]
        obj = message[2:]
        if action == '开启':
            v = True
        elif action == '关闭':
            v = False
        app.ctx.flag[obj] = v
        msg = f'指令【{message}】执行完毕'
    return msg


@app.websocket('/qqbot')
async def qqbot(request, ws):
    """QQ机器人"""
    app = request.app
    while True:
        data = await ws.recv()
        data = json.loads(data)

        # 记录是否是自己发送的消息
        is_me = False
        if 'user_id' in data and 'self_id' in data:
            is_me = data['user_id'] == data['self_id']

        # 机器人关闭时，仅自己可用
        if app.ctx.flag['机器人'] is False:
            logger.info(json.dumps(data, indent=4, ensure_ascii=False))
            if not is_me:
                continue

        msg = None
        # if 判断是群消息且文本消息不为空
        if data.get('message_type') == 'group' and data.get('raw_message'):
            message, ats = init_message(data)
            # who = data['sender']['user_id']
            who = data['user_id']

            # 限制每个人触发频率为15秒一次
            now = time.time()
            if not is_me and (now - app.ctx.last_ts.get(who, 0) < 15):
                continue

            if app.ctx.flag['代码'] and message[:3] == '###':
                msg = run_code(message)
                if not ats:
                    ats = [f'[CQ:at,qq={who}]']
            elif app.ctx.flag['回复']:
                msg = group_msg(message)

            if msg:
                app.ctx.last_ts[who] = now

        # 未触发任何回复、且是自己时，进一步判断是否时管理指令
        if (not msg) and is_me is True:
            msg = admin_action(message)

        if msg and ats:
            msg = ' '.join(ats) + '\n' + msg

        if msg:
            ret = {
                'action': 'send_group_msg',
                'params': {
                    'group_id': data['group_id'],
                    'message': msg,
                }
            }
            await ws.send(json.dumps(ret))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, auto_reload=True)
