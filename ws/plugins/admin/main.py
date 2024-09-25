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

    def is_match(self, message):
        """检测是否匹配此插件"""
        if self.data['sender']['role'] not in {'owner', 'admin'}:
            return False
        return True

    async def set_group_special_title(self, message):
        """设置专属头衔"""
        if not self.ats:
            return None
        tx = message.strip()[:6]
        for at in self.ats:
            re_s = r'qq=(\d+),*'
            info = re.findall(re_s, at)
            qq = info[0]
            ret = {
                'action': 'set_group_special_title',
                'params': {
                    'group_id': self.data['group_id'],
                    'user_id': int(qq),
                    'special_title': tx,
                }
            }
            await self.ws.send(json.dumps(ret))
        msg = '专属头衔设置成功'
        return msg

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
            msg = await self.set_group_special_title(message)
        elif message[:5] == r'\sign':
            message = message[5:]
            msg = self.web_sign(message)
        return msg
