# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmGraficoRes.ui'
#
# Created: Tue Dec  8 15:24:07 2009
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(622, 580)
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(22, 31, 586, 502))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.qwtPlot = QwtPlot(self.widget)
        self.qwtPlot.setMinimumSize(QtCore.QSize(0, 250))
        self.qwtPlot.setObjectName("qwtPlot")
        self.verticalLayout.addWidget(self.qwtPlot)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.tableView = QtGui.QTableView(self.widget)
        self.tableView.setMinimumSize(QtCore.QSize(550, 200))
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setCascadingSectionResizes(True)
        self.tableView.horizontalHeader().setShowSortIndicator(True)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.tableView)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))

from qwt_plot import QwtPlot
