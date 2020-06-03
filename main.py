from PyQt5.QtWidgets import *
import sys
import LoginDialog as loginDialog
import MainWindowStudent
import MainWindowUniversity
import os

app = QApplication(sys.argv)
passchick = loginDialog.LoginDialog()
if(passchick.exec_() == QDialog.Accepted):
    choossedlg = loginDialog.LoginChoice()
    status = choossedlg.exec_()
    if(status == QDialog.Accepted):
        if(choossedlg.getChoice() == "Student"):
            window = MainWindowStudent.MainWindowStudent()
            window.show()
            window.loaddata()

        elif(choossedlg.getChoice() == "university"):
            window = MainWindowUniversity.MainWindowUniversity()
            window.show()
            window.loaddata()

        sys.exit(app.exec_())
