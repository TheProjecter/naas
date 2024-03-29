# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

import sys, string

sys.path.append("source")

from frmmenu import Ui_frmmenu


from os.path import isfile
from os import chdir

import QtBlissGraph
qt = QtBlissGraph.qt
qwt = QtBlissGraph.qwt
import crtLerEspectro
import os
import crtCalculos
#import Numeric
import numpy as np
import math
from Icons import IconDict
import crtFuncoes
import time
import datetime
import DataObject
import Elementos
import crtManElementos
#import frmElementos
import string
# para imprimir o grafico
import PyMcaPrintPreview


import threading
import platform

__version__ = "0.0.2_20100105"



""" esta classe monta a janela principal do aplicativo.  """
class startGui(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
#" formulario principal gerado no QtDesigner frmmenu.ui "
        self.ui = Ui_frmmenu()
        self.ui.setupUi(self)



        self.saiuAba=0
        self.configDir  = ''
        self.graph=None
        self.printer=None
        self.painter=None
        self.printPreview = PyMcaPrintPreview.PyMcaPrintPreview(modal = 0)


        curdir = os.getcwd()
        self.Elementos=Elementos.Elementos(curdir+'/db/elementos')
#" cria objeto para os calculos das areas dos picos e energias  "
        self.vispectfit = crtCalculos.VispectFit()
        self.dataObjectsDict={}
        self.resConcentracao={}
        self.pAmostra={}
        self.pPadrao={}
        self.pElem={}
        self.amo={}
#        self.projeto=''
        self.setWindowTitle(u"SAANI - Versão: %s " % __version__)
        self.carregaGrafico()
        self._carregaElemnetos()
#" conectando botoes com suas respectivas rotinas "
        QtCore.QObject.connect(self.ui.cmdIncElem, QtCore.SIGNAL("clicked()"), self.incElemento)
        QtCore.QObject.connect(self.ui.cmdExcElem, QtCore.SIGNAL("clicked()"), self.excElemento)
        QtCore.QObject.connect(self.ui.cmdImpRes, QtCore.SIGNAL("clicked()"), self.imprimeResultados)
        QtCore.QObject.connect(self.ui.cmdImpConcentra, QtCore.SIGNAL("clicked()"), self.imprimeConcentracao)
        #QtCore.QObject.connect(self.ui.lstarqs, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.clicklst)
        QtCore.QObject.connect(self.ui.lstarqs, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.clicklst)
        QtCore.QObject.connect(self.ui.rba,QtCore.SIGNAL("toggled(bool)"),self.ver_abas_padrao)
        QtCore.QObject.connect(self.ui.calcularButton, QtCore.SIGNAL("clicked()"), self.calcAreas)
        QtCore.QObject.connect(self.ui.tabPropert,QtCore.SIGNAL("currentChanged(int)"),self.verificaAbas)
        QtCore.QObject.connect(self.cmdimpgraf, QtCore.SIGNAL("clicked()"), self.imprimeGrafico)
        #QtCore.QObject.connect(self.cmdFindAreaPeak, QtCore.SIGNAL("clicked()"), self.achapico)

#" cria atalhos para os menus e suas rotinas "
        qt.QIconSet = qt.QIcon
        self.printIcon    = qt.QIconSet(qt.QPixmap(IconDict["fileprint"]))
        self.saveIcon    = qt.QIconSet(qt.QPixmap(IconDict["filesave"]))
        self.openIcon    = qt.QIconSet(qt.QPixmap(IconDict["fileopen"]))
        self.closeIcon    = qt.QIconSet(qt.QPixmap(IconDict["close"]))
        self.saiuAba=4
        self.vlegend=''
        tb = self._addToolButton(self.openIcon,self.vispectLer,'Abrir Espectro')
        tb = self._addToolButton(self.closeIcon,self.fecharEsp,'Fechar Espectro')
        tb = self._addToolButton(QtGui.QIcon('icons/exit.png'),self.sair,'Sair')
#" criando menus Arquivos, Projeto e conectando com suas respectivas rotinas, "
        exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Sair', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Termina o SAANI')
        self.connect(exit, QtCore.SIGNAL('triggered()'), self.sair)
        abrirEsp = QtGui.QAction(self.openIcon, 'Abrir Espectro', self)
        abrirEsp.setShortcut('Ctrl+O')
        abrirEsp.setStatusTip('Abre Espectros')
        self.connect(abrirEsp, QtCore.SIGNAL('triggered()'), self.vispectLer)
        fecharEsp = QtGui.QAction(self.closeIcon, 'Fechar Espectro', self)
        fecharEsp.setShortcut('Ctrl+W')
        fecharEsp.setStatusTip('Fechar/Remover Espectros')
        self.connect(fecharEsp, QtCore.SIGNAL('triggered()'), self.fecharEsp)
        sobreSAANI = self.createAction("&Sobre",self.helpAbout,None,"sobre","Sobre o SAANI")

        lerCalib = self.createAction(u"&Ler Calibração",self.lerCalibracao,None,None,u"Ler Calibração de um Arquivo")
        calcCalib = self.createAction(u"&Calcular Calibração",self.calcularCalib,None,None,u"Calcular Calibração a partir do Espectro")
        entCalib = self.createAction(u"&Entrar Calibração",self.entrarCalib,None,None,u"Digitar parâmetros da Calibração")

# barra de menus
        menubar = self.menuBar()
        mnuArquivo = menubar.addMenu('&Arquivo')
        mnuArquivo.addAction(abrirEsp)
        mnuArquivo.addAction(fecharEsp)
#        mnuArquivo.addAction(manuElem)
        mnuArquivo.addAction(exit)
        mnuCalibrate = menubar.addMenu(u'&Calibração')
        mnuCalibrate.addAction(lerCalib)
        mnuCalibrate.addAction(calcCalib)
        mnuCalibrate.addAction(entCalib)
        mnuAnalise = menubar.addMenu(u'&Análises')

        mnuSobre = menubar.addMenu('&Help')
        mnuSobre.addAction(sobreSAANI)

#createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()")

        # recupera variavel de ambiente recentefiles
        self.settings = QtCore.QSettings()
        self.recenteFiles=[]
        recenteFiles = self.settings.value("RecenteFiles").toList()
#        mnuArquivo.addSeparator()
#        for arq in recenteFiles[:]:
#            self.recenteFiles+=[arq.toString()]
#            aq1 = self.createAction(arq.toString(),abrirEsp,False,"open","aq1 recente",None,"triggered()")
#            self.ultimo=aq1
#            mnuArquivo.addAction(aq1)


        self.dirty = False
        self.createStatusBar()
        # create progress bar
        self.pb = QtGui.QProgressBar(self.statusBar())
        self.statusBar().addPermanentWidget(self.pb)
        # lista de threads
        self.threads = []
        self.dictThreadsCalc = dict()


        ## barra de statusBar
        #self.sizeLabel = QtGui.QLabel()
        #self.sizeLabel.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        #status = self.statusBar()
        #status.setSizeGripEnabled(False)
        #status.addPermanentWidget(self.sizeLabel)
        #status.showMessage("Ready", 5000)


    def createAction(self, text, slot=None, shortcut=None, icon=None,
                 tip=None, checkable=False, signal="triggered()"):
        """ classe startGui - __init__
            cria acoes para o menu da janela principal"""
        action = QtGui.QAction(text, self)
        if icon is not None:
           action.setIcon(QtGui.QIcon("icons/%s.png" % icon))
        if shortcut is not None:
           action.setShortcut(shortcut)
        if tip is not None:
           action.setToolTip(tip)
           action.setStatusTip(tip)
        if slot is not None:
           self.connect(action, QtCore.SIGNAL(signal), slot)
        if checkable:
           action.setCheckable(True)
        return action

    def calcularCalib(self):
        pass

    def entrarCalib(self):
        pass

    def abreRecente(self):
        """ Executa sempre que fechar a janela
            pergunta se deseja salvar o projeto, neste momento salvar variaveis de ambiente
            self.dirty=True - variavel para abrir opção de salvamento....     """
        action = self.sender()
        self.abrirProj(0,action.text())

    def addRecenteFiles(self, parq):
        v=0
        for a in self.recenteFiles[:]:
          if a == parq:
             v=1
        if v==0:
           if len(self.recenteFiles) > 3:
             self.updateRecenteFiles(parq)
           else:
             self.recenteFiles+=[parq]


    def closeEvent(self, event):
        """ Executa sempre que fechar a janela
         pergunta se deseja salvar o projeto, neste momento salvar variaveis de ambiente
         self.dirty=True - variavel para abrir opção de salvamento....     """
