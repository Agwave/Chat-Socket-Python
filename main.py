from ui.login import Login
from ui.chat import Chat

from mysql.connectMysql import ConnetMysql
from PyQt5 import QtWidgets
import sys




if __name__ == "__main__":
    db = ConnetMysql()
    app = QtWidgets.QApplication(sys.argv)

    chat_window = Chat()
    login_window = Login(db, chat_window)
    login_window.show()

    sys.exit(app.exec_())