# -*- coding: utf-8 -*-

#import Numeric
import numpy.oldnumeric as Numeric
#import crtConcentracao
#import Elementos
#import QtBlissGraph
#qt = QtBlissGraph.qt
import os
import sys, string


class VispectFit:
    def __init__(self):
        self.dataObjectsDict = {}
        self.Isommet=Numeric.zeros([200], Numeric.Int)
#        self.VisTable = crtConcentracao.startGui()
        self.Vispectdic={}
        self.vinfo={}
        #self.Elementos=Elementos.Elementos('elementos')
        self.A1 = None
        self.B1 = None
        self.Absi = None
        self.NoPic = None
        self.Area = None
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
        """this is the main function for searching peaks and calculating
        area and bg;
        it receives the first and final channel and the name of the
        spectrum file.
        """
        self.Vispectdic={}
        self.vinfo = vlegend
#        print type(vlegend)
# recupera dados de calibracao
        self.slope=self.vinfo['slope']
        self.offset=self.vinfo['offset']
        self.enerquad = self.vinfo['enerquad']
        self.ro=self.vinfo['ro']
        self.kres=self.vinfo['kres']
        self.widthquad = self.vinfo['widthquad']
        nivel=int(self.vinfo['Nivel'])
        barre=int(self.vinfo['Nivel'])
        self.sig = int(self.vinfo['Sigma'])
        #self.ifin=xmax-600
        #if self.ifin > 8100:
        self.ifin = len(self.vy) - 1
#        self.ifin = 8191
        vfim=int(self.ifin)
        self.ideb=0
        sauveideb=self.ideb
        self.ideb=40
        oldfi=0
        for j in range(self.ideb,vfim):
            self.vy[j] = self.fncanal(j,4,0)
            self.vy[j] = self.fncanal(j,4,1)
        rescorrel = self.ro*(1+self.kres*Numeric.sqrt(float(self.ideb+self.ifin)/2*self.slope+self.offset))
        nccorrel = int(round(float(rescorrel)/self.slope)) - 2
        if nccorrel <= 0:
            nccorrel = 1
        i = self.ideb + nccorrel * 2
        contenucentre = 0
        self.f1zdeb = 0
        self.f1zfin = 0

        for j in range(i,i+nccorrel):
            contenucentre = contenucentre+Numeric.sqrt(self.fncanal(j,2,0))

        contenuailes = 0.0

        for j in range(self.ideb,self.ideb+(nccorrel*5)):
            contenuailes = contenuailes + Numeric.sqrt(self.fncanal(j,2,0))
        somcorrel = 0
        ipic = 0
        oldcanalcorrel = 0
        kcan = int(i + float(nccorrel)/2) - 1
        rescorrel = self.ro*(1+self.kres*Numeric.sqrt(float(self.ideb+self.ifin)/2*self.slope+self.offset))
        nccorrel = int(round(float(rescorrel)/self.slope)) - 2
        canalcorrel=0
#        for j in range(i,int(self.ifin - nccorrel*3)+1):
        for j in range(i,int(self.ifin - nccorrel*3)+1):
            kcan = kcan +1
            contenuailes = contenuailes - Numeric.sqrt((self.fncanal(j-nccorrel*2,2,0))) + Numeric.sqrt((self.fncanal(j+nccorrel*3,2,0)))
            contenucentre = contenucentre - Numeric.sqrt((self.fncanal(j,2,0))) + Numeric.sqrt((self.fncanal(j+nccorrel,2,0)))
            canalcorrel = contenucentre*5-contenuailes
            if canalcorrel > barre and self.f1zdeb == 0:
                self.fnzondeb(kcan,nccorrel)
            if self.f1zdeb == 1:
                somcorrel = somcorrel + canalcorrel
#silvio ver comparacao de interiro e float
            if (self.f1zdeb == 1) and (canalcorrel > oldcanalcorrel) :
                self.vy[kcan-1] = self.fncanal(kcan-1,4,1)
                self.vy[kcan] = self.fncanal(kcan,3,1)
            if canalcorrel < barre and self.f1zfin == 0 and self.f1zdeb == 1:
                self.fnzonfin(kcan,nccorrel)
            if self.f1zdeb == 1 and self.f1zfin == 1 :
                for il in range(self.Id,self.Fi+1):
                    if (int(self.fncanal(il,1,1)) & 2) == 2 :
                        ksommet = il+1
                        break
                ener = self.Energy(ksommet)
                ener2 = ksommet*self.slope + self.offset
                if ener - ener2 != 0.0:
                    print "Energy(ksommet): ",ener, "    ksommet*slop + offset: ", ener2
                lmh = float(self.ro*(1 + self.kres*Numeric.sqrt(ener)))/self.slope
                if self.Id < oldfi:
                    self.Id = oldfi + 1
                if (ksommet - self.Id + 1) > int(round(3*lmh)):
                    self.Id = ksommet - int(round(2*lmh))
                for il in range(self.Fi,self.Id-1,-1):
                    if (int(self.fncanal(il,1,1)) & 2) == 2 :
                        ksommet = il+1
                        break
                ener = self.Energy(ksommet)
                ener2 = ksommet*self.slope + self.offset
                if ener - ener2 != 0.0:
                    print "2o caso ==> Energy(ksommet): ",ener, "    ksommet*slop + offset: ", ener2
                lmh = float(self.ro*(1 + self.kres*Numeric.sqrt(ener)))/self.slope
                if (self.Fi - ksommet + 1) > int(round(3*lmh)):
                    self.Fi = ksommet + int(round(2*lmh))
                if float(self.Fi - self.Id) > float(nccorrel)/2 :
                    somcan = 0.0
                    som = 0.0
                    ipic = ipic + 1
                    for il in range(self.Id,self.Fi+1):
                        self.vy[il] = self.fncanal(il,3,0)
                        somcan = somcan + Numeric.sqrt(self.fncanal(il,2,0))
                        som = som + self.fncanal(il,2,0)
                    oldfi = self.Fi
                    somcan = somcan - (float(Numeric.sqrt(self.moyamont+self.moyaval))/2)*(self.Fi-self.Id+1)
                    rapport = float(somcan)/somcorrel
                    if rapport > 2 :
                        somnette = som -(float(self.moyamont+self.moyaval)/2)*(self.Fi-self.Id+1)
                        trapeze = som-somnette
                        sy =float(200*Numeric.sqrt(somnette + 2*trapeze))/somnette
                        if sy < 0 or sy > 100 or rapport > 5 or ipic == 1  :
                            for il in range(self.Id,self.Fi+1):
                                self.vy[il] = self.fncanal(il,4,0)
                                self.vy[il] = self.fncanal(il,4,1)
                else:
                    for il in range(self.Id,self.Fi+1):
                        self.vy[il] = self.fncanal(il,4,1)
                self.f1zdeb = 0
                self.f1zfin = 0
                somcorrel = 0.0
            oldcanalcorrel = canalcorrel
        self.f1zdeb = 0
        self.f1zfin = 0
