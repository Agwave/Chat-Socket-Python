from ui.login import Login
from ui.chat import Chat
from ui.signUp import SignUp

from PyQt5 import QtWidgets
import sys




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    chat_window = Chat()
    signup_window = SignUp()
    login_window = Login(chat_window, signup_window)
    login_window.show()

    sys.exit(app.exec_())