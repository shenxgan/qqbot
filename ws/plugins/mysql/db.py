import pymysql


class MySQL():
    """pymysql 的封装"""
    def __init__(self, **conn_info):
        if 'charset' not in conn_info:
            conn_info['charset'] = 'utf8mb4'
        if 'cursorclass' not in conn_info:
            conn_info['cursorclass'] = pymysql.cursors.DictCursor
        self.conn = pymysql.connect(**conn_info)

    def execute(self, sql):
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql)
                self.conn.commit()
        except Exception:
            import traceback
            print(traceback.format_exc())
            # 异常后回滚
            self.conn.rollback()

    def close(self):
        if self.conn:
            self.conn.close()
