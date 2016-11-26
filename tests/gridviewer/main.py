# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_window(object):
    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(791, 669)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(8)
        window.setFont(font)
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.view = QtWidgets.QGraphicsView(self.centralwidget)
        self.view.setObjectName("view")
        self.verticalLayout.addWidget(self.view)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, 0, 10, -1)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.opt_hex = QtWidgets.QRadioButton(self.centralwidget)
        self.opt_hex.setMinimumSize(QtCore.QSize(0, 28))
        self.opt_hex.setMaximumSize(QtCore.QSize(140, 28))
        self.opt_hex.setChecked(True)
        self.opt_hex.setObjectName("opt_hex")
        self.horizontalLayout_2.addWidget(self.opt_hex)
        self.opt_square = QtWidgets.QRadioButton(self.centralwidget)
        self.opt_square.setMinimumSize(QtCore.QSize(0, 28))
        self.opt_square.setMaximumSize(QtCore.QSize(140, 28))
        self.opt_square.setObjectName("opt_square")
        self.horizontalLayout_2.addWidget(self.opt_square)
        self.spb_width = QtWidgets.QSpinBox(self.centralwidget)
        self.spb_width.setMinimumSize(QtCore.QSize(20, 28))
        self.spb_width.setMaximumSize(QtCore.QSize(80, 28))
        self.spb_width.setMinimum(1)
        self.spb_width.setMaximum(9999)
        self.spb_width.setObjectName("spb_width")
        self.horizontalLayout_2.addWidget(self.spb_width)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMinimumSize(QtCore.QSize(10, 0))
        self.label_2.setMaximumSize(QtCore.QSize(10, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spb_height = QtWidgets.QSpinBox(self.centralwidget)
        self.spb_height.setMinimumSize(QtCore.QSize(20, 28))
        self.spb_height.setMaximumSize(QtCore.QSize(80, 28))
        self.spb_height.setMinimum(1)
        self.spb_height.setMaximum(9999)
        self.spb_height.setObjectName("spb_height")
        self.horizontalLayout_2.addWidget(self.spb_height)
        self.btn_make = QtWidgets.QToolButton(self.centralwidget)
        self.btn_make.setMinimumSize(QtCore.QSize(35, 35))
        self.btn_make.setObjectName("btn_make")
        self.horizontalLayout_2.addWidget(self.btn_make)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 791, 19))
        self.menubar.setObjectName("menubar")
        self.menuFichier = QtWidgets.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier")
        window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)
        self.actionQuitter = QtWidgets.QAction(window)
        self.actionQuitter.setObjectName("actionQuitter")
        self.menuFichier.addAction(self.actionQuitter)
        self.menubar.addAction(self.menuFichier.menuAction())

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "MainWindow"))
        self.label.setText(_translate("window", "Grid Viewer"))
        self.opt_hex.setText(_translate("window", "Hexagonal grid"))
        self.opt_square.setText(_translate("window", "Square grid"))
        self.label_2.setText(_translate("window", "X"))
        self.btn_make.setText(_translate("window", ">>"))
        self.menuFichier.setTitle(_translate("window", "Fichier"))
        self.actionQuitter.setText(_translate("window", "Quitter"))
