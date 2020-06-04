from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import *
import sys
import sqlite3
import MainWindowDepartments
import InsertDialog


class UniversitySearch(QMainWindow):
    def __init__(self, * args, **kwargs):
        super(UniversitySearch, self).__init__(*args, **kwargs)
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
        self.tableWidget.setColumnCount(4)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setColumnWidth(0, 70)
        self.tableWidget.setColumnWidth(1, 500)
        self.tableWidget.setColumnWidth(2, 185)
        self.tableWidget.setColumnWidth(3, 125)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(
            ("ID", "University", "New ", "Departments"))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        self.container = QWidget(self)
        self.container.setFixedWidth(950)
        toolbar.addWidget(self.container)

        close_deparments = QAction(
            QIcon("/home/salah/Desktop/Py-infoman-gui-project/icon/criss-cross.png"), "Close", self)
        close_deparments.triggered.connect(self.close_app)
        close_deparments.setStatusTip("Close")
        toolbar.addAction(close_deparments)

        close_action = QAction(QIcon(
            "/home/salah/Desktop/Py-infoman-gui-project/icon/close.png"), "Close", self)
        close_action.triggered.connect(self.close_app)
        file_menu.addAction(close_action)

    def loaddata(self, parmeter):
        self.connection = sqlite3.connect("info.db")
        query = "SELECT * FROM Universities WHERE uni_name LIKE '%"+parmeter+"%' "

        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))

            adddeptbut = QPushButton(self.tableWidget)
            adddeptbut.setText('Add')
            adddeptbut.clicked.connect(self.addDepartment)

            deptbut = QPushButton(self.tableWidget)
            deptbut.setText('Get')
            deptbut.clicked.connect(self.getDepartments)

            self.tableWidget.setCellWidget(row_number, 2, adddeptbut)
            self.tableWidget.setCellWidget(row_number, 3, deptbut)

        self.connection.close()

    def close_app(self):
        self.close()

    def getDepartments(self):
        window = MainWindowDepartments.MainWindowDepartments(self.tableWidget.item(
            self.tableWidget.currentRow(), 0).text(), self.tableWidget.item(
            self.tableWidget.currentRow(), 1).text())
        window.show()
        window.loaddata(self.tableWidget.item(
            self.tableWidget.currentRow(), 0).text())

    def addDepartment(self):
        dlg = InsertDialog.InsertDepartment(self.tableWidget.item(
            self.tableWidget.currentRow(), 0).text())
        dlg.exec_()
