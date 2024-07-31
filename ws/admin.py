from sanic import Sanic


class Admin():
    """机器人管理命令"""
    def __init__(self):
        self.app = Sanic.get_app()
        self.actions = {
            '00_机器人指令': 'show_actions',
            '01_开启机器人': 'open_bot',
            '02_关闭机器人': 'close_bot',
            '03_开启代码': 'open_code',
            '04_关闭代码': 'close_code',
            # '05_随机关键字': 'random_key',
        }
        self.actions_with_number = self.init_actions()

    def init_actions(self):
        actions = {}
        for k, v in self.actions.items():
            for kk in k.split('_', 1):
                actions[kk] = v
        return actions

    def run(self, action):
        if action not in self.actions_with_number:
            return
        func = getattr(self, self.actions_with_number[action])
        msg = func() or f'指令【{action}】执行完毕'
        return msg

    def show_actions(self):
        msg = '\n'.join(self.actions.keys())
        return msg

    def open_bot(self):
        self.app.ctx.db['flag']['bot'] = True

    def close_bot(self):
        self.app.ctx.db['flag']['bot'] = False

    def open_code(self):
        self.app.ctx.db['flag']['code'] = True

    def close_code(self):
        self.app.ctx.db['flag']['code'] = False
