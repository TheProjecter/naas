# -*- coding: utf-8 -*-
#
# Ler arquivo do tipo MCA e CHN - IPEN para conversão no sistema PYMCA
#
#

import DataObject
import string
#import Numeric
import numpy as np
from struct import *
import sys

class LerVispect:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.tt=0
        self.tv=0
        self.dt=""
        self.hora=""
        self.meses={"JAN":"01","FEV":"02","FEB":"02","MAR":"03","ABR":"04","APR":"04","MAI":"05","MAY":"05","JUN":"06","JUL":"07","AGO":"08","AUG":"08","SET":"07","SEP":"07","OUT":"10","OCT":"10","NOV":"11","DEZ":"12","DEC":"12"}
        print self.arquivo
        sys.stdout.flush()

    def ler_MCAeCHN(self):
        """this function is deprecated; replace all the call by the new function ler_arquivo()"""
        return self.ler_arquivo()

    def ler_arquivo(self):
        """read a spectrum file and create a DataObject to hold its data"""
        output = DataObject.DataObject()
        output.info["SourceType"] = "SpecFile"
        output.info["SourceName"] = self.arquivo
        output.info["Key"]        = "1.1.1.1"
        output.info['FileName']   = self.arquivo
        output.info['selectiontype'] = "1D"
        self.tipo = string.upper(self.arquivo[-3:])
        # EG&ORTEC file
        if self.tipo == 'CHN':
            output.data = self.ler_CHN()
        # Canberra S100 file MCA
        elif self.tipo == 'MCA':
            output.data = self.ler_MCA()
        # ASC file from IAEA Intercomparison program
        elif self.tipo == 'ASC':
            output.data = self.ler_ASC()
            
        
        #if output.data == None or len(output.data) == 0:
          #  print (output.data == None), len(output.data)
           # return None
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
        output.info['enerquad']=0
        output.info['ro']    = 0
        output.info['kres']  = 0
        output.info['widthquad'] = 0
        output.info['ArqCalib']  = ''
        output.info['Amostra']  = 0
        output.info['ResCalculo']  = 0
        output.info['lElem']  = ''
        output.info['NumCanais']=self.canais


        ch0 =  0
        output.x = [np.arange(ch0, ch0 + len(output.data)).astype(np.float)]
        output.y = [output.data[:].astype(np.float)]
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
        print self.dt
       
        # hora
        p5=fespec.read(4)
        self.hora=p5
        print self.hora
        sys.stdout.flush()
        # espaços em branco
        p6=fespec.read(4)
#        print calcsize(p6)
  #      sys.stdout.flush()
        p6u = unpack('=l',p6)[0]
        # numero de canais (pega 16 bits i.e., 2 bytes)
        self.canais = p6u >> 16
#        print self.canais
#        print "Parametros do arquivo CHN - sfontes.chn"
#        print p1
        self.tv=float(unpack('=l',p3)[0])/50
        self.tt=float(unpack('=l',p2)[0])/50
#        print "Tempo Total: %7.1f " % self.tt
#        print "Tempo Vivo : %7.1f " % self.tv

#        print p4
#        print unpack('l',p5)[0],
#        print p6,
# ler dados do arquivo CHN só as contagens e grava na saida
        i=0
        a=np.zeros([self.canais])
        while i<self.canais:
            a[i]=unpack('=l',fespec.read(4))[0]
            i = i + 1
        fespec.close()