#Formar ondas- o controle para determinar as mascaras pequenas dos picos pelos picos grandes
#silvio mostra valores de canais para entendimento
#        for j in range(int(self.ideb + nccorrel*2),int(self.ifin - nccorrel*2)):
#monta loop iniciando de ideb=40 + nccorrel=5*2 = 10
        syg=0
        for j in range(int(self.ideb + nccorrel*2),int(self.ifin - nccorrel*2)+1):
            vtes=int(self.fncanal(j,1,0))
            if (((vtes & 1)  == 1) and self.f1zdeb == 0):
                self.f1zdeb = 1
                self.Id = j

            if (((vtes & 1) == 0) and self.f1zdeb == 1):
                self.f1zfin = 1
                self.Fi = j-1
            if self.f1zdeb == 1 and self.f1zfin == 1 :
                for kcan in range(self.Id,self.Fi+1):
                    if (int(self.fncanal(kcan,1,1)) & 2) == 2 :
                        if self.fncanal(kcan,2,0) < self.fncanal(kcan-1,2,0) :
                            self.vy[kcan] = self.fncanal(kcan,4,1)
                            self.vy[kcan-1] = self.fncanal(kcan-1,3,1)
                        elif self.fncanal(kcan,2,0) < self.fncanal(kcan+1,2,0):
                            self.vy[kcan] = self.fncanal(kcan,4,1)
                            self.vy[kcan+1] = self.fncanal(kcan+1,3,1)
                som = 0
                ncanaux = 0
                kmax = self.Id
                for il in range(self.Id,(self.Id - nccorrel*2)-1,-1):
                    ncanaux=ncanaux+1
                    som = som + self.fncanal(il,2,0)
                    if self.fncanal(il,2,0) > self.fncanal(kmax,2,0):
                        kmax = il
                somnette = som - (self.fncanal(self.Id,2,0) + self.fncanal(il-1,2,0))*float(ncanaux)/2
                if somnette <> 0.0:
                    syg = float(200*Numeric.sqrt(somnette + 2*(som-somnette)))/somnette
                if syg > 0.0 and syg < 50.0 :
                    kcan = int(float(self.Id+il-1)/2)
                    oldid = self.Id
                    self.fnzondeb(kcan,nccorrel)
                    for i in range(self.Id,oldid+1):
                        self.vy[i] = self.fncanal(i,3,0)
                    self.vy[kmax] = self.fncanal(kmax,3,1)
                som = 0
                ncanaux = 0
                kmax = self.Fi
                for i1 in range(self.Fi,(self.Fi + nccorrel*2)+1):
                    ncanaux=ncanaux+1
                    som = som + self.fncanal(i1,2,0)
                    if self.fncanal(i1,2,0) > self.fncanal(kmax,2,0):
                        kmax = i1
                somnette = som - (self.fncanal(self.Fi,2,0) + self.fncanal(i1,2,0))*float(ncanaux)/2
                if somnette <> 0.0:
                    syg = float(200*Numeric.sqrt(somnette + 2*(som-somnette)))/somnette
                if syg > 0.0 and syg < 50.0 :
                    kcan = int(float(self.Fi+i1)/2)
                    oldfi = self.Fi
                    self.fnzonfin(kcan,nccorrel)
                    for i in range(oldfi,self.Fi+1):
                        self.vy[i] = self.fncanal(i,3,0)
                    self.vy[kmax] = self.fncanal(kmax,3,1)
                self.f1zdeb = 0
                self.f1zfin = 0
        self.ideb=sauveideb
        self.ImpZonesPic()
        return self.Vispectdic.copy()

    def Energy(self,no_can):
        """ returns channel energy based on calibration data """
        """ this is a quadratic function as describe in Practical Spectroscopy - Gilmore, pg 146
        E(keV) = I(keV) + G * C(channels) + Q * C^2
        where Q is the quadratic factor;
              G is the gradient (slope)
              I is the intercept (offset)
        """

        Coef_A_Cal_Ener = self.vinfo['enerquad']
        Coef_B_Cal_Ener = self.vinfo['slope']
        Coef_C_Cal_Ener = self.vinfo['offset']

        energy = no_can * (no_can * Coef_A_Cal_Ener + Coef_B_Cal_Ener) + Coef_C_Cal_Ener

        return energy

    def Resolution(self, ener):
        """ determination of the resolution for a given energy """

        Ro = self.vinfo['ro']
        K_Res = self.vinfo['kres']
        try:
            Widthquad = self.vinfo['widthquad']
        except:
            Widthquad = 0.0

        if ener < 513.0 and ener > 509.0:
            ener = ener * 1.8
        resolution = Ro + K_Res * ener + Widthquad * ener * ener
        return resolution

