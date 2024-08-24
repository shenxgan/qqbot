from plugins.base import Base


class Plugin(Base):
    """入群欢迎词"""
    def __init__(self):
        super().__init__()
        self.type = 'notice'

    def is_match(self, data):
        """检测是否匹配此插件"""
        if data.get('notice_type') == 'group_increase':
            return True
        else:
            return False

    def handle(self, data):
        msg = '欢迎入群~'
        return msg