#        self.dirty=True
        self.okToContinue()
        filenames = QtCore.QVariant(self.recenteFiles)
        self.settings.setValue("RecenteFiles", filenames)

    def updateStatus(self, message,timeout=0):
        self.statusBar().showMessage(message, timeout)


        ## connections
#        self.connect(self.sw, SIGNAL("okClicked"),
#                    self.rw.create)
#        self.connect(self.rw.table, SIGNAL("progressChanged"),
#                     self.update_progress)
#        self.connect(self.rw.table, SIGNAL("displayFinished"),
#                     self.hide_progress_bar)



    def update_progress(self, n, nrows):
        self.pb.show()
        self.pb.setRange(0, nrows)
        self.pb.setValue(n)
        self.statusBar().showMessage(self.tr("Trabalhando..."))

    def hide_progress_bar(self):
        self.pb.hide()
        self.statusBar().showMessage(self.tr("Finalizado..."))

    def createStatusBar(self):
            sb = QtGui.QStatusBar()
            sb.setFixedHeight(18)
            self.setStatusBar(sb)
            self.statusBar().showMessage(self.tr("SAANI pronto!"))
##
    def helpAbout(self):
        QtGui.QMessageBox.about(self, "Sobre o SAANI",
                """<b>Software de An&aacute;lise por Ativa&ccedil;&otilde;o com Neutrons Instrumental</b> v %s
                <p>Copyright &copy; 2008-2010 Grupo de Computa&ccedil;&atilde;o Cient&iacute;fica do IPEN.
                <p>Todos os direitos reservados.
                <p>Autores: S&iacute;lvio Rog&eacute;rio de L&uacute;cia e M&aacute;rio O. de Menezes

                <p>Python %s - Qt %s - PyQt %s on %s""" % (
                __version__, platform.python_version(),
                QtCore.QT_VERSION_STR, qt.PYQT_VERSION_STR, platform.system()))


    def okToContinue(self):
        if self.dirty:
            reply = QtGui.QMessageBox.question(self,
                            u"SAANI - Mudanças não salvas",
                            u"Salvar mudanças não salvas?",
                            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|
                            QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return False
            elif reply == QtGui.QMessageBox.Yes:
                self.salvarPro()
        return True


    def loadElementos(self):
        """ carrega elementos que já estão digitados no arquivo: elementos"""
        curdir = os.getcwd()
        self.Elementos=Elementos.Elementos(curdir+'/db/elementos')

    def verificaAbas(self):
        """ Objeto: tabWidget - quadro de abas
         executa rotina para verificar a movimentação das abas da janela principal """
        currentTab = self.ui.tabWidget.currentIndex()
        #print "Aba atual: ", currentTab
        self.ver_abas()

    def imprimeGrafico(self):
        """Botao: cmdImpGraf - Imprime grafico
           imprimir grafico que esta sendo exibido no video """
#        self.graph.printps()
        self.printGraph()

#    def fecharApp(self):
#        "serve para remover um espectro do projeto"
#        self.fecharProjeto()

    def fecharEsp(self):
        """Menu: Arquivo - Fechar Espectro
           serve para remover um espectro da lista de arquivos do projeto """
        n=self.ui.lstarqs.count()
        if n==0:
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Critical)
            msg.setText("Nenhum espectro a ser removido!")
            msg.exec_()
            return
        legend="%s" %(self.ui.lstarqs.item(self.ui.lstarqs.currentRow()).text())
        self.ui.lstarqs.takeItem(self.ui.lstarqs.currentRow())
        try:
            del(self.dataObjectsDict[legend])
        except KeyError:
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Critical)
            msg.setText(u"Erro ao remover espectro!")
            msg.exec_()
            return
        self.vlegend=legend
#        self.dirty = True
#        self.setWindowModified(self.dirty)

    def updateRecenteFiles(self,parqcaminho):
        self.recenteFiles[2]=self.recenteFiles[1]
        self.recenteFiles[1]=self.recenteFiles[0]
        self.recenteFiles[0]=parqcaminho



    def _carregaElemnetos(self):
        """ classe startGui - __init__
            cria lista dos elementos, que serao exibidos para selecao no lancamento dos padroes
            executa uma unica vez para carregar os elementos e suas energias """
        see=[]
        for i in range(len(self.Elementos.elem)):
            see.append(self.Elementos.elem[i][1]+"("+str(self.Elementos.elem[i][0])+")")
        see.sort()
        self.ui.cbElem.clear()
        for i in range(len(self.Elementos.elem)):
            self.ui.cbElem.addItem(QtGui.QApplication.translate("frmmenu", see[i], None, QtGui.QApplication.UnicodeUTF8))

    def _addToolButton(self, icon, action, tip, toggle=None):
        """ classe startGui - __init__
            cria acoes para os botoes de atalho da janela principal"""
        toolbar = self.toolbar
        tb      = qt.QToolButton(toolbar)
        tb.setIcon(icon)
        tb.setToolTip(tip)
        if toggle is not None:
           if toggle:
              tb.setCheckable(1)
        self.ui.hboxlayout.addWidget(tb)
        self.connect(tb,qt.SIGNAL('clicked()'), action)
        return tb

    def incElemento(self):
        """ Botao: cmdIncElem - aba parametros
            Inclui os elementos que constam no padrao, para efetuar o calculo das concentracoes
            converte a meia vida para minutos dependendo do tipo da meia vida (h,d,m,y)  """
        n=self.ui.tbElem.rowCount()
        self.ui.tbElem.setRowCount(n+1)
        valor=QtGui.QTableWidgetItem("%s" % (self.ui.cbElem.currentText()), QtGui.QTableWidgetItem.Type)
        self.ui.tbElem.setItem(n,0,valor)
        ss=string.split(str(self.ui.cbElem.currentText()),"(")
        xelem=self.Elementos.busca_elem(float(ss[1][:-1]),ss[0])
        valor=QtGui.QTableWidgetItem("%f" % float(xelem[0]), QtGui.QTableWidgetItem.Type)
        self.ui.tbElem.setItem(n,1,valor)
        if (xelem[3]=="h"):
           minutos=float(xelem[2])*60
        else:
         if (xelem[3]=="d"):
            minutos=float(xelem[2])*60*24
         else:
          if (xelem[3]=="m"):
             minutos=float(xelem[2])*60*24*30
          else:
           if (xelem[3]=="a"):
              minutos=float(xelem[2])*60*24*30*365
        valor=QtGui.QTableWidgetItem("%f" %(minutos), QtGui.QTableWidgetItem.Type)
        self.ui.tbElem.setItem(n,2,valor)
        valor=QtGui.QTableWidgetItem("%f" % float(self.ui.txtConcentra.text()), QtGui.QTableWidgetItem.Type)
        self.ui.tbElem.setItem(n,3,valor)
        valor=QtGui.QTableWidgetItem("%f" % float(self.ui.txtConcentradesv.text()), QtGui.QTableWidgetItem.Type)
        self.ui.tbElem.setItem(n,4,valor)
