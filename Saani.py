# -*- coding: ISO-8859-1 -*-

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
import Numeric
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

__version__ = "0.0.20080418"



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
#        print self.Elementos.elem
#        print self.Elementos.elem[0][0]
#        print self.Elementos.elem[0][1]
#        print self.Elementos.elem[0][2]
#        print self.Elementos.elem[0][3]
#        print self.Elementos.elem[1]
#        print self.Elementos.elem[2]
#        print self.Elementos.elem[3]
#" cria objeto para os calculos das areas dos picos e energias  "      
        self.vispectfit = crtCalculos.VispectFit()
        self.pprojeto={}
        self.pprojeto['slope'] = 0
        self.pprojeto['offset']= 0
        self.pprojeto['ro']    = 0
        self.pprojeto['kres']  = 0
        self.pprojeto['ArqCalib']  = ''
        self.pprojeto['titulo1']  = ''
        self.pprojeto['titulo2']  = ''
        self.dataObjectsDict={}
        self.resConcentracao={}
        self.pAmostra={}
        self.pPadrao={}
        self.pElem={}
        self.amo={}
        self.projeto=''
        self.setWindowTitle("SAANI - %s [*]" % os.path.basename(self.projeto))
        self.carregaGrafico()
        self._carregaElemnetos()
#" conectando botoes com suas respectivas rotinas "
        QtCore.QObject.connect(self.ui.cmdcalibracao, QtCore.SIGNAL("clicked()"), self.lerCalibracao)
        QtCore.QObject.connect(self.ui.cmdIncElem, QtCore.SIGNAL("clicked()"), self.incElemento)
        QtCore.QObject.connect(self.ui.cmdExcElem, QtCore.SIGNAL("clicked()"), self.excElemento)
        QtCore.QObject.connect(self.ui.cmdImpRes, QtCore.SIGNAL("clicked()"), self.imprimeResultados)
        QtCore.QObject.connect(self.ui.cmdImpConcentra, QtCore.SIGNAL("clicked()"), self.imprimeConcentracao)
        #QtCore.QObject.connect(self.ui.lstarqs, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.clicklst)
        QtCore.QObject.connect(self.ui.lstarqs, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.ver_abas)
        QtCore.QObject.connect(self.ui.rba,QtCore.SIGNAL("toggled(bool)"),self.ver_abas_padrao)
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
        tb = self._addToolButton(QtGui.QIcon('icons/open.png'),self.abrirProjeto,'Abrir Projeto')  
        tb = self._addToolButton(QtGui.QIcon('icons/save.png'),self.salvarPro,'Salvar Projeto')  
        tb = self._addToolButton(QtGui.QIcon('icons/close.png'),self.fecharProjeto,'Fechar Projeto')  
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
#MElem		
#        manuElem = QtGui.QAction(self.closeIcon, 'Manutenção Tabela de Elementos', self)
#        manuElem.setShortcut('Ctrl+E')
#        manuElem.setStatusTip('Manutenção Tabela de Elementos')
#        self.connect(manuElem, QtCore.SIGNAL('triggered()'), self.manuElem)
		
        novoProj = self.createAction("&Novo...",self.novoProjeto,None,"new","Novo Projeto")
        abrirProj = self.createAction("&Abrir",self.abrirProjeto,None,"open","Abrir Projeto")
        salvarProj = self.createAction("&Salvar",self.salvarPro,None,"save","Salvar o Projeto")
        salvarComoProj = self.createAction("&Salvar Como...",self.salvarComo,None,"save","Salvar o Projeto com novo nome")
#        abrirRecente = self.createAction("Recente",self.abrirRecente,None,"open","Projeto Recente")
        fecharProj = self.createAction("&Fechar",self.fecharProjeto,None,"close","Fechar o Projeto")
        sobreSAANI = self.createAction("&Sobre",self.helpAbout,None,"sobre","Sobre o SAANI")
        
#        novomenubar = self.menuBar()
#        novoAqs = novomenubar.addMenu('&Recentes')
#        novoAqs.addAction(abrirEsp)
#        novoAqs.addAction(fecharEsp)
        
        menubar = self.menuBar()
        mnuArquivo = menubar.addMenu('&Arquivo')
        mnuArquivo.addAction(abrirEsp)
        mnuArquivo.addAction(fecharEsp)
#        mnuArquivo.addAction(manuElem)
        mnuArquivo.addAction(exit)
        mnuProjeto = menubar.addMenu('&Projeto')
        mnuProjeto.addAction(novoProj)
        mnuProjeto.addAction(abrirProj)
        mnuSProjeto = mnuProjeto.addMenu('Recentes')
        mnuProjeto.addAction(salvarProj)
        mnuProjeto.addAction(salvarComoProj)
#        mnuProjeto.addAction(abrirRecente)
#        mnuProjeto.addAction(novomenubar)
        mnuProjeto.addAction(fecharProj)

        # recupera variavel de ambiente recentefiles
        self.settings = QtCore.QSettings()
        self.recenteFiles=[]
        recenteFiles = self.settings.value("RecenteFiles").toList()
        mnuProjeto.addSeparator()
        for arq in recenteFiles[:]:
            self.recenteFiles+=[arq.toString()]
            aq1 = self.createAction(arq.toString(),self.abreRecente,False,"open","aq1 recente",None,"triggered()")
            self.ultimo=aq1
            mnuSProjeto.addAction(aq1)
        
        mnuSobre = menubar.addMenu('&Help')
        mnuSobre.addAction(sobreSAANI)

        self.dirty = False
##        self.createStatusBar()
        # create progress bar
