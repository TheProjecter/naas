# -*- coding: utf-8 -*-

import Numeric
import crtConcentracao
import Elementos
import QtBlissGraph
qt = QtBlissGraph.qt
import os
import sys, string


class VispectFit:
    def __init__(self):
        self.dataObjectsDict = {}
        self.Isommet=Numeric.zeros([200], Numeric.Int)
        self.VisTable = crtConcentracao.startGui()
        self.Vispectdic={}
        self.vinfo={}
        #self.Elementos=Elementos.Elementos('elementos')
        self.A1 = None
        self.B1 = None
        self.Absi = None
        self.NoPic = None
        self.Aire = None
        self.Bgnd = None
        self.Resol=None
        self.Id=None
        self.Fi=None
        self.Erreur=None
        self.Lt=None
        self.sig=None
        self.ideb=None
        self.ifin=None
        self.moyamont = None
        self.moyaval = None
        self.Y1 = None
        self.Y2 = None
        self.ro=None
        self.kres=None
        self.slope=None
        self.offset=None
        self.f1zfin=None
        self.f1zdeb=None
        self.vy=Numeric.array([],Numeric.Float64)


#silvio rotinas de ajustes vispect


    def vispectfit(self,xmin,xmax,vlegend):
# ler calibracao arquivo .cal
#        if self.lerCalibracao():
#            print "erro: Leitura de Calibracao"
#            msg = qt.QMessageBox(self)
#            msg.setIcon(qt.QMessageBox.Critical)
#            msg.setText("Ler calibracao antes de processar!")
#            msg.exec_loop()
#            return
#        self.ro=0.85465008020401
#        self.ro=0.7478398680686951
#        self.ro=0.6709876656532288
#        self.ro=0.6244149804115295
#        self.ro=0.6709876656532288
#        self.kres=3.798957169055939e-002
#        self.kres=4.1902806609869e-002
#        self.kres=4.159772396087646E-002
#        self.kres=4.956839978694916E-002
#        self.kres=4.159772396087646E-002
#        self.slope=0.2497552037239075
#        self.slope=0.2231738120317459
#        self.slope=0.2449169903993607
#        self.slope=0.2489991188049316
#        self.slope=0.2449169903993607
#        self.offset=-0.8149404525756836
#        self.offset=-1.084661960601807
#        self.offset=0.3638114035129547
#        self.offset=5.074393272399902
#        self.offset=0.3638114035129547
# lt: o tempo vivo
        #        self.Lt = 180000.0/50
#quando da leitura do arquivo le o tempo Vivo e Morto
#       self.Lt = 7200
#        self.Lt = 3597.633136
#        if calon <> 2:
# ler nivel de procura = 15
#        print 'aaaalegend'
#        print vlegend
        self.Vispectdic={}
        self.vinfo = vlegend
# recupera dados de calibracao
        self.slope=self.vinfo['slope']
        self.offset=self.vinfo['offset']
        self.ro=self.vinfo['ro']
        self.kres=self.vinfo['kres']

        nivel=int(self.vinfo['Nivel'])
        barre=int(self.vinfo['Nivel'])
        self.sig = int(self.vinfo['Sigma'])

        #self.ifin=xmax-600
        #if self.ifin > 8100:
        self.ifin = 8191
        vfim=int(self.ifin)
        self.ideb=0
        sauveideb=self.ideb
        self.ideb=40
        oldfi=0
        #print xmax
        #???? verificar o fim para loop
        #print vfim

        for j in range(self.ideb,vfim):
            #print j
            self.vy[j] = self.fcanal(j,4,0)
            self.vy[j] = self.fcanal(j,4,1)
        rescorrel = self.ro*(1+self.kres*Numeric.sqrt(float(self.ideb+self.ifin)/2*self.slope+self.offset))
        nccorrel = int(round(float(rescorrel)/self.slope)) - 2
        if nccorrel <= 0: nccorrel = 1
        i = self.ideb+nccorrel*2
#        contenucentre = 0.0
        contenucentre = 0
        self.f1zdeb = 0
        self.f1zfin = 0
#        for j in range(i,i+nccorrel-1):
        for j in range(i,i+nccorrel):
            contenucentre = contenucentre+Numeric.sqrt(self.fcanal(j,2,0))
#        contenuailes = 0.0
        contenuailes = 0
#        for j in range(self.ideb,self.ideb+(nccorrel*5-1)):
        for j in range(self.ideb,self.ideb+(nccorrel*5)):
            contenuailes = contenuailes + Numeric.sqrt(self.fcanal(j,2,0))
        somcorrel = 0
        ipic = 0
        oldcanalcorrel = 0
        kcan = int(i + float(nccorrel)/2) - 1
#silvio mostra valores de canais para entendimento
#        file=open("c:param.txt",'w')
        #for j in range(0,8190):
        rescorrel = self.ro*(1+self.kres*Numeric.sqrt(float(self.ideb+self.ifin)/2*self.slope+self.offset))
        nccorrel = int(round(float(rescorrel)/self.slope)) - 2
 #       file.write("barre %f\n" %(barre))
 #       file.write("ro %f\n" %(self.ro))
 #       file.write("kres %f\n" %(self.kres))
 #       file.write("ideb %f\n" %(self.ideb))
 #       file.write("ifin %f\n" %(self.ifin))
 #       file.write("slope %f\n" %(self.slope))
 #       file.write("offset %f\n" %(self.offset))
 #       file.write("rescorrel %f\n" %(rescorrel))
 #       file.write("nccorrel %f\n" %(nccorrel))
 #       file.write("contenuailes %f\n" %(contenuailes))
 #       file.write("contenucentre %f\n" %(contenucentre))
 #       file.close
 #       file=0
        #print contenuailes
        #print contenucentre
#Correlator da iniciacao para optimize a velocidade
#'do calculo do spectrum (correlates reduzidos do Nb. raizes dos cross-sections)
#        for j in range(i,int(self.ifin - nccorrel*3)+1):
 #       file=open("c:correl.txt",'w')
 #       file.write("contenuailes;contenucentre;canalcorrel\n")
        canalcorrel=0
        for j in range(i,int(self.ifin - nccorrel*3)+1):
            kcan = kcan +1
