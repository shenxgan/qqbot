import json
import re
import secrets
import string

from plugins.base import Base


class Plugin(Base):
    """群主、管理员操作"""
    def __init__(self):
        super().__init__()
        self.is_at = False
        self.ws = None
        self.data = None
        self.ats = None
        self.done = set()
        self.is_tx_self = False

    async def set_group_special_title(self, message):
        """设置专属头衔"""
        if self.data['sender']['role'] not in {'owner', 'admin'}:
            return None
        if not self.ats:
            return None
        tx = message.strip()
        for at in self.ats:
            re_s = r'qq=(\d+),*'
            info = re.findall(re_s, at)
            qq = int(info[0])
            await self.set_special_title(qq, tx)
        msg = '专属头衔设置成功'
        return msg

    async def set_group_special_title_self(self, message):
        """设置专属头衔-自助"""
        if self.is_tx_self is False:
            return None
        qq = self.data['sender']['user_id']
        if qq in self.done:
            return None
        # self.done.add(qq)
        tx = message.strip()
        await self.set_special_title(qq, tx)
        msg = '专属头衔设置成功'
        return msg

    async def set_special_title(self, qq, tx):
        """设置专属头衔"""
        ret = {
            'action': 'set_group_special_title',
            'params': {
                'group_id': self.data['group_id'],
                'user_id': qq,
                'special_title': tx,
            }
        }
        await self.ws.send(json.dumps(ret))

    def web_sign(self, message):
        """获取或设置 web qq 访问的 sign 值"""
        from sanic import Sanic
        app = Sanic.get_app()

        if self.data['user_id'] != self.data['self_id']:
            return None
        sign = message.strip()
        if not sign:
            sign = ''.join(secrets.choice(
                string.digits+string.ascii_letters) for i in range(4))
        app.ctx.sign = sign
        msg = f'sign 值设置成功，当前为：{sign}'
        return msg

    async def handle(self, message):
        msg = None
        if message[:3] == r'\tx':
            message = message[3:]
            msg = await self.set_group_special_title(message)
        elif message[:2] == '头衔':
            message = message[2:]
            msg = await self.set_group_special_title_self(message)
        elif message[:5] == r'\sign':
            message = message[5:]
            msg = self.web_sign(message)
        elif '专属头衔' in message:
            if self.is_tx_self is True:
                return
            if self.data['user_id'] != self.data['self_id']:
                return None
            self.is_tx_self = True
            msg = '【专属头衔-自助设置】启动！\n示例：头衔 天才萌新'
        return msg
