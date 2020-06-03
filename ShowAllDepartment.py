from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import *
import sys
import sqlite3


class ShowAllDepartment(QMainWindow):
    def __init__(self, * args, **kwargs):
        super(ShowAllDepartment, self).__init__(*args, **kwargs)
        self.setMinimumSize(1000, 700)
        self.setMaximumSize(1000, 700)
        self.conn = sqlite3.connect("info.db")
        self.c = self.conn.cursor()
        file_menu = self.menuBar().addMenu("&File")
        self.setWindowTitle("All Departments")
#####################    ###################
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
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(
            ("University", "Department", "price", "detailes", "Delete"))

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

    def loaddata(self):
        self.connection = sqlite3.connect("info.db")
        query = "SELECT Universities.uni_name, Departments.dep_name, "
        query += "Departments.price,Departments.info From Departments "
        query += "INNER JOIN Universities on Departments.uni_id = Universities.uni_id"
        query += " ORDER BY Universities.uni_name"

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
            self.tableWidget.setCellWidget(row_number, 4, remove_dep_btn)

        self.connection.close()

    def close_app(self):
        self.close()

    def delete_department(self):
        qm = QMessageBox()
        ret = qm.question(
            self, '', "Are You sure?", qm.Yes | qm.No)
        if ret == qm.Yes:
            unId = self.tableWidget.item(
                self.tableWidget.currentRow(), 0).text()
            depName = self.tableWidget.item(
                self.tableWidget.currentRow(), 1).text()
            try:
                self.conn = sqlite3.connect("info.db")
                self.c = self.conn.cursor()
                query = "DELETE FROM Departments WHERE uni_id in"
                query += "( SELECT uni_id FROM Universities "
                query += "WHERE uni_name = ?) AND dep_name=?"
                self.c.execute(
                    query, (unId, depName))

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
