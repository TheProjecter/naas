# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmmenu.ui'
#
# Created: Mon Dec 28 21:44:51 2009
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmmenu(object):
    def setupUi(self, frmmenu):
        frmmenu.setObjectName("frmmenu")
        frmmenu.setEnabled(True)
        frmmenu.resize(1145, 819)
        frmmenu.setMinimumSize(QtCore.QSize(640, 480))
        frmmenu.setSizeIncrement(QtCore.QSize(32, 32))
        self.centralwidget = QtGui.QWidget(frmmenu)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QWidget(self.centralwidget)
        self.horizontalLayout.setGeometry(QtCore.QRect(10, 5, 151, 31))
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hboxlayout = QtGui.QHBoxLayout(self.horizontalLayout)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")
        self.lstarqs = QtGui.QListWidget(self.centralwidget)
        self.lstarqs.setGeometry(QtCore.QRect(4, 40, 190, 701))
        self.lstarqs.setMaximumSize(QtCore.QSize(16777187, 16777215))
        self.lstarqs.setObjectName("lstarqs")
        self.lblProjeto = QtGui.QLabel(self.centralwidget)
        self.lblProjeto.setGeometry(QtCore.QRect(230, 10, 721, 20))
        self.lblProjeto.setMinimumSize(QtCore.QSize(700, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setWeight(75)
        font.setUnderline(True)
        font.setBold(True)
        self.lblProjeto.setFont(font)
        self.lblProjeto.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblProjeto.setObjectName("lblProjeto")
        self.lblProjeto_2 = QtGui.QLabel(self.centralwidget)
        self.lblProjeto_2.setGeometry(QtCore.QRect(170, 10, 54, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.lblProjeto_2.setFont(font)
        self.lblProjeto_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblProjeto_2.setObjectName("lblProjeto_2")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(201, 41, 851, 621))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(831, 601))
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tabWidget.setSizeIncrement(QtCore.QSize(32, 32))
        self.tabWidget.setObjectName("tabWidget")
        self.tbresultados = QtGui.QWidget()
        self.tbresultados.setObjectName("tbresultados")
        self.groupBox = QtGui.QGroupBox(self.tbresultados)
        self.groupBox.setGeometry(QtCore.QRect(150, 10, 651, 501))
        self.groupBox.setObjectName("groupBox")
        self.tbElem = QtGui.QTableWidget(self.groupBox)
        self.tbElem.setGeometry(QtCore.QRect(10, 90, 641, 400))
        self.tbElem.setMinimumSize(QtCore.QSize(641, 400))
        self.tbElem.setAutoScrollMargin(16)
        self.tbElem.setRowCount(0)
        self.tbElem.setObjectName("tbElem")
        self.tbElem.setColumnCount(5)
        self.tbElem.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tbElem.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tbElem.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tbElem.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tbElem.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tbElem.setHorizontalHeaderItem(4, item)
        self.tbElem.horizontalHeader().setMinimumSectionSize(19)
        self.label_15 = QtGui.QLabel(self.groupBox)
        self.label_15.setGeometry(QtCore.QRect(160, 0, 280, 20))
        self.label_15.setMinimumSize(QtCore.QSize(280, 20))
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.layoutWidget = QtGui.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(14, 29, 621, 58))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(80, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.cbElem = QtGui.QComboBox(self.layoutWidget)
        self.cbElem.setMinimumSize(QtCore.QSize(90, 25))
        self.cbElem.setObjectName("cbElem")
        self.cbElem.addItem("")
        self.verticalLayout_4.addWidget(self.cbElem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_11 = QtGui.QLabel(self.layoutWidget)
        self.label_11.setMinimumSize(QtCore.QSize(98, 18))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_6.addWidget(self.label_11)
        self.txtConcentra = QtGui.QLineEdit(self.layoutWidget)
        self.txtConcentra.setMinimumSize(QtCore.QSize(110, 25))
        self.txtConcentra.setObjectName("txtConcentra")
        self.verticalLayout_6.addWidget(self.txtConcentra)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_13 = QtGui.QLabel(self.layoutWidget)
        self.label_13.setMinimumSize(QtCore.QSize(40, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_7.addWidget(self.label_13)
        self.txtConcentradesv = QtGui.QLineEdit(self.layoutWidget)
        self.txtConcentradesv.setMinimumSize(QtCore.QSize(114, 25))
        self.txtConcentradesv.setObjectName("txtConcentradesv")
        self.verticalLayout_7.addWidget(self.txtConcentradesv)
        self.horizontalLayout_2.addLayout(self.verticalLayout_7)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.cmdIncElem = QtGui.QPushButton(self.layoutWidget)
        self.cmdIncElem.setMinimumSize(QtCore.QSize(80, 25))
        self.cmdIncElem.setObjectName("cmdIncElem")
        self.verticalLayout_3.addWidget(self.cmdIncElem)
        self.cmdExcElem = QtGui.QPushButton(self.layoutWidget)
        self.cmdExcElem.setMinimumSize(QtCore.QSize(80, 25))
        self.cmdExcElem.setObjectName("cmdExcElem")
        self.verticalLayout_3.addWidget(self.cmdExcElem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.layoutWidget1 = QtGui.QWidget(self.tbresultados)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 340, 151, 61))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_8 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_8.addWidget(self.label_8)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem3)
        self.txtnivel = QtGui.QLineEdit(self.layoutWidget1)
        self.txtnivel.setObjectName("txtnivel")
        self.verticalLayout_8.addWidget(self.txtnivel)
        self.layoutWidget2 = QtGui.QWidget(self.tbresultados)
        self.layoutWidget2.setGeometry(QtCore.QRect(5, 410, 141, 81))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_9 = QtGui.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.label_14 = QtGui.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_2.addWidget(self.label_14)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.txtsigma = QtGui.QLineEdit(self.layoutWidget2)
        self.txtsigma.setObjectName("txtsigma")
        self.verticalLayout_2.addWidget(self.txtsigma)
        self.layoutWidget3 = QtGui.QWidget(self.tbresultados)
        self.layoutWidget3.setGeometry(QtCore.QRect(10, 20, 131, 68))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_5 = QtGui.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_10.addWidget(self.label_5)
        self.rba = QtGui.QRadioButton(self.layoutWidget3)
        self.rba.setCheckable(True)
        self.rba.setChecked(True)
        self.rba.setObjectName("rba")
        self.verticalLayout_10.addWidget(self.rba)
        self.rbp = QtGui.QRadioButton(self.layoutWidget3)
        self.rbp.setCheckable(True)
        self.rbp.setChecked(False)
        self.rbp.setObjectName("rbp")
        self.verticalLayout_10.addWidget(self.rbp)
        self.layoutWidget4 = QtGui.QWidget(self.tbresultados)
        self.layoutWidget4.setGeometry(QtCore.QRect(11, 100, 131, 101))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_4 = QtGui.QLabel(self.layoutWidget4)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_11.addWidget(self.label_4)
        self.lblvivo = QtGui.QLabel(self.layoutWidget4)
        self.lblvivo.setMinimumSize(QtCore.QSize(100, 20))
        self.lblvivo.setFrameShape(QtGui.QFrame.NoFrame)
        self.lblvivo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblvivo.setObjectName("lblvivo")
        self.verticalLayout_11.addWidget(self.lblvivo)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem5)
        self.label_6 = QtGui.QLabel(self.layoutWidget4)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_11.addWidget(self.label_6)
        self.lblmorto = QtGui.QLabel(self.layoutWidget4)
        self.lblmorto.setMinimumSize(QtCore.QSize(100, 20))
        self.lblmorto.setFrameShape(QtGui.QFrame.NoFrame)
        self.lblmorto.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmorto.setObjectName("lblmorto")
        self.verticalLayout_11.addWidget(self.lblmorto)
        self.layoutWidget5 = QtGui.QWidget(self.tbresultados)
        self.layoutWidget5.setGeometry(QtCore.QRect(6, 210, 137, 121))
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.layoutWidget5)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_3 = QtGui.QLabel(self.layoutWidget5)
        self.label_3.setMinimumSize(QtCore.QSize(50, 25))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_9.addWidget(self.label_3)
        self.txtmassa = QtGui.QLineEdit(self.layoutWidget5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtmassa.sizePolicy().hasHeightForWidth())
        self.txtmassa.setSizePolicy(sizePolicy)
        self.txtmassa.setMinimumSize(QtCore.QSize(135, 25))
        self.txtmassa.setObjectName("txtmassa")
        self.verticalLayout_9.addWidget(self.txtmassa)
        spacerItem6 = QtGui.QSpacerItem(65, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem6)
        self.label = QtGui.QLabel(self.layoutWidget5)
        self.label.setMinimumSize(QtCore.QSize(50, 25))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_9.addWidget(self.label)
        self.txtdatah = QtGui.QDateTimeEdit(self.layoutWidget5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtdatah.sizePolicy().hasHeightForWidth())
        self.txtdatah.setSizePolicy(sizePolicy)
        self.txtdatah.setMinimumSize(QtCore.QSize(135, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.txtdatah.setFont(font)
        self.txtdatah.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 2), QtCore.QTime(0, 0, 0)))
        self.txtdatah.setObjectName("txtdatah")
        self.verticalLayout_9.addWidget(self.txtdatah)
        self.tabWidget.addTab(self.tbresultados, "")
        self.tbconcetracao = QtGui.QWidget()
        self.tbconcetracao.setObjectName("tbconcetracao")
        self.cmdImpRes = QtGui.QPushButton(self.tbconcetracao)
        self.cmdImpRes.setGeometry(QtCore.QRect(0, 0, 75, 23))
        self.cmdImpRes.setObjectName("cmdImpRes")
        self.tableWidget = QtGui.QTableWidget(self.tbconcetracao)
        self.tableWidget.setGeometry(QtCore.QRect(0, 30, 820, 471))
        self.tableWidget.setMinimumSize(QtCore.QSize(820, 471))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(12)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(11, item)
        self.tabWidget.addTab(self.tbconcetracao, "")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget_2 = QtGui.QTabWidget(self.tab)
        self.tabWidget_2.setGeometry(QtCore.QRect(10, 30, 831, 461))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gAmostra1 = QtGui.QTableWidget(self.tab_2)
        self.gAmostra1.setGeometry(QtCore.QRect(0, 10, 821, 411))
        self.gAmostra1.setMinimumSize(QtCore.QSize(821, 411))
        self.gAmostra1.setObjectName("gAmostra1")
        self.gAmostra1.setColumnCount(3)
        self.gAmostra1.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.gAmostra1.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.gAmostra1.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.gAmostra1.setHorizontalHeaderItem(2, item)
        self.tabWidget_2.addTab(self.tab_2, "")
        self.cmdImpConcentra = QtGui.QPushButton(self.tab)
        self.cmdImpConcentra.setGeometry(QtCore.QRect(0, 0, 75, 23))
        self.cmdImpConcentra.setObjectName("cmdImpConcentra")
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_12 = QtGui.QLabel(self.tab_3)
        self.label_12.setGeometry(QtCore.QRect(230, 30, 181, 20))
        self.label_12.setMinimumSize(QtCore.QSize(180, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.layoutWidget6 = QtGui.QWidget(self.tab_3)
        self.layoutWidget6.setGeometry(QtCore.QRect(10, 60, 791, 272))
        self.layoutWidget6.setObjectName("layoutWidget6")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.layoutWidget6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_16 = QtGui.QLabel(self.layoutWidget6)
        self.label_16.setMinimumSize(QtCore.QSize(170, 20))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_5.addWidget(self.label_16)
        self.txtdproj1 = QtGui.QLineEdit(self.layoutWidget6)
        self.txtdproj1.setObjectName("txtdproj1")
        self.verticalLayout_5.addWidget(self.txtdproj1)
        self.label_7 = QtGui.QLabel(self.layoutWidget6)
        self.label_7.setMinimumSize(QtCore.QSize(160, 20))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_5.addWidget(self.label_7)
        self.txtdproj2 = QtGui.QTextEdit(self.layoutWidget6)
        self.txtdproj2.setMinimumSize(QtCore.QSize(650, 70))
        self.txtdproj2.setObjectName("txtdproj2")
        self.verticalLayout_5.addWidget(self.txtdproj2)
        self.tabWidget.addTab(self.tab_3, "")
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(630, 680, 426, 31))
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.caliblstwidget = QtGui.QListWidget(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.caliblstwidget.sizePolicy().hasHeightForWidth())
        self.caliblstwidget.setSizePolicy(sizePolicy)
        self.caliblstwidget.setMinimumSize(QtCore.QSize(300, 25))
        self.caliblstwidget.setAutoScrollMargin(1)
        self.caliblstwidget.setObjectName("caliblstwidget")
        self.horizontalLayout_4.addWidget(self.caliblstwidget)
        self.cmdcalibracao = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(120)
        sizePolicy.setVerticalStretch(25)
        sizePolicy.setHeightForWidth(self.cmdcalibracao.sizePolicy().hasHeightForWidth())
        self.cmdcalibracao.setSizePolicy(sizePolicy)
        self.cmdcalibracao.setMinimumSize(QtCore.QSize(120, 25))
        self.cmdcalibracao.setMaximumSize(QtCore.QSize(100, 1677))
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        font.setWeight(75)
        font.setBold(True)
        self.cmdcalibracao.setFont(font)
        self.cmdcalibracao.setObjectName("cmdcalibracao")
        self.horizontalLayout_4.addWidget(self.cmdcalibracao)
        self.widget1 = QtGui.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(350, 683, 190, 26))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_10 = QtGui.QLabel(self.widget1)
        self.label_10.setMinimumSize(QtCore.QSize(71, 21))
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_3.addWidget(self.label_10)
        spacerItem7 = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.comboBox = QtGui.QComboBox(self.widget1)
        self.comboBox.setMinimumSize(QtCore.QSize(91, 24))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox)
        frmmenu.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(frmmenu)
        self.statusbar.setObjectName("statusbar")
        frmmenu.setStatusBar(self.statusbar)
        self.actionAbrir = QtGui.QAction(frmmenu)
        self.actionAbrir.setObjectName("actionAbrir")
        self.actionFechar = QtGui.QAction(frmmenu)
        self.actionFechar.setObjectName("actionFechar")
        self.actionSair = QtGui.QAction(frmmenu)
        self.actionSair.setObjectName("actionSair")
        self.actionNovo = QtGui.QAction(frmmenu)
        self.actionNovo.setObjectName("actionNovo")
        self.actionAbrir_2 = QtGui.QAction(frmmenu)
        self.actionAbrir_2.setObjectName("actionAbrir_2")
        self.actionSalvar = QtGui.QAction(frmmenu)
        self.actionSalvar.setObjectName("actionSalvar")
        self.actionSalvar_Como = QtGui.QAction(frmmenu)
        self.actionSalvar_Como.setObjectName("actionSalvar_Como")
        self.actionFechar_2 = QtGui.QAction(frmmenu)
        self.actionFechar_2.setObjectName("actionFechar_2")
        self.actionSobre_o_SAANI = QtGui.QAction(frmmenu)
        self.actionSobre_o_SAANI.setObjectName("actionSobre_o_SAANI")

        self.retranslateUi(frmmenu)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frmmenu)

    def retranslateUi(self, frmmenu):
        frmmenu.setWindowTitle(QtGui.QApplication.translate("frmmenu", "SAANI - Software de Análise por Ativação Neutronica Instrumental", None, QtGui.QApplication.UnicodeUTF8))
        self.lblProjeto.setText(QtGui.QApplication.translate("frmmenu", "Sem Projeto.SAN", None, QtGui.QApplication.UnicodeUTF8))
        self.lblProjeto_2.setText(QtGui.QApplication.translate("frmmenu", "Projeto: ", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setToolTip(QtGui.QApplication.translate("frmmenu", "Slope=1,Offset=1,ro=1,kres=1", None, QtGui.QApplication.UnicodeUTF8))
        self.tbElem.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("frmmenu", "Elemento", None, QtGui.QApplication.UnicodeUTF8))
        self.tbElem.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("frmmenu", "Energia", None, QtGui.QApplication.UnicodeUTF8))
        self.tbElem.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("frmmenu", "Meia Vida (minutos)", None, QtGui.QApplication.UnicodeUTF8))
        self.tbElem.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("frmmenu", "Concentracao", None, QtGui.QApplication.UnicodeUTF8))
        self.tbElem.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("frmmenu", "Desv.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("frmmenu", "Concentração dos Elementos no Padrão", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmmenu", "Elemento", None, QtGui.QApplication.UnicodeUTF8))
        self.cbElem.setItemText(0, QtGui.QApplication.translate("frmmenu", "As-76", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("frmmenu", "Concentração", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("frmmenu", "Desv.", None, QtGui.QApplication.UnicodeUTF8))
        self.txtConcentradesv.setText(QtGui.QApplication.translate("frmmenu", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdIncElem.setText(QtGui.QApplication.translate("frmmenu", "Incluir", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdExcElem.setText(QtGui.QApplication.translate("frmmenu", "Excluir", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("frmmenu", "Nível de sensibilidde", None, QtGui.QApplication.UnicodeUTF8))
        self.txtnivel.setText(QtGui.QApplication.translate("frmmenu", "15", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("frmmenu", "Desvio padrão", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("frmmenu", "( % 1,2 ou 3)", None, QtGui.QApplication.UnicodeUTF8))
        self.txtsigma.setText(QtGui.QApplication.translate("frmmenu", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("frmmenu", "Tipo Arquivo", None, QtGui.QApplication.UnicodeUTF8))
        self.rba.setText(QtGui.QApplication.translate("frmmenu", "Amostra", None, QtGui.QApplication.UnicodeUTF8))
        self.rbp.setText(QtGui.QApplication.translate("frmmenu", "Padrão", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("frmmenu", "Tempo Vivo", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("frmmenu", "Tempo Morto", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmmenu", "Massa", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmmenu", "Data", None, QtGui.QApplication.UnicodeUTF8))
        self.txtdatah.setDisplayFormat(QtGui.QApplication.translate("frmmenu", "dd/MM/yyyy HH:mm:ss", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tbresultados), QtGui.QApplication.translate("frmmenu", "Parametros do Arquivo", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdImpRes.setText(QtGui.QApplication.translate("frmmenu", "Imprimir", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("frmmenu", "Energia", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("frmmenu", "Area", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("frmmenu", "BG", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("frmmenu", "Resol", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("frmmenu", "Canal Final", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(5).setText(QtGui.QApplication.translate("frmmenu", "Canal Inicial", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(6).setText(QtGui.QApplication.translate("frmmenu", "LP", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(7).setText(QtGui.QApplication.translate("frmmenu", "Cps", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(8).setText(QtGui.QApplication.translate("frmmenu", "S%", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(9).setText(QtGui.QApplication.translate("frmmenu", "Elemento", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(10).setText(QtGui.QApplication.translate("frmmenu", "Meia Vida", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(11).setText(QtGui.QApplication.translate("frmmenu", "Massa Padrão", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tbconcetracao), QtGui.QApplication.translate("frmmenu", "Resultado dos Cálculos", None, QtGui.QApplication.UnicodeUTF8))
        self.gAmostra1.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("frmmenu", "Elementos", None, QtGui.QApplication.UnicodeUTF8))
        self.gAmostra1.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("frmmenu", "P1", None, QtGui.QApplication.UnicodeUTF8))
        self.gAmostra1.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("frmmenu", "P2", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), QtGui.QApplication.translate("frmmenu", "Amostra 1", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdImpConcentra.setText(QtGui.QApplication.translate("frmmenu", "Imprime", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("frmmenu", "Resultado das Concentrações", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("frmmenu", "Dados do Projeto", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("frmmenu", "Título do Projeto:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("frmmenu", "Descrição do Projeto:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("frmmenu", "Projeto", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdcalibracao.setText(QtGui.QApplication.translate("frmmenu", "Calibração...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("frmmenu", "Calibração", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("frmmenu", "1st Order", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("frmmenu", "2nd Order", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbrir.setText(QtGui.QApplication.translate("frmmenu", "Abrir", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbrir.setStatusTip(QtGui.QApplication.translate("frmmenu", "Abrir Arquivo de Espectro", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbrir.setShortcut(QtGui.QApplication.translate("frmmenu", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFechar.setText(QtGui.QApplication.translate("frmmenu", "Fechar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFechar.setStatusTip(QtGui.QApplication.translate("frmmenu", "Fechar Arquivo de Espectro", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFechar.setShortcut(QtGui.QApplication.translate("frmmenu", "Ctrl+W", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSair.setText(QtGui.QApplication.translate("frmmenu", "Sair", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSair.setStatusTip(QtGui.QApplication.translate("frmmenu", "Sair do SAANI", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSair.setShortcut(QtGui.QApplication.translate("frmmenu", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNovo.setText(QtGui.QApplication.translate("frmmenu", "Novo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNovo.setStatusTip(QtGui.QApplication.translate("frmmenu", "Iniciar Novo Projeto", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbrir_2.setText(QtGui.QApplication.translate("frmmenu", "Abrir", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbrir_2.setStatusTip(QtGui.QApplication.translate("frmmenu", "Abrir Projeto Existente", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSalvar.setText(QtGui.QApplication.translate("frmmenu", "Salvar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSalvar.setStatusTip(QtGui.QApplication.translate("frmmenu", "Salvar Projeto", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSalvar_Como.setText(QtGui.QApplication.translate("frmmenu", "Salvar Como", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFechar_2.setText(QtGui.QApplication.translate("frmmenu", "Fechar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFechar_2.setStatusTip(QtGui.QApplication.translate("frmmenu", "Fechar Projeto", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSobre_o_SAANI.setText(QtGui.QApplication.translate("frmmenu", "Sobre o SAANI", None, QtGui.QApplication.UnicodeUTF8))

