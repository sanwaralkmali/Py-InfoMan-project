from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import *
import AboutDialog
import InsertDialog
import DeleteDialog
import SearchDialog
import sys
import sqlite3
import time
import MainWindowUniversity


class ShowAllStudents(QMainWindow):

    def __init__(self, * args, **kwargs):
        super(ShowAllStudents, self).__init__(*args, **kwargs)

        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setMinimumSize(1000, 700)
        self.setMaximumSize(1000, 700)

        self.conn = sqlite3.connect("info.db")
        self.c = self.conn.cursor()

        file_menu = self.menuBar().addMenu("&File")

        self.setWindowTitle("All Students")

#####################  Student Data  ###################
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
        self.tableWidget.setHorizontalHeaderLabels(
            ("uni_id", "name", "price", "detailes"))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        self.container = QWidget(self)
        self.container.setFixedWidth(650)
        toolbar.addWidget(self.container)

        close_deparments = QAction(
            QIcon("icon/logout.png"), "Logout", self)
        close_deparments.triggered.connect(self.closedeparments)
        close_deparments.setStatusTip("Logout")
        toolbar.addAction(close_deparments)

        close_action = QAction(QIcon("icon/close.png"), "Close", self)
        close_action.triggered.connect(self.close_app)
        file_menu.addAction(close_action)

    def loaddata(self):
        self.connection = sqlite3.connect("info.db")
        query = "SELECT * FROM Departments ORDER  BY uni_id"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))
        self.connection.close()

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(
            model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    def closedeparments(self):
        self.close()

    def close_app(self):
        self.close()
