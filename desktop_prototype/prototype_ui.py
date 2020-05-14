# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(855, 421)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.date_from = QtWidgets.QDateEdit(self.centralwidget)
        self.date_from.setGeometry(QtCore.QRect(10, 20, 110, 22))
        self.date_from.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 5, 1), QtCore.QTime(0, 0, 0)))
        self.date_from.setMinimumDate(QtCore.QDate(1970, 1, 1))
        self.date_from.setObjectName("date_from")
        self.date_to = QtWidgets.QDateEdit(self.centralwidget)
        self.date_to.setGeometry(QtCore.QRect(120, 20, 110, 22))
        self.date_to.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 5, 10), QtCore.QTime(0, 0, 0)))
        self.date_to.setObjectName("date_to")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(240, 20, 151, 23))
        self.pushButton.setObjectName("pushButton")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 80, 841, 291))
        self.tableView.setObjectName("tableView")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 50, 211, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 50, 271, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 855, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Load"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Ссылка на группу во Вконтакте"))
        self.label.setText(_translate("MainWindow", "Например hse_university, doxajournal, cshse"))
