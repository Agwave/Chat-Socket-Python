import pymysql

class A:

    def __init__(self):
        self.conn = pymysql.connect(host="localhost",
                                    user="root",
                                    password="mysqlfgh.00",
                                    db="QcChat",
                                    port=3306,
                                    charset="utf8")
        self.cursor = self.conn.cursor()
        sql = "select id, password from users;"
        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        self.conn.close()
        print(self.conn)
        self.conn = pymysql.connect(host="localhost",
                                    user="root",
                                    password="mysqlfgh.00",
                                    db="QcChat",
                                    port=3306,
                                    charset="utf8")
        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        print(ret)


class B:

    def __init__(self):
        self.conn = pymysql.connect(host="localhost",
                                    user="root",
                                    password="mysqlfgh.00",
                                    db="QcChat",
                                    port=3306,
                                    charset="utf8")
        self.cursor = self.conn.cursor()
        sql = "select id, password from users;"
        res = self.cursor.execute(sql)
        print(res)
        print("b mysql")

if __name__ == "__main__":
    conn = pymysql.connect(host="localhost",
                                    user="root",
                                    password="mysqlfgh.00",
                                    db="QcChat",
                                    port=3306,
                                    charset="utf8")
    print(conn)
    conn.close()
    print(conn)