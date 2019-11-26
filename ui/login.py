from .loginWindow import Ui_MainWindow

from mysql.connectMysql import ConnetMysql

from PyQt5 import QtWidgets


class Login(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self, chat_window, signup_window):
        super(Login, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.sign_up)
        self.chat_window = chat_window
        self.signup_window = signup_window
        self.db = ConnetMysql()

    def login(self):
        id, password = self.lineEdit.text(), self.lineEdit_2.text()
        is_user = False

        ids_and_passwords = self.db.search("select id, password from users")
        for i, p in ids_and_passwords:
            if i == id and p == password:
                is_user = True
                break

        if is_user:
            self.db.update("update users set alive = 1 where id = %s and password = %s", [id, password])
            self.chat_window.show()
            self.chat_window.login(id)
            self.setHidden(True)

        else:
            QtWidgets.QMessageBox.information(self, "警告", "账号或密码错误")

    def sign_up(self):
        self.signup_window.show()