#        self.dirty = True
#        self.setWindowModified(self.dirty)


    def excElemento(self):
        """ Botao: cmdExcElem - aba parametros
            Exclui um elemento que foi inserido errado, para efeito de calculo das concentracoes"""
        self.ui.tbElem.removeRow(self.ui.tbElem.currentRow())

    def clicklst(self):
        """ Objeto: lstarqs -  lista dos arquivos de espectros lancados no projeto
            ao clicar na lista de arquivos, seleciona o arquivo de espectro que deve ser trabalhado
            exibindo o grafico correspondente """
        if self.ui.lstarqs.count() == 0:
            return
        legend="%s" %(self.ui.lstarqs.item(self.ui.lstarqs.currentRow()).text())
        self.legend=legend
       #legend = self.graph.getactivecurve(justlegend = 1)
        if legend is None:
            return
        info,x,y = self.lerlegend(legend)
        # update spectrum parameters
        self.parametros_espectro(info)
        # update graph
        self.graph.clearcurves()
        curveinfo={}
        self.graph.newCurve(legend,x,y,logfilter=1, curveinfo=None) #curveinfo)
        self.graph.replot()


    def recupera(self,pEnergia=0.0,pIntervalo=0.0,plegend='0'):
        """ da rotina: calConcentra - que calcula as concentracoes
            retorna a atividade(cps) e o erro(erreur) para os parametros de energia (pEnergia)
            mais ou menos o intervalo (pIntervalo) dos dados produto do calculo do espectro (pLegend) """
        energiaI = float(pEnergia-pIntervalo)
        energiaF = float(pEnergia+pIntervalo)
        pResCalculo=self.dataObjectsDict[plegend].info["ResCalculo"]
        res=len(pResCalculo)
        for i in range(0,res):
            if ((float(pResCalculo[i]["energia"]) > energiaI) & (float(pResCalculo[i]["energia"]) < energiaF)):
               return float(pResCalculo[i]["cps"]), float(pResCalculo[i]["erreur"])
        return 0.0,0.0

    def imprimeConcentracao(self):
        """ Botao: cmdImpConcentra - da aba Resultado das Concentracoes
            Imprime os resultados do calculo das concentracoes"""
        if self.printer is None:
           self.printer = qt.QPrinter()
           self.printer.setPageSize(qt.QPrinter.A4)
           self.printer.setPrintRange(qt.QPrinter.AllPages)
           self.printer.setFromTo(0,99)
        dialog = qt.QPrintDialog(self.printer, self)
        if not dialog.exec_():
            return
        LeftMargin = 36
        sansFont = qt.QFont("Courier", 10)
        sansLineHeight = qt.QFontMetrics(sansFont).height()
        serifFont = qt.QFont("Courier", 11)
        fm = qt.QFontMetrics(serifFont)
        serifLineHeight = fm.height()
        centrado = QtCore.Qt.AlignHCenter
        if self.painter is None:
            self.painter = qt.QPainter(self.printer)
        self.painter.begin(self.printer)
        pageRect = self.printer.pageRect()
        page = 1
#        y = self.printcabecalho(pageRect,fm,LeftMargin,sansFont,sansLineHeight)
        y = 2 * serifLineHeight
        pageHeight = self.painter.window().height() - 2 * serifLineHeight;
        xpgnumber = pageRect.width()- 1.5 * fm.width("Pagina 123")

        if self.dataObjectsDict[legend].info['FakeCal']:
            calibra = qt.QString("%l").arg("Sem Calibração - Cuidado").rightJustified(15)
            self.painter.drawText(x,y,calibra)
        y += 1 * serifLineHeight
        for a in range(0,len(self.amo)):
            self.painter.save()
            self.painter.setFont(serifFont)
            x = LeftMargin
            y += 2 * serifLineHeight
            lP=len(self.amo[a])
            amostra = qt.QString("%1").arg("Amostra: %s" % self.pAmostra[a]).rightJustified(15)
            self.painter.drawText(x,y,amostra)
            y += 1 * serifLineHeight
            x+=fm.width(amostra)
            linha = qt.QString("%1").arg("Padrão").rightJustified(15)
            self.painter.drawText(x,y,linha)
            y += 1 * serifLineHeight
            for p in range(0, lP):
               x = LeftMargin
               y += 1 * serifLineHeight
               elem = qt.QString("%1").arg("%s" % (self.pElem[0]["elemento"])).rightJustified(15)
               x+=fm.width(elem)
               lE=len(self.amo[a][p])
               linha = qt.QString("%1").arg("%s" % self.pPadrao[p]).rightJustified(12)
               self.painter.drawText(x,y,linha)
               x+=fm.width(linha)
               linha = qt.QString("%1").arg("S").rightJustified(12)
               self.painter.drawText(x,y,linha)
               y += 2 * serifLineHeight
               for e in range(1, lE+1):
                  x = LeftMargin
                  if (self.amo[a][p][e]["conF"]==0) and (self.amo[a][p][e]["conE"]==0):
                    x = LeftMargin
                  else:
                    elem = qt.QString("%1").arg("%s" % (self.pElem[e]["elemento"])).rightJustified(15)
                    conf = qt.QString("%1").arg("%8.4f" % (self.amo[a][p][e]["conF"])).rightJustified(12)
                    cone = qt.QString("%1").arg("%8.4f" % (self.amo[a][p][e]["conE"])).rightJustified(12)
                    self.painter.drawText(x,y,elem)
                    x+=fm.width(elem)
                    self.painter.drawText(x,y,conf)
                    x+=fm.width(conf)
                    self.painter.drawText(x,y,cone)
                    x+=fm.width(cone)
                    y += serifLineHeight
                    if y + 3 * serifLineHeight > pageHeight:
                       self.painter.drawText(xpgnumber,pageHeight - serifLineHeight,qt.QString("Página %1").arg(page))
                       self.printer.newPage()
                       page += 1
                       y = 2 * serifLineHeight
#                     y = self.printcabecalho(pageRect,fm,LeftMargin,sansFont,sansLineHeight)
        self.painter.drawText(xpgnumber,pageHeight - serifLineHeight,qt.QString("Página %1").arg(page))
        self.painter.end()

    def calConcentra(self):
        """ da rotina: ver_abas - que verifica a movimentacao das abas na janela principal
            eh executada quando entra na aba Resultado das Concentracoes e efetua o calculo
            das concentracoes para cada arquivo (espectro) adicionado no projeto e ja identificado
            como amostra e/ou padrao a rotina identifica cada um dos arquivos e separa entre
            amostra e padrao se for padrao identifica os elemntos e suas concentracoes para
            efetuar o calculo para cada amostra atraves dos resultados ja calculos das areas
            dos picos, energias e atividades encontra os elementos apontados em cada padrao,
            efetuando então o calculo de cada concentracao para cada padrao em referencia a
            amostra, por fim exibe os resultados no video em forma de abas e tabelas
        """
        self.ui.tabWidget_2.clear()
        self.resConcentracao={}
        pElem={}
        pAmostra={}
        pPadrao={}
        linha={}
        linha['elemento']=str("0")
        linha['energia']=str("0")
        linha['meiavida']=str("0")
        pElem[0]=linha
        nP=0
        nA=0
        n=self.ui.lstarqs.count()
        for j in range(0,n):
            legend="%s" %(self.ui.lstarqs.item(j).text())
            if self.dataObjectsDict[legend].info['Amostra'] == 2:
               pPadrao[nP]=legend
               nP=nP+1
               pe=len(pElem)
# colocar o padrão concentração em cada emento
               for k in range(0,pe):
                  legCon={}
                  legCon["conP"]=0
                  legCon["conF"]=0
                  legCon["conE"]=0
                  legCon["conPD"]=0
                  legCon["conFD"]=0
                  legCon["conED"]=0
                  pElem[k][legend]=legCon
               pdic=self.dataObjectsDict[legend].info['lElem']
               e=len(pdic)
               for i in range(0,e):
                  pe=len(pElem)
                  achou=0
                  for k in range(0,pe):
                     if pdic[i]["elemento"] == pElem[k]["elemento"] :
                        pElem[k][legend]["conP"]=pdic[i]["concentra"]
                        pElem[k][legend]["conPD"]=pdic[i]["concentradesv"]
                        achou=1
                  if achou == 0:
                     pElem[pe]=pdic[i]
                     for nl in range(0,n):
                        nlegend="%s" %(self.ui.lstarqs.item(nl).text())
                        legCon={}
                        legCon["conP"]=0
                        legCon["conF"]=0
                        legCon["conE"]=0
                        legCon["conPD"]=0
                        legCon["conFD"]=0
                        legCon["conED"]=0
                        pElem[pe][nlegend]=legCon
                     pElem[pe][legend]["conP"]=pdic[i]["concentra"]
                     pElem[pe][legend]["conPD"]=pdic[i]["concentradesv"]
            else:
               pAmostra[nA]=legend
               nA=nA+1
        pe=len(pElem)
        intervalo = 1.6
