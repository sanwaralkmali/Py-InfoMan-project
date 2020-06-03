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


class MainWindowDepartments(QMainWindow):

    def __init__(self, u_id, u_name, * args, **kwargs):
        super(MainWindowDepartments, self).__init__(*args, **kwargs)

        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setMinimumSize(800, 700)
        self.setMaximumSize(800, 700)

        self.conn = sqlite3.connect("info.db")
        self.c = self.conn.cursor()
        uni_id = u_id
        file_menu = self.menuBar().addMenu("&File")

        help_menu = self.menuBar().addMenu("&About")

        self.setWindowTitle(str(u_name)+" University")

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

        btn_ac_adduser = QAction(QIcon("icon/add.png"), "Add Department", self)
        btn_ac_adduser.triggered.connect(lambda: self.insert(uni_id))
        btn_ac_adduser.setStatusTip("Add Student")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon("icon/refresh .png"), "Refresh", self)
        btn_ac_refresh.triggered.connect(lambda: self.loaddata(u_id))
        btn_ac_refresh.setStatusTip("Refresh Table")
        toolbar.addAction(btn_ac_refresh)

        btn_ac_delete = QAction(QIcon("icon/trash.png"), "Delete", self)
        btn_ac_delete.triggered.connect(lambda: self.delete(u_id))
        btn_ac_delete.setStatusTip("Delete User")
        toolbar.addAction(btn_ac_delete)

        self.container = QWidget(self)
        self.container.setFixedWidth(650)
        toolbar.addWidget(self.container)

        close_deparments = QAction(
            QIcon("icon/logout.png"), "Logout", self)
        close_deparments.triggered.connect(self.closedeparments)
        close_deparments.setStatusTip("Logout")
        toolbar.addAction(close_deparments)

        adduser_action = QAction(
            QIcon("icon/add.png"), "Insert Department", self)
        adduser_action.triggered.connect(lambda: self.insert(uni_id))
        file_menu.addAction(adduser_action)

        deluser_action = QAction(QIcon("icon/trash.png"), "Delete", self)
        deluser_action.triggered.connect(lambda: self.delete(u_id))
        file_menu.addAction(deluser_action)

        close_action = QAction(QIcon("icon/close.png"), "Close", self)
        close_action.triggered.connect(self.close_app)
        file_menu.addAction(close_action)

        about_action = QAction(QIcon("icon/info.png"), "Developer", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

    def loaddata(self, uniIDP):
        self.connection = sqlite3.connect("info.db")
        query = "SELECT * FROM Departments WHERE uni_id=" + str(uniIDP)
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

    def insert(self, uniIDP):
        dlg = InsertDialog.InsertDepartment(uniIDP)
        dlg.exec_()
        self.loaddata(uniIDP)

    def delete(self, uni_id):
        dlg = DeleteDialog.DeleteDepartment()
        dlg.exec_()
        self.loaddata(uni_id)

    def about(self):
        dlg = AboutDialog.AboutDialog()
        dlg.exec_()

    def closedeparments(self):
        MainWindowDepartments.close(self)

    def close_app(self):
        self.close()
