import pymysql

class ConnetMysql:

    def __init__(self):
        self.conn = None

    def get_conn(self):
        try:
            if self.conn is None:
                self.conn = pymysql.connect(host="localhost",
                                            user="root",
                                            password="mysqlfgh.00",
                                            db="QcChat",
                                            port=3306,
                                            charset="utf8")
        except Exception as e:
            print("Error: {}".format(e))

    def vericate(self, input_id, input_password):
        self.get_conn()
        cursor = self.conn.cursor()
        sql = "select id, password from users"
        cursor.execute(sql)
        id_and_password = cursor.fetchall()
        for id, password in id_and_password:
            if id == input_id and password == input_password:
                update_sql = "update users set alive = 1 where id = %s and password = %s"
                cursor.execute(update_sql, [id, password])
                print("vercate successfully")
                self.cut_conn()
                return True
        self.cut_conn()
        return False

    def insert(self, sql, params=None):
        try:
            self.get_conn()
            cursor = self.conn.cursor()
            if params is not None:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            self.conn.commit()

            self.cut_conn()
            print("insert successfuly")

        except Exception as e:
            print("Error: {}".format(e))
            print("Error: {}".format(sql))

    def delete(self, sql, params=None):
        try:
            self.get_conn()
            cursor = self.conn.cursor()

            if params is not None:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            self.conn.commit()
            self.cut_conn()
            print("delete successfuly")

        except Exception as e:
            print("Error: {}".format(e))
            print("Error: {}".format(sql))

    def search(self, sql, params=None):
        try:
            self.get_conn()
            cursor = self.conn.cursor()

            if params is not None:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            result = cursor.fetchall()
            self.cut_conn()
            return result

        except Exception as e:
            print("Error: {}".format(e))
            print("Error: {}".format(sql))
            return None

    def update(self, sql, params=None):
        try:
            self.get_conn()
            cursor = self.conn.cursor()

            if params is not None:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            self.conn.commit()

            self.cut_conn()
            print("update successfuly")

        except Exception as e:
            print("Error: {}".format(e))
            print("Error: {}".format(sql))

    def save_chat_record(self, record, row, id):
        try:
            self.get_conn()
            cursor = self.conn.cursor()
            if len(record) != 0:
                for r in record[row:]:
                    date = r[1:11]
                    time = r[12:27]
                    params = (date, time, r)
                    print(params)
                    cursor.execute("insert into {} values(%s, %s, %s)".format(id+"_record"), params)
                    row += 1
                self.conn.commit()
            self.cut_conn()
            return row
        except Exception as e:
            print("Error: {}".format(e))
            print("Error: record")
            return

    def get_record(self):
        try:
            self.get_conn()
            cursor = self.conn.cursor()

        except Exception as e:
            print("Error: {}".format(e))
            print("Error: get record")

    def sign_out(self, addr):
        try:
            self.get_conn()
            id = self.search("select id from users where ip = %s and port = %s", addr)[0][0]
            self.update("update users set alive = 0, ip = '0', port = 0 where id = %s", id)
            print("sign out successfuly")
            return id

        except Exception as e:
            print("Error: {}".format(e))
            print("Error: {}".format(addr))

    def create_table(self, sql, params=None):
        self.get_conn()
        cursor = self.conn.cursor()
        if params is not None:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        self.cut_conn()
        print("create table successfully")

    def cut_conn(self):
        try:
            self.conn.close()
            self.conn = None
        except Exception as e:
            print("Error: {}".format(e))