##        self.pb = QtGui.QProgressBar(self.statusBar())
##        self.statusBar().addPermanentWidget(self.pb)
        # lista de threads 
        self.threads = []
        

        ## barra de statusBar
        #self.sizeLabel = QtGui.QLabel()
        #self.sizeLabel.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        #status = self.statusBar()
        #status.setSizeGripEnabled(False)
        #status.addPermanentWidget(self.sizeLabel)
        #status.showMessage("Ready", 5000)

    
    


#    def manuElem(self):
#        """      """
#        print "teste"
#        a=crtManElementos.crtManElementos()
#        a.exec_loop()
#        Form = QtGui.QWidget()
#        ui = frmElementos.Ui_Form()
#        ui.setupUi(Form)
#        Form.show()	
#        #Form.setWindowModality(QtCore.Qt.WindowModal)		 
#        Form.exec_()


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
        
##\    def updateStatus(self, message,timeout=0):
##        self.statusBar().showMessage(message, timeout)


        ## connections
        #self.connect(self.sw, SIGNAL("okClicked"),
                    #self.rw.create)
        #self.connect(self.rw.table, SIGNAL("progressChanged"),
                     #self.update_progress)
        #self.connect(self.rw.table, SIGNAL("displayFinished"),
                     #self.hide_progress_bar)



##    def update_progress(self, n, nrows):
#        self.pb.show()
#        self.pb.setRange(0, nrows)
#        self.pb.setValue(n)
#        self.statusBar().showMessage(self.tr("Trabalhando..."))
#
#    def hide_progress_bar(self):
#        self.pb.hide()
#        self.statusBar().showMessage(self.tr("Finalizado..."))
#
#    def createStatusBar(self):
#            sb = QtGui.QStatusBar()
#            sb.setFixedHeight(18)
#            self.setStatusBar(sb)
#            self.statusBar().showMessage(self.tr("SAANI pronto!"))
##
    def helpAbout(self):
        QtGui.QMessageBox.about(self, "Sobre o SAANI",
                """<b>Software de An&aacute;lise por Ativa&ccedil;&otilde;o com Neutrons Instrumental</b> v %s
                <p>Copyright &copy; 2008 Grupo de Computa&ccedil;&atilde;o Cient&iacute;fica do IPEN.
                <p>Todos os direitos reservados.
                <p>Autores: S&iacute;lvio Rog&eacute;rio de L&uacute;cia e M&aacute;rio O. de Menezes

                <p>Python %s - Qt %s - PyQt %s on %s""" % (
                __version__, platform.python_version(),
                QtCore.QT_VERSION_STR, qt.PYQT_VERSION_STR, platform.system()))


    def okToContinue(self):
        if self.dirty:
            reply = QtGui.QMessageBox.question(self,
                            "SAANI - Mudanças não salvas",
                            "Salvar mudanças não salvas?",
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

    def abrirProjeto(self):
        """ Menu: Projeto - Abrir Projeto  
         executa rotina para abertura do projeto ja salvo """
        self.abrirProj(1)

    def verificaAbas(self):
        """ Objeto: tabWidget - quadro de abas 
         executa rotina para verificar a movimentaï¿½ï¿½o das abas da janela principal """
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
        self.dataObjectsDict[legend]=''
        self.vlegend=legend
        self.dirty = True
        self.setWindowModified(self.dirty)

    def fecharProjeto(self):
        """ Menu: Projeto - Fechar Projeto 
        serve para fechar um projeto verifica se existe um projeto aberto, se sim executa 
        rotina novoProjeto para limpar as variaveis """
#        self.dirty = True
#        print "Fechar"
#        self.okToContinue()
        if not self.okToContinue():
            return

        if self.projeto == '': 
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Critical)
            msg.setText("Nenhum projeto aberto para ser fechado!")
            msg.exec_()
            return
        self.pprojeto['slope'] = 0
        self.pprojeto['offset']= 0
        self.pprojeto['ro']    = 0
        self.pprojeto['kres']  = 0
        self.pprojeto['ArqCalib']  = ''
        self.ui.lblcalibracao.setText(self.pprojeto['ArqCalib'])
        self.dirty = False
        self.projeto = ''
        self.novoProjeto()
        self.ui.lblProjeto.setText("")   

        

    def novoProjeto(self):
        """Menu: Projeto - Novo Projeto
          limpar as variaveis para abertura ou contruï¿½ï¿½o de um novo projeto"""
        
        if not self.okToContinue():
            return

        self.ui.lstarqs.clear()
        self.dataObjectsDict={}
        " limpar tela do grafico"
        self.graph.clearcurves()        
        curveinfo={}
        " limpar elemntos - dos padroes "
        self.ui.tbElem.clear()
        "limpar tabelas de resultados/concentraï¿½ï¿½o e nome do projeto"
        self.ui.tableWidget.clear()
        self.ui.gAmostra1.clear()
        self.ui.lblProjeto.setText("")   

    def salvarComo(self):
        """Menu: Projeto - Salvar Como
           salva projeto com novo nome, abre janela para entrada do nome do projeto 
           e executa rotina salvarProjeto """
        cwd = os.getcwd()
        olddirt = self.dirty
        outfile = qt.QFileDialog(self)
        outfile.setFilter('*.san')
        outfile.setFileMode(outfile.AnyFile)
        outfile.setAcceptMode(qt.QFileDialog.AcceptSave)
        if os.path.exists(self.configDir):cwd =self.configDir 
        outfile.setDirectory(cwd)
        ret = outfile.exec_()
        if ret:
            filterused = str(outfile.selectedFilter()).split()
            extension = ".san"
            try:
                outdir=str(outfile.selectedFiles()[0])
            except:
                msg = qt.QMessageBox(self)
                msg.setIcon(qt.QMessageBox.Critical)
                msg.setText("Erro nome do arquivo (acentuação!): %s" % (sys.exc_info()[1]))
                msg.exec_()
                return
            try:
                outputDir  = os.path.dirname(outdir)
            except:
                outputDir  = "."
            try:
                outputFile = os.path.basename(outdir)
            except:
                outputFile  = "Projeto1.san"
            outfile.close()
            del outfile
        else:
            outfile.close()
            del outfile
            return
        if len(outputFile) < len(extension[:]):
            outputFile += extension[:]
        elif outputFile[-4:] != extension[:]:
            outputFile += extension[:]
        filename = os.path.join(outputDir, outputFile)
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except IOError:
                msg = qt.QMessageBox(self)
                msg.setIcon(qt.QMessageBox.Critical)
                msg.setText("Erro: %s" % (sys.exc_info()[1]))
                msg.exec_()
                return
        try:
            self.salvarProjeto(filename)
            self.configDir = outputDir
            self.ui.lblProjeto.setText(filename)   
            self.projeto = filename
            self.dirty = False
            self.setWindowTitle("SAANI - %s [*]" % filename)
            self.setWindowModified(self.dirty)
            self.addRecenteFiles(filename)
        except:
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Critical)
            msg.setText("Erro Salvando Projeto: %s" % (sys.exc_info()[1]))
            msg.exec_()
            self.dirty = olddirt
            return

    def salvarPro(self):
        """ menu: Projeto - Salvar
            executa a rotina salvarProjeto com o nome e caminho do projeto corrente(ativo)"""
        if self.projeto == '': 
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Critical)
            msg.setText("Nenhum projeto aberto para ser salvo!")
            msg.exec_()
            return
        self.salvarProjeto(self.projeto)
        
    def salvarRecenteProjeto(self,pfilename):
        """ da rotina: sair
            executa quando clicado no menu sair, grava arquivo: recentes"""
        f = open(pfilename, 'w') # no Windows 
        f.write("%s" %(self.ui.lblProjeto.text()))
        f.close 

    def updateRecenteFiles(self,parqcaminho):
        self.recenteFiles[2]=self.recenteFiles[1] 
        self.recenteFiles[1]=self.recenteFiles[0] 
        self.recenteFiles[0]=parqcaminho 
        
        
    def salvarProjeto(self,pfilename):
        """ da rotina: salvapro
            salva projeto no arquivo e caminho passado no parametro pfilename 
            o arquivo gerado tem extensao .SAN e eh um arq. texto, onde eh gravado todos os dados dos 
            espectros contagens dos canais, nome do arquivo, e os dados adicionais (.info)"""
        f = open(pfilename, 'w') # no Windows 
        self.pprojeto['titulo1']  = str(self.ui.txtdproj1.text())
        self.pprojeto['titulo2']  = str(self.ui.txtdproj2.text())
        f.write("PROJ#%s#\n" %(self.pprojeto))
        n=self.ui.lstarqs.count() 
        for j in range(0,n):
            legend="%s" %(self.ui.lstarqs.item(j).text())