#            print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
#            print contenuailes
#            print j
#            print nccorrel
#            print contenuailes
#            print contenucentre
#            print canalcorrel
#            print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
#            if j > 60:
#               return
            contenuailes = contenuailes - Numeric.sqrt((self.fcanal(j-nccorrel*2,2,0))) + Numeric.sqrt((self.fcanal(j+nccorrel*3,2,0)))
            contenucentre = contenucentre - Numeric.sqrt((self.fcanal(j,2,0))) + Numeric.sqrt((self.fcanal(j+nccorrel,2,0)))
            canalcorrel = contenucentre*5-contenuailes
 #           file.write("%f;%f;%f;%f;%f;%f\n" %(kcan,j,self.fcanal(j,2,0),contenuailes,contenucentre,canalcorrel))
            if canalcorrel > barre and self.f1zdeb == 0:
                self.fnzondeb(kcan,nccorrel)
            if self.f1zdeb == 1:
                somcorrel = somcorrel + canalcorrel
#silvio ver comparacao de interiro e float
            if (self.f1zdeb == 1) and (canalcorrel > oldcanalcorrel) :
                self.vy[kcan-1] = self.fcanal(kcan-1,4,1)
                self.vy[kcan] = self.fcanal(kcan,3,1)
            if canalcorrel < barre and self.f1zfin == 0 and self.f1zdeb == 1:
                self.fnzonfin(kcan,nccorrel)
            if self.f1zdeb == 1 and self.f1zfin == 1 :
#                for il in range(self.Id,self.Fi):
#                print "inicio = %d Fim = %d " %(self.Id,self.Fi)
                for il in range(self.Id,self.Fi+1):
    #                    if (int(self.fcanal(il,1,1)) & &B10) = &B10 :
                    if (int(self.fcanal(il,1,1)) & 2) == 2 :
                        ksommet = il+1
                        break
                ener = ksommet*self.slope + self.offset
                lmh = float(self.ro*(1 + self.kres*Numeric.sqrt(ener)))/self.slope
                if self.Id < oldfi:
                    self.Id = oldfi + 1
                if (ksommet - self.Id + 1) > int(round(3*lmh)):
                    self.Id = ksommet - int(round(2*lmh))
    #            if (int(self.fcanal(il,1,1)) & &B10) = &B10 :
#                for i1 in range(self.Fi,self.Id,-1):
                for il in range(self.Fi,self.Id-1,-1):
                    if (int(self.fcanal(il,1,1)) & 2) == 2 :
                        ksommet = il+1
                        break
                ener=ksommet*self.slope+self.offset
                lmh = float(self.ro*(1 + self.kres*Numeric.sqrt(ener)))/self.slope
                if (self.Fi - ksommet + 1) > int(round(3*lmh)):
                    self.Fi = ksommet + int(round(2*lmh))
                if float(self.Fi - self.Id) > float(nccorrel)/2 :
#                    print "passou aqui"
                    somcan = 0.0
                    som = 0.0
                    ipic = ipic + 1
#                    for i1 in range(self.Id,self.Fi):
                    for il in range(self.Id,self.Fi+1):
                        self.vy[il] = self.fcanal(il,3,0)
                        somcan = somcan + Numeric.sqrt(self.fcanal(il,2,0))
                        som = som + self.fcanal(il,2,0)
                    oldfi = self.Fi
#                    print "soma"
#                    print somcan
#                    print self.moyamont
#                    print self.moyaval
                    somcan = somcan - (float(Numeric.sqrt(self.moyamont+self.moyaval))/2)*(self.Fi-self.Id+1)
                    rapport = float(somcan)/somcorrel
                    if rapport > 2 :
                        somnette = som -(float(self.moyamont+self.moyaval)/2)*(self.Fi-self.Id+1)
                        trapeze = som-somnette
                        sy =float(200*Numeric.sqrt(somnette + 2*trapeze))/somnette
                        if sy < 0 or sy > 100 or rapport > 5 or ipic == 1  :
#                            for il in range(self.Id,self.Fi):
# silvio retirei pois estava desmarcando canal 747 apartir do if acima
                            for il in range(self.Id,self.Fi+1):
                                self.vy[il] = self.fcanal(il,4,0)
                                self.vy[il] = self.fcanal(il,4,1)
                else:
#                    for il in range(self.Id,self.Fi):
                    for il in range(self.Id,self.Fi+1):
                        self.vy[il] = self.fcanal(il,4,1)
                self.f1zdeb = 0
                self.f1zfin = 0
                somcorrel = 0.0
            oldcanalcorrel = canalcorrel
        self.f1zdeb = 0
        self.f1zfin = 0
#Formar ondas- o controle para determinar as mascaras pequenas dos picos pelos picos grandes
#silvio mostra valores de canais para entendimento
 #       file.close
 #       file=0
 #       file=open("c:fit1.txt",'w')
 #       for j in range(0,8190):
 #          file.write("%d;%d\n" %(j,self.vy[j]))
 #       file.close
 #       file=0
#        for j in range(int(self.ideb + nccorrel*2),int(self.ifin - nccorrel*2)):
#monta loop iniciando de ideb=40 + nccorrel=5*2 = 10
        syg=0
        for j in range(int(self.ideb + nccorrel*2),int(self.ifin - nccorrel*2)+1):
    #    if (int(self.fcanal(j,1,0)) & &B1)  = &B1 & f1zdeb = 0:f1zdeb = 1 : Id = J
            vtes=int(self.fcanal(j,1,0))
            if (((vtes & 1)  == 1) and self.f1zdeb == 0):
                self.f1zdeb = 1
                self.Id = j
    #    if (int(self.fcanal(j,1,0)) & &B1) = 0 & f1zdeb = 1:f1zfin = 1 : Fi = J-1

            if (((vtes & 1) == 0) and self.f1zdeb == 1):
                self.f1zfin = 1
                self.Fi = j-1
            if self.f1zdeb == 1 and self.f1zfin == 1 :
