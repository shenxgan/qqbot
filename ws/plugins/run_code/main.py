import random
import requests

from plugins.base import Base


class Plugin(Base):
    """运行代码"""
    def __init__(self):
        super().__init__()
        self.url = 'http://python:8001/code'    # 代码运行的服务器
        self.result_prefix = '🏄✨🚀⚡⚽🧐'     # 运行结果要添加的前缀序列
        self.result_empty = '😶无输出😲'        # 无输出时的提示文字

    def is_match(self, message):
        """检测是否匹配此插件"""
        if message[:3] == '###':
            return True
        else:
            return False

    async def handle(self, message):
        code = message[3:].strip()
        # qq会进行转义，此处是对转义的字符进行还原
        replace_kv = {
            '&#91;': '[',
            '&#93;': ']',
            '&amp;': '&',
            '\r\n': '\n',
        }
        for k, v in replace_kv.items():
            code = code.replace(k, v)

        r = requests.post(self.url, json={'code': code})
        msg = r.text
        if msg:
            # 添加一个emoji前缀是为了防止代码输出会触发关键字
            msg = random.choice(self.result_prefix) + msg
        else:
            msg = self.result_empty
        return msg