##            self.updateStatus(legend)
##            self.update_progress(j,n)
            f.write("ARQ#%s#\n" %(legend))
            f.write("INFO#%s#\n" %(self.dataObjectsDict[legend].info))
            f.write("Y#%s#\n" %(self.dataObjectsDict[legend].y))
            f.write("FY#\n")
        f.close 
#        self.updateRecenteFiles(pfilename)
##        self.hide_progress_bar()
        self.dirty = False
        self.setWindowTitle("SAANI - %s [*]" % pfilename)
        self.setWindowModified(self.dirty)

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
        self.dirty = True
        self.setWindowModified(self.dirty)
        

    def excElemento(self):
        """ Botao: cmdExcElem - aba parametros 
            Exclui um elemento que foi inserido errado, para efeito de calculo das concentracoes"""                 
        self.ui.tbElem.removeRow(self.ui.tbElem.currentRow())
        
    def clicklst(self):
        """ Objeto: lstarqs -  lista dos arquivos de espectros lancados no projeto
            ao clicar na lista de arquivos, seleciona o arquivo de espectro que deve ser trabalhado 
            exibindo o grafico correspondente """
        legend="%s" %(self.ui.lstarqs.item(self.ui.lstarqs.currentRow()).text())
        self.legend=legend
        if self.ui.tabWidget.currentIndex() == 2:  # se estiver na aba de Resultados, mostra-os
            self.montagrade(legend)
        elif self.ui.tabWidget.currentIndex() == 0: # aba de grafico
            info,x,y = self.lerlegend(legend)
            self.graph.clearcurves()        
            curveinfo={}
            self.graph.newCurve(legend,x,
                                    y,
                                    logfilter=1, curveinfo=curveinfo)
            self.graph.replot()
            self.ui.tabWidget.setCurrentIndex(0)
        
        

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
            linha = qt.QString("%1").arg("Padrï¿½o").rightJustified(15)
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
                       self.painter.drawText(xpgnumber,pageHeight - serifLineHeight,qt.QString("Pï¿½gina %1").arg(page))
                       self.printer.newPage()
                       page += 1
                       y = 2 * serifLineHeight
