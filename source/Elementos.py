# -*- coding: ISO-8859-1 -*-
# Recupera tabela (nuclear) com elementos, energias , meia vida para localização dos elementos através das energias
import sys, string
from os.path import isfile
from os import chdir
import os

class Elementos:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.elem=[]
        self.ler_ArqElementos()

    def ler_ArqElementos(self):
# Abre e lê o arquivo (tabela) de elementos     
        f = open(self.arquivo)
        self.elem = []
# ignora primeira linha cabec.
        linha = f.readline()
        linha = f.readline()
        while (len(linha)):
            self.elem.append(eval(linha))
            linha = f.readline()

    def carrega_lista(self,pcombo):
# Eletua a busca da energia retornando o elemento    
        for i in range(len(self.elem)):
            see=self.elem[i][1]+"("+str(self.elem[i][0])+")"


    def busca_elem(self,penergia,pelem=''):
# Eletua a busca da energia retornando o elemento    
        if (pelem==''):
           for i in range(len(self.elem)):
              if self.elem[i][0] == penergia:
                 return self.elem[i]
        else:
           for i in range(len(self.elem)):
              if (self.elem[i][0] == penergia) & (self.elem[i][1] == pelem):
                 return self.elem[i]
        return (0,'',0,0)
