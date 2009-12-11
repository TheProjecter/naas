# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmResultado.ui'
#
# Created: Tue Nov 20 15:38:07 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_frmvispect(object):
    def setupUi(self, frmvispect):
        frmvispect.setObjectName("frmvispect")
        frmvispect.resize(QtCore.QSize(QtCore.QRect(0,0,1227,565).size()).expandedTo(frmvispect.minimumSizeHint()))

        self.layoutWidget = QtGui.QWidget(frmvispect)
        self.layoutWidget.setGeometry(QtCore.QRect(10,10,1211,551))
        self.layoutWidget.setObjectName("layoutWidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.hboxlayout.addWidget(self.label_5)

        self.lblespectro = QtGui.QLabel(self.layoutWidget)
        self.lblespectro.setObjectName("lblespectro")
        self.hboxlayout.addWidget(self.lblespectro)

        self.label_7 = QtGui.QLabel(self.layoutWidget)
        self.label_7.setObjectName("label_7")
        self.hboxlayout.addWidget(self.label_7)

        self.lblvivo = QtGui.QLabel(self.layoutWidget)
        self.lblvivo.setObjectName("lblvivo")
        self.hboxlayout.addWidget(self.lblvivo)

        self.label_9 = QtGui.QLabel(self.layoutWidget)
        self.label_9.setObjectName("label_9")
        self.hboxlayout.addWidget(self.label_9)

        self.lblmorto = QtGui.QLabel(self.layoutWidget)
        self.lblmorto.setObjectName("lblmorto")
        self.hboxlayout.addWidget(self.lblmorto)

        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.hboxlayout.addWidget(self.label_3)

        self.txtdata = QtGui.QDateEdit(self.layoutWidget)
        self.txtdata.setObjectName("txtdata")
        self.hboxlayout.addWidget(self.txtdata)

        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.hboxlayout.addWidget(self.label_4)

        self.txthora = QtGui.QTimeEdit(self.layoutWidget)
        self.txthora.setObjectName("txthora")
        self.hboxlayout.addWidget(self.txthora)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.label = QtGui.QLabel(self.layoutWidget)

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setItalic(False)
        font.setUnderline(True)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.tableWidget = QtGui.QTableWidget(self.layoutWidget)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.vboxlayout.addWidget(self.tableWidget)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem)

        self.cmdgracon = QtGui.QPushButton(self.layoutWidget)
        self.cmdgracon.setObjectName("cmdgracon")
        self.hboxlayout2.addWidget(self.cmdgracon)

        self.cmdlercon = QtGui.QPushButton(self.layoutWidget)
        self.cmdlercon.setObjectName("cmdlercon")
        self.hboxlayout2.addWidget(self.cmdlercon)

        self.cmdGravar = QtGui.QPushButton(self.layoutWidget)
        self.cmdGravar.setObjectName("cmdGravar")
        self.hboxlayout2.addWidget(self.cmdGravar)

        self.cmdteste = QtGui.QPushButton(self.layoutWidget)
        self.cmdteste.setObjectName("cmdteste")
        self.hboxlayout2.addWidget(self.cmdteste)

        self.cmdconcentra = QtGui.QPushButton(self.layoutWidget)
        self.cmdconcentra.setObjectName("cmdconcentra")
        self.hboxlayout2.addWidget(self.cmdconcentra)

        self.cmdimprimir = QtGui.QPushButton(self.layoutWidget)
        self.cmdimprimir.setObjectName("cmdimprimir")
        self.hboxlayout2.addWidget(self.cmdimprimir)

        self.cmdsair = QtGui.QPushButton(self.layoutWidget)
        self.cmdsair.setObjectName("cmdsair")
        self.hboxlayout2.addWidget(self.cmdsair)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.retranslateUi(frmvispect)
        QtCore.QObject.connect(self.cmdsair,QtCore.SIGNAL("clicked()"),frmvispect.close)
        QtCore.QMetaObject.connectSlotsByName(frmvispect)

    def retranslateUi(self, frmvispect):
        frmvispect.setWindowTitle(QtGui.QApplication.translate("frmvispect", "Vispect - Resultados", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("frmvispect", "Espectro:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblespectro.setText(QtGui.QApplication.translate("frmvispect", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("frmvispect", "Tempo Vivo:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblvivo.setText(QtGui.QApplication.translate("frmvispect", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("frmvispect", "Tempo Morto:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblmorto.setText(QtGui.QApplication.translate("frmvispect", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmvispect", "Data:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("frmvispect", "Hora:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmvispect", "Resultados - Spectro", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(12)
        self.tableWidget.setRowCount(0)

        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText(QtGui.QApplication.translate("frmvispect", "Energia", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(0,headerItem)

        headerItem1 = QtGui.QTableWidgetItem()
        headerItem1.setText(QtGui.QApplication.translate("frmvispect", "Area", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(1,headerItem1)

        headerItem2 = QtGui.QTableWidgetItem()
        headerItem2.setText(QtGui.QApplication.translate("frmvispect", "BG", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(2,headerItem2)

        headerItem3 = QtGui.QTableWidgetItem()
        headerItem3.setText(QtGui.QApplication.translate("frmvispect", "Resol", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(3,headerItem3)

        headerItem4 = QtGui.QTableWidgetItem()
        headerItem4.setText(QtGui.QApplication.translate("frmvispect", "Canal Final", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(4,headerItem4)

        headerItem5 = QtGui.QTableWidgetItem()
        headerItem5.setText(QtGui.QApplication.translate("frmvispect", "Canal Inicial", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(5,headerItem5)

        headerItem6 = QtGui.QTableWidgetItem()
        headerItem6.setText(QtGui.QApplication.translate("frmvispect", "LP", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(6,headerItem6)

        headerItem7 = QtGui.QTableWidgetItem()
        headerItem7.setText(QtGui.QApplication.translate("frmvispect", "Cps", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(7,headerItem7)

        headerItem8 = QtGui.QTableWidgetItem()
        headerItem8.setText(QtGui.QApplication.translate("frmvispect", "S%", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(8,headerItem8)

        headerItem9 = QtGui.QTableWidgetItem()
        headerItem9.setText(QtGui.QApplication.translate("frmvispect", "Elemento", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(9,headerItem9)

        headerItem10 = QtGui.QTableWidgetItem()
        headerItem10.setText(QtGui.QApplication.translate("frmvispect", "Meia Vida", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(10,headerItem10)

        headerItem11 = QtGui.QTableWidgetItem()
        headerItem11.setText(QtGui.QApplication.translate("frmvispect", "Massa Padrão", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(11,headerItem11)
        self.cmdgracon.setText(QtGui.QApplication.translate("frmvispect", "Grav concentra", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdlercon.setText(QtGui.QApplication.translate("frmvispect", "Ler Concetra", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdGravar.setText(QtGui.QApplication.translate("frmvispect", "Gravar X na energia", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdteste.setText(QtGui.QApplication.translate("frmvispect", "tttt", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdconcentra.setText(QtGui.QApplication.translate("frmvispect", "Concentração", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdimprimir.setText(QtGui.QApplication.translate("frmvispect", "Imprimir", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdsair.setText(QtGui.QApplication.translate("frmvispect", "Sair", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmvispect = QtGui.QWidget()
    ui = Ui_frmvispect()
    ui.setupUi(frmvispect)
    frmvispect.show()
    sys.exit(app.exec_())