#                     y = self.printcabecalho(pageRect,fm,LeftMargin,sansFont,sansLineHeight)
        self.painter.drawText(xpgnumber,pageHeight - serifLineHeight,qt.QString("Pï¿½gina %1").arg(page)) 
        self.painter.end()

    def calConcentra(self):
        """ da rotina: ver_abas - que verifica a movimentacao das abas na janela principal
            eh executada quando entra na aba Resultado das Concentracoes e efetua o calculo das concentracoes
            para cada arquivo (espectro) adicionado no projeto e ja identificado como amostra e/ou padrao 
            a rotina identifica cada um dos arquivos e separa entre amostra e padrao 
            se for padrao identifica os elemntos e suas concentracoes para efetuar o calculo
            para cada amostra atraves dos resultados ja calculos das areas dos picos, energias e atividades
            encontra os elementos apontados em cada padrao, efetuando entï¿½o o calculo de cada concentracao 
            para cada padrao em referencia a amostra, por fim exibe os resultados no video em forma de abas e tabelas"""
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
               # colocar o padrï¿½o concentraï¿½ï¿½o em cada emento 
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
# ---- mostra os elementos e as concentraï¿½ï¿½es em cada padrï¿½o        
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
    #                  print 'con----------------------------------------------------------------------------'
    #                  print '%f = (%f * %f * %f * math.exp(%f * %f)) / ( %f * %f) ' %(con, cpsA, massaP, float(pElem[e][pPadrao[p]]["conP"]), lambd,difdt, cpsP, massaA)
                      if (cpsA == 0):
                         errCon=0
                      else:
                        if float(pElem[e][pPadrao[p]]["conP"]) == 0.0 : 
                           errCon= con * math.sqrt((((sA * cpsA) / 100) / cpsA)**2 + (((sP * cpsP) / 100) / cpsP)**2 ) 
                        else:
                           errCon= con * math.sqrt((((sA * cpsA) / 100) / cpsA)**2 + (((sP * cpsP) / 100) / cpsP)**2 + (((float(pElem[e][pPadrao[p]]["conPD"]) / float(pElem[e][pPadrao[p]]["conP"])) ))**2) 
    #                  print '%f = %f * (%f * %f)/100 / %f) + (%f * %f)/100 / %f) + (%f / %f)' %(errCon, con,sA, cpsA, cpsA, sP, cpsP, cpsP, float(pElem[e][pPadrao[p]]["conPD"]), float(pElem[e][pPadrao[p]]["conP"]))
    #                  print 'err----------------------------------------------------------------------------'
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
# dentro da table Widget_2 adiciona a aba jï¿½ com o table
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
              
    def abrirProj(self,recent,arq=""):
        """ da rotina: abrirProjeto do menu Projeto - Abrir Projeto  
            executa rotina para abertura do projeto ja salvo 
            atualiza todas as variaveis, carregando o projeto atraves da leitura do arquivo 
            utiliza o parametro recent para abertura do arquivo mais recente se for o caso """
        vys=''
        if recent==0:
           ret=1
           if (arq==""):
              vfile = self.ui.lblProjeto.text()
           else: 
              vfile = arq
        else:
           cwd = os.getcwd()
           openfile = qt.QFileDialog(self)
           openfile.setFilter('*.san')
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
        if os.path.exists(vfile) and ret == 1:
            if self.projeto == '': 
               self.novoProjeto()
            else:
               self.fecharProjeto()
            fileToOpen = open(vfile)
            initialFile = fileToOpen.readlines()  
            self.projeto=vfile
#            self.ui.setWindowTitle("SAANI - Software de Anï¿½lise por Ativaï¿½ï¿½o Neutronica Instrumental - "+vfile)
            self.ui.lblProjeto.setText(vfile)   
            indlegend=''
            vn=0
            nl = len(initialFile) # numero de linhas para a barra de progresso
            for linha in initialFile:
                vlinha=string.strip(linha)
                vn=vn+1
##                self.update_progress(vn,nl)
                if vlinha[0:3] == 'ARQ':
                   sep=string.split(vlinha,'#')
                   indlegend=string.strip(sep[1])
                   self.ui.lstarqs.addItem(indlegend)
                   output = DataObject.DataObject()
                   output.data=Numeric.zeros([8200])
                   ch0 =  0
                   output.x = [Numeric.arange(ch0, ch0 + len(output.data)).astype(Numeric.Float)]
                   output.y = [output.data[:].astype(Numeric.Float)]
                   self.dataObjectsDict[indlegend]=output
##                   self.updateStatus("%s" % ("Abrindo arquivo: " + indlegend))
                if vlinha[0:4] == 'PROJ':
                   sep=string.split(vlinha,'#')
                   self.pprojeto=eval(sep[1])
                   self.ui.txtdproj1.setText(self.pprojeto['titulo1'])
                   self.ui.txtdproj2.setText(self.pprojeto['titulo2'])
                   self.ui.lblcalibracao.setText(self.pprojeto['ArqCalib'])
                if vlinha[0:4] == 'INFO':
                   sep=string.split(vlinha,'#')
                   self.dataObjectsDict[indlegend].info=eval(sep[1])
                if vlinha[0:1] == 'Y':
                   sep=string.split(vlinha,'#')
                   vys=sep[1]
                else:
                   if vlinha[0:2] == 'FY':
                      vys="Numeric."+vys[1:len(vys)-2]
                      vt=eval(vys)
                      li={}
                      self.dataObjectsDict[indlegend].y[0]=eval(vys)
                      self.dataObjectsDict[indlegend].x[0]= Numeric.arange(0, len(self.dataObjectsDict[indlegend].y[0])).astype(Numeric.Float)
                   else:
                      vys=vys+string.strip(vlinha)
            
            # acho tb que devemos mudar a estrutura do arquivo de projeto.
            # guardar os espectros dentro dele nao eh uma boa ideia - me parece!
            # aqui deve vir a chamada para fazer o calculo em background
            # vou chamar uma funcao/classe fazCalculos que recebera a lista de arquivos de
            # espectro e calculara um por um
            
            self.setWindowTitle("SAANI - %s [*] " % self.projeto)
            
