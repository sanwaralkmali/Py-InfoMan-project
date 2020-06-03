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
import LoginDialog as loginDialog


class MainWindowStudent(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindowStudent, self).__init__(*args, **kwargs)

        self.conn = sqlite3.connect("info.db")
        self.c = self.conn.cursor()
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS students(roll INTEGER PRIMARY KEY AUTOINCREMENT ,name TEXT,branch TEXT,sem INTEGER,mobile INTEGER,address TEXT)")
        self.c.close()

        file_menu = self.menuBar().addMenu("&File")

        help_menu = self.menuBar().addMenu("&About")
        self.setWindowTitle("Students Management")
        self.setWindowState(Qt.WindowMaximized)
        self.setMinimumWidth(500)
        self.setMinimumHeight(250)

#####################  Student Data  ###################
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(
            ("ID", "Name", "Surname", "Mobile", "Details"))

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction(
            QIcon("icon/user-profiles.png"), "Add Student", self)
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

        # show_universities = QAction(
        # QIcon("icon/school.png"), "Show Universities", self)
        # show_universities.triggered.connect(self.goToUniversities)
        # show_universities.setStatusTip("Show Universities")
        # toolbar.addAction(show_universities)

        self.container = QWidget(self)
        self.container.setFixedWidth(20)
        toolbar.addWidget(self.container)

        show_deparments = QAction(
            QIcon("icon/info.png"), "Show Departments", self)
        show_deparments.triggered.connect(self.showdeparments)
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
       # toolbar.addWidget(search_by_name)

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

        adduser_action = QAction(QIcon("icon/add.png"), "Insert Student", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        searchuser_action = QAction(
            QIcon("icon/search.png"), "Search Student", self)
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
        query = "SELECT * FROM Students"
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

    def insert(self):
        dlg = InsertDialog.InsertDialog()
        dlg.exec_()
        self.loaddata()

    def delete(self):
        dlg = DeleteDialog.DeleteDialog()
        dlg.exec_()
        self.loaddata()

    def search(self):
        dlg = SearchDialog.SearchDialog()
        dlg.exec_()

    def about(self):
        dlg = AboutDialog.AboutDialog()
        dlg.exec_()

    def search_by(self, income):
        print(income)

    def goToUniversities(self):
        if(not self.close()):
            self.show()
        else:
            window = MainWindowUniversity.MainWindowUniversity(self)
            window.show()
            window.loaddata()

    def showdeparments(self):
        return

    def logout(self):
        self.close()
        passchick = loginDialog.LoginDialog()
        if(passchick.exec_() == QDialog.Accepted):
            choossedlg = loginDialog.LoginChoice()
            status = choossedlg.exec_()
            if(status == QDialog.Accepted):
                if(choossedlg.getChoice() == "Student"):
                    self.show()

                elif(choossedlg.getChoice() == "university"):
                    window = MainWindowUniversity.MainWindowUniversity()
                    window.show()
                    window.loaddata()

    def close_app(self):
        self.close()
