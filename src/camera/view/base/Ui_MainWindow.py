# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 847)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.columnView = QtWidgets.QColumnView(self.frame)
        self.columnView.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.columnView.setObjectName("columnView")

        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 791, 601))
        self.label.setText("")
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")

        self.connect_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_btn.setGeometry(QtCore.QRect(600, 640, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.connect_btn.setFont(font)
        self.connect_btn.setObjectName("connect_btn")

        self.cancel_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_btn.setGeometry(QtCore.QRect(230, 760, 341, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.cancel_btn.setFont(font)
        self.cancel_btn.setObjectName("cancel_btn")

        self.camera_url = QtWidgets.QLineEdit(self.centralwidget)
        self.camera_url.setGeometry(QtCore.QRect(230, 640, 331, 41))
        self.camera_url.setWhatsThis("")
        self.camera_url.setObjectName("camera_url")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(90, 640, 111, 41))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(80, 630, 141, 61))

        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(80, 690, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.connect_statu = QtWidgets.QLabel(self.centralwidget)
        self.connect_statu.setGeometry(QtCore.QRect(230, 700, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.connect_statu.setFont(font)
        self.connect_statu.setObjectName("connect_statu")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "camera"))
        self.connect_btn.setText(_translate("MainWindow", "连接"))
        self.cancel_btn.setText(_translate("MainWindow", "关闭"))
        self.label_3.setText(_translate("MainWindow", "摄像头的IP地址："))
        self.label_4.setText(_translate("MainWindow", "状态："))
        self.connect_statu.setText(_translate("MainWindow", "未连接"))
