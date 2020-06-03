from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3


class InsertDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Register")
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.setWindowTitle("Add Student")
        self.setFixedWidth(300)
        self.setFixedHeight(250)

        self.QBtn.clicked.connect(self.addstudent)

        layout = QVBoxLayout()

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Name")
        layout.addWidget(self.nameinput)

        self.surnameinput = QLineEdit()
        self.surnameinput.setPlaceholderText("Surname")
        layout.addWidget(self.surnameinput)
        self.mobileinput = QLineEdit()
        self.mobileinput.setPlaceholderText("Mobile")
        layout.addWidget(self.mobileinput)

        self.infoinput = QLineEdit()
        self.infoinput.setPlaceholderText("Detailes")
        layout.addWidget(self.infoinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addstudent(self):
        name = self.nameinput.text()
        surname = self.surnameinput.text()
        mobile = self.mobileinput.text()
        detailes = self.infoinput.text()
        try:
            if(name.strip() != "" and surname.strip() != ""):
                self.conn = sqlite3.connect("info.db")
                self.c = self.conn.cursor()
                self.c.execute("INSERT INTO Students (stu_name,stu_surname,phone_number,stu_info) VALUES (?,?,?,?)",
                               (name, surname, mobile, detailes))
                self.conn.commit()
                self.c.close()
                self.conn.close()
                QMessageBox.information(
                    QMessageBox(), 'Successful', 'Student is added successfully to the database.')

            else:
                c = 5/0
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error',
                                'Could not add student to the database.')


class InsertUniversity(QDialog):

    def __init__(self, *args, **kwargs):
        super(InsertUniversity, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Add")

        self.setWindowTitle("Add University")
        self.setFixedWidth(200)
        self.setFixedHeight(150)

        self.QBtn.clicked.connect(self.addstudent)

        layout = QVBoxLayout()

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("University Name")
        layout.addWidget(self.nameinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addstudent(self):

        name = self.nameinput.text()

        try:
            if(name.strip() != ""):
                self.conn = sqlite3.connect("info.db")
                self.c = self.conn.cursor()
                self.c.execute(
                    "INSERT INTO Universities (uni_name) VALUES ('"+name+"')")
                self.conn.commit()
                self.c.close()
                self.conn.close()
                QMessageBox.information(
                    QMessageBox(), 'Successful', 'University is added successfully to the database.')

            else:
                u = c/0

        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error',
                                'Could not add university to the database.')


class InsertDepartment(QDialog):
    def __init__(self, id, *args, **kwargs):
        super(InsertDepartment, self).__init__(*args, **kwargs)

        uni_id = id
        self.QBtn = QPushButton()
        self.QBtn.setText("Add")

        self.setWindowTitle("Add Department")
        self.setFixedWidth(300)
        self.setFixedHeight(250)

        self.QBtn.clicked.connect(lambda: self.addDept(uni_id))

        layout = QVBoxLayout()

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Department Name")
        layout.addWidget(self.nameinput)

        self.priceInput = QLineEdit()
        self.priceInput.setPlaceholderText("price")
        layout.addWidget(self.priceInput)

        self.InfoInput = QLineEdit()
        self.InfoInput.setPlaceholderText("Detailes")
        layout.addWidget(self.InfoInput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addDept(self, uni_id):
        uniId = uni_id
        name = self.nameinput.text()
        price = self.priceInput.text()
        info = self.InfoInput.text()
        message = "This record alredy i your database! "

        try:
            if(name.strip() != "" and price.strip() != ""):
                self.conn = sqlite3.connect("info.db")
                self.c = self.conn.cursor()
                self.c.execute(
                    "INSERT INTO Departments (uni_id,dep_name,price,info) VALUES (?,?,?,?)", (uniId, name, price, info))
                self.conn.commit()
                self.c.close()
                self.conn.close()
                QMessageBox.information(
                    QMessageBox(), 'Successful', 'University is added successfully to the database.')
                self.close()

            else:
                if(name.strip() == ""):
                    print(message)
                    message = "You forget to enter department's name !"
                    print(message)

                elif(price.strip() == ""):
                    message = "You forgot to enter the department's Price! "

                c = 5/0

        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', message)
            self.close()