# ---- mostra os elementos e as concentrações em cada padrão
        self.pAmostra=pAmostra
        self.pPadrao=pPadrao
        self.pElem=pElem
        self.amo={}
        self.rescon={}
        for a in range(0,nA):
           massaA=float(self.dataObjectsDict[pAmostra[a]].info["Massa"])
           dataA=self.dataObjectsDict[pAmostra[a]].info['DataTempo']
           pad={}
           for p in range(0,nP):
               massaP=float(self.dataObjectsDict[pPadrao[p]].info["Massa"])
               dataP=self.dataObjectsDict[pPadrao[p]].info['DataTempo']
               ele={}
               for e in range(1,pe):
                   energia = float(pElem[e]["energia"])
                   legend=pAmostra[a]
                   cpsA,sA = self.recupera(energia,intervalo,legend)
                   legend=pPadrao[p]
                   cpsP,sP = self.recupera(energia,intervalo,legend)
                   dA=datetime.datetime(int(dataA[6:10]),int(dataA[3:5]),int(dataA[0:2]),int(dataA[11:13]),int(dataA[14:16]),int(dataA[17:19]))
                   dP=datetime.datetime(int(dataP[6:10]),int(dataP[3:5]),int(dataP[0:2]),int(dataP[11:13]),int(dataP[14:16]),int(dataP[17:19]))
                   if dA > dP:
                      dF=(dA - dP)*-1
                   else:
                      dF=dP - dA
                   difdt=dF.days*24*60 + dF.seconds/60
                   lambd=math.log(2)/(float(pElem[e]["meiavida"]))
                   if (cpsP == 0):
                      con=0
                      errCon=0
                   else:
                      con=(cpsA * massaP * float(pElem[e][pPadrao[p]]["conP"]) * math.exp(-lambd * difdt)) / (cpsP * massaA)
                      if (cpsA == 0):
                         errCon=0
                      else:
                        if float(pElem[e][pPadrao[p]]["conP"]) == 0.0 :
                           errCon= con * math.sqrt((((sA * cpsA) / 100) / cpsA)**2 + (((sP * cpsP) / 100) / cpsP)**2 )
                        else:
                           errCon= con * math.sqrt((((sA * cpsA) / 100) / cpsA)**2 + (((sP * cpsP) / 100) / cpsP)**2 + (((float(pElem[e][pPadrao[p]]["conPD"]) / float(pElem[e][pPadrao[p]]["conP"])) ))**2)
                   d={}
                   d["conF"]=con
                   d["conE"]=errCon
                   pElem[e][pPadrao[p]]["conF"]=con
                   pElem[e][pPadrao[p]]["conE"]=errCon
                   ele[e]=d
               pad[p]=ele
           self.amo[a]=pad
           self.tabn = QtGui.QWidget()
           self.tabn.setObjectName("tabn")
# cria quadro table dentro da aba
           self.gAmostra1 = QtGui.QTableWidget(self.tabn)
           self.gAmostra1.setGeometry(QtCore.QRect(0,0,741,391))
           self.gAmostra1.setObjectName("gAmostra1")
# dentro da table Widget_2 adiciona a aba já com o table
           self.gAmostra1.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
           self.ui.tabWidget_2.addTab(self.tabn,"")
           self.ui.tabWidget_2.setTabText(self.ui.tabWidget_2.indexOf(self.tabn), pAmostra[a])
           lin=0
           col=1
           self.gAmostra1.clear()
           self.gAmostra1.setColumnCount(col)
           headerItem01 = QtGui.QTableWidgetItem()
           headerItem01.setText(QtGui.QApplication.translate("frmmenu", "Elemento", None, QtGui.QApplication.UnicodeUTF8))
           self.gAmostra1.setHorizontalHeaderItem(0,headerItem01)
           for lp in range(0,nP):
              col=col+1
              self.gAmostra1.setColumnCount(col)
              headerItem02 = QtGui.QTableWidgetItem()
              headerItem02.setText(pPadrao[lp])
              self.gAmostra1.setHorizontalHeaderItem(col-1,headerItem02)
              col=col+1
              self.gAmostra1.setColumnCount(col)
              headerItem03 = QtGui.QTableWidgetItem()
              headerItem03.setText("S(%)")
              self.gAmostra1.setHorizontalHeaderItem(col-1,headerItem03)
           lE=len(pElem)
           for le in range(0,lE):
              self.gAmostra1.setRowCount(lin)
              valor=QtGui.QTableWidgetItem("%s" % pElem[le]["elemento"], QtGui.QTableWidgetItem.Type)
              self.gAmostra1.setItem(lin-1,0,valor)
              col=2
              for lp in range(0,nP):
                 valor=QtGui.QTableWidgetItem("%f" % (pElem[le][pPadrao[lp]]["conF"]), QtGui.QTableWidgetItem.Type)
                 self.gAmostra1.setItem(lin-1,col-1,valor)
                 valor=QtGui.QTableWidgetItem("%f" % (pElem[le][pPadrao[lp]]["conE"]), QtGui.QTableWidgetItem.Type)
                 self.gAmostra1.setItem(lin-1,col,valor)
                 col=col+2
              lin =lin + 1

    def lerCalibracao(self):
        """ Botao: cmdcalibracao -
            abre janela para localizar arquivo de calibracao do sistema (equipamento que efetuou a contagem)
            efetua a leitura e armazena os dados na variavel self.pprojeto, para posterior uso no calculo
            das areas dos picos, energias e atividades

            E preciso ter um espectro aberto para ler a calibração para ele.
            Calibração é individual - por espectro;
            Pode-se, entretanto, atribuir a mesma calibração já lida a um novo espectro.
        """


        try:
            legend="%s" %(self.ui.lstarqs.item(self.ui.lstarqs.currentRow()).text())
        except:
             msg = qt.QMessageBox(self)
             msg.setIcon(qt.QMessageBox.Critical)
             msg.setText("Nenhum espectro aberto!\nAbra primeiro um Espectro!!")
             msg.exec_()
             return

        cwd = os.getcwd()
        openfile = qt.QFileDialog(self)
        openfile.setFilter('*.cal')
        openfile.setFileMode(openfile.ExistingFile)
        openfile.setAcceptMode(qt.QFileDialog.AcceptOpen)
#        print "diretorios "
#        print cwd
#        print self.configDir

        if os.path.exists(self.configDir):cwd =self.configDir
        openfile.setDirectory(cwd)
        ret = openfile.exec_()
# coloquei devido a problemas com arquivo ou diretorio com acentuacao
        try:
             vfile=str(openfile.selectedFiles()[0])
        except:
             msg = qt.QMessageBox(self)
             msg.setIcon(qt.QMessageBox.Critical)
             msg.setText("Erro nome do arquivo (acentuação!): %s" % (sys.exc_info()[1]))
             msg.exec_()
             return
        if os.path.exists(vfile):
            fileToOpen = open(vfile)
            linhas = fileToOpen.readlines()
#            initialFile = [string.split(line) for line in fileToOpen]
            energyterms = linhas[0].split()
            linha0 = linhas[0].split()
#            vartmp, slope, offset = linhas[0].split()
            linha1 = linhas[1].split
#            ro, kres = linhas[1].split()
            self.dataObjectsDict[legend].info['slope'] =  float(linha0[1])   #float(initialFile[0][1])
            self.dataObjectsDict[legend].info['offset']=  float(linha0[2]) # float(initialFile[0][2])
            try:
                self.dataObjectsDict[legend].info['enerquad'] = float(linha0[3])
            except:
                self.dataObjectsDict[legend].info['enerquad'] = 0.0

            self.dataObjectsDict[legend].info['ro']    =  float(linha1[0])     #float(initialFile[1][0])
            self.dataObjectsDict[legend].info['kres']  =  float(linha1[1])   # float(initialFile[1][1])
            try:
                self.dataObjectsDict[legend].info['widthquad'] = float(linha1[2])
            except:
                self.dataObjectsDict[legend].info['widthquad'] = 0.0
            self.dataObjectsDict[legend].info['ArqCalib']  = "%s" %(vfile)
            self.dataObjectsDict[legend].info['FakeCal']=False
            #self.ui.lblcalibracao.setText(self.pprojeto['ArqCalib'])
