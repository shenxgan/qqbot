import random
import re
import requests
import json

from sanic import Sanic
from sanic.log import logger

app = Sanic('qqbot')


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


@app.websocket('/qqbot')
async def qqbot(request, ws):
    """QQ机器人"""
    while True:
        data = await ws.recv()
        data = json.loads(data)
        logger.debug(json.dumps(data, indent=4, ensure_ascii=False))

        msg = None
        # if 判断是群消息且文本消息不为空
        if data.get('message_type') == 'group' and data.get('raw_message'):
            message, ats = init_message(data)
            if message[:3] == '###':
                msg = run_code(message)
            else:
                msg = group_msg(message)

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
