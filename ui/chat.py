from .chatWindow import Ui_MainWindow
from object.client import Client
from object.message import Message
from mysql.connectMysql import ConnetMysql

from PyQt5 import QtWidgets


class Chat(QtWidgets.QWidget, Ui_MainWindow):

    def __init__(self):
        super(Chat, self).__init__()
        self.setupUi(self)
        self.db = ConnetMysql()
        self.id = None
        self.pushButton.clicked.connect(self.send)
        self.pushButton_3.clicked.connect(self.sign_out)

    def login(self, id):
        self.id = id
        result = self.db.search("select id from users where alive = 1 and id != %s", self.id)
        print(result)
        if result != ():
            users_alive = list(zip(*result))[0]
            self.listWidget.addItems(users_alive)
        self.client = Client()

    def send(self):
        msg = self.textEdit.toPlainText()
        users = self._get_users()
        for user in users:
            byte_msg = Message("transmit", self.id, user, msg).content_bytes
            self.client.socket.send(byte_msg)

    def sign_out(self):
        self.client.sign_out()
        self.close()

    def _get_users(self):
        users = []
        items = self.listWidget.selectedItems()
        for item in items:
            users.append(item.text())
        return users

