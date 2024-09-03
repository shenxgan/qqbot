import time

from plugins.base import Base


class Plugin(Base):
    """入群欢迎词"""
    def __init__(self):
        super().__init__()
        self.type = 'notice'
        self.last_ts = {}       # 记录每个群的触发时间
        self.cd = 3600          # 同一群回复间隔为1小时

    def is_match(self, data):
        """检测是否匹配此插件"""
        if data.get('notice_type') == 'group_increase':
            group_id = data['group_id']
            now = time.time()
            if now - self.last_ts.get(group_id, 0) > self.cd:
                self.last_ts[group_id] = now
                return True
        else:
            return False

    async def handle(self, data):
        msg = '欢迎入群~'
        return msg
