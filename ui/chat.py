from .chatWindow import Ui_MainWindow

from PyQt5 import QtWidgets


class Chat(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self):
        super(Chat, self).__init__()
        self.setupUi(self)