#            self.dirty = True
#            self.setWindowModified(self.dirty)
            self.projeto='Projeto1.san'
            return 0
        else:
            raise "IOError",("Arquivo não existe %s " % vfile)
            self.dataObjectsDict[legend].info['slope'] =   1.0
            self.dataObjectsDict[legend].info['offset']=   0.0
            self.dataObjectsDict[legend].info['enerquad'] = 0.0
            self.dataObjectsDict[legend].info['ro']    =   0.0
            self.dataObjectsDict[legend].info['kres']  =   1.0
            self.dataObjectsDict[legend].info['widthquad'] = 0.0
            self.dataObjectsDict[legend].info['ArqCalib']   = ''
            self.dataObjectsDict[legend].info['FakeCal']=True
            #self.ui.lblcalibracao.setText(self.pprojeto['ArqCalib'])
            return 1

    def consiste(self):
        """ da rotina: ver_abas - que verifica a movimentação das abas
            quando entra na aba - Resultado de Concentracoes executa esta rotrina para
            consistencia dos dados verificando se o arquivo de calibração do Arquivo ja
            foi lido, se esta Faltando a Massa do Arquivo de espectro para o calculo,
            se existe Elementos lancados para o Padrão, se tem os arquivos de amostra
            e padrao para os calculos
            retorna 1 se deu erro
            retorna 0 se OK """
        smsg=""
        padrao=0
        amostra=0
        n=self.ui.lstarqs.count()
        if n == 0:
            smsg = u"Nenhum espectro lido"
            return 1, smsg
        for j in range(0,n):
            legend="%s" %(self.ui.lstarqs.item(j).text())
            if (self.dataObjectsDict[legend].info['FakeCal']  == True):
               smsg = u"Entrar com o arquivo de calibração do Arquivo: %s" % (legend)
               return 1,smsg
            if (self.dataObjectsDict[legend].info['Massa']==""):
               smsg = u"Falta a Massa do Arquivo: %s" %(legend)
               return 1,smsg
            if (self.dataObjectsDict[legend].info['Amostra'] == 2):
               if self.dataObjectsDict[legend].info['lElem'] == '':
                  smsg = u"Elementos do Padrao, Arquivo: %s" %(legend)
                  return 1,smsg
               padrao=1
            if (self.dataObjectsDict[legend].info['Amostra'] == 1):
               amostra=1
        if (amostra==1) and (padrao==1):
           return 0,smsg
        else:
           smsg = u"No minimo temos que ter uma amostra e um padrão para o cálculo das concentrações"
           return 1,smsg

    def ver_abas_padrao(self):
        """ Objeto: rba - botao de opcao (amostra ou padrao) da aba de parametros
           Se for padrao deixa visivel a entrada dos dados da Concentração dos Elementos no Padrão
           Se for amostra deixa invisivel esta entrada
        """
        if self.ui.rba.isChecked():
            self.ui.groupBox.setVisible(0)
        else:
            self.ui.groupBox.setVisible(1)

    def parametros_espectro(self,rec_info=None):
        """rotina chamada para atualizar os dados relativos ao espectro atual
               (aba tbParEspec)
           recebe como parâmetro o nome do arquivo atual (legend) - aquele
               selecionado na lista de arquivos
        """
        if rec_info == None:
            return
        info = rec_info
        self.ui.lblvivo.setText(str(info['TempoVivo']))
        self.ui.lblmorto.setText(str(info['TempoTotal']))
        aux22=(info['DataTempo'])
        aux=QtCore.QString(aux22)
        now2 = QtCore.QDateTime.fromString(aux22, QtCore.QString("dd/MM/yyyy hh:mm:ss"))
        self.ui.txtdatamedida.setDateTime(now2)
        self.ui.txtmassa.setText(str(info['Massa']))
        self.ui.txtnivel.setText(str(info['Nivel']))
        self.ui.txtsigma.setText(str(info['Sigma']))


    def ver_abas(self):
        """ da rotina: verifcaAbas do Objeto: tabPropert - quadro de abas
            verificar a movimentação das abas da janela principal e excuta procedimentos
            especificos para cada uma delas
            self.ui.tabPropert.currentIndex() ==
             0:Grafico - nao executa nada
             1:Parametros - recupera os dados da variavel global e exibe na janela
             2:Resultado de Calculos  - executa a rotina vispectFit para os calculos
             3:Resultado das Concentracoes - executa a rotina calConcentra para os calculos
             4:Projeto - guarda na variavel saiuAba o valor 4 para efetuar consistencias
            variavel self.saiuAba =
             4: indica que saiu da aba Projetos entao efetua consistencias: se deu entrada dos
               dados de calibracao e se ja salvou o projeto
             1: indica que saiu da aba Parametros entao identifica se eh amostra ou padrao
               aguarda os dados (parametros) na variavel de global para o arquivo (espectro)
        """

        try:
            legend="%s" %(self.ui.lstarqs.item(self.ui.lstarqs.currentRow()).text())
            self.legend=legend
        except AttributeError:
            return
       #legend = self.graph.getactivecurve(justlegend = 1)
        if legend is None:
            return
        info,x,y = self.lerlegend(legend)
        self.ui.lblvivo.setText(str(info['TempoVivo']))
        self.ui.lblmorto.setText(str(info['TempoTotal']))
        aux22=(info['DataTempo'])
        aux=QtCore.QString(aux22)
        now2 = QtCore.QDateTime.fromString(aux22, QtCore.QString("dd/MM/yyyy hh:mm:ss"))
        self.ui.txtdatamedida.setDateTime(now2)
        self.ui.txtmassa.setText(str(info['Massa']))
        self.ui.txtnivel.setText(str(info['Nivel']))
        self.ui.txtsigma.setText(str(info['Sigma']))

# aba - Grafico
        if self.ui.tabWidget.currentIndex() == 0:
            if self.ui.lstarqs.count() > 0:
                legend="%s" %(self.ui.lstarqs.item(self.ui.lstarqs.currentRow()).text())
                info,x,y = self.lerlegend(legend)
                self.graph.clearcurves()
                curveinfo={}
                self.graph.newCurve(legend,x,
                                    y,
                                    logfilter=1, curveinfo=None) #curveinfo)
                self.graph.replot()
            else:
            # não tem espectro aberto, apaga os gráficos
                self.graph.clearcurves()
