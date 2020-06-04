from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QPixmap


class LoginDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(250)
        self.setFixedHeight(150)
        layout = QVBoxLayout()
        self.container = QWidget(self)
        self.labelLog = QLabel(self.container)
        self.pixmap = QPixmap(
            '/home/salah/Desktop/Py-infoman-gui-project/icon/login.png')
        self.labelLog.setPixmap(self.pixmap)
        self.labelLog.setFixedWidth(self.width())
        self.labelLog.setAlignment(Qt.AlignCenter)
        self.passinput = QLineEdit()
        self.passinput.setEchoMode(QLineEdit.Password)
        self.passinput.setPlaceholderText("Enter Password.")
        self.QBtn = QPushButton()
        self.QBtn.setText("Login")
        self.setWindowTitle('Login')
        self.QBtn.clicked.connect(self.login)
        title = QLabel("Login")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)
        layout.addWidget(self.container)
        layout.addWidget(self.passinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def login(self):
        if(self.passinput.text() == ""):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Wrong Password')


class LoginChoice(QDialog):
    choise = "Nothing"

    def __init__(self, *args, **kwargs):
        super(LoginChoice, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(120)

        mainLayout = QtWidgets.QGridLayout(self)

        self.QBtn = QPushButton()
        self.QBtn.setFixedSize(130, 100)
        self.QBtn.setIcon(
            QIcon("/home/salah/Desktop/Py-infoman-gui-project/icon/school.png"))
        self.QBtn.setIconSize(QSize(40, 40))
        self.QBtn.setText("Unversities")

        self.QBtn2 = QPushButton()
        self.QBtn2.setIcon(
            QIcon("/home/salah/Desktop/Py-infoman-gui-project/icon/male-and-female.png"))
        self.QBtn2.setIconSize(QSize(40, 40))
        self.QBtn2.setText("Students")
        self.QBtn2.setFixedSize(130, 100)

        font = self.QBtn.font()
        font.setPointSize(10)
        self.QBtn.setFont(font)
        self.QBtn2.setFont(font)

        self.setWindowTitle('INFOMAN')

        self.QBtn2.clicked.connect(self.student)
        self.QBtn.clicked.connect(self.Unvircities)

        mainLayout.addWidget(self.QBtn, 0, 1)
        mainLayout.addWidget(self.QBtn2, 0, 0)
       # layout.addWidget(title)

        self.setLayout(mainLayout)

    def student(self):
        self.choise = "Student"
        self.accept()

    def Unvircities(self):
        self.choise = "university"
        self.accept()

    def getChoice(self):
        return self.choise
