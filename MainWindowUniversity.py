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
import MainWindowDepartments
import MainWindowStudent
import LoginDialog as loginDialog


class MainWindowUniversity(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindowUniversity, self).__init__(*args, **kwargs)

        self.conn = sqlite3.connect("info.db")
        self.c = self.conn.cursor()
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS students(uni_id INTEGER PRIMARY KEY AUTOINCREMENT ,uni_name TEXT)")
        self.c.close()

        file_menu = self.menuBar().addMenu("&File")

        help_menu = self.menuBar().addMenu("&About")
        self.setWindowTitle("Universities Management")
        self.setWindowState(Qt.WindowMaximized)
        self.setMinimumWidth(500)
        self.setMinimumHeight(250)
        self.main_container = QWidget(self)
        main_layout = QGridLayout(self.main_container)
#####################  Student Data  ###################
        self.tableWidget = QTableWidget()
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setFixedWidth(700)
        self.tableWidget.setColumnWidth(0, 70)
        self.tableWidget.setColumnWidth(1, 400)
        self.tableWidget.setColumnWidth(2, 85)
        self.tableWidget.setColumnWidth(3, 125)
        self.tableWidget.setHorizontalHeaderLabels(
            ("ID", "University", "New ", "Departments"))

        main_layout.addWidget(self.tableWidget, 0, 0)
        self.setCentralWidget(self.main_container)

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction(
            QIcon("icon/real-estate.png"), "Add University", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Add Student")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon("icon/refresh .png"), "Refresh", self)
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Refresh Table")
        toolbar.addAction(btn_ac_refresh)

        btn_ac_search = QAction(QIcon("icon/search.png"), "Search", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Search User")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("icon/trash.png"), "Delete", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Delete User")
        toolbar.addAction(btn_ac_delete)

        self.container = QWidget(self)
        self.container.setFixedWidth(20)
        toolbar.addWidget(self.container)

        self.container = QWidget(self)
        self.container.setFixedWidth(20)
        toolbar.addWidget(self.container)

        show_deparments = QAction(
            QIcon("icon/info.png"), "Show Departments", self)
        show_deparments.triggered.connect(
            lambda: self.showdeparments(main_layout))
        show_deparments.setStatusTip("Show Departments")
        toolbar.addAction(show_deparments)

        self.container = QWidget(self)
        self.container.setFixedWidth(650)
        toolbar.addWidget(self.container)

        self.container2 = QWidget(self)
        self.container2.setFixedWidth(400)
        layout = QGridLayout(self.container2)

        search_by_name = QLineEdit()
        search_by_name.setPlaceholderText("Name or surname")
        search_by_name.setFixedWidth(200)
        layout.addWidget(search_by_name, 0, 0)

        QBtn = QPushButton()
        QBtn.setIcon(QIcon("icon/search.png"))
        QBtn.clicked.connect(
            lambda: self.search_by(search_by_name.text()))

        loout_Btn = QPushButton()
        loout_Btn.setIcon(QIcon("icon/logout.png"))
        loout_Btn.setStatusTip("Logout")
        loout_Btn.clicked.connect(self.logout)

        space = QWidget(self)
        space.setFixedWidth(50)

        layout.addWidget(QBtn, 0, 1)
        layout.addWidget(space, 0, 2)
        layout.addWidget(loout_Btn, 0, 3)

        toolbar.addWidget(self.container2)

        adduser_action = QAction(
            QIcon("icon/real-estate.png"), "Insert University", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        searchuser_action = QAction(
            QIcon("icon/search.png"), "Search university", self)
        searchuser_action.triggered.connect(self.search)
        file_menu.addAction(searchuser_action)

        deluser_action = QAction(QIcon("icon/trash.png"), "Delete", self)
        deluser_action.triggered.connect(self.delete)
        file_menu.addAction(deluser_action)

        close_action = QAction(QIcon("icon/close.png"), "Close", self)
        close_action.triggered.connect(self.close_app)
        file_menu.addAction(close_action)

        about_action = QAction(QIcon("icon/info.png"), "Developer", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

    def loaddata(self):
        self.connection = sqlite3.connect("info.db")
        query = "SELECT * FROM Universities"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            uniName = ""
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
        self.loaddata()

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

    def insert(self):
        dlg = InsertDialog.InsertUniversity()
        dlg.exec_()
        self.loaddata()

    def delete(self):
        dlg = DeleteDialog.DeleteUniversity()
        dlg.exec_()
        self.loaddata()

    def search(self):
        dlg = SearchDialog.SearchUniversity()
        dlg.exec_()

    def about(self):
        dlg = AboutDialog.AboutDialog()
        dlg.exec_()

    def search_by(self, income):
        print(income)

    def goToStudents(self):
        self.close()
        window = MainWindowStudent.MainWindowStudent(self)
        window.show()
        window.loaddata()

    def showdeparments(self, main_layout):
        self.widef = QWidget(self)
        self.widef.setFixedWidth(100)
        self.but = QPushButton(self.widef)
        self.but.clicked.connect(
            lambda: self.removwidget(main_layout, self.widef))
        main_layout.addWidget(self.widef, 0, 1)

    def removwidget(self, main_layout, widef):
        main_layout.removeWidget(self.widef)
        self.widef.deleteLater()
        self.widef = None

    def logout(self):
        self.close()
        passchick = loginDialog.LoginDialog()
        if(passchick.exec_() == QDialog.Accepted):
            choossedlg = loginDialog.LoginChoice()
            status = choossedlg.exec_()
            if(status == QDialog.Accepted):
                if(choossedlg.getChoice() == "university"):
                    self.show()

                elif(choossedlg.getChoice() == "Student"):
                    window = MainWindowStudent.MainWindowStudent()
                    window.show()
                    window.loaddata()

    def close_app(self):
        self.close()