# aba - Parametros
        elif self.ui.tabWidget.currentIndex() == 1:
           if self.ui.lstarqs.count() == 0:
               return
           legend="%s" %(self.ui.lstarqs.item(self.ui.lstarqs.currentRow()).text())
           if legend is None:
               msg = qt.QMessageBox(self)
               msg.setIcon(qt.QMessageBox.Critical)
               msg.setText("Please Select an active curve")
               if qt.qVersion() < '4.0.0':
                  msg.exec_loop()
               else:
                  msg.exec_()
               return
           info,x,y = self.lerlegend(legend)
           self.vlegend=legend
           self.ui.lblvivo.setText(str(info['TempoVivo']))
           self.ui.lblmorto.setText(str(info['TempoTotal']))
           aux22=(info['DataTempo'])
           aux=QtCore.QString(aux22)
           now2 = QtCore.QDateTime.fromString(aux22, QtCore.QString("dd/MM/yyyy hh:mm:ss"))
           self.ui.txtdatamedida.setDateTime(now2)
           self.ui.txtmassa.setText(str(info['Massa']))
           self.ui.txtnivel.setText(str(info['Nivel']))
           self.ui.txtsigma.setText(str(info['Sigma']))

           if self.dataObjectsDict[legend].info['Amostra']==1:
              self.ui.rba.setChecked(True)
              self.ui.rbp.setChecked(False)
           else:
              self.ui.rba.setChecked(False)
              self.ui.rbp.setChecked(True)
              if len(self.dataObjectsDict[legend].info['lElem'])==0:
                 te=self.ui.tbElem.rowCount()
                 self.dataObjectsDict[legend].info['lElem']=''
                 for e in range(0,te):
                    self.ui.tbElem.removeRow(0)
              else:
                 te=len(self.dataObjectsDict[legend].info['lElem'])
                 self.ui.tbElem.clear()
                 headerItem = QtGui.QTableWidgetItem()
                 headerItem.setText(QtGui.QApplication.translate("frmmenu", "Elemento", None, QtGui.QApplication.UnicodeUTF8))
                 self.ui.tbElem.setHorizontalHeaderItem(0,headerItem)
                 headerItem1 = QtGui.QTableWidgetItem()
                 headerItem1.setText(QtGui.QApplication.translate("frmmenu", "Energia", None, QtGui.QApplication.UnicodeUTF8))
                 self.ui.tbElem.setHorizontalHeaderItem(1,headerItem1)
                 headerItem2 = QtGui.QTableWidgetItem()
                 headerItem2.setText(QtGui.QApplication.translate("frmmenu", "Meia Vida (minutos)", None, QtGui.QApplication.UnicodeUTF8))
                 self.ui.tbElem.setHorizontalHeaderItem(2,headerItem2)
                 headerItem3 = QtGui.QTableWidgetItem()
                 headerItem3.setText(QtGui.QApplication.translate("frmmenu", "Concentracao", None, QtGui.QApplication.UnicodeUTF8))
                 self.ui.tbElem.setHorizontalHeaderItem(3,headerItem3)
                 headerItem4 = QtGui.QTableWidgetItem()
                 headerItem4.setText(QtGui.QApplication.translate("frmmenu", "Desv.", None, QtGui.QApplication.UnicodeUTF8))
                 self.ui.tbElem.setHorizontalHeaderItem(4,headerItem4)
                 for j in range(0,te):
                    self.ui.tbElem.setRowCount(j+1)
                    valor=QtGui.QTableWidgetItem("%s" % (self.dataObjectsDict[legend].info['lElem'][j]['elemento']), QtGui.QTableWidgetItem.Type)
                    self.ui.tbElem.setItem(j,0,valor)
                    valor=QtGui.QTableWidgetItem("%f" % float(self.dataObjectsDict[legend].info['lElem'][j]['energia']), QtGui.QTableWidgetItem.Type)
                    self.ui.tbElem.setItem(j,1,valor)
                    valor=QtGui.QTableWidgetItem("%f" % float(self.dataObjectsDict[legend].info['lElem'][j]['meiavida']), QtGui.QTableWidgetItem.Type)
                    self.ui.tbElem.setItem(j,2,valor)
                    valor=QtGui.QTableWidgetItem("%f" % float(self.dataObjectsDict[legend].info['lElem'][j]['concentra']), QtGui.QTableWidgetItem.Type)
                    self.ui.tbElem.setItem(j,3,valor)
                    valor=QtGui.QTableWidgetItem("%f" % float(self.dataObjectsDict[legend].info['lElem'][j]['concentradesv']), QtGui.QTableWidgetItem.Type)
                    self.ui.tbElem.setItem(j,4,valor)
           if self.ui.rba.isChecked():
              self.ui.groupBox.setVisible(0)
           else:
              self.ui.groupBox.setVisible(1)

# ------ aba - Resultado de Calculos
        elif self.ui.tabWidget.currentIndex() == 2:
           if self.ui.lstarqs.count() == 0:
               return
           legend="%s" %(self.ui.lstarqs.item(self.ui.lstarqs.currentRow()).text())
           self.montagrade(legend)

# ------ aba - Resultado das Concentracoes
        elif self.ui.tabWidget.currentIndex() == 3:
           resp,smsg = self.consiste()
           if resp:
               msg = qt.QMessageBox(self)
               msg.setIcon(qt.QMessageBox.Critical)
               msg.setText(smsg)
               if qt.qVersion() < '4.0.0':
                  msg.exec_loop()
               else:
                  msg.exec_()
               return
           self.calConcentra()


    def imprimeResultados(self):
        """ Botao: cmdImpRes - da aba Resultado dos Calculos
           imprime os resultados dos calculos, energia, BG , etc...
        """
        if self.printer is None:
           self.printer = qt.QPrinter()
           self.printer.setPageSize(qt.QPrinter.A4)
           self.printer.setPrintRange(qt.QPrinter.AllPages)
           self.printer.setFromTo(0,99)
        dialog = qt.QPrintDialog(self.printer, self)
        if not dialog.exec_():
            return
        legend="%s" %(self.ui.lstarqs.item(self.ui.lstarqs.currentRow()).text())
        self.legend=legend
        LeftMargin = 36
        sansFont = qt.QFont("Courier", 10)
        sansLineHeight = qt.QFontMetrics(sansFont).height()
        serifFont = qt.QFont("Courier", 11)
        fm = qt.QFontMetrics(serifFont)
        serifLineHeight = fm.height()
        centrado = QtCore.Qt.AlignHCenter
        if self.painter is None:
            self.painter = qt.QPainter(self.printer)
        self.painter.begin(self.printer)
        pageRect = self.printer.pageRect()
        page = 1
        y = self.printcabecalho(pageRect,fm,LeftMargin,sansFont,sansLineHeight)
        tbRes=self.dataObjectsDict[self.legend].info['ResCalculo']
        pageHeight = self.painter.window().height() - 2 * serifLineHeight;
        xpgnumber = pageRect.width()- 1.5 * fm.width("Pagina 123")
        for i in range(0,len(tbRes)):
            self.painter.save()
            self.painter.setFont(serifFont)
            x = LeftMargin
            seq = qt.QString("%1").arg("%d" %(i+1)).rightJustified(4)
            energia = qt.QString("%1").arg("%8.2f" % float(tbRes[i]['energia'])).rightJustified(8)
            area = qt.QString("%1").arg("%8.0f" % float(tbRes[i]['area'])).rightJustified(9)
            bg = qt.QString("%1").arg("%8.0f" % float(tbRes[i]['bg'])).rightJustified(7)
            resol = qt.QString("%1").arg("%5.2f" % float(tbRes[i]['resol'])).rightJustified(6)
            canfin = qt.QString("%6.2f" % float(tbRes[i]['fi'])).rightJustified(10)
            canini = qt.QString("%6.0f" % float(tbRes[i]['id'])).rightJustified(8)
            lp = qt.QString("%3d" % tbRes[i]['lp']).rightJustified(5)
            cps = qt.QString("%4.4f" % float(tbRes[i]['cps'])).rightJustified(8)
            erro = qt.QString("%5.1f" % float(tbRes[i]['erreur'])).rightJustified(6)
            self.painter.drawText(x,y,seq)
            x+=fm.width(seq)
            self.painter.drawText(x,y,energia)
            x+=fm.width(energia)
            self.painter.drawText(x,y,area)
            x+=fm.width(area)
            self.painter.drawText(x,y,bg)
            x+=fm.width(bg)
            self.painter.drawText(x,y,resol)
            x+=fm.width(resol)
            self.painter.drawText(x,y,canfin)
            x+=fm.width(canfin)
            self.painter.drawText(x,y,canini)
            x+=fm.width(canini)
            self.painter.drawText(x,y,lp)
            x+=fm.width(lp)
            self.painter.drawText(x,y,cps)
            x+=fm.width(cps)
            self.painter.drawText(x,y,erro)
            y += serifLineHeight
            if y + 3 * serifLineHeight > pageHeight:
                self.painter.drawText(xpgnumber,pageHeight - serifLineHeight,qt.QString("Página %1").arg(page))
                self.printer.newPage()
                page += 1
                y = self.printcabecalho(pageRect,fm,LeftMargin,sansFont,sansLineHeight)
        self.painter.drawText(xpgnumber,pageHeight - serifLineHeight,qt.QString("Página %1").arg(page))
        self.painter.end()

    def printcabecalho(self,pageRect,fm,LeftMargin,sansFont,sansLineHeight):
        """ da rotina: imprimeResultados do Botao: cmdImpRes - da aba Resultado dos Calculos
            imprime o cabecalho do relatorio energia, BG , etc...
        """
        cabec1 = 'Resultados'
        cabec2 = 'Arquivo: '+self.legend
        if self.dataObjectsDict[self.legend].info['Amostra'] == 2:
           cabec2 += ' - Padrao'
        else:
           cabec2 += ' - Amostra'
        DATE_FORMAT= 'ddd, d/MMMM/yyyy'
        xpos = pageRect.width()
        seqwidth = fm.width("Seq.")
        enerwidth = fm.width("Energia ")
        areawidth = fm.width("Area    ")
        x = LeftMargin + pageRect.width()/6
        y = 2 * sansLineHeight
        self.painter.setFont(sansFont)
        self.painter.drawText(x,y, cabec1)
        x+=fm.width(cabec1) + 2
        self.painter.drawText(x,y, cabec2)
        x+=fm.width(cabec2) + 2
        x+=fm.width(qt.QDate.currentDate().toString(DATE_FORMAT))/2
        self.painter.drawText(x,y,
                qt.QDate.currentDate().toString(DATE_FORMAT))
        y += 2 * sansLineHeight
        x = LeftMargin
        linha = 'Tempo Total: %s seg.   Massa: %s  Data contagem: %s' % (self.dataObjectsDict[self.vlegend].info['TempoTotal'],self.dataObjectsDict[self.legend].info['Massa'],self.dataObjectsDict[self.legend].info['DataTempo'])
        self.painter.drawText(x,y, linha)
        y += 1 * sansLineHeight
        linha = 'Tempo Vivo : %s seg.   Nível sensibilidade: %s  ' % (self.dataObjectsDict[self.legend].info['TempoVivo'],self.dataObjectsDict[self.legend].info['Nivel'])
        self.painter.drawText(x,y, linha)
        y += 2 * sansLineHeight
        x = LeftMargin
        seq = qt.QString("Seq.").rightJustified(4)
        self.painter.drawText(x,y,seq)
        x+=fm.width(seq)
        energia= qt.QString("Energia").rightJustified(8)
        self.painter.drawText(x,y,energia)
        x+=fm.width(energia)
        area = qt.QString("Area").rightJustified(9)
        self.painter.drawText(x,y,area)
        x+=fm.width(area)
        bg = qt.QString("BG").rightJustified(7)
        self.painter.drawText(x,y,bg)
        x+=fm.width(bg)
        resol = qt.QString("Resol.").rightJustified(6)
        self.painter.drawText(x,y,resol)
        x+=fm.width(resol)
        canfin= qt.QString("Can.Final").rightJustified(10)
        self.painter.drawText(x,y,canfin)
        x+=fm.width(canfin)
        canini = qt.QString("Can.Inic").rightJustified(8)
        self.painter.drawText(x,y,canini)
        x+=fm.width(canini)
        lp = qt.QString("LP").rightJustified(5)
        self.painter.drawText(x,y,lp)
        x+=fm.width(lp)
        cps = qt.QString("CPS").rightJustified(8)
        self.painter.drawText(x,y,cps)
        x+=fm.width(cps)
        sigma="%s" % self.dataObjectsDict[self.vlegend].info['Sigma']
        sigma+="S(%)"
        erro = qt.QString(sigma).rightJustified(6)
        self.painter.drawText(x,y,erro)
        y += 2* sansLineHeight
        return y

    def sair(self):
        """ Menu: Sair
           executa quando clicado no menu sair, grava arquivo: recentes"""