##            self.hide_progress_bar()
            
            fc = fazCalculos(self.ui.lstarqs)
            self.threads.append(fc)
            fc.start()
            self.addRecenteFiles(vfile)
            self.ui.lstarqs.setCurrentRow(0) 
            self.clicklst()
            legend = self.graph.getactivecurve(justlegend = 1)
            self.vlegend=legend

    def lerCalibracao(self):
        """ Botao: cmdcalibracao - aba Projeto 
            abre janela para localizar arquivo de calibracao do sistema (equipamento que efetuou a contagem)                 
            efetua a leitura e armazena os dados na variavel self.pprojeto, para posterior uso no calculo                 
            das areas dos picos, energias e atividades """                 
        cwd = os.getcwd()
        openfile = qt.QFileDialog(self)
        openfile.setFilter('*.cal')
        openfile.setFileMode(openfile.ExistingFile)
        openfile.setAcceptMode(qt.QFileDialog.AcceptOpen)
        print "diretorios "
        print cwd
        print self.configDir
		
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
            initialFile = [string.split(line) for line in fileToOpen]
            self.pprojeto['slope'] = float(initialFile[0][1])
            self.pprojeto['offset']= float(initialFile[0][2])
            self.pprojeto['ro']    = float(initialFile[1][0])
            self.pprojeto['kres']  = float(initialFile[1][1])
            self.pprojeto['ArqCalib']  = "%s" %(vfile)
            self.ui.lblcalibracao.setText(self.pprojeto['ArqCalib'])
            self.dirty = True
            self.setWindowModified(self.dirty)
            self.projeto='Projeto1.san'
            return 0
        else:
            raise "IOError",("Arquivo nï¿½o existe %s " % vfile)
            self.pprojeto['slope'] = 0
            self.pprojeto['offset']= 0
            self.pprojeto['ro']    = 0
            self.pprojeto['kres']  = 0
            self.pprojeto['ArqCalib']  = ''
            self.ui.lblcalibracao.setText(self.pprojeto['ArqCalib'])
            return 1 

    def consiste(self): 
        """ da rotina: ver_abas - que verifica a movimentaï¿½ï¿½o das abas 
            quando entra na aba - Resultado de Concentracoes executa esta rotrina para consistencia dos dados
            verificando se o arquivo de calibraï¿½ï¿½o do Arquivo ja foi lido, se esta Faltando a Massa do Arquivo 
            de espectro para o calculo, se existe Elemesntos lancados para o Padrï¿½o, se tem os arquivos de  
            amostra e padrao para os calculos 
            retorna 1 se deu erro 
            retorna 0 se OK """
        smsg=""
        padrao=0
        amostra=0 
        n=self.ui.lstarqs.count() 
        for j in range(0,n):
            legend="%s" %(self.ui.lstarqs.item(j).text())
            if (self.dataObjectsDict[legend].info['ArqCalib']  == ''): 
               smsg = "Entrar com o arquivo de calibraï¿½ï¿½o do Arquivo: %s" %(legend)
               return 1,smsg
            if (self.dataObjectsDict[legend].info['Massa']==""):
               smsg = "Falta a Massa do Arquivo: %s" %(legend)
               return 1,smsg
            if (self.dataObjectsDict[legend].info['Amostra'] == 2):
               if self.dataObjectsDict[legend].info['lElem'] == '':         
                  smsg = "Elementos do Padrao, Arquivo: %s" %(legend)
                  return 1,smsg
               padrao=1   
            if (self.dataObjectsDict[legend].info['Amostra'] == 1):
               amostra=1
        if (amostra==1) and (padrao==1):
           return 0,smsg    
        else:
           smsg = "No minimo temos que ter uma amostra e um padrï¿½o para o cï¿½lculo das concentraï¿½ï¿½es"
           return 1,smsg        

    def ver_abas_padrao(self):
        """ Objeto: rba - botao de opcao (amostra ou padrao) da aba de parametros 
           Se for padrao deixa visivel a entrada dos dados da Concentraï¿½ï¿½o dos Elementos no Padrï¿½o         
           Se for amostra deixa invisivel esta entrada"""
        if self.ui.rba.isChecked():
            self.ui.groupBox.setVisible(0)
        else:
            self.ui.groupBox.setVisible(1)

    def ver_abas(self):
        """ da rotina: verifcaAbas do Objeto: tabWidget - quadro de abas 
            verificar a movimentaï¿½ï¿½o das abas da janela principal e excuta procedimentos especificos para cada uma delas 
            self.ui.tabWidget.currentIndex() == 
             0:Grafico - nao executa nada
             1:Parametros - recupera os dados da variavel global e exibe na janela
             2:Resultado de Calculos  - executa a rotina vispectFit para os calculos 
             3:Resultado das Concentracoes - executa a rotina calConcentra para os calculos 
             4:Projeto - guarda na variavel saiuAba o valor 4 para efetuar consistencias
            variavel self.saiuAba = 
             4: indica que saiu da aba Projetos entao efetua consistencias: se deu entrada dos
               dados de calibracao e se ja salvou o projeto 
             1: indica que saiu da aba Parametros entao identifica se eh amostra ou padrao  
               aguarda os dados (parametros) na variavel de global para o arquivo (espectro)"""
        if self.saiuAba == 4:
           if self.pprojeto['ArqCalib'] == '': 
              msg = qt.QMessageBox(self)
              msg.setIcon(qt.QMessageBox.Critical)
              msg.setText("Sem arquivo de calibraï¿½ï¿½o, nï¿½o pode calcular!")
              msg.exec_()
              self.saiuAba = 0
              self.ui.tabWidget.setCurrentIndex(4)
              return
           self.pprojeto['titulo1']  = str(self.ui.txtdproj1.text())
           self.pprojeto['titulo2']  = str(self.ui.txtdproj2.text())
           self.saiuAba = 0