# localiza inicio da zona
    def fnzondeb(self,kcan,nccorrel):
        for i1 in range(kcan,(kcan-nccorrel*2)-1,-1):
            self.Id = i1 - 1
            if i1 < 3 :
                return 0
            co = self.fncanal((i1-1),2,0) + self.fncanal((i1-2),2,0)
            if ((self.fncanal(i1,2,0)+co) <= (self.fncanal(i1-3,2,0)+co)) :
                break
        self.moyamont = float(self.fncanal(i1,2,0)+co)/3
        self.f1zdeb = 1
        return 1

# localiza o fim da zona
    def fnzonfin(self,kcan,nccorrel):
        for il in range(kcan,(kcan+nccorrel*2)+1):
            self.Fi = il + 1
            co = self.fncanal(il+1,2,0) + self.fncanal(il+2,2,0)
            if ((self.fncanal(il,2,0)+co) <= (self.fncanal(il+3,2,0)+co)) :
                break
        self.moyaval = (float(self.fncanal(il,2,0)+co)/3)
        self.f1zfin = 1
        return 1

    def fncanal(self,i,nfoco,acao):
        """Esta função tem 4 ações dependendo de nfoco:
           1 - para obter o byte forte de um canal
           2 - remove o byte forte (usado como marcação) e obtem o valor puro (conteúdo original) do canal.
           3 - para ativar um bit de estado do byte forte de acordo com a variável de ação (0-7)
           4 - desativar um bit de estado do byte forte de acordo com a variável de ação (0-7)
        """

        decal=16777216
        octetfort = int(int(self.vy[i])/decal)
        if nfoco == 1:
           return long(octetfort)
        if nfoco == 2:
           return self.vy[i] - long(octetfort)*decal
        if nfoco == 3:
           octetfort = octetfort | int(2**acao)
           return self.fncanal(i,2,0) + long(octetfort)*decal
        if nfoco == 4:
           octetfort = octetfort & ~(int(2**acao))
           return self.fncanal(i,2,0) + long(octetfort)*decal



    def FNcanexact(self,Fm,Ind):
        """ Function to determine the exact peak channel
        Determine the channel that divides the peak area at
        half (given by Fm parameter).
        It seems that there's a problem with this function:
        the background is subtracted channel by channel (the
        counting in the channel bellow the BG line.
        If the BG has a different form (poly ou step function),
        it seems not to take in account.
        """
        vAq = 0.0
        I = Ind - 1
        while vAq < self.Area*Fm:
            I = I + 1
            vAq = vAq + self.fncanal(I,2,0) - (self.A1*I+self.B1)
        vAp = vAq - (self.fncanal(I,2,0) - (self.A1*I+self.B1))
        return ((I-1) + float(self.Area*Fm - vAp)/(vAq - vAp) + 0.5)

# verifica regioes e calcula area
    def ImpZonesPic(self):
        if self.Lt == 0.0:
            self.Lt = 1000.0
        Flag = 0
        Sum = 0
        Cmax = 0
        NbSommets = 0
        self.NoPic = 0
        self.Id=0
        self.ideb=0
#        for Il in range(self.ideb,self.ifin+1):
        for Il in range(self.ideb,self.ifin+1):
            vres=int(self.fncanal(Il,1,0))
            if (vres & 1) == 0:
                if Flag <> 0 :
                    self.Fi = Il-1
                    self.Y1 = float(self.fncanal((self.Id-1),2,0) + self.fncanal(self.Id,2,0) + self.fncanal((self.Id+1),2,0))/3
                    self.Y2 = float(self.fncanal((self.Fi-1),2,0) + self.fncanal(self.Fi,2,0) + self.fncanal((self.Fi+1),2,0))/3
                    # por algum motivo quando o Nivel de Sensibilidade eh muito baixo, esta dando erro neste pedaco
                    # self.Id - self.Fi = 0
                    # coloquei o try para eliminar este problema, mas nao sei se esta correto.
                    try:
                        self.A1 = float(self.Y1-self.Y2)/(self.Id-self.Fi)
                    except ZeroDivisionError:
                        pass
                    self.B1 = self.Y1 - self.A1*self.Id
                    oldfi = self.Fi
                    if NbSommets <= 1 :
                        self.TraiPicSimple()
                    else:
                        Npic = 1
                        for K in range(1,int(NbSommets-1)+1):
                            ContVallee = 2**24
                            for J in range(self.Isommet[K],self.Isommet[K+1]+1):
                                if self.fncanal(J,2,0) < ContVallee :
                                    ContVallee = self.fncanal(J,2,0)
                                    Ivallee = J
                            Ecart = ContVallee-(Ivallee*self.A1+self.B1)
                            if (Ecart < Numeric.sqrt(self.fncanal(self.Isommet[K],2,0))) and (Ecart < Numeric.sqrt(self.fncanal(self.Isommet[K+1],2,0))):
                                self.Y1 = float(self.Id*self.A1+self.B1)
                                self.Y2 = float(ContVallee)
                                if ContVallee-(Ivallee*self.A1+self.B1) < 0 :
                                    if Ivallee <> oldfi:
                                        self.A1 = float(ContVallee-(oldfi*self.A1+self.B1))/(Ivallee-oldfi)
                                    else:
                                        self.A1 = float(ContVallee-(oldfi*self.A1+self.B1))/1
                                    self.B1 = ContVallee-self.A1*Ivallee
                                self.Fi = Ivallee
                                if Npic > 1 :
                                    self.Multiplet(self.Id,self.Fi)
                                else:
                                    self.TraiPicSimple()
                                Npic = 1
                                self.Id = self.Fi
                            else:
                                Npic=Npic+1
                        self.Fi = oldfi
                        self.Y1 = float(self.Id*self.A1)+float(self.B1)
                        self.Y2 = float(self.Fi*self.A1)+float(self.B1)
                        if Npic > 1 :
                            self.Multiplet(self.Id,self.Fi)
                        else:
                            self.TraiPicSimple()
                    Flag = 0
                    Sum = 0
                    Cmax = 0
                    NbSommets = 0
            if (vres & 1) == 1:
                if Flag == 0:
                    self.Id = Il
                Flag=Flag+1
                Sum = Sum + self.fncanal(Il,2,0)
                if (int(self.fncanal(Il,1,1)) & 2) == 2 :
                    NbSommets=NbSommets+1
                    self.Isommet[NbSommets] = Il
                if (self.fncanal(Il,2,0)) > Cmax:
                    Cmax = self.fncanal(Il,2,0)
