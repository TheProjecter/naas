# -*- coding: ISO-8859-1 -*-
# Funções utilizadas para a criação da tabela de resultados do formulario frmresultado.
import string, random, math
from PyQt4 import QtGui, QtCore
 
##
def criarGrade(tb,l,c,cabec):
    te=tb.rowCount()
    for e in range(0,te):
        tb.removeRow(0)
    tb.setRowCount(l)
    tb.setColumnCount(c)            

def cabecGradeRes(tb):
        headerItem4 = QtGui.QTableWidgetItem()
        headerItem4.setText(QtGui.QApplication.translate("frmmenu", "Energia", None, QtGui.QApplication.UnicodeUTF8))
        tb.setHorizontalHeaderItem(0,headerItem4)

        headerItem5 = QtGui.QTableWidgetItem()
        headerItem5.setText(QtGui.QApplication.translate("frmmenu", "Area", None, QtGui.QApplication.UnicodeUTF8))
        tb.setHorizontalHeaderItem(1,headerItem5)

        headerItem6 = QtGui.QTableWidgetItem()
        headerItem6.setText(QtGui.QApplication.translate("frmmenu", "BG", None, QtGui.QApplication.UnicodeUTF8))
        tb.setHorizontalHeaderItem(2,headerItem6)

        headerItem7 = QtGui.QTableWidgetItem()
        headerItem7.setText(QtGui.QApplication.translate("frmmenu", "Resol", None, QtGui.QApplication.UnicodeUTF8))
        tb.setHorizontalHeaderItem(3,headerItem7)

        headerItem8 = QtGui.QTableWidgetItem()
        headerItem8.setText(QtGui.QApplication.translate("frmmenu", "Canal Final", None, QtGui.QApplication.UnicodeUTF8))
        tb.setHorizontalHeaderItem(4,headerItem8)

        headerItem9 = QtGui.QTableWidgetItem()
        headerItem9.setText(QtGui.QApplication.translate("frmmenu", "Canal Inicial", None, QtGui.QApplication.UnicodeUTF8))
        tb.setHorizontalHeaderItem(5,headerItem9)

        headerItem10 = QtGui.QTableWidgetItem()
        headerItem10.setText(QtGui.QApplication.translate("frmmenu", "LP", None, QtGui.QApplication.UnicodeUTF8))
        tb.setHorizontalHeaderItem(6,headerItem10)

        headerItem11 = QtGui.QTableWidgetItem()
        headerItem11.setText(QtGui.QApplication.translate("frmmenu", "Cps", None, QtGui.QApplication.UnicodeUTF8))
        tb.setHorizontalHeaderItem(7,headerItem11)

        headerItem12 = QtGui.QTableWidgetItem()
        headerItem12.setText(QtGui.QApplication.translate("frmmenu", "S%", None, QtGui.QApplication.UnicodeUTF8))
        tb.setHorizontalHeaderItem(8,headerItem12)

        headerItem13 = QtGui.QTableWidgetItem()
        headerItem13.setText(QtGui.QApplication.translate("frmmenu", "Elemento", None, QtGui.QApplication.UnicodeUTF8))
        tb.setHorizontalHeaderItem(9,headerItem13)

        headerItem14 = QtGui.QTableWidgetItem()
        headerItem14.setText(QtGui.QApplication.translate("frmmenu", "Meia Vida", None, QtGui.QApplication.UnicodeUTF8))
        tb.setHorizontalHeaderItem(10,headerItem14)

        headerItem15 = QtGui.QTableWidgetItem()
        headerItem15.setText(QtGui.QApplication.translate("frmmenu", "Massa Padrão", None, QtGui.QApplication.UnicodeUTF8))
        tb.setHorizontalHeaderItem(11,headerItem15)


def incGradeE(tb,line, pdic):
#    print "Incluir dados na grade"
#    print pdic
#    tb.setRowCount(line)
#    valor=QtCore.QTableItem(tb,QtCore.QTableItem.Never,campo)
    valor=QtGui.QTableWidgetItem("%s" % pdic['elemento'], QtGui.QTableWidgetItem.Type)
    tb.setItem(line,0,valor)
    valor=QtGui.QTableWidgetItem("%d" % pdic['meiaVida'], QtGui.QTableWidgetItem.Type)
    tb.setItem(line,1,valor)

def incGrade(tb,line, pdic):
#    print "Incluir dados na grade"
#    print pdic
#    tb.setRowCount(line)
#    valor=QtCore.QTableItem(tb,QtCore.QTableItem.Never,campo)
    valor=QtGui.QTableWidgetItem("%8.2f" % pdic['energia'], QtGui.QTableWidgetItem.Type)
    tb.setItem(line,0,valor)
    valor=QtGui.QTableWidgetItem("%d" % pdic['area'], QtGui.QTableWidgetItem.Type)
    tb.setItem(line,1,valor)
    valor=QtGui.QTableWidgetItem("%d" % pdic['bg'], QtGui.QTableWidgetItem.Type)
    tb.setItem(line,2,valor)
    valor=QtGui.QTableWidgetItem("%8.2f" % pdic['resol'], QtGui.QTableWidgetItem.Type)
    tb.setItem(line,3,valor)
    valor=QtGui.QTableWidgetItem("%8.2f" % pdic['fi'], QtGui.QTableWidgetItem.Type)
    tb.setItem(line,4,valor)
    valor=QtGui.QTableWidgetItem("%d" % pdic['id'], QtGui.QTableWidgetItem.Type)
    tb.setItem(line,5,valor)
    valor=QtGui.QTableWidgetItem("%d" % pdic['lp'], QtGui.QTableWidgetItem.Type)
    tb.setItem(line,6,valor)
    valor=QtGui.QTableWidgetItem("%8.3f" % pdic['cps'], QtGui.QTableWidgetItem.Type)
    tb.setItem(line,7,valor)
    valor=QtGui.QTableWidgetItem("%8.1f" % pdic['erreur'], QtGui.QTableWidgetItem.Type)
    tb.setItem(line,8,valor)
    valor=QtGui.QTableWidgetItem("%s" % pdic['elem'], QtGui.QTableWidgetItem.Type)
    tb.setItem(line,9,valor)
    valor=QtGui.QTableWidgetItem("%s" % pdic['meiavida'], QtGui.QTableWidgetItem.Type)
    tb.setItem(line,10,valor)
    valor=QtGui.QTableWidgetItem("%s" % pdic['massa'], QtGui.QTableWidgetItem.Type)
    tb.setItem(line,11,valor)
