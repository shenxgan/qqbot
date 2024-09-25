import importlib
import json
import os
import re

from functools import wraps

from sanic import Sanic
from sanic import response
from sanic import exceptions
from sanic.log import logger

from message import group_msg
from notice import notice

app = Sanic('qqbot')


@app.before_server_start
async def init(app):
    """初始化"""
    app.ctx.msgs = {}
    app.ctx.msg_maxlen = 30
    app.ctx.sign = None


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
    while True:
        app.ctx.ws = ws
        data = await ws.recv()
        data = json.loads(data)
        logger.debug(json.dumps(data, indent=4, ensure_ascii=False))

        # 记录是否是自己发送的消息
        is_me = False
        if 'user_id' in data and 'self_id' in data:
            is_me = data['user_id'] == data['self_id']

        post_type = data.get('post_type')
        # 根据消息类型、内容来进行分别处理
        if post_type == 'message' \
                and data.get('message_type') == 'group' \
                and data.get('raw_message'):
            await group_msg(ws, data, is_me)
        elif post_type == 'notice':
            await notice(ws, data)


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            sign = request.args.get('sign')
            is_authorized = sign and sign == request.app.ctx.sign
            if is_authorized:
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


@app.get('/webqq/msgs')
@authorized()
async def get_msgs(request):
    data = {k: list(v) for k, v in request.app.ctx.msgs.items()}
    return response.json(data)


@app.post('/webqq/msgs')
@authorized()
async def post_msgs(request):
    data = request.json
    msg = data['msg']
    re_s = r'@(\d+)?'
    ats = re.findall(re_s, msg)
    for at in ats:
        msg = msg.replace(f'@{at}', f'[CQ:at,qq={at}]')
    ret = {
        'action': 'send_group_msg',
        'params': {
            'group_id': int(data['group_id']),
            'message': msg,
        }
    }
    await request.app.ctx.ws.send(json.dumps(ret))
    return response.empty()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, auto_reload=True, workers=1)