#        if not self.okToContinue():
#            return
        if self.painter:
             self.painter.end()
        self.closeEvent(self)
        sys.exit(1)

    def printGraph(self):
        "Botao: cmdImpGraf - Imprime grafico"
        "imprimir grafico que esta sendo exibido no video "
        pixmap = qt.QPixmap.grabWidget(self.graph)
        self.printPreview.addPixmap(pixmap)
        if self.printPreview.isHidden():
            self.printPreview.show()
    #    if QTVERSION < '4.0.0':
    #        self.printPreview.raiseW()
    #    else:
            self.printPreview.raise_()


    def vispectFit(self,legend=None):
        """   Vai executar rotina para localização dos picos e o cálculo das energias, area do pico , etc...
            1. Recupera a legenda do grafico, que é o nome do arquivo
            2. Através da legenda executa rotina lerlegend()  que retona parametros, os canais e conmtagens
            3. Após executa a rotina da classe vispectfit para efetuar a localização dos picos e calculos
        """
        """Executa a rotina para a localização dos picos e o cálculo das energias, etc.   """
        if legend == None:
            return

        info,x,y = self.lerlegend(legend)
        if info is not None:

            verde = QtGui.QColor("lightgreen")
            vermelho = QtGui.QColor(255,191,191)
            xmin,xmax=self.graph.getx1axislimits()
            self.vispectfit.Lt = info['TempoVivo']
            self.vispectfit.vy=np.array(y,np.float64)
            self.updateStatus("%s" % ("Calculando espectro: " + legend))
            ppdic={}
            ppdic=self.vispectfit.vispectfit(xmin=xmin,xmax=xmax,vlegend=info).copy()
            self.dataObjectsDict[legend].info['ResCalculo']=ppdic
            n=len(ppdic)
            self.nlinhas=n
            self.updateStatus("%s" % ("Espectro "  + legend + " Calculado!"))
            return
        else:
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Critical)
            msg.setText("Erro não pode ajustar?")
            msg.exec_loop()

    def carregaGrafico(self, vertical=True):
        self.splitter = qt.QSplitter(self)
        if vertical:
            self.splitter.setOrientation(qt.Qt.Vertical)
        else:
            self.splitter.setOrientation(qt.Qt.Horizontal)
        self.graphBox = qt.QWidget(self.splitter)
        self.graphBoxlayout = qt.QVBoxLayout(self.graphBox)
        self.graphBoxlayout.setMargin(0)
        self.graphBoxlayout.setSpacing(0)



        self.toolbar  = qt.QWidget(self.graphBox)

        self.toolbar.layout  = qt.QHBoxLayout(self.toolbar)
        self.toolbar.layout.setMargin(0)
        self.toolbar.layout.setSpacing(0)

        self.graphBoxlayout.addWidget(self.toolbar)


#        self.graphBox.addButton(self.cmdimpgraf)


#        self.graph    = QtBlissGraph.QtBlissGraph(self.graphBox,uselegendmenu=1)
        self.graph    = QtBlissGraph.QtBlissGraph(self.ui.tabWidget,uselegendmenu=1)
        self.graph.xlabel('Canais')
        self.graph.ylabel('Contagens')
        self.graph.canvas().setMouseTracking(1)
        self.graph.setCanvasBackground(qt.Qt.white)
        self.graph.showGrid()

        self.cmdimpgraf = QtGui.QPushButton(self.graph)
        self.cmdimpgraf.setGeometry(QtCore.QRect(5,1,60,23))
        self.cmdimpgraf.setObjectName("cmdimpgraf")
        self.cmdimpgraf.setText(QtGui.QApplication.translate("frmmenu", "Imprimir", None, QtGui.QApplication.UnicodeUTF8))

#        self.ui.tabWidget.addTab(self.graph,"Grï¿½fico")
        self.ui.tabWidget.removeTab(0)        
        self.ui.tabWidget.insertTab(0,self.graph,u"Gráfico")
        self.ui.tabWidget.setCurrentIndex(0)

# posiciona aba
#        self.ui.tabWidget.setCurrentIndex(4)


    def lerlegend(self,legend,full=0):
# Recupera do dicionario dataObjectsDict, atraves da legenda os dados do espectro e retorna os valores
        info = None
        xdata    = None
        ydata    = None
        if legend in self.dataObjectsDict.keys():
            info  = self.dataObjectsDict[legend].info
            xdata = self.dataObjectsDict[legend].x[0]
            ydata = self.dataObjectsDict[legend].y[0]
        else:
            info = None
            xdata    = None
            ydata    = None
        if full:
            return info,None
        else:
            return info,xdata,ydata


    def vispectLer(self, arquivo = None):
        """ Efetua a leitura do arquivo de espectro e apresenta o grafico na tela
             1. Abre janela para localizar o arquivo
             2. Executa a rotina ler_MCAeCHN, passando como parametro o arquivo
             3. Recebe os dados do arquivo em um DataObject
             4. Guarda os dados em um dicionario dataObjectsDict, com o nome do arquivo
             5. Exibe grafico no video do arquivo que foi aberto
        """

        cwd = os.getcwd()
        openfile = qt.QFileDialog(self)
        openfile.setFilter('*.MCA ; *.CHN')
        openfile.setFileMode(openfile.ExistingFile)
        openfile.setAcceptMode(qt.QFileDialog.AcceptOpen)
        if os.path.exists(self.configDir):cwd =self.configDir
        openfile.setDirectory(cwd)
        ret = openfile.exec_()
    # coloquei devido a problemas com arquivo ou diretorio com acentuacao
        try:
            vfile=str(openfile.selectedFiles()[0])
        except:
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Critical)
            msg.setText("Erro nome do arquivo (acentuação!): %s" % (sys.exc_info()[1]))
            msg.exec_()
            return
    #verificar no Linux.....
        n=string.rfind(vfile,'\\')
        legend=vfile[n+1:]
        try:
            existe=self.dataObjectsDict[legend].info["SourceName"]
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Critical)
            msg.setText("Arquivo já foi lido, verifique!")
            msg.exec_()
            return
        except:
            existe="Não existe, pode ser incluido"

