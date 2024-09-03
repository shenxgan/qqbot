import os
import json
import random

from plugins.base import Base


class Plugin(Base):
    """成语"""
    def __init__(self):
        super().__init__()
        self.is_at = False
        self.data = None
        self.idiom, self.pinyin = self.load_data()

    def load_data(self):
        """加载到本地内存"""
        fdir = os.path.dirname(os.path.abspath(__file__))
        fpath = os.path.join(fdir, 'idiom.json')
        with open(fpath) as f:
            data = f.read()
        data = json.loads(data)

        idiom = {}
        pinyin = {}
        for item in data:
            word = item['word']
            info = item['pinyin'].split()
            first = info[0]
            last = info[-1]
            idiom[word] = last
            if first not in pinyin:
                pinyin[first] = []
            pinyin[first].append(word)
        print(f'所有成语加载完毕，共 {len(idiom)} 条数据')
        return idiom, pinyin

    async def handle(self, message):
        data = self.data
        if 'user_id' in data and 'self_id' in data:
            if data['user_id'] == data['self_id']:
                return None

        key = message.strip()
        if key in self.idiom:
            last = self.idiom[key]
            if last in self.pinyin:
                msg = random.choice(self.pinyin[last])
                return msg
