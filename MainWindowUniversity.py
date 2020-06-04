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
import ShowAllDepartment
import UniversitySearch


class MainWindowUniversity(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindowUniversity, self).__init__(*args, **kwargs)

        self.conn = sqlite3.connect("info.db")
        self.c = self.conn.cursor()
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS Universities (" +
            "uni_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE," +
            "uni_name TEXT NOT NULL UNIQUE)")
        self.c.close()

        file_menu = self.menuBar().addMenu("&File")

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
        self.tableWidget.setFixedWidth(800)
        self.tableWidget.setColumnWidth(0, 70)
        self.tableWidget.setColumnWidth(1, 495)
        self.tableWidget.setColumnWidth(2, 105)
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
            QIcon("/home/salah/Desktop/Py-infoman-gui-project/icon/real-estate.png"), "Add University", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Add Student")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon(
            "/home/salah/Desktop/Py-infoman-gui-project/icon/refresh .png"), "Refresh", self)
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Refresh Table")
        toolbar.addAction(btn_ac_refresh)

        btn_ac_search = QAction(QIcon(
            "/home/salah/Desktop/Py-infoman-gui-project/icon/search.png"), "Search", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Search User")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon(
            "/home/salah/Desktop/Py-infoman-gui-project/icon/trash.png"), "Delete", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Delete User")
        toolbar.addAction(btn_ac_delete)

        self.container = QWidget(self)
        self.container.setFixedWidth(20)
        toolbar.addWidget(self.container)

        self.container = QWidget(self)
        self.container.setFixedWidth(20)
        toolbar.addWidget(self.container)

        self.container = QWidget(self)
        self.container.setFixedWidth(650)
        toolbar.addWidget(self.container)

        self.container2 = QWidget(self)
        self.container2.setFixedWidth(400)
        layout = QGridLayout(self.container2)

        search_by_name = QLineEdit()
        search_by_name.setPlaceholderText("search")
        search_by_name.setFixedWidth(200)
        layout.addWidget(search_by_name, 0, 0)

        QBtn = QPushButton()
        QBtn.setIcon(
            QIcon("/home/salah/Desktop/Py-infoman-gui-project/icon/search.png"))
        QBtn.clicked.connect(
            lambda: self.search_by(search_by_name.text()))

        loout_Btn = QPushButton()
        loout_Btn.setIcon(
            QIcon("/home/salah/Desktop/Py-infoman-gui-project/icon/logout.png"))
        loout_Btn.setStatusTip("Logout")
        loout_Btn.clicked.connect(self.logout)

        space = QWidget(self)
        space.setFixedWidth(100)

        layout.addWidget(QBtn, 0, 1)
        layout.addWidget(space, 0, 2)
        toolbar.addWidget(self.container2)

        logout_Btn = QAction(
            QIcon("/home/salah/Desktop/Py-infoman-gui-project/icon/logout.png"), "Logout", self)
        logout_Btn.triggered.connect(self.logout)
        logout_Btn.setStatusTip("LOGOUT")
        toolbar.addAction(logout_Btn)

        btn_ac_close = QAction(
            QIcon("/home/salah/Desktop/Py-infoman-gui-project/icon/criss-cross.png"), "Closs App", self)
        btn_ac_close.triggered.connect(self.close_app)
        btn_ac_close.setStatusTip("Closs App")
        toolbar.addAction(btn_ac_close)

        show_deparments = QAction(
            QIcon("/home/salah/Desktop/Py-infoman-gui-project/icon/school.png"), "Show All Deparments", self)
        show_deparments.triggered.connect(self.show_all_departments)
        file_menu.addAction(show_deparments)

        adduser_action = QAction(
            QIcon("/home/salah/Desktop/Py-infoman-gui-project/icon/real-estate.png"), "Insert University", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        searchuser_action = QAction(
            QIcon("/home/salah/Desktop/Py-infoman-gui-project/icon/search.png"), "Search university", self)
        searchuser_action.triggered.connect(self.search)
        file_menu.addAction(searchuser_action)

        deluser_action = QAction(
            QIcon("/home/salah/Desktop/Py-infoman-gui-project/icon/trash.png"), "Delete University", self)
        deluser_action.triggered.connect(self.delete)
        file_menu.addAction(deluser_action)

        rm_all_action = QAction(
            QIcon("/home/salah/Desktop/Py-infoman-gui-project/icon/criss-cross.png"), "Delete All Universities", self)
        rm_all_action.triggered.connect(self.delete_all)
        file_menu.addAction(rm_all_action)

        about_action = QAction(QIcon(
            "/home/salah/Desktop/Py-infoman-gui-project/icon/info.png"), "About Developer", self)
        about_action.triggered.connect(self.about)
        file_menu.addAction(about_action)

        close_action = QAction(QIcon(
            "/home/salah/Desktop/Py-infoman-gui-project/icon/close.png"), "Close", self)
        close_action.triggered.connect(self.close_app)
        file_menu.addAction(close_action)

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

    def delete_all(self):
        qm = QMessageBox()
        ret = qm.warning(
            self, '', "All the departments will be removed !\n\n\n Are You sure?", qm.Yes | qm.No)
        if ret == qm.Yes:
            try:
                self.conn = sqlite3.connect("info.db")
                self.c = self.conn.cursor()
                self.c.execute("DELETE from Universities")
                self.conn.commit()
                self.c.close()
                self.conn.close()
                QMessageBox.information(
                    QMessageBox(), 'Successful', 'All the records are removed from the database.')

            except Exception as error:
                print(error)
                QMessageBox.warning(QMessageBox(), 'Error',
                                    'Could not delete the records from the database.')

            self.loaddata()

    def search(self):
        dlg = SearchDialog.SearchUniversity()
        dlg.exec_()

    def about(self):
        dlg = AboutDialog.AboutDialog()
        dlg.exec_()

    def show_all_departments(self):
        window = ShowAllDepartment.ShowAllDepartment(self)
        window.show()
        window.loaddata()

    def removwidget(self, main_layout, widef):
        main_layout.removeWidget(self.widef)
        try:
            self.widef.deleteLater()
        except Exception:
            print("error")

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

    def search_by(self, parmeter):
        if(parmeter.strip() == ""):
            QMessageBox.warning(QMessageBox(), 'Error',
                                'Yu must enter at leasr one key word!')
        else:
            window = UniversitySearch.UniversitySearch(self)
            window.show()
            window.loaddata(parmeter)
