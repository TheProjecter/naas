# -*- coding: ISO-8859-1 -*-
#
# Ler arquivo do tipo MCA e CHN - IPEN para conversão no sistema PYMCA
#
#

import DataObject
import string
import Numeric
from struct import *

class LerVispect:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.tt=0
        self.tv=0 
        self.dt=""
        self.hora=""
        self.meses={"JAN":"01","FEV":"02","FEB":"02","MAR":"03","ABR":"04","APR":"04","MAI":"05","MAY":"05","JUN":"06","JUL":"07","AGO":"08","AUG":"08","SET":"07","SEP":"07","OUT":"10","OCT":"10","NOV":"11","DEZ":"12","DEC":"12"}
        
    def ler_MCAeCHN(self):
        output = DataObject.DataObject()
        output.info["SourceType"] = "SpecFile"
        output.info["SourceName"] = self.arquivo
        output.info["Key"]        = "1.1.1.1"
        output.info['FileName']   = self.arquivo
        output.info['selectiontype'] = "1D"
        self.tipo = string.upper(self.arquivo[-3:])
        if self.tipo == 'CHN':
            output.data = self.ler_CHN()
        else:
            output.data = self.ler_MCA()
        output.info['TempoTotal']   = self.tt
#        print self.tv
        output.info['TempoVivo']   = self.tv
        if self.dt <>"":
           self.dt = self.dt[0:2]+"/"+self.meses[self.dt[2:5]]+"/20"+self.dt[5:7]+" "+self.hora[0:2]+":"+self.hora[2:4]+":00"             
        output.info['DataTempo']   = self.dt
        output.info['HoraTempo']   = ""
        output.info['Massa']   = ""
        output.info['Nivel']   = "15"
        output.info['Sigma']   = "1"
        output.info['JaElementos']   = 0
        output.info['JaCalculado']   = 0
        output.info['slope'] = 0
        output.info['offset']= 0
        output.info['ro']    = 0
        output.info['kres']  = 0
        output.info['ArqCalib']  = ''
        output.info['Amostra']  = 0
        output.info['ResCalculo']  = 0
        output.info['lElem']  = ''


        ch0 =  0
        output.x = [Numeric.arange(ch0, ch0 + len(output.data)).astype(Numeric.Float)]
        output.y = [output.data[:].astype(Numeric.Float)]
#            output.x = []
#            output.y = []
        output.m = None
        output.data = None
        return output

    def ler_CHN(self):
        fespec=open(self.arquivo,'rb')
        # ler dados do CHN espaços em branco 
        p1=fespec.read(8) 
        # tempo total 
        p2=fespec.read(4)
        # tempo vivo 
        p3=fespec.read(4)
        # data 
        p4=fespec.read(8)
        self.dt=p4
        # hora 
        p5=fespec.read(4)
        self.hora=p5
        # espaços em branco 
        p6=fespec.read(4)
#        print p6
#        print "Parametros do arquivo CHN - sfontes.chn"
#        print p1
        self.tv=float(unpack('l',p3)[0])/50
        self.tt=float(unpack('l',p2)[0])/50
#        print "Tempo Total: %7.1f " % self.tt
#        print "Tempo Vivo : %7.1f " % self.tv
      
#        print p4
#        print unpack('l',p5)[0],
#        print p6,
# ler dados do arquivo CHN só as contagens e grava na saida     
        i=0
        a=Numeric.zeros([8200])
        while i<8191:
            a[i]=unpack('l',fespec.read(4))[0]
            i = i + 1
        fespec.close()
        return a
        
    def ler_MCA(self):
        try:  
         fespec=open(self.arquivo,'rb')
        # espaços em branco 
         p1=fespec.read(32) 
        # branco 2 
         p11=fespec.read(16)
        # tempo total 
         p2=fespec.read(4)
        # tempo vivo 
         p3=fespec.read(4)
        # espacos 
         p4=fespec.read(8)
        # espacos 
         p41=fespec.read(32)
        # espacos 
         p42=fespec.read(32)
        # espacos 
#        print "Parametros do arquivo CHN - sfontes.chn"
         self.tv=float(unpack('l',p2)[0])/100
         self.tt=float(unpack('l',p3)[0])/100
#        print "Tempo Total: %7.1f " % self.tt
#        print "Tempo Vivo : %7.1f " % self.tv
#        print p4
#        print p41
#        print p42
# ler dados do arquivo CHN só as contagens e grava na saida     
         i=0
         a=Numeric.zeros([8200])
         while i<8191:
            a[i]=unpack('l',fespec.read(4))[0]
            i = i + 1
         fespec.close()
         return a
        except:
         msg = qt.QMessageBox(self)
         msg.setIcon(qt.QMessageBox.Critical)
         msg.setText("Erro nome do arquivo (acentuação!): %s" % (sys.exc_info()[1]))
         msg.exec_()
         a=Numeric.zeros([8200])
         return a
        
if __name__ == "__main__":
    import sys,time
    try:
        arquivo=sys.argv[1]
    except:
        print "Chamar por: LerVispect nome-do-arquivo(CHN ou MCA)"
        sys.exit()
    obj = LerVispect(arquivo)
    data = obj.ler_MCAeCHN()
#    print "data = ",data.y
#    print "info = ",data.info
        

        
