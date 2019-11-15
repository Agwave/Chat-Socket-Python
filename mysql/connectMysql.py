import pymysql

class ConnetMysql:
    def __init__(self):
        self.get_conn()

    def get_conn(self):
        try:
            self.conn = pymysql.connect(host="localhost",
                                        user="root",
                                        password="mysqlfgh.00",
                                        db="QcChat",
                                        port=3306,
                                        charset="utf8")
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("Error: {}".format(e))

    def vericate(self, input_id, input_password):
        sql = "select id, password from users;"
        self.cursor.execute(sql)
        id_and_password = self.cursor.fetchall()
        for id, password in id_and_password:
            if id == input_id and password == input_password:
                return True
        return False