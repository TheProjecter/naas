# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmResConcentra.ui'
#
# Created: Tue Nov 13 08:34:05 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_fResConcentra(object):
    def setupUi(self, fResConcentra):
        fResConcentra.setObjectName("fResConcentra")
        fResConcentra.resize(QtCore.QSize(QtCore.QRect(0,0,767,543).size()).expandedTo(fResConcentra.minimumSizeHint()))

        self.tableWidget = QtGui.QTableWidget(fResConcentra)
        self.tableWidget.setGeometry(QtCore.QRect(0,0,1119,480))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")

        self.pushButton = QtGui.QPushButton(fResConcentra)
        self.pushButton.setGeometry(QtCore.QRect(420,500,75,23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(fResConcentra)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),fResConcentra.close)
        QtCore.QMetaObject.connectSlotsByName(fResConcentra)

    def retranslateUi(self, fResConcentra):
        fResConcentra.setWindowTitle(QtGui.QApplication.translate("fResConcentra", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)

        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText(QtGui.QApplication.translate("fResConcentra", "Energia", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(0,headerItem)

        headerItem1 = QtGui.QTableWidgetItem()
        headerItem1.setText(QtGui.QApplication.translate("fResConcentra", "Area", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(1,headerItem1)

        headerItem2 = QtGui.QTableWidgetItem()
        headerItem2.setText(QtGui.QApplication.translate("fResConcentra", "BG", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(2,headerItem2)

        headerItem3 = QtGui.QTableWidgetItem()
        headerItem3.setText(QtGui.QApplication.translate("fResConcentra", "Resol", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(3,headerItem3)

        headerItem4 = QtGui.QTableWidgetItem()
        headerItem4.setText(QtGui.QApplication.translate("fResConcentra", "Canal Final", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(4,headerItem4)

        headerItem5 = QtGui.QTableWidgetItem()
        headerItem5.setText(QtGui.QApplication.translate("fResConcentra", "Canal Inicial", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(5,headerItem5)

        headerItem6 = QtGui.QTableWidgetItem()
        headerItem6.setText(QtGui.QApplication.translate("fResConcentra", "Calculo", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(6,headerItem6)
        self.pushButton.setText(QtGui.QApplication.translate("fResConcentra", "Retornar", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    fResConcentra = QtGui.QWidget()
    ui = Ui_fResConcentra()
    ui.setupUi(fResConcentra)
    fResConcentra.show()
    sys.exit(app.exec_())
