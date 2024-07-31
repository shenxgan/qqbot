import json

from sanic import Sanic
from sanic.log import logger

from group_msg import group_msg
from admin import Admin

app = Sanic('qqbot')


@app.before_server_start
async def load_botmsg(app):
    """加载机器人回复内容到本地内存"""
    with open('botmsg.txt') as f:
        res = f.read()

    botmsg = {}
    botkeys = []
    for r in res.split('\n'):
        if not r.strip():
            continue
        keys, value = r.split('###', 1)
        keys = keys.split(';')
        value = value.replace('\\n', '\n')
        botkeys.append(keys[0])
        for key in keys:
            if key in botmsg:
                logger.error(f'key {key} 重复')
            botmsg[key] = value
    logger.info(f'botmsg 关键字加载完毕，共 {len(botmsg)} 条数据')
    app.ctx.botmsg = botmsg
    app.ctx.botkeys = botkeys


@app.before_server_start
async def load_db(app):
    """加载数据库
    使用json文件来充当数据库
    """
    fpath = 'db.json'
    with open(fpath) as f:
        data = f.read()
        db_data = json.loads(data)
    app.ctx.db = db_data


@app.before_server_start
async def load_admin(app):
    """加载机器人管理指令"""
    app.ctx.admin = Admin()


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

        # 机器人关闭时，仅自己可用
        if app.ctx.db['flag']['bot'] is False:
            if not is_me:
                continue

        # 根据消息类型、内容来进行分别处理
        if data.get('message_type') == 'group' and data.get('raw_message'):
            await group_msg(ws, data, is_me)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, auto_reload=True)
