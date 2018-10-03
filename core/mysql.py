# coding=utf-8
# auth: zhangyiling
# time: 2018/9/26 下午8:07
# description: 发布代码之后的返回


import MySQLdb


class DB_Operate(object):
    """MySQL的操作相关"""

    def mysql_command(self, conn, sql_cmd):
        try:
            ret = []
            conn = MySQLdb.connect(host=conn["host"], user=conn["user"], passwd=conn["password"], db=conn["database"],
                                   port=conn["port"], charset="utf8")
            cursor = conn.cursor()
            n = cursor.execute(sql_cmd)
            for row in cursor.fetchall():
                for i in row:
                    ret.append(i)
        except MySQLdb.Error as e:
            ret.append(e)

        return ret

    def select_table(self, conn, sql_cmd):
        try:
            ret = []
            conn = MySQLdb.connect(host=conn["host"], user=conn["user"], passwd=conn["password"], db=conn["database"],
                                   port=conn["port"], charset="utf8")
            cursor = conn.cursor()

            n = cursor.execute(sql_cmd)
            for row in cursor.fetchall():
                for i in row:
                    ret.append(i)
        except MySQLdb.Error as e:
            ret.append(e)
        return ret
