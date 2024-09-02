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
        if message.strip() == r'\mysql':
            return True
        else:
            return False

    async def handle(self, message):
        sqls = [
            'create database db{0};',
            "CREATE USER '{0}'@'%' IDENTIFIED BY '{0}';",
            "GRANT ALL ON db{0}.* TO '{0}'@'%';",
        ]
        at = list(self.ats)[0]  # 一次只能一个，多个取第一个
        re_s = r'qq=(\d+),*'
        info = re.findall(re_s, at)
        qq = info[0]

        mysql = MySQL(**self.conn_info)
        for sql in sqls:
            sql = sql.format(qq)
            mysql.execute(sql)
        mysql.close()

        msgs = [
            '数据库、账号和密码创建成功：',
            f'\t连接地址：{self.conn_info["host"]}',
            f'\t端口：{self.conn_info["port"]}',
            '\t用户名：{你的qq号}',
            '\t密码：{你的qq号}',
            '\t数据库：db{你的qq号}',
        ]
        msg = '\n'.join(msgs)
        return msg
