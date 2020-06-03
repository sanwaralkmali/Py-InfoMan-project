from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import *
import sys
import sqlite3


class StudentSearch(QMainWindow):
    def __init__(self, * args, **kwargs):
        super(StudentSearch, self).__init__(*args, **kwargs)
        self.setMinimumSize(1000, 700)
        self.setMaximumSize(1000, 700)
        self.conn = sqlite3.connect("info.db")
        self.c = self.conn.cursor()
        file_menu = self.menuBar().addMenu("&File")
        self.setWindowTitle("Search")
#####################    ###################
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setColumnWidth(0, 40)
        self.tableWidget.setColumnWidth(1, 180)
        self.tableWidget.setColumnWidth(2, 160)
        self.tableWidget.setColumnWidth(3, 180)
        self.tableWidget.setColumnWidth(4, 320)
        self.tableWidget.setColumnWidth(5, 100)

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(
            ("ID", "Name", "Surname", "Phone Number", "Detailes", "Delete"))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        self.container = QWidget(self)
        self.container.setFixedWidth(950)
        toolbar.addWidget(self.container)

        close_deparments = QAction(
            QIcon("icon/criss-cross.png"), "Close", self)
        close_deparments.triggered.connect(self.close_app)
        close_deparments.setStatusTip("Close")
        toolbar.addAction(close_deparments)

        close_action = QAction(QIcon("icon/close.png"), "Close", self)
        close_action.triggered.connect(self.close_app)
        file_menu.addAction(close_action)

    def loaddata(self, parmeter):
        self.connection = sqlite3.connect("info.db")
        query = "SELECT * FROM Students WHERE stu_name LIKE '%"+parmeter+"%' "
        query += " OR stu_surname LIKE '%"+parmeter+"%' "

        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))

            remove_stu_btn = QPushButton(self.tableWidget)
            remove_stu_btn.setText('remove')
            remove_stu_btn.clicked.connect(self.delte_student)
            self.tableWidget.setCellWidget(row_number, 5, remove_stu_btn)

        self.connection.close()

    def close_app(self):
        self.close()

    def delte_student(self):
        qm = QMessageBox()
        ret = qm.question(
            self, '', "Are You sure?", qm.Yes | qm.No)
        if ret == qm.Yes:
            delrol = self.tableWidget.item(
                self.tableWidget.currentRow(), 0).text()
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
