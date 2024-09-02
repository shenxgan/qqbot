import os
import re

from plugins.base import Base
# from plugins.mysql.db import MySQL
from .db import MySQL


class Plugin(Base):
    """创建数据库、账号和密码"""
    def __init__(self):
        super().__init__()
        self.is_at = False
        self.data = None
        self.ats = None
        self.conn_info = self.get_mysql_conn()

    def get_mysql_conn(self):
        conn_info = {
            'host': os.getenv('MYSQL_HOST', '127.0.0.1'),
            'port': os.getenv('MYSQL_PORT', '3306'),
            'user': os.getenv('MYSQL_USER', 'root'),
            'passwd': os.getenv('MYSQL_PASSWORD', '123456'),
        }
        conn_info['port'] = int(conn_info['port'])
        return conn_info

    def is_match(self, message):
        """检测是否匹配此插件"""
        if self.data['sender']['role'] not in {'owner', 'admin'}:
            return False
        if not self.ats:
            return False
        if message.startswith(r'\mysql'):
            return True
        else:
            return False

    async def handle(self, message):
        at = list(self.ats)[0]  # 一次只能一个，多个取第一个
        re_s = r'qq=(\d+),*'
        info = re.findall(re_s, at)
        qq = info[0]

        if message.strip() == r'\mysql drop':
            sqls = [
                f"DROP USER '{qq}'@'%';",       # 删除用户
                f"DROP DATABASE db{qq};"        # 删除数据库
            ]
            msgs = [
                '数据库和账号均已删除。',
            ]
        else:
            sqls = [
                f"CREATE DATABASE db{qq};",                         # 创建数据库
                f"CREATE USER '{qq}'@'%' IDENTIFIED BY '{qq}';",    # 创建账号和密码
                f"GRANT ALL ON db{qq}.* TO '{qq}'@'%';",            # 分配数据库权限
                f"ALTER USER '{qq}'@'%' PASSWORD EXPIRE;",          # 将密码过期
            ]
            msgs = [
                '数据库、账号和密码创建成功：',
                f'\t连接地址：{self.conn_info["host"]}',
                f'\t端口：{self.conn_info["port"]}',
                f'\t用户名：{qq}',
                f'\t密码：{qq}（首次登录需要重置密码）',
                f'\t数据库：db{qq}',
            ]

        mysql = MySQL(**self.conn_info)
        for sql in sqls:
            sql = sql.format(qq)
            mysql.execute(sql)
        mysql.close()

        msg = '\n'.join(msgs)
        return msg
