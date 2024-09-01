import json
import re

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
        if not self.ats:
            return False
        if message[:3] == r'\tx':
            return True
        else:
            return False

    async def handle(self, message):
        tx = message[3:].strip()[:6]
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