#                if self.Id == 129:
#                    print "id = %d Fi = %d" %(self.Id,self.Fi)
#                for kcan in range(self.Id,self.Fi):
                for kcan in range(self.Id,self.Fi+1):
#                    if (int(self.fcanal(kcan,1,1)) & &B10) == &B10 :
                    if (int(self.fcanal(kcan,1,1)) & 2) == 2 :
                        if self.fcanal(kcan,2,0) < self.fcanal(kcan-1,2,0) :
                            self.vy[kcan] = self.fcanal(kcan,4,1)
                            self.vy[kcan-1] = self.fcanal(kcan-1,3,1)
#                            if self.Id == 129:
#                               print "-Kcan = %d F(kan) = %d F(kan-1) = %d" %(kcan,self.vy[kcan],self.vy[kcan-1])
                        elif self.fcanal(kcan,2,0) < self.fcanal(kcan+1,2,0):
                            self.vy[kcan] = self.fcanal(kcan,4,1)
                            self.vy[kcan+1] = self.fcanal(kcan+1,3,1)
#                            if self.Id == 129:
#                               print "+Kcan = %d F(kan) = %d F(kan+1) = %d" %(kcan,self.vy[kcan],self.vy[kcan+1])
                som = 0
                ncanaux = 0
                kmax = self.Id
#                for il in range(self.Id,self.Id - nccorrel*2,-1):
#                for il in range(self.Id,(self.Id - nccorrel*2)+1,-1):
                for il in range(self.Id,(self.Id - nccorrel*2)-1,-1):
                    ncanaux=ncanaux+1
                    som = som + self.fcanal(il,2,0)
                    if self.fcanal(il,2,0) > self.fcanal(kmax,2,0):
                        kmax = il
                somnette = som - (self.fcanal(self.Id,2,0) + self.fcanal(il-1,2,0))*float(ncanaux)/2
                #silvio coloquei pois estava dando erro quando ideb=0
                #syg=0.01
#                if self.Id == 129:
#                   print "som = %d somnette = %d ncanaux = %d" %(som,somnette,ncanaux)
#                   print "Id = %d FNcanal&(Id,2,0) = %d il = %d self.fcanal(il,2,0) = %d" %(self.Id,self.fcanal(self.Id,2,0),il-1,self.fcanal(il-1,2,0))
                if somnette <> 0.0:
                    syg = float(200*Numeric.sqrt(somnette + 2*(som-somnette)))/somnette
 #               if self.Id == 129:
 #                  print "syg = %d " %(syg)
                if syg > 0.0 and syg < 50.0 :
#                    if self.Id == 129:
#                       print "Passous syg = %d " %(syg)
                    kcan = int(float(self.Id+il-1)/2)
                    oldid = self.Id
                    self.fnzondeb(kcan,nccorrel)
                    #self.moyamont,f1zdeb,self.Id = self.fnzondeb(kcan,nccorrel)
                    for i in range(self.Id,oldid+1):
                        self.vy[i] = self.fcanal(i,3,0)
                    self.vy[kmax] = self.fcanal(kmax,3,1)
                som = 0
                ncanaux = 0
                kmax = self.Fi
#                for i1 in range(self.Fi,(self.Fi + nccorrel*2)):
                for i1 in range(self.Fi,(self.Fi + nccorrel*2)+1):
                    ncanaux=ncanaux+1
                    som = som + self.fcanal(i1,2,0)
                    if self.fcanal(i1,2,0) > self.fcanal(kmax,2,0):
                        kmax = i1
# estava il ele e nao i1 um
                somnette = som - (self.fcanal(self.Fi,2,0) + self.fcanal(i1,2,0))*float(ncanaux)/2
                if somnette <> 0.0:
                    syg = float(200*Numeric.sqrt(somnette + 2*(som-somnette)))/somnette
                if syg > 0.0 and syg < 50.0 :
                    kcan = int(float(self.Fi+i1)/2)
                    oldfi = self.Fi
                    self.fnzonfin(kcan,nccorrel)
                    for i in range(oldfi,self.Fi+1):
                        self.vy[i] = self.fcanal(i,3,0)
                    self.vy[kmax] = self.fcanal(kmax,3,1)
                self.f1zdeb = 0
                self.f1zfin = 0
#        print 'fim ajuste'
#silvio mostra valores de canais para entendimento
  #      file=open("c:fit2.txt",'w')
  #      for j in range(0,8190):
  #         file.write("%d;%d\n" %(j,self.vy[j]))
  #      file.close
  #      file=0
        self.ideb=sauveideb
        self.ImpZonesPic()
        return self.Vispectdic

    #    RETURN
#  remonta grafico


# localiza inicio da zona
    def fnzondeb(self,kcan,nccorrel):
#        for i1 in range(kcan,kcan-nccorrel*2,-1):
        for i1 in range(kcan,(kcan-nccorrel*2)-1,-1):
            self.Id = i1 - 1
            if i1 < 3 :
                return 0
            co = self.fcanal((i1-1),2,0) + self.fcanal((i1-2),2,0)
            if ((self.fcanal(i1,2,0)+co) <= (self.fcanal(i1-3,2,0)+co)) :
                break
        self.moyamont = float(self.fcanal(i1,2,0)+co)/3
        self.f1zdeb = 1
        return 1

# localiza o fim da zona
    def fnzonfin(self,kcan,nccorrel):
#        for il in range(kcan,kcan+nccorrel*2):
        for il in range(kcan,(kcan+nccorrel*2)+1):
            self.Fi = il + 1
            co = self.fcanal(il+1,2,0) + self.fcanal(il+2,2,0)
            if ((self.fcanal(il,2,0)+co) <= (self.fcanal(il+3,2,0)+co)) :
                break
        self.moyaval = (float(self.fcanal(il,2,0)+co)/3)
        self.f1zfin = 1
        return 1