#           if self.projeto == '': 
#              self.salvarComo()

        if self.saiuAba == 1:
         try:
           if (self.projeto == ''): 
              msg = qt.QMessageBox(self)
              msg.setIcon(qt.QMessageBox.Critical)
              msg.setText("Nenhum projeto aberto!")
              msg.exec_()
              self.ui.tabWidget.setCurrentIndex(4)
              return
           legend = self.graph.getactivecurve(justlegend = 1)
           if self.ui.rba.isChecked():
              self.dataObjectsDict[self.vlegend].info['Amostra']=1
              self.dataObjectsDict[self.vlegend].info['lElem']=''
           else: 
              if self.ui.rbp.isChecked():
                 self.dataObjectsDict[self.vlegend].info['Amostra']=2
                 n=self.ui.tbElem.rowCount()
                 lElem={}
                 for j in range(0,n):
                    linha={}
                    linha['elemento']=str(self.ui.tbElem.item(j, 0).text())
                    linha['energia']=str(self.ui.tbElem.item(j, 1).text())
                    linha['meiavida']=str(self.ui.tbElem.item(j, 2).text())
                    linha['concentra']=str(self.ui.tbElem.item(j, 3).text())
                    linha['concentradesv']=str(self.ui.tbElem.item(j, 4).text())
                    lElem[j]=linha 
                 self.dataObjectsDict[self.vlegend].info['lElem']=lElem
              else:
                 print "erro selecione tipo amostra ou padrï¿½o"
           #print self.dataObjectsDict[self.vlegend].info['TempoVivo']
           self.dataObjectsDict[self.vlegend].info['TempoVivo']=float(self.ui.lblvivo.text())
           self.dataObjectsDict[self.vlegend].info['TempoTotal']=float(self.ui.lblmorto.text())
           self.dataObjectsDict[self.vlegend].info['DataTempo']=("%s" %(self.ui.txtdatah.text()))
           #print self.vlegend
           #print self.dataObjectsDict[self.vlegend].info['TempoVivo']
           #print "ddddddddddd            abas    ddddddddddddddd"
#           print self.dataObjectsDict[self.vlegend].info['DataTempo']
           if self.dataObjectsDict[self.vlegend].info['Massa'] <> str(self.ui.txtmassa.text()):
              self.dataObjectsDict[self.vlegend].info['Massa']=str(self.ui.txtmassa.text())
              self.dirty = True
           calcula=True
           if self.dataObjectsDict[self.vlegend].info['Nivel']==str(self.ui.txtnivel.text()): 
              if self.dataObjectsDict[self.vlegend].info['Sigma']==str(self.ui.txtsigma.text()):
                 calcula=False 
           self.dataObjectsDict[self.vlegend].info['Nivel']=str(self.ui.txtnivel.text())
           self.dataObjectsDict[self.vlegend].info['Sigma']=str(self.ui.txtsigma.text())
           self.saiuAba = 0
           if calcula: 
        # ao ler um arquivo de espectro individual, tb faz o calculo em background
              fc = fazCalculos(self.ui.lstarqs,self.ui.lstarqs.currentRow())
#        fc = fazCalculos(self.ui.lstarqs)
              self.threads.append(fc)
              fc.start()
              self.dirty = True
              self.setWindowModified(self.dirty)
         except:
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Critical)
            msg.setText("Calculo ainda em processo: %s" % (sys.exc_info()[1]))
            msg.exec_()
            self.saiuAba = 0
            self.ui.tabWidget.setCurrentIndex(0)
            return
              
# aba - Grafico 
        if self.ui.tabWidget.currentIndex() == 0:
            if (self.projeto == ''): 
              msg = qt.QMessageBox(self)
              msg.setIcon(qt.QMessageBox.Critical)
              msg.setText("Nenhum projeto aberto!")
              msg.exec_()
              self.ui.tabWidget.setCurrentIndex(4)
              return
            legend="%s" %(self.ui.lstarqs.item(self.ui.lstarqs.currentRow()).text())
            info,x,y = self.lerlegend(legend)
            self.graph.clearcurves()        
            curveinfo={}
            self.graph.newCurve(legend,x,
                                    y,
                                    logfilter=1, curveinfo=curveinfo)
            self.graph.replot()
            self.ui.tabWidget.setCurrentIndex(0)
# aba - Parametros
        elif self.ui.tabWidget.currentIndex() == 1:
           if (self.projeto == ''): 
              msg = qt.QMessageBox(self)
              msg.setIcon(qt.QMessageBox.Critical)
              msg.setText("Nenhum projeto aberto para ser fechado!")
              msg.exec_()
              self.ui.tabWidget.setCurrentIndex(4)
              return
           self.saiuAba = 1 
           legend="%s" %(self.ui.lstarqs.item(self.ui.lstarqs.currentRow()).text())
           #legend = self.graph.getactivecurve(justlegend = 1)
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
#           print "aux22"
#           print aux22
           aux=QtCore.QString(aux22)
#           print aux
#           print type(aux)
           now2 = QtCore.QDateTime.fromString(aux22, QtCore.QString("dd/MM/yyyy hh:mm:ss"))
#           print now2
#           print type(now2)
           self.ui.txtdatah.setDateTime(now2)
           self.ui.txtmassa.setText(str(info['Massa']))
           self.ui.txtnivel.setText(str(info['Nivel']))
           self.ui.txtsigma.setText(str(info['Sigma']))
