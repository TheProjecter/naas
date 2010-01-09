# -*- coding: utf-8 -*-

import numpy as np
import crtConcentracao
import Elementos
import QtBlissGraph
qt = QtBlissGraph.qt
import os
import sys, string


class VispectFit:
    def __init__(self):
        self.dataObjectsDict = {}
        self.Isommet=np.zeros([200], np.int32)
        self.VisTable = crtConcentracao.startGui()
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
        self.InitChannel=None
        self.FinalChannel=None
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
        self.vy=np.array([],np.float64)



    def FNcanal(self,i,nfoco,acao): #I, N_fonction, N_bit):
        """Esta função desempenha quatro ações segundo o núm. N_fonction
        1 - Permite obter o byte forte de um canal (byte de estado).
        2 - Permite mascarar o byte forte de um canal e assim obter o seu conteúdo (valor).
        3 - Permite ativar um bit de estado do byte forte segundo a variável N_bit (0 - 7)
        4 - Permite desativar o bit de estado do byte forte segundo a variável N_bit (0 - 7)

        I - núm do canal de trabalho
        """
        decal=16777216
        octetfort = int(int(self.vy[i])/decal)
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


        def Energy(self,i):
            """Determinação da energia de um dado canal"""
            return Energy = (i*(i*(Coef_A_Cal_Ener + Coef_B_Cal_Ener) + Coef_C_Cal_Ener))



    { Détermination de l'énergie d'un canal donné }

FUNCTION Energy ( No_Can : Integer) : Real;
BEGIN
  Energy :=((No_Can)*((No_Can)*Coef_A_Cal_Ener+Coef_B_Cal_Ener)+Coef_C_Cal_Ener);
END;

    { Détermination de la résolution pour une énergie donné }

FUNCTION Resolution ( Ener : Real) : Real;
BEGIN
  IF ((Ener < 513) AND (Ener > 509)) THEN Ener := Ener*1.8;
  Resolution := Ro + K_Res*Ener;
END;

    { Fonction recherche début de zone }
FUNCTION FNzonDeb : INTEGER;
VAR
   Co : LONGINT;
BEGIN
     FOR Il := K_Can DOWNTO (K_Can - (Nc_Correl+1)*2) DO
         BEGIN
              Id := Il -1;
              IF Il < 3 THEN EXIT;
              Co := FNcanal((Il-1),2,0) + FNcanal((Il-2),2,0);
              IF (FNcanal(Il,2,0)+Co <= FNcanal(Il-3,2,0)+Co) OR (Il = (K_Can - Nc_Correl*2)) THEN
              BEGIN
                   Moy_Amont := ((FNcanal(Il,2,0)+Co) DIV 3);
                   FlZdeb := True;
                   FNzonDeb := Id;
                   EXIT;
              END;
         END;
END;
     { Fonction recherche fin de zone }
FUNCTION FNzonFin : INTEGER;
VAR
   Co : LONGINT;
BEGIN
     FOR Il := K_Can TO (K_Can+(Nc_Correl+1)*3) DO
     BEGIN
          Fi := Il + 1;
          Co := FNcanal(Il+1,2,0) + FNcanal(Il+2,2,0);
          IF ((FNcanal(Il,2,0) <= Moy_Amont)
           AND (FNcanal(Il,2,0) + Co <= FNcanal(Il+3,2,0) + Co))
           OR (Il = (K_Can+(Nc_Correl + 1)*3)) THEN
          BEGIN
               Moy_Aval := ((FNcanal(Il,2,0)+Co) DIV 3);
               FlZfin := True;
               FNzonFin := Fi;
               EXIT;
          END;
     END;
END;












