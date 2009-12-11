# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmmenu.ui'
#
# Created: Mon Nov 24 16:26:28 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmmenu(object):
    def setupUi(self, frmmenu):
        frmmenu.setObjectName("frmmenu")
        frmmenu.resize(QtCore.QSize(QtCore.QRect(0,0,751,510).size()).expandedTo(frmmenu.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(frmmenu)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtGui.QWidget(self.centralwidget)
        self.verticalLayout.setGeometry(QtCore.QRect(170,40,561,441))
        self.verticalLayout.setObjectName("verticalLayout")

        self.vboxlayout = QtGui.QVBoxLayout(self.verticalLayout)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(self.verticalLayout)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")

        self.tbresultados = QtGui.QWidget()
        self.tbresultados.setObjectName("tbresultados")

        self.label_6 = QtGui.QLabel(self.tbresultados)
        self.label_6.setGeometry(QtCore.QRect(0,130,121,20))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        self.label_3 = QtGui.QLabel(self.tbresultados)
        self.label_3.setGeometry(QtCore.QRect(0,170,121,16))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.label = QtGui.QLabel(self.tbresultados)
        self.label.setGeometry(QtCore.QRect(0,220,121,16))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.label_4 = QtGui.QLabel(self.tbresultados)
        self.label_4.setGeometry(QtCore.QRect(0,90,121,16))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtGui.QLabel(self.tbresultados)
        self.label_5.setGeometry(QtCore.QRect(0,20,121,16))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")

        self.label_9 = QtGui.QLabel(self.tbresultados)
        self.label_9.setGeometry(QtCore.QRect(0,320,121,16))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")

        self.lblmorto = QtGui.QLabel(self.tbresultados)
        self.lblmorto.setGeometry(QtCore.QRect(0,150,121,16))
        self.lblmorto.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmorto.setObjectName("lblmorto")

        self.lblvivo = QtGui.QLabel(self.tbresultados)
        self.lblvivo.setGeometry(QtCore.QRect(0,110,121,16))
        self.lblvivo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblvivo.setObjectName("lblvivo")

        self.txtmassa = QtGui.QLineEdit(self.tbresultados)
        self.txtmassa.setGeometry(QtCore.QRect(0,190,121,20))
        self.txtmassa.setObjectName("txtmassa")

        self.txtdatah = QtGui.QDateTimeEdit(self.tbresultados)
        self.txtdatah.setGeometry(QtCore.QRect(0,240,130,22))
        self.txtdatah.setDateTime(QtCore.QDateTime(QtCore.QDate(2000,1,2),QtCore.QTime(0,0,0)))
        self.txtdatah.setObjectName("txtdatah")

        self.txtnivel = QtGui.QLineEdit(self.tbresultados)
        self.txtnivel.setGeometry(QtCore.QRect(40,290,48,20))
        self.txtnivel.setObjectName("txtnivel")

        self.txtsigma = QtGui.QLineEdit(self.tbresultados)
        self.txtsigma.setGeometry(QtCore.QRect(40,360,31,20))
        self.txtsigma.setObjectName("txtsigma")

        self.label_8 = QtGui.QLabel(self.tbresultados)
        self.label_8.setGeometry(QtCore.QRect(0,270,121,20))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")

        self.rbp = QtGui.QRadioButton(self.tbresultados)
        self.rbp.setGeometry(QtCore.QRect(30,60,83,18))
        self.rbp.setCheckable(True)
        self.rbp.setChecked(False)
        self.rbp.setObjectName("rbp")

        self.rba = QtGui.QRadioButton(self.tbresultados)
        self.rba.setGeometry(QtCore.QRect(30,40,83,18))
        self.rba.setCheckable(True)
        self.rba.setChecked(True)
        self.rba.setObjectName("rba")

        self.groupBox = QtGui.QGroupBox(self.tbresultados)
        self.groupBox.setGeometry(QtCore.QRect(130,10,421,391))
        self.groupBox.setObjectName("groupBox")

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(70,10,53,16))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.cbElem = QtGui.QComboBox(self.groupBox)
        self.cbElem.setGeometry(QtCore.QRect(0,30,181,22))
        self.cbElem.setObjectName("cbElem")

        self.label_11 = QtGui.QLabel(self.groupBox)
        self.label_11.setGeometry(QtCore.QRect(190,10,78,16))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")

        self.txtConcentra = QtGui.QLineEdit(self.groupBox)
        self.txtConcentra.setGeometry(QtCore.QRect(200,30,61,20))
        self.txtConcentra.setObjectName("txtConcentra")

        self.cmdIncElem = QtGui.QPushButton(self.groupBox)
        self.cmdIncElem.setGeometry(QtCore.QRect(340,10,75,23))
        self.cmdIncElem.setObjectName("cmdIncElem")

        self.cmdExcElem = QtGui.QPushButton(self.groupBox)
        self.cmdExcElem.setGeometry(QtCore.QRect(340,30,75,23))
        self.cmdExcElem.setObjectName("cmdExcElem")

        self.tbElem = QtGui.QTableWidget(self.groupBox)
        self.tbElem.setGeometry(QtCore.QRect(4,60,411,311))
        self.tbElem.setObjectName("tbElem")

        self.label_13 = QtGui.QLabel(self.groupBox)
        self.label_13.setGeometry(QtCore.QRect(280,10,31,16))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")

        self.txtConcentradesv = QtGui.QLineEdit(self.groupBox)
        self.txtConcentradesv.setGeometry(QtCore.QRect(280,30,48,20))
        self.txtConcentradesv.setObjectName("txtConcentradesv")

        self.label_14 = QtGui.QLabel(self.tbresultados)
        self.label_14.setGeometry(QtCore.QRect(0,340,121,16))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.tabWidget.addTab(self.tbresultados,"")

        self.tbconcetracao = QtGui.QWidget()
        self.tbconcetracao.setObjectName("tbconcetracao")

        self.cmdImpRes = QtGui.QPushButton(self.tbconcetracao)
        self.cmdImpRes.setGeometry(QtCore.QRect(0,0,75,23))
        self.cmdImpRes.setObjectName("cmdImpRes")

        self.tableWidget = QtGui.QTableWidget(self.tbconcetracao)
        self.tableWidget.setGeometry(QtCore.QRect(0,30,541,371))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tabWidget.addTab(self.tbconcetracao,"")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.tabWidget_2 = QtGui.QTabWidget(self.tab)
        self.tabWidget_2.setGeometry(QtCore.QRect(10,30,531,381))
        self.tabWidget_2.setObjectName("tabWidget_2")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gAmostra1 = QtGui.QTableWidget(self.tab_2)
        self.gAmostra1.setGeometry(QtCore.QRect(0,10,521,341))
        self.gAmostra1.setObjectName("gAmostra1")
        self.tabWidget_2.addTab(self.tab_2,"")

        self.cmdImpConcentra = QtGui.QPushButton(self.tab)
        self.cmdImpConcentra.setGeometry(QtCore.QRect(0,0,75,23))
        self.cmdImpConcentra.setObjectName("cmdImpConcentra")
        self.tabWidget.addTab(self.tab,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.cmdcalibracao = QtGui.QPushButton(self.tab_3)
        self.cmdcalibracao.setGeometry(QtCore.QRect(170,147,101,23))
        self.cmdcalibracao.setObjectName("cmdcalibracao")

        self.lblcalibracao = QtGui.QLabel(self.tab_3)
        self.lblcalibracao.setGeometry(QtCore.QRect(10,180,531,20))

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.lblcalibracao.setFont(font)
        self.lblcalibracao.setAlignment(QtCore.Qt.AlignCenter)
        self.lblcalibracao.setObjectName("lblcalibracao")

        self.txtdproj1 = QtGui.QLineEdit(self.tab_3)
        self.txtdproj1.setGeometry(QtCore.QRect(10,70,531,20))
        self.txtdproj1.setObjectName("txtdproj1")

        self.label_7 = QtGui.QLabel(self.tab_3)
        self.label_7.setGeometry(QtCore.QRect(10,50,120,16))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        self.txtdproj2 = QtGui.QLineEdit(self.tab_3)
        self.txtdproj2.setGeometry(QtCore.QRect(10,100,531,20))
        self.txtdproj2.setObjectName("txtdproj2")

        self.label_12 = QtGui.QLabel(self.tab_3)
        self.label_12.setGeometry(QtCore.QRect(230,30,141,20))

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")

        self.label_10 = QtGui.QLabel(self.tab_3)
        self.label_10.setGeometry(QtCore.QRect(10,150,154,16))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.tabWidget.addTab(self.tab_3,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.horizontalLayout = QtGui.QWidget(self.centralwidget)
        self.horizontalLayout.setGeometry(QtCore.QRect(10,5,151,31))
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.hboxlayout = QtGui.QHBoxLayout(self.horizontalLayout)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")

        self.lstarqs = QtGui.QListWidget(self.centralwidget)
        self.lstarqs.setGeometry(QtCore.QRect(10,40,151,441))
        self.lstarqs.setMaximumSize(QtCore.QSize(16777187,16777215))
        self.lstarqs.setObjectName("lstarqs")

        self.lblProjeto = QtGui.QLabel(self.centralwidget)
        self.lblProjeto.setGeometry(QtCore.QRect(230,10,721,20))

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
        self.lblProjeto_2.setGeometry(QtCore.QRect(170,10,54,20))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.lblProjeto_2.setFont(font)
        self.lblProjeto_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblProjeto_2.setObjectName("lblProjeto_2")
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
        self.label_6.setText(QtGui.QApplication.translate("frmmenu", "Tempo Morto", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmmenu", "Massa", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmmenu", "Data", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("frmmenu", "Tempo Vivo", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("frmmenu", "Tipo Arquivo", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("frmmenu", "Desvio padrão", None, QtGui.QApplication.UnicodeUTF8))
        self.txtdatah.setDisplayFormat(QtGui.QApplication.translate("frmmenu", "dd/MM/yyyy HH:mm:ss", None, QtGui.QApplication.UnicodeUTF8))
        self.txtnivel.setText(QtGui.QApplication.translate("frmmenu", "15", None, QtGui.QApplication.UnicodeUTF8))
        self.txtsigma.setText(QtGui.QApplication.translate("frmmenu", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("frmmenu", "Nível de sensibilidde", None, QtGui.QApplication.UnicodeUTF8))
        self.rbp.setText(QtGui.QApplication.translate("frmmenu", "Padrão", None, QtGui.QApplication.UnicodeUTF8))
        self.rba.setText(QtGui.QApplication.translate("frmmenu", "Amostra", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("frmmenu", "Concentração dos Elementos no Padrão", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmmenu", "Elemento", None, QtGui.QApplication.UnicodeUTF8))
        self.cbElem.addItem(QtGui.QApplication.translate("frmmenu", "As-76", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("frmmenu", "Concentração", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdIncElem.setText(QtGui.QApplication.translate("frmmenu", "Incluir", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdExcElem.setText(QtGui.QApplication.translate("frmmenu", "Excluir", None, QtGui.QApplication.UnicodeUTF8))
        self.tbElem.setRowCount(0)
        self.tbElem.clear()
        self.tbElem.setColumnCount(5)
        self.tbElem.setRowCount(0)

        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText(QtGui.QApplication.translate("frmmenu", "Elemento", None, QtGui.QApplication.UnicodeUTF8))
        self.tbElem.setHorizontalHeaderItem(0,headerItem)

        headerItem1 = QtGui.QTableWidgetItem()
        headerItem1.setText(QtGui.QApplication.translate("frmmenu", "Energia", None, QtGui.QApplication.UnicodeUTF8))
        self.tbElem.setHorizontalHeaderItem(1,headerItem1)

        headerItem2 = QtGui.QTableWidgetItem()
        headerItem2.setText(QtGui.QApplication.translate("frmmenu", "Meia Vida (minutos)", None, QtGui.QApplication.UnicodeUTF8))
        self.tbElem.setHorizontalHeaderItem(2,headerItem2)

        headerItem3 = QtGui.QTableWidgetItem()
        headerItem3.setText(QtGui.QApplication.translate("frmmenu", "Concentracao", None, QtGui.QApplication.UnicodeUTF8))
        self.tbElem.setHorizontalHeaderItem(3,headerItem3)

        headerItem4 = QtGui.QTableWidgetItem()
        headerItem4.setText(QtGui.QApplication.translate("frmmenu", "Desv.", None, QtGui.QApplication.UnicodeUTF8))
        self.tbElem.setHorizontalHeaderItem(4,headerItem4)
        self.label_13.setText(QtGui.QApplication.translate("frmmenu", "Desv.", None, QtGui.QApplication.UnicodeUTF8))
        self.txtConcentradesv.setText(QtGui.QApplication.translate("frmmenu", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("frmmenu", "( % 1,2 ou 3)", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tbresultados), QtGui.QApplication.translate("frmmenu", "Parametros do Arquivo", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdImpRes.setText(QtGui.QApplication.translate("frmmenu", "Imprimir", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(12)
        self.tableWidget.setRowCount(0)

        headerItem5 = QtGui.QTableWidgetItem()
        headerItem5.setText(QtGui.QApplication.translate("frmmenu", "Energia", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(0,headerItem5)

        headerItem6 = QtGui.QTableWidgetItem()
        headerItem6.setText(QtGui.QApplication.translate("frmmenu", "Area", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(1,headerItem6)

        headerItem7 = QtGui.QTableWidgetItem()
        headerItem7.setText(QtGui.QApplication.translate("frmmenu", "BG", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(2,headerItem7)

        headerItem8 = QtGui.QTableWidgetItem()
        headerItem8.setText(QtGui.QApplication.translate("frmmenu", "Resol", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(3,headerItem8)

        headerItem9 = QtGui.QTableWidgetItem()
        headerItem9.setText(QtGui.QApplication.translate("frmmenu", "Canal Final", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(4,headerItem9)

        headerItem10 = QtGui.QTableWidgetItem()
        headerItem10.setText(QtGui.QApplication.translate("frmmenu", "Canal Inicial", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(5,headerItem10)

        headerItem11 = QtGui.QTableWidgetItem()
        headerItem11.setText(QtGui.QApplication.translate("frmmenu", "LP", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(6,headerItem11)

        headerItem12 = QtGui.QTableWidgetItem()
        headerItem12.setText(QtGui.QApplication.translate("frmmenu", "Cps", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(7,headerItem12)

        headerItem13 = QtGui.QTableWidgetItem()
        headerItem13.setText(QtGui.QApplication.translate("frmmenu", "S%", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(8,headerItem13)

        headerItem14 = QtGui.QTableWidgetItem()
        headerItem14.setText(QtGui.QApplication.translate("frmmenu", "Elemento", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(9,headerItem14)

        headerItem15 = QtGui.QTableWidgetItem()
        headerItem15.setText(QtGui.QApplication.translate("frmmenu", "Meia Vida", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(10,headerItem15)

        headerItem16 = QtGui.QTableWidgetItem()
        headerItem16.setText(QtGui.QApplication.translate("frmmenu", "Massa Padrão", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(11,headerItem16)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tbconcetracao), QtGui.QApplication.translate("frmmenu", "Resultado dos Cálculos", None, QtGui.QApplication.UnicodeUTF8))
        self.gAmostra1.clear()
        self.gAmostra1.setColumnCount(3)
        self.gAmostra1.setRowCount(0)

        headerItem17 = QtGui.QTableWidgetItem()
        headerItem17.setText(QtGui.QApplication.translate("frmmenu", "Elementos", None, QtGui.QApplication.UnicodeUTF8))
        self.gAmostra1.setHorizontalHeaderItem(0,headerItem17)

        headerItem18 = QtGui.QTableWidgetItem()
        headerItem18.setText(QtGui.QApplication.translate("frmmenu", "P1", None, QtGui.QApplication.UnicodeUTF8))
        self.gAmostra1.setHorizontalHeaderItem(1,headerItem18)

        headerItem19 = QtGui.QTableWidgetItem()
        headerItem19.setText(QtGui.QApplication.translate("frmmenu", "P2", None, QtGui.QApplication.UnicodeUTF8))
        self.gAmostra1.setHorizontalHeaderItem(2,headerItem19)
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), QtGui.QApplication.translate("frmmenu", "Amostra 1", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdImpConcentra.setText(QtGui.QApplication.translate("frmmenu", "Imprime", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("frmmenu", "Resultado das Concentrações", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdcalibracao.setText(QtGui.QApplication.translate("frmmenu", "Abrir calibração", None, QtGui.QApplication.UnicodeUTF8))
        self.lblcalibracao.setText(QtGui.QApplication.translate("frmmenu", "Sem calibração", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("frmmenu", "Descrição do Projeto:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("frmmenu", "Dados do Projeto", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("frmmenu", "Clique para abrir calibração", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("frmmenu", "Projeto", None, QtGui.QApplication.UnicodeUTF8))
        self.lblProjeto.setText(QtGui.QApplication.translate("frmmenu", "Sem Projeto.SAN", None, QtGui.QApplication.UnicodeUTF8))
        self.lblProjeto_2.setText(QtGui.QApplication.translate("frmmenu", "Projeto: ", None, QtGui.QApplication.UnicodeUTF8))
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



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmmenu = QtGui.QMainWindow()
    ui = Ui_frmmenu()
    ui.setupUi(frmmenu)
    frmmenu.show()
    sys.exit(app.exec_())
