import os
import random
import time

from plugins.base import Base


class Plugin(Base):
    """入群欢迎词"""
    def __init__(self):
        super().__init__()
        self.type = 'notice'
        self.last_ts = {}       # 记录每个群的触发时间
        self.cd = 3600 * 1      # 同一群回复间隔为1小时
        self.fdir = os.path.dirname(os.path.abspath(__file__))
        self.welcome_msg = self.load_msg()
        self.db = self.load_config()

    def load_msg(self):
        """加载欢迎语到本地内存"""
        fpath = os.path.join(self.fdir, 'msg.txt')
        with open(fpath) as f:
            data = f.read()
        welcome_msg = [line for line in data.split('\n') if line.strip()]
        print(f'入群欢迎语加载完毕，共 {len(welcome_msg)} 条数据')
        return welcome_msg

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
        msg = random.choice(self.welcome_msg)
        return msg