# comentei por enquanto - mas isto deve sair daqui
#        self.VisTable.ui.lblespectro.setText(self.vinfo['SourceName'])
#        self.VisTable.ui.lblvivo.setText(str(self.vinfo['TempoVivo']))
#        self.VisTable.ui.lblmorto.setText(str(self.vinfo['TempoTotal']))
# Procedure pour determiner l'abscisse exacte  et la self.Resolution d'un pic
# Determination de la pente du bruit de fond

    def ResAbsiPic(self,Ind,vInf,Mode):
        """Calcula a abscissa exata e a resolução de um pico
        Determina a inclinação do background
        """
        if Mode == 0 :
            Y1 = (float(self.fncanal((Ind-1),2,0) + self.fncanal(Ind,2,0) + self.fncanal((Ind+1),2,0))/3)
            Y2 = (float(self.fncanal((Inf-1),2,0) + self.fncanal(Inf,2,0) + self.fncanal((Inf+1),2,0))/3)
        if (Ind-vInf) == 0:
            A1=0.0
        else:
            A1 = float(self.Y1-self.Y2) / (Ind-vInf)
        B1 = self.Y1 - self.A1*Ind
        self.IntZone(Ind,vInf,Mode)
        self.Absi = self.FNcanexact(0.5,Ind)
        self.Resol = float(self.FNcanexact(0.75,Ind) - self.FNcanexact(0.25,Ind))*self.slope*1.74
        #self.NResol = self.Resolution(self.Energy(self.Absi))
        #print "diferença: Resol - NResol: ", self.Resol - self.NResol

#        self.Resol = float(self.Energy(self.FNcanexact(0.75,Ind)) - self.Energy(self.FNcanexact(0.25,Ind)))



    def ImpRes(self,pIt,pAbsi,pArea,pBgnd,pResol,pId,pFi,pErreur,pLt):
        vdic={}
        vdic['it']   =pIt
        # mudar para pegar a energia da função Energy
        vdic['energia']= self.Energy(pAbsi) #pAbsi*self.slope+self.offset
        vdic['area']=pArea
        vdic['bg']=pBgnd
        vdic['resol']=pResol
        vdic['fi']=pAbsi
        vdic['id']=pId
        vdic['lp']=pFi-pId+1
        vdic['cps']=float(pArea)/pLt
        vdic['erreur']=pErreur
        vr=float("%8.2f" %(vdic['energia']))
        vdic['elem']=0 #xelem[1]
        vdic['meiavida']=0 #xelem[2]
        vdic['massa']=0 #xelem[3]
        self.Vispectdic[self.NoPic]=vdic
        self.NoPic = self.NoPic + 1


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
        for I in range(Deb,Fin+1):
            Sum = Sum + self.fncanal(I,2,0)
        S = Kfin - Kdeb + 1
        if Mode == 0:
            self.Bgnd = self.fncanal(Deb,2,0)+self.fncanal((Deb+1),2,0)+self.fncanal((Deb-1),2,0)+self.fncanal((Fin),2,0)+self.fncanal((Fin+1),2,0)+self.fncanal((Fin-1),2,0)
            self.Bgnd = float(float(self.Bgnd)/6)*S
        if Mode == 1:
            self.Bgnd = float(float(self.Y1+self.Y2)*S)/2
        self.Area = Sum - self.Bgnd

    def TraiPicSimple(self):