# a funcao tem 4 acoes dependendo do nfoco:
# 1 - para obter o byte de peso forte de um canal
# 2 - para mascarar o byte de peso forte de um canal e para obter assim
#     seus indices
# 3 - para ativar um pouco de estado do byte do peso forte de acordo com
#     a variavel de acao (0 7)
# 4 - Desativar um pouco de estado do byte do peso forte de acordo com a
#     variavel de acao (0 7)
#
    def fcanal(self,i,nfoco,acao):
        #print i
        decal=16777216
#   deu erro quando vy contem numeros negativos
#        octetfort = int(float(self.vy[i])/decal)
        octetfort = int(int(self.vy[i])/decal)
#        if self.vy[i] < 0 :
#           print "octetfort = int(float(self.vy[i])/decal)"
#           print type(self.vy[i])
#           print self.vy[i]
#           print decal
#           print type(decal)
#           print octetfort
#           print type(octetfort)
#           print acao
#           print self.vy[i] - long(octetfort)*decal
#           return
        if nfoco == 1:
           return long(octetfort)
        if nfoco == 2:
           return self.vy[i] - long(octetfort)*decal
        if nfoco == 3:
           octetfort = octetfort | int(2**acao)
           return self.fcanal(i,2,0) + long(octetfort)*decal
        if nfoco == 4:
           octetfort = octetfort & ~(int(2**acao))
           return self.fcanal(i,2,0) + long(octetfort)*decal

#'        Fonction pour determiner le canal sommet exact
    def FNcanexact(self,Fm,Ind):
        vAq = 0.0
        I = Ind - 1
        while vAq < self.Aire*Fm:
            I = I + 1
#            print 'i=%d A1=%d B1=%d' %(I,self.A1,self.B1)
            vAq = vAq + self.fcanal(I,2,0) - (self.A1*I+self.B1)
        vAp = vAq - ( self.fcanal(I,2,0) - (self.A1*I+self.B1))
        return ((I-1) + float(self.Aire*Fm - vAp)/(vAq - vAp) + 0.5)

# verifica regioes e calcula area
#   def GravaTeste(self,y):
#LOCATE 12,17 : INPUT "Desvio padrao, % de incerteza (1,2 ou 3) = ",Sig%
#    file=open("c:teste",'w')
#    for j in range(0,8000):
#       file.write("%d;%d;%d\n" %(j,y[j],self.vy[j]))
#  file.close
#    file=0

    def ImpZonesPic(self):
#LOCATE 12,17 : INPUT "Desvio padrao, % de incerteza (1,2 ou 3) = ",Sig%
#        self.VisTable.show()
        if self.Lt == 0.0:
            self.Lt = 1000.0
        Flag = 0
        Sum = 0
        Cmax = 0
        NbSommets = 0
        self.NoPic = 0
        self.Id=0
        self.ideb=0
        #print 'loop ideb=%d Ifin=%d ' %(self.ideb,self.ifin)
#        for Il in range(self.ideb,self.ifin):
        for Il in range(self.ideb,self.ifin+1):
            #print Il
            vres=int(self.fcanal(Il,1,0))
            #print 'i=%d Flag %d' %(Il,Flag)
            if (vres & 1) == 0:
                if Flag <> 0 :
                    self.Fi = Il-1
                    self.Y1 = float(self.fcanal((self.Id-1),2,0) + self.fcanal(self.Id,2,0) + self.fcanal((self.Id+1),2,0))/3
                    self.Y2 = float(self.fcanal((self.Fi-1),2,0) + self.fcanal(self.Fi,2,0) + self.fcanal((self.Fi+1),2,0))/3
#                    if self.Id == 479:
#                       print "aaaaaaaaaaaaaa self.Fi                    "
#                       print self.Fi
#                       print self.Y1
#                       print self.Y2
#                        self.A1 = 0.0
#                    else:
                    self.A1 = float(self.Y1-self.Y2)/(self.Id-self.Fi)
                    self.B1 = self.Y1 - self.A1*self.Id
 #                   if self.Id == 479:
 #                      print "bbbbbbbbbbbbb     self.Fi                    "
 #                      print self.Fi
 #                      print self.Y1
 #                      print self.Y2
 #                      print self.A1
 #                      print self.B1
                    oldfi = self.Fi
 #                   print 'Antes Id=%d Fi=%d OldFi=%d \n' %(self.Id,self.Fi,oldfi)
                    if NbSommets <= 1 :
 #                       print 'mais de um pico'
                        self.TraiPicSimple()
                    else:
                        Npic = 1
#                        for K in range(1,int(NbSommets-1)):
                        for K in range(1,int(NbSommets-1)+1):
                            ContVallee = 2**24
