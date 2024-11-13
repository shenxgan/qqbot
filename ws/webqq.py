import os
import json
import time

from functools import wraps

from sanic import Blueprint
from sanic import exceptions
from sanic import response

webqq = Blueprint('webqq', url_prefix='/webqq')

webqq.static('/static/', './static/')


def authorized():
    """鉴权"""
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


@webqq.get('/')
@authorized()
async def index(request):
    with open('index.html') as f:
        html = f.read()
    return response.html(html)


def save_private_msg(request):
    """存储主动发送的私聊消息
    机器人发送的群聊消息，会自动获取一遍
    私聊消息，需要主动在发送的时候存储一遍
    """
    data = request.json
    msg = data['msg']
    user_id = int(data['group_id'][2:])
    self_id = 123456  # 机器人的qq号，没有获取，随机指定一个值
    _time = int(time.time())
    _data = {
        "message_type": "private",
        "message_id": _time,
        "user_id": self_id,
        "message": [
            {
                "type": "text",
                "data": {
                    "text": msg
                }
            }
        ],
        "raw_message": msg,
        "font": 0,
        "sender": {
            "user_id": self_id,
            "nickname": "我",  # 机器人昵称，随意
            "sex": "unknown"
        },
        "target_id": user_id,
        "time": _time,
        "self_id": self_id,
        "post_type": "message",
        "group_id": data['group_id']
    }
    request.app.ctx.msgs[data['group_id']].append(_data)


@webqq.post('/msgs')
@authorized()
async def post_msgs(request):
    """获取、发送消息"""
    data = request.json
    if 'msg' in data:
        msg = data['msg']
        if data['group_id'][:2] == 'qq':  # 私聊消息
            ret = {
                'action': 'send_private_msg',
                'params': {
                    'user_id': int(data['group_id'][2:]),
                    'message': msg,
                }
            }
            save_private_msg(request)
        else:  # 群组消息
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


@webqq.get('/groups')
@authorized()
async def get_group_list(request):
    """获取群组列表信息"""
    request.app.ctx.delete_groups.clear()
    return response.json(request.app.ctx.group_id_name)


@webqq.delete('/group/<group_id:int>')
@authorized()
async def delete_group(request, group_id):
    """删除本地群组记录"""
    del request.app.ctx.msgs[group_id]
    request.app.ctx.delete_groups.add(group_id)
    return response.empty()