#    Tratamento de picos simples
        self.IntZone(self.Id,self.Fi,1)
        if self.Area == 0:
            self.Erreur=0.0
            self.Resol=0.0
            self.Absi=0
        else:
            self.Erreur = float(Numeric.sqrt(abs(self.Bgnd*2+self.Area))*100*self.sig)/self.Area
            self.ResAbsiPic (self.Id,self.Fi,1)
        It = 0
        self.ImpRes(It,self.Absi,self.Area,self.Bgnd,self.Resol,self.Id,self.Fi,self.Erreur,self.Lt)

    def Multiplet(self,Id,Fi):
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
            if (int(self.fncanal(J,1,1)) & 2) == 2 :
                Np=Np+1
                Absi[Np] = J
                OldAbsi[Np] = Absi[Np]
                Ener = float(J*self.slope + self.offset)
                Dlmh[Np] = float((self.ro*(1+self.kres*Numeric.sqrt(Ener))))/(self.slope*2)
                Alp[Np] = float(0.69315)/Dlmh[Np]**2
                OldAlp[Np] = Alp[Np]
                Azo[Np] = float(self.fncanal(J,2,0) - (J*self.A1+self.B1))
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
        while Jtest <> Np:
#    'formation des matrices A,B et W
            L = 0
            for I in range(Id,Fi+1):
                L=L+1
                C[L] = float(self.fncanal(I,2,0)) - (float(I)*self.A1+self.B1)
                if C[L] <= 0.0 :
                    C[L] = 1.0
                W[L] = float(1.0)/C[L]
                Yzot = 0.0
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
#    'formation de la matrice Ainv#
            for J in range(1,Nx+1):
                for K in range(1,Nx+1):
                    Ainv[J,K] = 0.0
                    for I in range(1,Nc+1):
                        Ainv[J,K] = float(Ainv[J,K] + A[I,J]*W[I]*A[I,K])
#    ' Inversion de la matrice

            Ainv=self.InvMd(Nx+1,Ainv)
#    ' formation de la matrice V
            for J in range(1,Nx+1):
                V[J] = 0
                for I in range(1,Nc+1):
                    V[J] = float(V[J] + A[I,J]*W[I]*B[I])
#    ' Solution
            for I in range(1,Nx+1):
                T[I] = 0
                for J in range(1,Nx+1):
                    T[I] = T[I] + Ainv[I,J]*V[J]
                    aa=Ainv[I,J]
#    ' Test de convergence
            Jtest = 0
            for J in range(1,Np+1):
                Dif3 = 0.0
                K = 1 + Jv*(J-1)
                Azo[J] = Azo[J] + T[K]
                if Azo[J] <= 0.0 :
                    Sortie=Sortie+1
                    break
                Dif1 = abs(float(T[K])/Azo[J])
                raux = long(float(Absi[J]) + float(T[K+1]))
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
                if Dif1 < 0.01 and Dif2 < 0.01 and Dif3 < 0.01 :
                    Jtest=Jtest+1
            It=It+1
            if It == 10 :
                break
    # Si non convergence, on impose la self.Resolution
            if Sortie > 0 :
                for J in range(1,Np+1):
                    Absi[J] = OldAbsi[J]
                    Alp[J] = OldAlp[J]
                    Azo[J] = self.fncanal(int(Absi[J]),2,0) - (Absi[J]*self.A1+self.B1)
                Sortie = 0
                Jv = 2
                Nx = Jv*Np
        if Sortie == 0 :
    #' Calcul statistique et sortie correcte
            Socare = 0.0
            Chi2 = 0.0
            for I in range(1,Nc+1):
                Res[I] = 0
                Yt[I] = 0
                for J in range(1,Np+1):
                    Yg[J,I] = 0
            I = 0
            for K in range(Id,Fi+1):
                I=I+1
                for J in range(1,Np+1):
                    Mu = -Alp[J]*(K-Absi[J])**2
                    if Mu < -81 :
                        Yg[J,I] = 0
                    else:
                        Yg[J,I] = Azo[J]*Numeric.exp(Mu)
                    Yt[I] = Yt[I] + Yg[J,I]
                Res[I] = self.fncanal(K,2,0) - (K*self.A1+self.B1) - Yt[I]
                Socare = Socare + Res[I]*Res[I]*W[I]
                if self.fncanal(K,2,0) <> 0 :
                    Res[I] = float(Res[I]*Res[I])/self.fncanal(K,2,0)
                Chi2 = Chi2 + Res[I]
            Xndl = Nc - Nx
            Chi2 = float(Chi2)/Xndl
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
                if (2*self.Bgnd) > Sur[J]:
                    self.Erreur = float(self.sig*100*Numeric.sqrt(2*self.Bgnd+Sur[J]))/Sur[J]
                else:
                   self.Erreur = 0

                self.ImpRes(It,Absi[J],Sur[J],self.Bgnd,Resk,Id,Fi,self.Erreur,self.Lt)


#'        Procedure d'invertion de matrice
    def InvMd(self,N,A):
     #cria matriz con n elemento, mais um espaco de n elementos para preencher
        AB=Numeric.zeros([N,(N)*2], Numeric.Float64)
        BB=Numeric.zeros([N,(N)*2], Numeric.Float64)
#preenche os primeiros n elementos com a matriz A
        for I in range(1,N):
            for J in range(1,N):
                AB[I,J] = A[I,J]
#silvio
        Id = N + 1
        Fi = N * 2
#preenche com zeros o segundo espaco da matriz AB
        for I in range(1,N):
            for J in range(Id,Fi):
                AB[I,J] = 0.0
# coloca o numero 1 na diagonal da segunda parte da matriz
        for I in range(1,N):
            J = I + N
            AB[I,J] = 1
