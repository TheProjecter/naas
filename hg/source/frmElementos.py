# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmElementos.ui'
#
# Created: Tue Nov 25 09:44:39 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,453,321).size()).expandedTo(Form.minimumSizeHint()))

        self.tableWidget = QtGui.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(20,110,411,191))
        self.tableWidget.setObjectName("tableWidget")

        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(370,10,75,23))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(370,40,75,23))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(370,70,75,23))
        self.pushButton_3.setObjectName("pushButton_3")

        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(90,20,81,20))
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtGui.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(90,50,81,20))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.lineEdit_3 = QtGui.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(260,20,81,20))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.lineEdit_4 = QtGui.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(260,50,81,20))
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20,20,46,14))
        self.label.setObjectName("label")

        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(190,20,46,14))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(20,50,46,14))
        self.label_3.setObjectName("label_3")

        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(190,60,46,14))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton_3,QtCore.SIGNAL("clicked()"),Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.pushButton.setText(QtGui.QApplication.translate("Form", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Form", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("Form", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
