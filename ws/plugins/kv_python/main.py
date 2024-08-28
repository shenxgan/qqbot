import os

from plugins.base import Base


class Plugin(Base):
    """Python 知识点，关键字触发"""
    def __init__(self):
        super().__init__()
        self.is_at = False
        self.kvmsg = self.load_kvmsg()

    def load_kvmsg(self):
        """加载机器人回复内容到本地内存"""
        fdir = os.path.dirname(os.path.abspath(__file__))
        fpath = os.path.join(fdir, 'kvmsg.txt')
        with open(fpath) as f:
            res = f.read()

        kvmsg = {}
        for r in res.split('\n'):
            if not r.strip():
                continue
            keys, value = r.split('###', 1)
            keys = keys.split(';')
            value = value.replace('\\n', '\n')
            for key in keys:
                if key in kvmsg:
                    print(f'key {key} 重复')
                kvmsg[key] = value
        print(f'kvmsg 关键字加载完毕，共 {len(kvmsg)} 条数据')
        return kvmsg

    async def handle(self, message):
        key = message.lower().replace('()', '').strip()
        msg = self.kvmsg.get(key)
        return msg
