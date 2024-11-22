import os
import json


class Base:
    def __init__(self):
        self.is_open = True     # 插件开关
        self.is_at = True       # 回复消息时是否at触发之人
        self.type = 'message'   # 类型
        self.ats = None
        self.user_cd = 15

    def load_config(self):
        """从本地文件中加载插件的配置"""
        fpath = os.path.join(self.fdir, 'db.json')
        if not os.path.exists(fpath):
            return {}
        with open(fpath) as f:
            db = f.read()
        db = json.loads(db)
        if 'is_open' in db:
            self.is_open = db['is_open']
        if 'is_at' in db:
            self.is_at = db['is_at']
        print('插件配置加载完成，db.json 内容为', db)
        return db

    def save_config(self):
        """存储配置"""
        fpath = os.path.join(self.fdir, 'db.json')
        self.db['is_open'] = self.is_open
        self.db['is_at'] = self.is_at
        with open(fpath, 'w') as f:
            f.write(json.dumps(self.db, indent=4, ensure_ascii=False))

    def is_match(self, message):
        """检测是否匹配此插件"""
        return True

    def is_allow(self):
        """黑白名单判断"""
        if not hasattr(self, 'db'):
            return True
        if not hasattr(self, 'data'):
            return True
        if 'user_id' in self.data and 'self_id' in self.data:
            if self.data['user_id'] == self.data['self_id']:
                return True
        group_id = self.data['group_id']
        if group_id in self.db.get('group_blacklist', []):
            return False
        if self.db.get('group_whitelist') \
                and group_id not in self.db.get('group_whitelist'):
            return False
        return True

    async def handle(self, message):
        """核心处理逻辑"""
        pass

    async def run(self, message):
        """外部调用入口"""
        if not self.is_open:
            return
        if not self.is_allow():
            return
        if not self.is_match(message):
            return
        return await self.handle(message)
