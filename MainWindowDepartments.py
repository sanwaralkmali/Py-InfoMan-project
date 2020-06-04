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

        self.setMinimumSize(800, 700)
        self.setMaximumSize(800, 700)

        self.conn = sqlite3.connect("info.db")
        self.c = self.conn.cursor()
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS Departments (" +
            "uni_id INTEGER," +
            "dep_name TEXT NOT NULL, " +
            "price INTEGER NOT NULL, " +
            "info TEXT, " +
            "FOREIGN KEY(uni_id) REFERENCES Universities(uni_id), " +
            "PRIMARY KEY(uni_id,dep_name) ")
        self.c.close()

        uni_id = u_id
        file_menu = self.menuBar().addMenu("&File")

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
        self.tableWidget.setColumnWidth(0, 180)
        self.tableWidget.setColumnWidth(1, 140)
        self.tableWidget.setColumnWidth(2, 380)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setHorizontalHeaderLabels(
            ("Department", "price", "detailes", "Delete"))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction(QIcon(
            "/home/salah/Desktop/Py-infoman-gui-project/icon/add.png"), "Add Department", self)
        btn_ac_adduser.triggered.connect(lambda: self.insert(uni_id))
        btn_ac_adduser.setStatusTip("Add Student")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon(
            "/home/salah/Desktop/Py-infoman-gui-project/icon/refresh .png"), "Refresh", self)
        btn_ac_refresh.triggered.connect(lambda: self.loaddata(u_id))
        btn_ac_refresh.setStatusTip("Refresh Table")
        toolbar.addAction(btn_ac_refresh)

        btn_ac_delete = QAction(QIcon(
            "/home/salah/Desktop/Py-infoman-gui-project/icon/trash.png"), "Delete", self)
        btn_ac_delete.triggered.connect(lambda: self.delete(u_id))
        btn_ac_delete.setStatusTip("Delete User")
        toolbar.addAction(btn_ac_delete)

        self.container = QWidget(self)
        self.container.setFixedWidth(650)
        toolbar.addWidget(self.container)

        close_deparments = QAction(
            QIcon("/home/salah/Desktop/Py-infoman-gui-project/icon/logout.png"), "Logout", self)
        close_deparments.triggered.connect(self.close_app)
        close_deparments.setStatusTip("Logout")
        toolbar.addAction(close_deparments)

        rm_all_action = QAction(
            QIcon("/home/salah/Desktop/Py-infoman-gui-project/icon/criss-cross.png"), "Delete All Deparments", self)
        rm_all_action.triggered.connect(lambda: self.delete_all(uni_id))
        file_menu.addAction(rm_all_action)

        close_action = QAction(QIcon(
            "/home/salah/Desktop/Py-infoman-gui-project/icon/close.png"), "Close", self)
        close_action.triggered.connect(self.close_app)
        file_menu.addAction(close_action)

    def loaddata(self, uniIDP):
        self.connection = sqlite3.connect("info.db")
        query = "SELECT dep_name , price , info FROM Departments WHERE uni_id=" + \
            str(uniIDP)
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(data)))

            remove_dep_btn = QPushButton(self.tableWidget)
            remove_dep_btn.setText('remove')
            remove_dep_btn.clicked.connect(self.delete_department)
            self.tableWidget.setCellWidget(row_number, 3, remove_dep_btn)

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

    def delete_department(self):
        qm = QMessageBox()
        qm.setWindowTitle("Warining")
        ret = qm.warning(
            self, '', "Are You sure?", qm.Yes | qm.No)
        if ret == qm.Yes:
            unId = self.tableWidget.item(
                self.tableWidget.currentRow(), 0).text()
            depName = self.tableWidget.item(
                self.tableWidget.currentRow(), 1).text()
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
                    self.loaddata(unId)

    def delete_all(self, uni_id):
        try:
            self.conn = sqlite3.connect("info.db")
            self.c = self.conn.cursor()
            self.c.execute(
                "DELETE from Departments Where uni_id=" + str(uni_id))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(
                QMessageBox(), 'Successful', 'All the records are removed from the database.')

        except Exception as error:
            print(error)
            QMessageBox.warning(QMessageBox(), 'Error',
                                'Could not delete the records from the database.')
        self.loaddata(uni_id)

    def about(self):
        dlg = AboutDialog.AboutDialog()
        dlg.exec_()

    def close_app(self):
        self.close()
