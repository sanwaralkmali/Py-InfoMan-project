from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3


class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Search")

        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.searchstudent)
        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.searchinput.setPlaceholderText("Student ID")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def searchstudent(self):

        searchrol = ""
        searchrol = self.searchinput.text()
        try:
            self.conn = sqlite3.connect("info.db")
            self.c = self.conn.cursor()
            result = self.c.execute(
                "SELECT * from Students WHERE stu_id="+str(searchrol))
            row = result.fetchone()
            serachresult = "Student ID : "+str(row[0])+'\n'+"Name : "+str(row[1])+'\n'+"Surname : "+str(
                row[2])+'\n'+"Phone Number : "+str(row[3])+'\n'+"Detailes : "+str(row[4])
            QMessageBox.information(QMessageBox(), 'Successful', serachresult)
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error',
                                'Could not Find student from the database.')

        self.close()


class SearchUniversity(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchUniversity, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Search")

        self.setWindowTitle("Search University")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.search_university)
        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.searchinput.setPlaceholderText("University Name")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def search_university(self):

        searchrol = ""
        searchrol = self.searchinput.text()
        try:
            self.conn = sqlite3.connect("info.db")
            self.c = self.conn.cursor()
            result = self.c.execute(
                "SELECT * from Universities WHERE uni_name= '"+str(searchrol) + "'")
            row = result.fetchone()
            serachresult = "ID : " + \
                str(row[0])+'\n'+"University : "+str(row[1])+'\n'
            QMessageBox.information(QMessageBox(), 'Successful', serachresult)
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except Exception as error:
            print(error)
            QMessageBox.warning(QMessageBox(), 'Error',
                                'Could not Find student from the database.')

        self.close()
