import pymysql

def db_execute(sql, params):
    try:
        conn = pymysql.connect(host="localhost",
                                user="root",
                                password="mysqlfgh.00",
                                db="QcChat",
                                port=3306,
                                charset="utf8")
        cursor = conn.cursor()
        cursor.execute(sql, params)

    except Exception as e:
        print("Error: {}".format(e))