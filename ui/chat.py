from .chatWindow import Ui_MainWindow
from object.client import Client

from PyQt5 import QtWidgets


class Chat(QtWidgets.QWidget, Ui_MainWindow):

    def __init__(self):
        super(Chat, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send)
        self.pushButton_3.clicked.connect(self.sign_out)

    def login(self):
        self.client = Client()


    def send(self):
        msg = self.textEdit.toPlainText()
        byte_msg = bytes(msg, encoding='utf-8')
        self.client.socket.send(byte_msg)

    def sign_out(self):
        self.client.sign_out()
        self.close()