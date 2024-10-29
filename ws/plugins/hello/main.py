import os

from plugins.base import Base


class Plugin(Base):
    """早中晚问候"""
    def __init__(self):
        super().__init__()
        self.type = 'cron'      # 定时任务类型
        self.fdir = os.path.dirname(os.path.abspath(__file__))
        self.db = self.load_config()
        self.group_ids = self.db.get('group_whitelist', [])     # 要发送的群组列表

    async def handle(self, now):
        msg = None
        h = now.hour
        m = now.minute
        if h == 8 and m == 0:
            msg = '早上好~'
        if h == 8 and m == 5:
            msg = '早早早~\n找呀找呀找朋友，找到一个女朋友，牵个手呀亲个嘴，生下一个小朋友。嘿！'
        if h == 12 and m == 0:
            msg = '中午好~'
        if h == 20 and m == 0:
            msg = '晚上好~'
        return msg
