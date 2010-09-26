# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

import sys, string
import frmElementos
#import formtes

""" esta classe monta a janela principal do aplicativo.  """
class crtManElementos(QtGui.QWidget):
    def __init__(self, parent=None, modal=1):
         QtGui.QWidget.__init__(self, parent)
#" formulario principal gerado no QtDesigner frmmenu.ui "
# Dialog
#        Dialog = QtGui.QDialog()
#        ui = formtes.Ui_Dialog()
#        ui.setupUi(Dialog)
#        Dialog.show()
#        Dialog.exec_()
         Form = QtGui.QWidget()
         ui = frmElementos.Ui_Form()
         ui.setupUi(Form)
         Form.setWindowModality(QtCore.Qt.WindowModal)
         Form.show()
    	 self._carregaLista()
    	 Form.exec_()

    def _carregaLista(self):
	    print "carrega lista"

    def mostra(self):
        a=1

if __name__ == "__main__":
    mostra()