#                            for J in range(self.Isommet[K],self.Isommet[K+1]):
                            for J in range(self.Isommet[K],self.Isommet[K+1]+1):
                                if self.fcanal(J,2,0) < ContVallee :
                                    ContVallee = self.fcanal(J,2,0)
                                    Ivallee = J
                            Ecart = ContVallee-(Ivallee*self.A1+self.B1)
                            if (Ecart < Numeric.sqrt(self.fcanal(self.Isommet[K],2,0))) and (Ecart < Numeric.sqrt(self.fcanal(self.Isommet[K+1],2,0))):
                                self.Y1 = float(self.Id*self.A1+self.B1)
                                self.Y2 = float(ContVallee)
                                if ContVallee-(Ivallee*self.A1+self.B1) < 0 :
 #                                   print "Y1=%f Y2=%f Fi=%f Ivallee=%f ContVallee=%f " %(self.Y1,self.Y2,self.Fi,Ivallee,ContVallee)
                                    #print oldfi
                                    #silvio coloquei pois Ivallee - oldfi = 0
 #                                   print 'Oldfi=%f self.A1=%f self.B1=%f' %(oldfi,self.A1,self.B1)
                                    if Ivallee <> oldfi:
                                        self.A1 = float(ContVallee-(oldfi*self.A1+self.B1))/(Ivallee-oldfi)
                                    else:
                                        self.A1 = float(ContVallee-(oldfi*self.A1+self.B1))/1
                                    #    self.A1 = 1
                                    self.B1 = ContVallee-self.A1*Ivallee
 #                               print 'Res=%f self.A1=%f self.B1=%f' %(oldfi,self.A1,self.B1)
                                self.Fi = Ivallee
                                if Npic > 1 :
 #                                   print 'ssssssssssssseg'
                                    self.Multiplet(self.Id,self.Fi)
                                else:
 #                                   print 'ttttttttttttter  Id=%d Fi=%d OldFi=%d \n' %(self.Id,self.Fi,oldfi)

                                    self.TraiPicSimple()
                                Npic = 1
                                self.Id = self.Fi
                            else:
                                Npic=Npic+1
                        self.Fi = oldfi
                        #print '222 - Depois Id=%d Fi=%d OldFi=%d \n' %(self.Id,self.Fi,oldfi)
                        self.Y1 = float(self.Id*self.A1)+float(self.B1)
                        self.Y2 = float(self.Fi*self.A1)+float(self.B1)
                        if Npic > 1 :
    #                        print 'qua'
    #                        if self.Id == 479:
    #                          print "qqqqqqqqqqqq     self.Fi                    "
    #                          print self.Fi
    #                          print self.Y1
    #                          print self.Y2
    #                          print self.A1
    #                          print self.B1
                            self.Multiplet(self.Id,self.Fi)
                        else:
 #                           print 'qui  Id=%d Fi=%d OldFi=%d \n' %(self.Id,self.Fi,oldfi)
 #                           print 'y1 = %d y2=%d\n' %(self.Y1,self.Y2)
 #                           print 'a1 = %d b1=%d\n' %(self.A1,self.B1)
                            self.TraiPicSimple()
 #                   print 'Depois Id=%d Fi=%d OldFi=%d \n' %(self.Id,self.Fi,oldfi)
                    Flag = 0
                    Sum = 0
                    Cmax = 0
                    NbSommets = 0
            if (vres & 1) == 1:
                if Flag == 0:
                    self.Id = Il
                Flag=Flag+1
                Sum = Sum + self.fcanal(Il,2,0)
                if (int(self.fcanal(Il,1,1)) & 2) == 2 :
                    NbSommets=NbSommets+1
#                    print NbSommets
#                    print Il
#                    print Flag
                    self.Isommet[NbSommets] = Il
                if (self.fcanal(Il,2,0)) > Cmax:
                    Cmax = self.fcanal(Il,2,0)
#CALL ChgtEcran(self.ideb,self.ifin)

        #print 'imppppppppppppppppppppppppp'
#        print self.Vispectdic
        self.VisTable.ui.lblespectro.setText(self.vinfo['SourceName'])
        self.VisTable.ui.lblvivo.setText(str(self.vinfo['TempoVivo']))
        self.VisTable.ui.lblmorto.setText(str(self.vinfo['TempoTotal']))
#        if self.info['DataTempo'] <> None:
#           self.VisTable.ui.txtdata.setDate(self.info['DataTempo'])
#        else:
#           self.VisTable.ui.txtdata.setDate('10/10/2007')
#        self.VisTable.adicionar(self.Vispectdic)
#'        Procedure pour determiner l'abscisse exacte
#'            et la self.Resolution d'un pic
#' Determination de la pente du bruit de fond

    def ResAbsiPic(self,Ind,vInf,Mode):
        if Mode == 0 :
#            self.Y1 = (float(self.fcanal((Ind-1),2,0) + self.fcanal(Ind,2,0) + self.fcanal((Ind+1),2,0))/3)
#            self.Y2 = (float(self.fcanal((Inf-1),2,0) + self.fcanal(Inf,2,0) + self.fcanal((Inf+1),2,0))/3)
            Y1 = (float(self.fcanal((Ind-1),2,0) + self.fcanal(Ind,2,0) + self.fcanal((Ind+1),2,0))/3)
            Y2 = (float(self.fcanal((Inf-1),2,0) + self.fcanal(Inf,2,0) + self.fcanal((Inf+1),2,0))/3)
        if (Ind-vInf) == 0:
#            self.A1=0.0
            A1=0.0
        else:
#            self.A1 = float(self.Y1-self.Y2) / (Ind-vInf)
            A1 = float(self.Y1-self.Y2) / (Ind-vInf)
#        self.B1 = self.Y1 - self.A1*Ind
        B1 = self.Y1 - self.A1*Ind
        self.IntZone(Ind,vInf,Mode)
        self.Absi = self.FNcanexact(0.5,Ind)
        self.Resol = float(self.FNcanexact(0.75,Ind) - self.FNcanexact(0.25,Ind))*self.slope*1.74

        #    imprime resultados

    def ImpRes(self,pIt,pAbsi,pAire,pBgnd,pResol,pId,pFi,pErreur,pLt):
#        self.NoPic = self.NoPic + 1
#        print " %4i  %3i %8.2f %6i %6i %6.2f %6.2f %5i %5i %8.3f %6.1f" %(self.NoPic+1,pIt,(pAbsi*self.slope+self.offset),pAire,pBgnd,pResol,pAbsi,pId,(pFi-pId+1),(float(pAire)/pLt),pErreur)
        vdic={}
        vdic['it']   =pIt
        vdic['energia']=pAbsi*self.slope+self.offset
        vdic['area']=pAire
        vdic['bg']=pBgnd
        vdic['resol']=pResol
        vdic['fi']=pAbsi
        vdic['id']=pId
        vdic['lp']=pFi-pId+1
        vdic['cps']=float(pAire)/pLt
        vdic['erreur']=pErreur
        vr=float("%8.2f" %(vdic['energia']))
#        print vdic['energia']
#        print vr
        #xelem=self.Elementos.busca_elem(vr)
#        print xelem
        vdic['elem']=0 #xelem[1]
        vdic['meiavida']=0 #xelem[2]
        vdic['massa']=0 #xelem[3]
        self.Vispectdic[self.NoPic]=vdic
        self.NoPic = self.NoPic + 1
#        self.VisTable.adicionar(self.NoPic,pIt,(pAbsi*self.slope+self.offset),pAire,pBgnd,pResol,pAbsi,pId,(pFi-pId+1),(float(pAire)/pLt),pErreur)