#           self.ui.txtdatah.text()self.dataObjectsDict[self.vlegend].info['DataTempo']=("%s" %(self.ui.txtdatah.text()))
           
           if self.dataObjectsDict[legend].info['Amostra']==1:
              self.ui.rba.setChecked(True)
              self.ui.rbp.setChecked(False)
           else:
              self.ui.rba.setChecked(False)
              self.ui.rbp.setChecked(True)
              if len(self.dataObjectsDict[legend].info['lElem'])==0:
                 #print "clearclearclearclear"
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
           #if (self.dataObjectsDict[self.vlegend].info['ArqCalib']  == ''): 
               #msg = qt.QMessageBox(self)
               #msg.setIcon(qt.QMessageBox.Critical)
               #msg.setText("Sem arquivo de calibraï¿½ï¿½o, nï¿½o pode calcular!")
               #if qt.qVersion() < '4.0.0':
                  #msg.exec_loop()
               #else:
                  #msg.exec_()
               #return
           if (self.projeto == ''): 
              msg = qt.QMessageBox(self)
              msg.setIcon(qt.QMessageBox.Critical)
              msg.setText("Nenhum projeto aberto para ser fechado!")
              msg.exec_()
              self.ui.tabWidget.setCurrentIndex(4)
              return
           legend="%s" %(self.ui.lstarqs.item(self.ui.lstarqs.currentRow()).text())
           #legend = self.graph.getactivecurve(justlegend = 1)
           
           self.montagrade(legend) 
           #self.vispectFit()
# ------ aba - Resultado das Concentracoes
        elif self.ui.tabWidget.currentIndex() == 3:
           if (self.projeto == ''): 
              msg = qt.QMessageBox(self)
              msg.setIcon(qt.QMessageBox.Critical)
              msg.setText("Nenhum projeto aberto!")
              msg.exec_()
              self.ui.tabWidget.setCurrentIndex(4)
              return
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
# ------ aba -Projeto
        elif self.ui.tabWidget.currentIndex() == 4:
           self.saiuAba=self.ui.tabWidget.currentIndex()

    def imprimeResultados(self):
        """ Botao: cmdImpRes - da aba Resultado dos Calculos 
           imprime os resultados dos calculos, energia, BG , etc..."""                 
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
                self.painter.drawText(xpgnumber,pageHeight - serifLineHeight,qt.QString("Pï¿½gina %1").arg(page))
                self.printer.newPage()
                page += 1
                y = self.printcabecalho(pageRect,fm,LeftMargin,sansFont,sansLineHeight)
        self.painter.drawText(xpgnumber,pageHeight - serifLineHeight,qt.QString("Pï¿½gina %1").arg(page)) 
        self.painter.end()
        
    def printcabecalho(self,pageRect,fm,LeftMargin,sansFont,sansLineHeight):
        """ da rotina: imprimeResultados do Botao: cmdImpRes - da aba Resultado dos Calculos 
            imprime o cabecalho do relatorio energia, BG , etc..."""                 
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
        linha = 'Tempo Vivo : %s seg.   Nï¿½vel sensibilidade: %s  ' % (self.dataObjectsDict[self.legend].info['TempoVivo'],self.dataObjectsDict[self.legend].info['Nivel'])
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
        """   Vai executar rotina para localizaï¿½ï¿½o dos picos e o cï¿½lculo das energias, area do pico , etc...  
            1. Recupera a legenda do grafico, que ï¿½ o nome do arquivo
            2. Atravï¿½s da legenda executa rotina lerlegend()  que retona parametros, os canais e conmtagens
            3. Apï¿½s executa a rotina da classe vispectfit para efetuar a localizaï¿½ï¿½o dos picos e calculos """

        if legend == None:
            legend = self.graph.getactivecurve(justlegend = 1)
        #print type(legend),legend
        #legend2 = self.graph.getactivecurve(justlegend = 1)
        #print type(legend2),legend2
        vvl=legend
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
#silvio mostra valores de canais para entendimento
#        print "ajustennnnnnnnnnnnnnnnnnnnnnnnnnnn"
#        print legend
#        print info
#        print x
#        print y 
#        file=open("c:testy",'w')
#        for j in range(0,8000):
#            file.write("%d;%d\n" %(j,y[j]))
#        file.close
#        file=0       
#        self.simplefit.show()
        if info is not None:
            xmin,xmax=self.graph.getx1axislimits()
            self.vispectfit.Lt = info['TempoVivo']
#            print info['TempoVivo']
            self.vispectfit.vy=Numeric.array(y,Numeric.Float64)
##            self.updateStatus("%s" % ("Calculando espectro: " + legend))
            ppdic={}
            ppdic=self.vispectfit.vispectfit(xmin=xmin,xmax=xmax,vlegend=info).copy()
#            print legend
#            print vvl
#            print "ANTESpdicrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr" 
#            print pdic 
#            if legend <> 'M2022I3.MCA':
#               Alegend='M2022I3.MCA'
#               print self.dataObjectsDict[Alegend].info['ResCalculo'][0]
#            print "pdicrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr" 

            self.dataObjectsDict[legend].info['ResCalculo']=ppdic
            n=len(ppdic)
            self.nlinhas=n
 #           self.ui.tableWidget.clear()
#            te=self.ui.tableWidget.rowCount()
#            print "te %d n=%d" % (te,n) 
#            for e in range(0,te):
#                print "passou %d" % e 
#                self.ui.tableWidget.removeRow(0)
            #VispectFuncs.criarGrade(self.ui.tableWidget, n,12,{})
            #VispectFuncs.cabecGradeRes(self.ui.tableWidget)
            #for i in range(0,n):
               #VispectFuncs.incGrade(self.ui.tableWidget,i,ppdic[i])
            #self.ui.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)   
#            legend='M2022I3.MCA'
 #           print self.dataObjectsDict[legend].info['ResCalculo'][0]
#            legend='OT031I3.MCA'
#            print self.dataObjectsDict[legend].info['ResCalculo'][0]
#            print self.dataObjectsDict

            return
        else:
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Critical)
            msg.setText("Erro nï¿½o pode ajustar?")
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
        self.ui.tabWidget.insertTab(0,self.graph,"Gráfico")
        self.ui.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.ui.tabWidget,QtCore.SIGNAL("currentChanged(int)"),self.verificaAbas)
        QtCore.QObject.connect(self.cmdimpgraf, QtCore.SIGNAL("clicked()"), self.imprimeGrafico)
