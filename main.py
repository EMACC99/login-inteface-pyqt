import sys
import hashlib
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from logged import Ui_MainWindow as logged_MainWindow
from login_ui import Ui_MainWindow as login_MainWindow


def get_users():
    try:
        with open("users.json") as json_file:
            users = json.load(json_file)
        return users
    except FileNotFoundError:
        QMessageBox.critical(MainWindow, "Error", "No hay usuarios registrados, registrando root")
        user = "root"
        p = hashlib.sha512(b'admin').hexdigest()
        register_user({user:p})
        return

def register_user(users):
    with open("users.json", "w+") as write_file:
        json.dump(users, write_file)


class MainWindow(QMainWindow, logged_MainWindow, login_MainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.loginWindow = login_MainWindow()
        self.loggedWindow = logged_MainWindow()
        self.StartLoginWindow()

    def StartLoginWindow(self):
        self.loginWindow.setupUi(self)
        self.loginWindow.pushButton.clicked.connect(self.login)
        self.loginWindow.pushButton_2.clicked.connect(self.sign_in)
        self.show()

    def StartLoggedWindow(self):
        self.loggedWindow.setupUi(self)
        self.loggedWindow.pushButton.clicked.connect(self.StartLoginWindow)
        self.show()
        
    def login(self):
        users = get_users()
        user = self.loginWindow.lineEdit.text()
        password = hashlib.sha512(self.loginWindow.lineEdit_2.text().encode()).hexdigest()

        try:
            if users[user] == password:
                self.StartLoggedWindow()
            else:
                QMessageBox.critical(self, "Error", "Wrong password")
                self.loginWindow.lineEdit_2.setText("")
                return
        except:
            QMessageBox.critical(self, "Error", "Ha ocurrido un error")
            self.loginWindow.lineEdit.setText("")
            self.loginWindow.lineEdit_2.setText("")
            
        
    def sign_in(self):
        users=get_users()
        if self.loginWindow.lineEdit.text() != "" or self.loginWindow.lineEdit_2.text() != "":
            user = self.loginWindow.lineEdit.text()
            password = hashlib.sha512(self.loginWindow.lineEdit_2.text().encode()).hexdigest()
            if user not in users:
                users.update({user:password})
            else:
                QMessageBox.warning(self, "Registro", "Usuario ya ocupado")
                self.loginWindow.lineEdit.setText("")
                self.loginWindow.lineEdit_2.setText("")

            register_user(users)
            QMessageBox.information(self, "Registro", "Ususario Registrado Exitosamente")
            self.StartLoggedWindow()
        else:
            QMessageBox.critical(self, "Erro", "campos en blanco")
            self.loginWindow.lineEdit.setText("")
            self.loginWindow.lineEdit_2.setText("")
            return



if __name__ == '__main__':
    APP = QApplication(sys.argv)

    GUI = MainWindow()
    GUI.show()

    sys.exit(APP.exec_())