#SHARED  Sum,self.Aire,self.Bgnd,Y1,Y2,B&()
#LOCAL Fin,Deb,I,S
    def IntZone(self,Kdeb,Kfin,Mode):
        Sum = 0.0
        Fin = Kfin
        Deb = Kdeb
        if Deb > Fin:
            vaux=Deb
            Deb=Fin
            Fin=Deb
        if Deb == 0:
            Deb = 1
#        for I in range(Deb,Fin):
        for I in range(Deb,Fin+1):
            Sum = Sum + self.fcanal(I,2,0)
        S = Kfin - Kdeb + 1
        if Mode == 0:
            self.Bgnd = self.fcanal(Deb,2,0)+self.fcanal((Deb+1),2,0)+self.fcanal((Deb-1),2,0)+self.fcanal((Fin),2,0)+self.fcanal((Fin+1),2,0)+self.fcanal((Fin-1),2,0)
            self.Bgnd = float(float(self.Bgnd)/6)*S
        if Mode == 1:
            self.Bgnd = float(float(self.Y1+self.Y2)*S)/2
        self.Aire = Sum - self.Bgnd
        #silvio caso self.Aire = 0
        #if self.Aire == 0:
        #    self.Aire = 1

    def TraiPicSimple(self):
#    Tratamento de picos simples
        self.IntZone(self.Id,self.Fi,1)
        #silvio coloquei if caso zero isso quando inicio ideb de 0 e nao 40
        if self.Aire == 0:
            self.Erreur=0.0
            self.Resol=0.0
            self.Absi=0
        else:
            #print self.Bgnd
            #print self.Aire
            #print self.sig
            #print self.Erreur
            #silvio colequei abs pois esta dando negativo o Bgnd
            self.Erreur = float(Numeric.sqrt(abs(self.Bgnd*2+self.Aire))*100*self.sig)/self.Aire
            self.ResAbsiPic (self.Id,self.Fi,1)
        It = 0
        self.ImpRes(It,self.Absi,self.Aire,self.Bgnd,self.Resol,self.Id,self.Fi,self.Erreur,self.Lt)

    def Multiplet(self,Id,Fi):
#silvio ler Sig
#        print 'multiplet'
        Absi=Numeric.zeros([100], Numeric.Float64)
        Dlmh=Numeric.zeros([100], Numeric.Float64)
        Alp=Numeric.zeros([100], Numeric.Float64)
        Azo=Numeric.zeros([100], Numeric.Float64)
        OldAbsi=Numeric.zeros([100], Numeric.Float64)
        OldAlp=Numeric.zeros([100], Numeric.Float64)
#' Determination du nb. de pics et du nb. de canaux de la zone
        Nc = 0
        Np = 0
        Jv = 3
#        for J in range(self.Id,self.Fi):
        for J in range(Id,Fi+1):
            Nc=Nc+1
            if (int(self.fcanal(J,1,1)) & 2) == 2 :
                Np=Np+1
                Absi[Np] = J
                OldAbsi[Np] = Absi[Np]
                Ener = float(J*self.slope + self.offset)
                Dlmh[Np] = float((self.ro*(1+self.kres*Numeric.sqrt(Ener))))/(self.slope*2)
                Alp[Np] = float(0.69315)/Dlmh[Np]**2
                OldAlp[Np] = Alp[Np]
                Azo[Np] = float(self.fcanal(J,2,0) - (J*self.A1+self.B1))
    #    file=open("c:Absi.txt",'w')
    #    for j in range(0,100):
    #        file.write("%d;%d\n" %(j,Absi[j]))
    #    file.close
    #    file=0
    #    file=open("c:Dlmh.txt",'w')
    #    for j in range(0,100):
    #        file.write("%d;%f\n" %(j,Dlmh[j]))
    #    file.close
    #    file=0
    #    file=open("c:Alp.txt",'w')
    #    for j in range(0,100):
    #        file.write("%d;%f\n" %(j,Alp[j]))
    #    file.close
    #    file=0
    #    file=open("c:Azo.txt",'w')
    #    for j in range(0,100):
    #        file.write("%d;%f\n" %(j,Azo[j]))
    #    file.close
    #    file=0
        Nx = Jv*Np
        A=Numeric.zeros([Nc+1,Nx+1], Numeric.Float64)
        C=Numeric.zeros([Nc+1], Numeric.Float64)
        B=Numeric.zeros([Nc+1], Numeric.Float64)
        V=Numeric.zeros([Nx+1], Numeric.Float64)
        T=Numeric.zeros([Nx+1], Numeric.Float64)
        W=Numeric.zeros([Nc+1], Numeric.Float64)
        Yg=Numeric.zeros([Nx+1,Nc+1], Numeric.Float64)
        Yt=Numeric.zeros([Nc+1], Numeric.Float64)
        Res=Numeric.zeros([Nc+1], Numeric.Float64)
        Sur=Numeric.zeros([100], Numeric.Float64)
        Sigm=Numeric.zeros([100], Numeric.Float64)
        Ainv=Numeric.zeros([Nx+1,Nx+1], Numeric.Float64)
        It = 0
        Sortie = 0
        Jtest = 0
#' Debut de la boucle de convergence
    #    print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    #    print self.A1
    #    print self.B1
        while Jtest <> Np:
#    'formation des matrices A,B et W
            L = 0
#            print 'Id %' %self.Fi
#            print 'Fi %' %self.Fi
#            for I in range(self.Id,self.Fi):
            for I in range(Id,Fi+1):
                L=L+1
#                print 'L'
#                print L
                C[L] = float(self.fcanal(I,2,0)) - (float(I)*self.A1+self.B1)
                if C[L] <= 0.0 :
                    C[L] = 1.0
                W[L] = float(1.0)/C[L]
                Yzot = 0.0
