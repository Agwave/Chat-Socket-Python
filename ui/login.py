from .loginWindow import Ui_MainWindow
from .chat import Chat

from PyQt5 import QtWidgets


class Login(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self, db, chat_window):
        super(Login, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login)
        self.db = db
        self.chat_window = chat_window

    def login(self):
        id, password = self.lineEdit.text(), self.lineEdit_2.text()
        is_user = self.db.vericate(id, password)

        if is_user:
            self.chat_window.show()
            self.chat_window.login()
            self.setHidden(True)

        else:
            QtWidgets.QMessageBox.information(self, "警告", "账号或密码错误")