#esta rotina pega o primeiro termo da matriz AB e divide pela linha inteira da matriz AB depois continua para a segunda linha até o fim da matriz AB
# colocando o resultado na matriz BB, depois continua ......
        for K in range(1,N):
            for J in range(1,Fi):
                if AB[K,K] <> 0.0:
                    BB[K,J] = float(AB[K,J])/AB[K,K]
            for I in range(1,N):
                if I <> K:
                    for J in range(1,Fi):
                        BB[I,J] = AB[I,J] - AB[I,K]*BB[K,J]
            for I in range(1,N):
                for J in range(1,Fi):
                    AB[I,J] = BB[I,J]
        for I in range(1,N):
            for J in range(1,N):
                K = J + N
                A[I,J] = AB[I,K]
        return A


##############################################################


def testDissert(nivel = 15):
    """function to test the vispect peak search algorithm against some spectra used
    in the Silvio Master Thesis.
    The output will be the comparison between the values of CSV file and calculated ones.
    """
    """Energy, Counts, Centroid, FWHM, Actual counts, Actual centroid """
    import sys, time
    import crtLerEspectro as lesp
    import numpy as np

    #arquivos = ["CritLimit100.chn", "CritLimit10k.chn", "CritLimit1k.chn",  "LD-100.chn",  "LD-10k.chn",  "LD-1k.chn", "QCYKpeaks.chn"]
    arquivos = ["MT4-B.CHN", "112-1B.CHN"]
    #arquivosref = ["CritLimit100.csv", "CritLimit10k.csv", "CritLimit1k.csv",  "LD-100.csv",  "LD-10k.csv",  "LD-1k.csv", "QCYKpeaks.csv"]
    arquivosref = ["QCYKpeaks.csv","QCYKpeaks.csv"]
    j = 0
    dirarq = "../espectros/Silvio-Thesis/"

    for j in range(len(arquivos)):
        arq = arquivos[j]
        arqref = arquivosref[j]
        arquivo = dirarq + arq
#        arquivo = "../espectros/SpecMaker/"+arq
        vfit = VispectFit()
        obj = lesp.LerVispect(arquivo)
        data = obj.ler_MCAeCHN()
        if data == None:
            print "Erro ao ler arquivo"
            return
        vfit.Lt = data.info['TempoVivo']
        vfit.vy=np.array(data.y[0],np.float64)
        # data from SpecMaker manual as informed by email msg from Dr. Gilmore
        data.info['slope'] = 0.2491279989480972
        data.info['offset']= -.9475258588790894
        data.info['enerquad'] = 0.0
        data.info['ro']    = 0.5267921090126038
        data.info['kres']  = 6.619893759489059E-002
        data.info['widthquad']= 0.0
        data.info['Nivel'] = nivel
        data.info['ArqCalib']  = ' '
        resultado = vfit.vispectfit(data.x[0][0],data.x[0][-1],data.info).copy()
        resultcomp = [[x['energia'],x['area'],x['fi'],x['resol'],x['erreur']] for x in [resultado[y] for y in range(len(resultado))]]
#        print resultado, vfit.vy[1:10], data.x[0][1:10],data.x[0][-1],data.y[0][1:10]
        """Energy, Counts, Centroid, FWHM, Actual counts, Actual centroid """
        try:
            tmparq = "/tmp/"+"SLucDis"+arq[:-3]+"CSV"
            tres = open(tmparq, 'w')
            tres.write("Energia, Contagem, Centroide, Resolucao, Erro\n")
            for res in resultcomp:
                tres.write("%7.2f, %10.2f, %12d, %4.2f, %5.5f\n" % (res[0],res[1],res[2],res[3],res[4]))
            tres.close()
        except:
            print resultcomp
        vfit = None
        j += 1



########-------------------------------#######################

def testGeneric(dirarqs="../espectros/Debora/geologico/", arquivs=["asbrs012.mca","brs01-1.mca","fn100a-2.chn"] , nivel = 15):
    """function to test the vispect peak search algorithm against some generated spectra
    To test, call the module with -t option and a spectrum file name (from SpecMaker test spectra).
    There would be a CSV file with the same name as the spectrum file -- the assessment file generated by
    SpecMaker. The output will be the comparison between the values of CSV file and calculated ones.
    """
    """Energy, Counts, Centroid, FWHM, Actual counts, Actual centroid """
    import sys, time
    import crtLerEspectro as lesp
    import numpy as np

    arquivos = arquivs
    arquivosref = arquivos
    j = 0
    dirarq = dirarqs

    for j in range(len(arquivos)):
        arq = arquivos[j]
        arqref = arquivosref[j]
        arquivo = dirarq + arq
        vfit = VispectFit()
        obj = lesp.LerVispect(arquivo)
        data = obj.ler_MCAeCHN()
        if data == None:
            print "Erro ao ler arquivo"
            return
        vfit.Lt = data.info['TempoVivo']
        vfit.vy=np.array(data.y[0],np.float64)
        # Nestes espectros foi utilizado o Canberra 3
        # Os dados de calibração são:
        # slope = .250454843044281    offset =  .6895981431007385 
        # ro = .7115383744239807        kres =    4.069770872592926E-002 
        data.info['slope'] = .250454843044281
        data.info['offset']= .6895981431007385 
        data.info['enerquad'] = 0
        data.info['ro']    =.7115383744239807
        data.info['kres']  = 4.069770872592926E-002 
        data.info['widthquad']= 0
        data.info['Nivel'] = nivel
        data.info['ArqCalib']  = ' '
        resultado = vfit.vispectfit(data.x[0][0],data.x[0][-1],data.info).copy()
        resultcomp = [[x['energia'],x['area'],x['fi'],x['resol'],x['erreur']] for x in [resultado[y] for y in range(len(resultado))]]