#        print n
#        print filename[0][n+1:]
#        print filename[0]
        vobj = crtLerEspectro.LerVispect(vfile)
        vdata = vobj.ler_arquivo()
#        vdata = vobj.ler_MCAeCHN()
        print "info = ",vdata.info
#        print "datay = ",vdata.y[0],  "type(datay)",  type(vdata.y[0])
#      print "datax = ",vdata.x[0],  "type(datax)",  type(vdata.x[0])
        dataObject = vdata
        self.dataObjectsDict[legend] = dataObject
# por enquanto estou atribuindo os valores de calibracao a todos os espectros,
        self.dataObjectsDict[legend].info['slope'] = 1.0
        self.dataObjectsDict[legend].info['offset']= 0.0
        self.dataObjectsDict[legend].info['ro']    = 1.0
        self.dataObjectsDict[legend].info['kres']  = 1.0
        self.dataObjectsDict[legend].info['ArqCalib']  = ' '
        self.dataObjectsDict[legend].info['FakeCal']=True

        self.vaux=legend
        self.vlegend=legend
        self.ui.lstarqs.addItem(self.vaux)
        posicao=self.ui.lstarqs.count() - 1
        curveinfo={}
        self.graph.clearcurves()
        self.graph.newCurve(legend,x=vdata.x[0],
                                   y=vdata.y[0],
                                   logfilter=1, curveinfo=None) #curveinfo)

        #self.graph.setxofy(legend)
        self.graph.replot()

#coloquei saiuAba=0 pois na leitura estava matando valores de Tempo VIVO e MORTO
        self.saiuAba = 0
        self.ui.tabWidget.setCurrentIndex(0)

        # ao ler um arquivo de espectro individual, tb faz o calculo em background
        # fc = fazCalculos(self.ui.lstarqs,posicao)
        # fc = fazCalculos(self.ui.lstarqs)
        # self.threads.append(fc)
        # fc.start()
        # self.dirty = True
        # self.setWindowModified(self.dirty)

    def calcAreas(self):

        posicao = self.ui.lstarqs.currentRow()
        if posicao == -1:
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Critical)
            msg.setText(u"Nenhum arquivo selecionado")
            msg.exec_()
            return
        arq ="%s" %(self.ui.lstarqs.item(posicao).text())
#        print "posicao: ", posicao
        verde = QtGui.QColor("lightgreen")
        vermelho = QtGui.QColor(255,191,191)
        self.ui.lstarqs.item(posicao).setBackgroundColor(vermelho)
        self.vispectFit(arq)
        self.ui.lstarqs.item(posicao).setBackgroundColor(verde)
        return
#        if arq not in self.dictThreadsCalc.keys():
#            fc = fazCalculos(self.ui.lstarqs,arq,posicao)
#            self.dictThreadsCalc[arq] = fc
#            fc.start()
#            try:
#                self.dictThreadsCalc.pop(arq)
#            except KeyError:
#                msg = qt.QMessageBox(self)
#                msg.setIcon(qt.QMessageBox.Critical)
#                msg.setText(u"Erro não esperado \n\n %s não localizado no dicionário!" %(arq))
#                msg.exec_()
#        elif self.ui.lstarqs.item(posicao).backgroundColor() == vermelho:
#            msg = qt.QMessageBox(self)
#            msg.setIcon(qt.QMessageBox.Critical)
#            msg.setText(u"%s já está sendo calculado \n\n Espere!" %(arq))
#            msg.exec_()
#        elif self.ui.lstarqs.item(posicao).backgroundColor() == verde:
#            msg = qt.QMessageBox(self)
#            msg.setIcon(qt.QMessageBox.Critical)
#            msg.setText(u"%s já calculado \n\n Calculando novamente" %(arq))
#            msg.exec_()
#            fc = fazCalculos(self.ui.lstarqs,arq,posicao)
#            self.dictThreadsCalc[arq] = fc
#            fc.start()
#            try:
#                self.dictThreadsCalc.pop(arq)
#            except KeyError:
#                msg = qt.QMessageBox(self)
#                msg.setIcon(qt.QMessageBox.Critical)
#                msg.setText(u"Erro não esperado \n %s não localizado no dicionário!" %(arq))
#                msg.exec_()

    def montagrade(self,legend):
        """rotina para montar a tabela com o resultado dos calculos (busca de picos e energias)
        """
#        for t in self.threads:
#            print "threads"
#            print t
#            print type(t)
        ppdic={}
        ppdic=self.dataObjectsDict[legend].info['ResCalculo']
        try:
            n=len(ppdic)
        except:
            self.updateStatus("Sem Resultados para mostrar")
#            crtFuncoes.criarGrade(self.ui.tableWidget, 1, 12, {})
#            crtFuncoes.cabecGradeRes(self.ui.tableWidget)
#            crtFuncoes.incGrade(self.ui.tabWidget, 0, "Sem Resultados")
            return
        if n > 0:
            self.nlinhas=n
            crtFuncoes.criarGrade(self.ui.tableWidget, n,12,{})
            crtFuncoes.cabecGradeRes(self.ui.tableWidget)
            for i in range(0,n):
                crtFuncoes.incGrade(self.ui.tableWidget,i,ppdic[i])
            self.ui.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        else:
            crtFuncoes.criarGrade(self.ui.tableWidget, 0,12,{})
            crtFuncoes.cabecGradeRes(self.ui.tableWidget)
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Critical)
            msg.setText("Sem resultados!")
            msg.exec_()
        return
#silvio rotinas de ajustes vispect



#class fazCalculos(QtCore.QThread):
class fazCalculos(threading.Thread):
       """Classe utilizada para realizar os calculos dos espectros em background
          Recebe um nome de arquivo de espectro para calcular"""
#       sem = QtCore.QSemaphore(1)

#       def __init__(self,listaarqs, parent=None):
#           super(fazCalculos,self).__init__(parent)
       def __init__(self, listarqs, arq,posicao=0):
           threading.Thread.__init__(self)

           self.listaarqs = listarqs
           self.arq = arq
           self.posicao   = posicao
           self.verde = QtGui.QColor("lightgreen")
           self.vermelho = QtGui.QColor(255,191,191)

#           fazCalculos.sem.acquire(1)


       def run(self):
           """faz os calculos dos espectros chamando a vispectfit"""
           self.listaarqs.item(self.posicao).setBackgroundColor(self.vermelho)
           appStart.vispectFit(self.arq)
           self.listaarqs.item(self.posicao).setBackgroundColor(self.verde)

#           if self.posicao == 0:
#            for i in range(self.listaarqs.count()):
#               arq = "%s" % (self.listaarqs.item(i).text())
#               appStart.vispectFit(arq)
#               verde = QtGui.QColor("lightgreen")
#               self.listaarqs.item(i).setBackgroundColor(verde)
#           else:
#               arq = "%s" % (self.listaarqs.item(self.posicao).text())
#               appStart.vispectFit(arq)
#               verde = QtGui.QColor("lightgreen")
#               self.listaarqs.item(self.posicao).setBackgroundColor(verde)

#               self.listaarqs.setCurrentRow(i)
#           fazCalculos.sem.release(1)
           appStart.updateStatus("Calculos Finalizados.")



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("IPEN.")
    app.setOrganizationDomain("IPEN.SAANI")
    app.setApplicationName("SAANI")
    appStart = startGui()
    appStart.show()
    sys.exit(app.exec_())
