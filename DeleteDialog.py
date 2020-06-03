from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3


class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Delete")

        self.setWindowTitle("Delete Student")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deletestudent)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Student ID")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deletestudent(self):

        qm = QMessageBox()
        ret = qm.question(
            self, '', "Are You sure?", qm.Yes | qm.No)
        if ret == qm.Yes:
            delrol = self.deleteinput.text()
            try:
                self.conn = sqlite3.connect("info.db")
                self.c = self.conn.cursor()
                self.c.execute(
                    "DELETE from Students WHERE stu_id="+str(delrol))
                self.conn.commit()
                self.c.close()
                QMessageBox.information(
                    QMessageBox(), 'Successful', 'Student removed from the database ')
            except Exception:
                QMessageBox.warning(QMessageBox(), 'Error',
                                    'This Id in not valid!')
            finally:
                if(self.conn):
                    self.conn.close()
                    self.close()


class DeleteUniversity(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteUniversity, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Delete")

        self.setWindowTitle("Delete University")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deleteUniversity)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Unversity Id.")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deleteUniversity(self):
        qm = QMessageBox()
        ret = qm.question(
            self, '', "Are You sure?", qm.Yes | qm.No)
        if ret == qm.Yes:
            delrol = self.deleteinput.text()
            try:
                self.conn = sqlite3.connect("info.db")
                self.c = self.conn.cursor()
                self.c.execute(
                    "DELETE from Universities WHERE uni_id= "+str(delrol))
                self.conn.commit()
                QMessageBox.information(
                    QMessageBox(), 'Successful', 'Deleted From Table ')
                self.c.close()

            except sqlite3.Error as errot:
                print(errot)
                QMessageBox.warning(QMessageBox(), 'Error',
                                    'Could not Delete This university from the database.')

            finally:
                if(self.conn):
                    self.conn.close()
                    self.close()

    class DeleteDepartment(QDialog):
        def __init__(self, *args, **kwargs):
            super(DeleteDepartment, self).__init__(*args, **kwargs)

            self.QBtn = QPushButton()
            self.QBtn.setText("Delete")

            self.setWindowTitle("Delete Department")
            self.setFixedWidth(300)
            self.setFixedHeight(100)
            self.QBtn.clicked.connect(self.deleteDepartment)
            layout = QVBoxLayout()

            self.unvIdInput = QLineEdit()
            self.onlyInt = QIntValidator()
            self.unvIdInput.setValidator(self.onlyInt)
            self.unvIdInput.setPlaceholderText("Unversity Id.")

            self.depIdInput = QLineEdit()
            self.depIdInput.setPlaceholderText("Department name.")

            layout.addWidget(self.unvIdInput)
            layout.addWidget(self.depIdInput)
            layout.addWidget(self.QBtn)
            self.setLayout(layout)

        def deleteDepartment(self):
            qm = QMessageBox()
            ret = qm.question(
                self, '', "Are You sure?", qm.Yes | qm.No)
            if ret == qm.Yes:
                unId = self.unvIdInput.text()
                depName = self.depIdInput.text()
                try:
                    self.conn = sqlite3.connect("info.db")
                    self.c = self.conn.cursor()
                    self.c.execute(
                        "DELETE from Departments WHERE uni_id=? AND dep_name=?", (unId, depName))

                    i = self.conn.commit()

                    QMessageBox.information(
                        QMessageBox(), 'Successful', 'Department was Deleted From the database')

                    self.c.close()

                except sqlite3.Error as errot:
                    QMessageBox.warning(QMessageBox(), 'Error',
                                        'Could not Delete Department from the database.')

                finally:
                    if(self.conn):
                        self.conn.close()
                        self.close()