#        print resultado, vfit.vy[1:10], data.x[0][1:10],data.x[0][-1],data.y[0][1:10]
        """Energy, Counts, Centroid, FWHM, Actual counts, Actual centroid """
        try:
            tmparq = "/tmp/"+"ASS"+arq[:-3]+"CSV"
            tres = open(tmparq, 'w')
            tres.write("Energia, Contagem, Centroide, Resolucao, Erro\n")
            for res in resultcomp:
                tres.write("%7.2f, %10.2f, %12f, %4.2f, %5.5f\n" % (res[0],res[1],res[2],res[3],res[4]))
            tres.close()
        except:
            print resultcomp
        vfit = None
        j += 1



def testSpecMaker(nivel = 4):
    """function to test the vispect peak search algorithm against some generated spectra
    To test, call the module with -t option and a spectrum file name (from SpecMaker test spectra).
    There would be a CSV file with the same name as the spectrum file -- the assessment file generated by
    SpecMaker. The output will be the comparison between the values of CSV file and calculated ones.
    """
    """Energy, Counts, Centroid, FWHM, Actual counts, Actual centroid """
    import sys, time
    import crtLerEspectro as lesp
    import numpy as np

    arquivos = ["CritLimit100.chn", "CritLimit10k.chn", "CritLimit1k.chn",  "LD-100.chn",  "LD-10k.chn",  "LD-1k.chn", "QCYKpeaks.chn"]
    #arquivos = ["QCYKpeaks.chn"]
    arquivosref = ["CritLimit100.csv", "CritLimit10k.csv", "CritLimit1k.csv",  "LD-100.csv",  "LD-10k.csv",  "LD-1k.csv", "QCYKpeaks.csv"]
    #arquivosref = ["QCYKpeaks.csv"]
    j = 0
    dirarq = "../espectros/SpecMaker/"

    for j in range(len(arquivos)):
        arq = arquivos[j]
        arqref = arquivosref[j]
        arquivo = dirarq + arq
#        arquivo = "../espectros/SpecMaker/"+arq
        vfit = VispectFit()
        obj = lesp.LerVispect(arquivo)
        data = obj.ler_MCAeCHN()
        if data == None:
            print "Erro ao ler arquivo"
            return
        vfit.Lt = data.info['TempoVivo']
        vfit.vy=np.array(data.y[0],np.float64)
        # data from SpecMaker manual as informed by email msg from Dr. Gilmore
        #The calibration equations are:
        # Energy:  keV = -3.87  + 0.26931 * ch  -4.706 E-10*ch^2
        #Width  keV = 0.716 + 9.730 E-4 * keV - 1.02384 E-7 keV^2
        #or      ch = 2.66 + 9.730 E-4 *ch   -2.76E-08 * ch^2
        data.info['slope'] = 0.26931
        data.info['offset']= -3.87
        data.info['enerquad'] = -4.706e-10
        data.info['ro']    = 0.716
        data.info['kres']  = 9.73e-4
        data.info['widthquad']= -1.02384e-7
        data.info['Nivel'] = nivel
        data.info['ArqCalib']  = ' '
        resultado = vfit.vispectfit(data.x[0][0],data.x[0][-1],data.info).copy()
        resultcomp = [[x['energia'],x['area'],x['fi'],x['resol'],x['erreur']] for x in [resultado[y] for y in range(len(resultado))]]
#        print resultado, vfit.vy[1:10], data.x[0][1:10],data.x[0][-1],data.y[0][1:10]
        """Energy, Counts, Centroid, FWHM, Actual counts, Actual centroid """
        try:
            tmparq = "/tmp/"+"ASS"+arq[:-3]+"CSV"
            tres = open(tmparq, 'w')
            tres.write("Energia, Contagem, Centroide, Resolucao, Erro\n")
            for res in resultcomp:
                tres.write("%7.2f, %10.2f, %12d, %4.2f, %5.5f\n" % (res[0],res[1],res[2],res[3],res[4]))
            tres.close()
        except:
            print resultcomp
        vfit = None
        j += 1

def testIAEA(nivel = 10):
    """function to test the vispect peak search algorithm against some generated spectra
    To test, call the module with -t option and a spectrum file name (from SpecMaker test spectra).
    There would be a CSV file with the same name as the spectrum file -- the assessment file generated by
    SpecMaker. The output will be the comparison between the values of CSV file and calculated ones.
    """
    """Energy, Counts, Centroid, FWHM, Actual counts, Actual centroid """
    import sys, time, os
    import crtLerEspectro as lesp
    import numpy as np

    arquivos = ["ADD10N1.ASC", "ADD1N1.ASC", "ADD3N1.ASC", "DISTORT.ASC" , "ADD1N100.ASC", "ADD1N3.ASC", "STRAIGHT.ASC"]
    arquivosref = ["ADD10N1.REF", "ADD1N1.REF", "ADD3N1.REF", "DISTORT.REF" , "ADD1N100.REF", "ADD1N3.REF", "STRAIGHT.REF"]
    dirarq = "../espectros/IAEA-1995/TSTSPEC/"
    dirref = "../espectros/IAEA-1995/REFRSL/"
    cmpprog = " wineconsole ../espectros/IAEA-1995/PROGS/CMPSPEC.EXE"
    j = 0
    for j in [0]:  #range(len(arquivos)):
        arq = arquivos[j]
        arqref = arquivosref[j]
        arquivo = dirarq + arq
        obj = lesp.LerVispect(arquivo)
        data = obj.ler_MCAeCHN()
        vfit = VispectFit()
        if data == None:
            print "Erro ao ler arquivo"
            return
        vfit.Lt = data.info['TempoVivo']
        vfit.vy=np.array(data.y[0],np.float64)
        data.info['slope'] = 0.2
        data.info['offset']= 0.3
        data.info['enerquad'] = -4.71e-10
        data.info['ro']    = 0.5
        data.info['kres']  = 0.039
        data.info['widthquad']= -1.02e-7
        data.info['ArqCalib']  = ' '
        data.info['Nivel'] = nivel
        resultado = vfit.vispectfit(data.x[0][0],data.x[0][-1],data.info).copy()
        resultcomp = [[x['energia'],x['energia']*0.01,x['area'],x['erreur']] for x in [resultado[y] for y in range(len(resultado))]]
        try:
            tmparq = "/tmp/"+arq[:-3]+"RES"
            tres = open(tmparq, 'w')
            for res in resultcomp:
                tres.write("%7.2f %5.2f %12d %9.2f\n" % (res[0],res[1],res[2],res[3]))
            tres.close()
