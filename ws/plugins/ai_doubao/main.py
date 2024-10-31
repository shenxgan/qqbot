import os
import random
import requests

from plugins.base import Base


class Plugin(Base):
    """豆包AI
    申请地址：https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint
    API 地址：https://www.volcengine.com/docs/82379/1298454
    """
    def __init__(self):
        super().__init__()
        self.is_at = True
        self.system_content = '你的每次回复都在50字以内'
        self.fdir = os.path.dirname(os.path.abspath(__file__))
        self.db = self.load_config()

    def doubao(self, content):
        api_key = os.environ.get('DOUBAO_API_KEY')
        models = os.environ.get('DOUBAO_MODEL').split(',')
        model = random.choice(models)
        url = 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        }
        data = {
            'model': model,
            'messages': [
                {'role': 'system', 'content': self.system_content},
                {'role': 'user', 'content': content},
            ]
        }
        r = requests.post(url, json=data, headers=headers)
        msg = r.json()['choices'][0]['message']['content']
        return msg

    def is_match(self, message):
        """检测是否匹配此插件"""
        if message[:4] == r'\gpt':
            return True
        else:
            return False

    async def handle(self, message):
        content = message[4:].strip()
        msg = self.doubao(content)
        msg = '🚀' + msg
        return msg