#        print a[1:10]
        return a

    def ler_MCA(self):
        try:
         fespec=open(self.arquivo,'rb')
         # vendo o codigo do ConvertCAM do HypermetPC descobri mais informacoes sobre o formato do MCA.
         # readtype (integer in Visual Basic 6.0 - 16 bits, i.e., 2 bytes)
         p1a = fespec.read(2)
         
         # mcanumber (integer in VisualBasic)
         p1b = fespec.read(2)
         
         # readregion (integer in VisualBasic)
         p1c = fespec.read(2)
         
         # tagno (long in Visual Basic 6.0 - 32 bits, i.e., 4 bytes)
         p1d = fespec.read(4)
         
         # spectrname (classe string * 26 - supondo 26 bytes de armazenamento)
         p1e = fespec.read(26)
         
         # acqumode (integer in VisualBasic)
         p1f = fespec.read(2)
         
         # time (long in VB)
         p1g = fespec.read(4)
         
         # millitm (integer in VB)
         p1h = fespec.read(2)
         
         # timezone (integer in VB)
         p1i = fespec.read(2)
         
         # dstflag (integer in VB)
         p1j = fespec.read(2)
         
         print "readtype: ",  unpack('=h', p1a)
         print "mcanumber: ",  unpack("=h", p1b)
         print "readregion: ",  unpack("=h", p1c)
         print "tagno: ",  unpack("=l",  p1d)
         print "spectrname: ",  unpack('26s', p1e)
         print "acqumode: ",  unpack('=h', p1f)
         print "time: ",  unpack('=l', p1g)
         print "millitm: ",  unpack('=h',  p1h)
         print "timezone: ",  unpack('=h',  p1i)
         print "dstflag: ",  unpack('=h', p1j)
# espaços em branco
#         p1=fespec.read(32)
        # branco 2
 #        p11=fespec.read(16)
        # tempo total
         p2=fespec.read(4)
        # tempo vivo
         p3=fespec.read(4)
         print unpack('=l', p3)
        # espacos
         p4=fespec.read(8)
        # espacos
         p41=fespec.read(32)
        # espacos
         p42=fespec.read(28)
        # num. de canais
         p5 = fespec.read(4)
         p5u = unpack('=l',p5)[0]
        # numero de canais (pega 16 bits i.e., 2 bytes)
         self.canais = p5u >> 16
#        print "Parametros do arquivo CHN - sfontes.chn"
         self.tv=float(unpack('=l',p2)[0])/100
         self.tt=float(unpack('=l',p3)[0])/100
#        print "Tempo Total: %7.1f " % self.tt
#        print "Tempo Vivo : %7.1f " % self.tv
#        print p4
#        print p41
#        print p42
# ler dados do arquivo CHN só as contagens e grava na saida
         i=0
         a=np.zeros([self.canais])
         while i < self.canais:
            a[i]=unpack('=l',fespec.read(4))[0]
            i = i + 1
         fespec.close()
         return a
        except:
            return []

    def ler_ASC(self):
        try:
            fespec=open(self.arquivo,'r')
            linhas = fespec.readlines()
            fespec.close()
            # tempo total
            p1 = float(linhas[0])
            # tempo vivo
            p2 = float(linhas[1])
            self.tt=p1
            self.tv=p2
            self.canais = 8191
            a = [int(x) for x in linhas[2:]]
            return np.asarray(a,dtype=int)
#            i = 0
#            a = np.zeros([self.canais])
#            print "p1, p2, type(a)",p1, p2, type(a)
#            while i < self.canais:
#                a[i] = int(linhas[2+i])
#                i += 1
        except:
            print "nao consegui abrir arquivo", self.arquivo
            return []
            
    

if __name__ == "__main__":
    import sys,time
    try:
        arquivo=sys.argv[1]
    except:
        print "Chamar por: LerVispect nome-do-arquivo(CHN ou MCA) nome-do-arquivo.dat"
        sys.exit()
    obj = LerVispect(arquivo)
    data = obj.ler_MCAeCHN()
    try:
       f = open(sys.argv[2],'w')
       #print "datax =", data.x
       print len(data.x[0]), len(data.y[0])
       for i in range(len(data.x[0])):
           f.write("%d\t%d\n" % (data.x[0][i],data.y[0][i]))
       f.flush()
       f.close()
       print "espectro gravado em ",sys.argv[2]
    except:
       print "erro abrindo arquivo ",sys.argv[2]
#    print "data = ",data.y
#    print "info = ",data.info