#            print "Comparando %s e %s\n" % (dirref + arqref, arquivo)
#            os.system("%s %s %s" % (cmpprog, dirref + arqref, tmparq))
        except:
            print resultcomp
#        arquivoref = dirref + arqref
#        try:
#            arqr = open(arquivoref,'r')
#        except:
#            print resultcomp
#            print "arquivo referencia nao aberto, terminando!"
#        linhas = arqr.readlines()
#        comparacao = []
#        for l in linhas:
        vfit = None
        j += 1

def toDAT(especname=None,filename=None):
    """An utility function to write a spectrum to a ascii file, containing
    channel number and count only"""

    import crtLerEspectro as lesp

    if especname is None:
        especname = "../espectros/cp-1a.mca"
        # if especname was not supplied, give the same base name to output
        # file but the extension (dat)
        if filename is None:
            filename = "/tmp/cp-1a.dat"
    # especname was supplied
    if filename is None:
        # but filename not; then pick a name generated by os.tmpnam() function
        import os
        filename = os.tmpnam()

    obj = lesp.LerVispect(especname)
    data = obj.ler_MCAeCHN()
    try:
       f = open(filename,'w')
       #print "datax =", data.x
       print len(data.x[0]), len(data.y[0])
       for i in range(len(data.x[0])):
           f.write("%d\t%d\n" % (data.x[0][i],data.y[0][i]))
       f.flush()
       f.close()
       print "Sucesso! Espectro gravado em ", filename
    except:
       print "Erro abrindo arquivo de saida ...",filename

#The ASCII fileformat for both should be identical:
#   - One peak per line
#   - For each peak energy, its uncertainty, area, its uncertainty, [0 or 1]
#   - The uncertainties must be absolute 1 standard deviation uncertainties
#   - The four numbers must be separated by spaces only
#   - The last number is meaningful in the reference file only. If 0, the
#     peak is disregarded in the comparison, if 1, the peak is used if its
#     energy is larger than 100 keV
# {'meiavida': 0, 'bg': 3.0, 'area': 6.0, 'it': 0, 'elem': 0, 'energia': 1840.0253322580645, 'massa': 0, 'erreur': 57.735026918962575, 'lp': 9, 'fi': 7508.822580645161, 'resol': 0.81134516129036005, 'cps': 0.0015182186234817814, 'id': 7504}


if __name__ == "__main__":
    import sys,time
    import crtLerEspectro as lesp
    try:
        arquivo=sys.argv[1]
    except:
        print "Chamar por: LerVispect nome-do-arquivo(CHN ou MCA) nome-do-arquivo.dat"
        sys.exit()
    obj = lesp.LerVispect(arquivo)
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


#        vobj = crtLerEspectro.LerVispect(vfile)
#        vdata = vobj.ler_MCAeCHN()

#        print "info = ",vdata.info
#        print "datay = ",vdata.y[0],  "type(datay)",  type(vdata.y[0])
  #      print "datax = ",vdata.x[0],  "type(datax)",  type(vdata.x[0])
#        dataObject = vdata
#        self.dataObjectsDict[legend] = dataObject
# por enquanto estou atribuindo os valores de calibracao a todos os espectros,
#        self.dataObjectsDict[legend].info['slope'] = 1.0
#        self.dataObjectsDict[legend].info['offset']= 0.0
#        self.dataObjectsDict[legend].info['ro']    = 1.0
#        self.dataObjectsDict[legend].info['kres']  = 1.0
#        self.dataObjectsDict[legend].info['ArqCalib']  = ' '


#The first command-line argument is supposed to be the name of the reference
#file, the second of the file to be tested.
#The ASCII fileformat for both should be identical:
#   - One peak per line
#   - For each peak energy, its uncertainty, area, its uncertainty, [0 or 1]
#   - The uncertainties must be absolute 1 standard deviation uncertainties
#   - The four numbers must be separated by spaces only
#   - The last number is meaningful in the reference file only. If 0, the
#     peak is disregarded in the comparison, if 1, the peak is used if its
#     energy is larger than 100 keV


#        Res_Correl = self.Resolution(self.Energy((self.ideb+self.ifin)/2))
#        Nc_Correl = int(Res_Correl/self.vinfo['slope']) -2
#        print "rescorrel: %4.4f   nccorrel: %5d   Res_Correl: %4.4f  Nc_Correl: %5d\n" % (rescorrel, nccorrel, Res_Correl, Nc_Correl)