#                for J in range(1,Np):
                for J in range(1,Np+1):
                    CalInt = float(-Alp[J]*(float(I)-Absi[J])**2)
                    if CalInt < -81 :
                        Yzo = 0.0
                    else:
                        Yzo = float(Azo[J]*Numeric.exp(CalInt))
                    Yzot = Yzot + Yzo
                    B[L] = C[L] - Yzot
                    K = 1 + Jv*(J-1)
                    #silvio coloquei pois qdo divide por zero da erro
                    if Azo[J] == 0:
                        A[L,K] = 0
                    else:
                        A[L,K] = float(Yzo)/Azo[J]
                    A[L,K+1] = float(2*Yzo*Alp[J]*(I-Absi[J]))
                    if Jv == 3 :
                        A[L,K+2] = float(-Yzo*(I-Absi[J])**2)
    #        file=open("c:C.txt",'w')
    #        for j in range(0,Nc+1):
    #           file.write("%-f;%-f\n" %(j,C[j]))
    #        file.close
    #        file=0
    #        file=open("c:W.txt",'w')
    #        for j in range(0,Nc+1):
    #           file.write("%f;%f\n" %(j,W[j]))
    #        file.close
    #        file=0
    #        file=open("c:B.txt",'w')
    #        for j in range(0,Nc+1):
    #           file.write("%f;%f\n" %(j,B[j]))
    #        file.close
    #        file=0
#    'formation de la matrice Ainv#
#silvio mostra valores de canais para entendimento
#            file=open("c:Avet.txt",'w')
#            for e in range(1,NC):
#                file.write(str(e)+' - '+str(A[e].tolist()))
#            file.close
#            file=0
#           for J in range(1,Nx):
#               for K in range(1,Nx):
            for J in range(1,Nx+1):
                for K in range(1,Nx+1):
                    Ainv[J,K] = 0.0
#                    for I in range(1,Nc):
                    for I in range(1,Nc+1):
#                        print 'j=%d k=%d i=%d' %(J,K,I)
#                        print 'Ainv[%d,%d]=%d + A[%d,%d]=%d * W[%d]=%d * A[%d,%d]=%d' %(J,K,Ainv[J,K],I,J,A[I,J],I,W[I],I,K,A[I,K])
                        Ainv[J,K] = float(Ainv[J,K] + A[I,J]*W[I]*A[I,K])
#    ' Inversion de la matrice
#silvio
# verificar se a matriz A retorna
    #        file=open("c:Ainva.txt",'w')
    #        for i in range(1,Nx):
    #          for j in range(1,Nx):
    #            file.write("%d,%d;%f\n" %(i,j,Ainv[i,j]))
    #        file.close
    #        file=0

            Ainv=self.InvMd(Nx+1,Ainv)
    #        file=open("c:Ainvd.txt",'w')
    #        for i in range(1,Nx):
    #          for j in range(1,Nx):
    #            file.write("%d,%d;%f\n" %(i,j,Ainv[i,j]))
    #        file.close
    #        file=0
#            A=LinearAlgebra.inverse(Ainv)
#    ' formation de la matrice V
#            for J in range(1,Nx):
            for J in range(1,Nx+1):
                V[J] = 0
#                for I in range(1,Nc):
                for I in range(1,Nc+1):
                    V[J] = float(V[J] + A[I,J]*W[I]*B[I])
#    ' Solution
#            for I in range(1,Nx):
    #        file=open("c:ttt.txt",'w')
            for I in range(1,Nx+1):
                T[I] = 0
#                for J in range(1,Nx):
                for J in range(1,Nx+1):
                    T[I] = T[I] + Ainv[I,J]*V[J]
                    aa=Ainv[I,J]
    #                file.write('%f;%f;%f\n' %(T[I],aa,V[J]))
#    ' Test de convergence
    #        file.close
    #        file=0
            Jtest = 0
            #print 'passou '
#            for J in range(1,Np):
    #        file=open("c:Alp2.txt",'w')
    #        for j in range(0,100):
    #            file.write("%d;%f\n" %(j,Alp[j]))
    #        file.close
    #        file=0
    #        file=open("c:Azo2.txt",'w')
    #        for j in range(0,100):
    #            file.write("%d;%f\n" %(j,Azo[j]))
    #        file.close
    #        file=0

            for J in range(1,Np+1):
                Dif3 = 0.0
                K = 1 + Jv*(J-1)
                Azo[J] = Azo[J] + T[K]
                if Azo[J] <= 0.0 :
                    Sortie=Sortie+1
                    break
                #print 'dife'
                Dif1 = abs(float(T[K])/Azo[J])
                #silvio converti para inteiro
                #print 'absi T'
                #print J
                #print K
                #print Absi[J]
                #print T[K+1]
                #print abs(T[K+1])
                #print int(T[K+1])
                raux = long(float(Absi[J]) + float(T[K+1]))
    #            print "Absi=%f T=%d" %(Absi[J],T[K+1])
                Absi[J] = raux
                if Absi[J] <= 0.0 :
                    Sortie=Sortie+1
                    break
                Dif2 = abs(float(T[K+1])/Absi[J])
                if Jv == 3 :
                    Alp[J] = Alp[J] + T[K+2]
                    if Alp[J] <= 0.0 :
                        Sortie=Sortie+1
                        break
                    Dif3 = abs(float(T[K+2])/Alp[J])
    #            print 'Dif1=%f Dif2=%f Dif3=%f Jtest=%d' %(Dif1,Dif2,Dif3,Jtest)
                if Dif1 < 0.01 and Dif2 < 0.01 and Dif3 < 0.01 :
                    Jtest=Jtest+1
            It=It+1
            #print 'it'
            #print It
            if It == 10 :
                #silvio coloquei para forcar entrar na proxima condicao
                #Sortie = 0
                break
    # Si non convergence, on impose la self.Resolution
            if Sortie > 0 :
#                for J in range(1,Np):
                for J in range(1,Np+1):
                    Absi[J] = OldAbsi[J]
                    Alp[J] = OldAlp[J]
#                    print 'J e Absi'
#                    print J
#                    print Absi[J]
                    Azo[J] = self.fcanal(int(Absi[J]),2,0) - (Absi[J]*self.A1+self.B1)
                Sortie = 0
                Jv = 2
                Nx = Jv*Np
        if Sortie == 0 :
    #' Calcul statistique et sortie correcte
            Socare = 0.0
            Chi2 = 0.0