# posiciona aba
        self.ui.tabWidget.setCurrentIndex(4)


    def lerlegend(self,legend,full=0):
# Recupera do dicionario dataObjectsDict, atravï¿½s da legenda os dados do espectro e retorna os valores    
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
        
        
    def vispectLer(self):
# Efetua a leitura do arquivo de espectro e apresenta o grafico na tela
# 1. Abre janela para localizar o arquivo
# 2. Executa a rotina ler_MCAeCHN, passando como parametro o arquivo
# 3. Recebe os dados do arquivo em um DataObject 
# 4. Guarda os dados em um dicionario dataObjectsDict, com o nome do arquivo
# 5. Exibe grafico no video do arquivo que foi aberto
#        filetypes = ""
#        wdir = ":"
#        lastFileFilter = "*.MCA ; *.CHN"
       
#        filelist = qt.QFileDialog.getOpenFileNames(self,
#                            "Abrir Arquivo",          wdir,
#                             filetypes,
#                            lastFileFilter)
#        filelist.sort()
#        filename=[]
#        for f in filelist:
#            filename.append(str(f))
#        if not len(filename):    return
#        if len(filename):
#            lastInputDir  = os.path.dirname(filename[0])
#            justloaded = True
#        if justloaded:
#            if type(filename) != type([]):
#                filename = [filename]
#        if not os.path.exists(filename[0]):
#            raise "IOError",("Arquivo nï¿½o existe %s " % filename[0])
#        n=string.rfind(filename[0],'/')
#        legend=filename[0][n+1:]
#        print "self.projeto['ArqCalib']"
#        print self.pprojeto
        if self.pprojeto['ArqCalib'] == '': 
           msg = qt.QMessageBox(self)
           msg.setIcon(qt.QMessageBox.Critical)
           msg.setText("Sem arquivo de calibração, não pode calcular!")
           msg.exec_()
           return
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
        vdata = vobj.ler_MCAeCHN()
#        print "info = ",vdata.info
#        print "datay = ",vdata.y
#        print "datax = ",vdata.x
        dataObject = vdata
        self.dataObjectsDict[legend] = dataObject
# por enquanto estou atribuindo os valores de calibraï¿½ï¿½o a todos os espectros, mais uma unica vez o usuario entra com o arquivo-(rotina lercalibracao).         
        self.dataObjectsDict[legend].info['slope'] = self.pprojeto['slope']
        self.dataObjectsDict[legend].info['offset']= self.pprojeto['offset']
        self.dataObjectsDict[legend].info['ro']    = self.pprojeto['ro']
        self.dataObjectsDict[legend].info['kres']  = self.pprojeto['kres']
        self.dataObjectsDict[legend].info['ArqCalib']  = self.pprojeto['ArqCalib']

        self.vaux=legend
        self.vlegend=legend
        self.ui.lstarqs.addItem(self.vaux)
        posicao=self.ui.lstarqs.count() - 1
        curveinfo={}
        self.graph.clearcurves()        
        self.graph.newCurve(legend,x=vdata.x[0],
                                   y=vdata.y[0],
                                   logfilter=1, curveinfo=curveinfo)
                                    
        #self.graph.setxofy(legend)
        self.graph.replot()
        
#coloquei saiuAba=0 pois na leitura estava matando valores de Tempo VIVO e MORTO
        self.saiuAba = 0
        self.ui.tabWidget.setCurrentIndex(0)
        
        # ao ler um arquivo de espectro individual, tb faz o calculo em background
        fc = fazCalculos(self.ui.lstarqs,posicao)
#        fc = fazCalculos(self.ui.lstarqs)
        self.threads.append(fc)
        fc.start()
        self.dirty = True
        self.setWindowModified(self.dirty)

    def montagrade(self,legend):
        """rotina para montar a tabela com o resultado dos calculos (busca de picos e energias)
        """
#        for t in self.threads:
#            print "threads" 
#            print t
#            print type(t)
        ppdic={}
        ppdic=self.dataObjectsDict[legend].info['ResCalculo']
        n=len(ppdic)
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
          Recebe uma lista de nomes de arquivos de espectro para calculara"""
#       sem = QtCore.QSemaphore(1)
       
#       def __init__(self,listaarqs, parent=None):
#           super(fazCalculos,self).__init__(parent)
       def __init__(self,listaarqs,posicao=0):
           threading.Thread.__init__(self)
           
           self.listaarqs = listaarqs
           self.posicao   = posicao 
#           fazCalculos.sem.acquire(1)
           
           
       def run(self):
           """faz os calculos dos espectros chamando a vispectfit"""
           if self.posicao == 0:
            for i in range(self.listaarqs.count()):
               arq = "%s" % (self.listaarqs.item(i).text())
               appStart.vispectFit(arq)
               verde = QtGui.QColor("lightgreen")
               self.listaarqs.item(i).setBackgroundColor(verde)
           else: 
               arq = "%s" % (self.listaarqs.item(self.posicao).text())
               appStart.vispectFit(arq)
               verde = QtGui.QColor("lightgreen")
               self.listaarqs.item(self.posicao).setBackgroundColor(verde)
                       
#               self.listaarqs.setCurrentRow(i)
#           fazCalculos.sem.release(1)
#           appStart.updateStatus("Calculos Finalizados.")
           
        
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("IPEN.")
    app.setOrganizationDomain("IPEN.SAANI")
    app.setApplicationName("SAANI")
    appStart = startGui()
    appStart.show()
    sys.exit(app.exec_())
