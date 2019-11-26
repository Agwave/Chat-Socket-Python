from PyQt5 import QtWidgets
from ui.signUpWindow import Ui_MainWindow
from mysql.connectMysql import ConnetMysql

class SignUp(QtWidgets.QWidget, Ui_MainWindow):

    def __init__(self):
        super(SignUp, self).__init__()
        self.setupUi(self)
        self.db = ConnetMysql()
        self.pushButton.clicked.connect(self.sign_up)

    def sign_up(self):
        if self.lineEdit_2.text() != self.lineEdit_3.text():
            return
        id = self.lineEdit.text()
        password = self.lineEdit_2.text()
        users = self.db.search("select id from users")
        for user in users:
            if user[0] == id:
                QtWidgets.QMessageBox.information(self, "提示", "该用户已存在，请直接登录")
                return
        self.db.insert("insert into users values(%s, %s, '0', 0, 0)", (id, password))
        create_record_sql = "create table {}_record(" \
                            "date char(10) not null," \
                            "time char(15) not null," \
                            "record varchar(500) not null)engine = InnoDB".format(id)
        self.db.create_table(create_record_sql)
        QtWidgets.QMessageBox.information(self, "提示", "账号注册成功")
        self.close()

