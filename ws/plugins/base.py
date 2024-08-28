class Base:
    def __init__(self):
        self.is_open = True     # 插件开关
        self.is_at = True       # 回复消息时是否at触发之人
        self.type = 'message'   # 类型

    def is_match(self, message):
        """检测是否匹配此插件"""
        return True

    async def handle(self, message):
        """核心处理逻辑"""
        pass

    async def run(self, message):
        """外部调用入口"""
        if not self.is_open:
            return
        if not self.is_match(message):
            return
        return await self.handle(message)