#            for I in range(1,Nc):
            for I in range(1,Nc+1):
                Res[I] = 0
                Yt[I] = 0
#                for J in range(1,Np):
                for J in range(1,Np+1):
                    Yg[J,I] = 0
            I = 0
#            for K in range(self.Id,self.Fi):
            for K in range(Id,Fi+1):
                I=I+1
#                for J in range(1,Np):
                for J in range(1,Np+1):
                    Mu = -Alp[J]*(K-Absi[J])**2
                    if Mu < -81 :
                        Yg[J,I] = 0
                    else:
                        Yg[J,I] = Azo[J]*Numeric.exp(Mu)
                    Yt[I] = Yt[I] + Yg[J,I]
                Res[I] = self.fcanal(K,2,0) - (K*self.A1+self.B1) - Yt[I]
                Socare = Socare + Res[I]*Res[I]*W[I]
                if self.fcanal(K,2,0) <> 0 :
                    Res[I] = float(Res[I]*Res[I])/self.fcanal(K,2,0)
                Chi2 = Chi2 + Res[I]
            Xndl = Nc - Nx
            Chi2 = float(Chi2)/Xndl
#            for J in range(1,Np):
            for J in range(1,Np+1):
                Sur[J] = float(1.773*Azo[J])/Numeric.sqrt(Alp[J])
                K = 1 + Jv*(J-1)
                Vazo = float(Socare*Ainv[K,K])/Xndl
                Valp = float(Socare*Ainv[K+2,K+2])/Xndl
                Sigm[J] = float(Azo[J]**2)/Alp[J] * (float(Vazo)/Azo[J]**2 + float(0.25*Valp)/Alp[J]**2)
                Sigm[J] = abs(Sigm[J])
                Sigm[J] = float(Numeric.sqrt(Sigm[J])*200)/Sur[J]
                Resl = float(200*Numeric.sqrt(float(0.69315)/Alp[J]))/Absi[J]
                Resk = 2*self.slope*Numeric.sqrt(float(0.69315)/Alp[J])
                Ener = Absi[J]*self.slope + self.offset
                Decal = float(Resk*1.5)/self.slope
                self.Bgnd = (((Absi[J]-Decal)*self.A1+self.B1)+((Absi[J]+Decal)*self.A1+self.B1))*Decal
                #problema com raiz de numero negativo.....verificar A T E N C A O
    #            print 'aaaaaaaaaaa multiplet aaaaaaaaaaaaa %d' %(Absi[J])
    #            print 'Vazo=%d Valp=%d Resl=%d Resk=%d Ener=%d Decal=%d' %(Vazo,Valp,Resl,Resk,Ener,Decal)
                if (2*self.Bgnd) > Sur[J]:
                    self.Erreur = float(self.sig*100*Numeric.sqrt(2*self.Bgnd+Sur[J]))/Sur[J]
                else:
                   self.Erreur = 0

    #            print 'aaaaaaaaaaa multiplet aaaaaaaaaaaaa %d' %(Absi[J])
    #            print 'it=%d Absi=%d Sur=%d Bg=%d Resk=%d id=%d Fi=%d Erreur=%d Lt=%d' %(It,Absi[J],Sur[J],self.Bgnd,Resk,Id,Fi,self.Erreur,self.Lt)
                self.ImpRes(It,Absi[J],Sur[J],self.Bgnd,Resk,Id,Fi,self.Erreur,self.Lt)
                if J == 1 :
#                    print "rotina para resolver quando imprime erro na listagem do VISPECT errro"
#                    print '%d' % (Chi2)
                    J=1
        #else:
        #    for I in range(1,Nc):
        #        print I
        #        print C[I]
        #ERASE self.Absi,Dlmh,Alp,Azo,A,C,B,V,T,W,Yg,Yt,Res,Sur,Sigm,Ainv#,Oldself.Absi,OldAlp

#'        Procedure d'invertion de matrice
    def InvMd(self,N,A):
        #cria matriz con n elemento, mais um espaco de n elementos para preencher
        AB=Numeric.zeros([N,(N)*2], Numeric.Float64)
        BB=Numeric.zeros([N,(N)*2], Numeric.Float64)
#        for I in range(1,N):
#            for J in range(1,N):
#preenche os primeiros n elementos com a matriz A
        for I in range(1,N):
            for J in range(1,N):
                AB[I,J] = A[I,J]
#silvio
        Id = N + 1
        Fi = N * 2
#        for I in range(1,N):
#            for J in range(Id,Fi):
#preenche com zeros o segundo espaco da matriz AB
        for I in range(1,N):
            for J in range(Id,Fi):
                AB[I,J] = 0.0
#        for I in range(1,N):
# coloca o numero 1 na diagonal da segunda parte da matriz
        for I in range(1,N):
            J = I + N
            AB[I,J] = 1
#        for K in range(1,N):
#            for J in range(1,Fi):
#esta rotina pega o primeiro termo da matriz AB e divide pela linha inteira da matriz AB depois continua para a segunda linha at� o fim da matriz AB
# colocando o resultado na matriz BB, depois continua ......
        for K in range(1,N):
            for J in range(1,Fi):
#silvio coloquei div 0 , pois deu erro
                if AB[K,K] <> 0.0:
                    BB[K,J] = float(AB[K,J])/AB[K,K]
#            for I in range(1,N):
            for I in range(1,N):
                if I <> K:
                    for J in range(1,Fi):
                        BB[I,J] = AB[I,J] - AB[I,K]*BB[K,J]
#            for I in range(1,N):
#                for J in range(1,Fi):
            for I in range(1,N):
                for J in range(1,Fi):
                    AB[I,J] = BB[I,J]
#        for I in range(1,N):
#            for J in range(1,N):
        for I in range(1,N):
            for J in range(1,N):
                K = J + N
#                print 'k=%d J=%d I=%d N=%d \n' %(K,J,I,N)
#                print AB[I,K]
#                print A[I,J]
                A[I,J] = AB[I,K]
#        ERASE AB#,BB#
        return A



#silvio dim vispect
