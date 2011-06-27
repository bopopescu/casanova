#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def pmat(mat):
    for linha in mat:
        print linha

def menor(a, b, c):
    if a<=b and a<=c:
        return a
    elif b<=a and b<=c:
        return b
    else:
        return c

def levenshteinDistance(strO, strD):
    # roubada para acrescentar uma linha e uma coluna
    strO = " " + sys.argv[1]
    strD = " " + sys.argv[2]
    
    mat = []
    for x, a in enumerate(strO):
        l=[] 
        mat.insert(x,l)
        for y, b in enumerate(strD):
            mat[x].insert(y,l)
            mat[x][y] = []
            mat[x][y] = 0 

    for x, a in enumerate(strO):
        mat[x][0] = 0

    for y, b in enumerate(strD):
        mat[0][y] = 0
            
    for x, a in enumerate(strO):
        if a!=' ':
            for y, b in enumerate(strD):
                if b!=' ':
                    if a==b:
                        cost = 0
                    else:
                        cost = 1
                    
                    m = menor(mat[x-1][y] + 1,      # Deletar
                                          mat[x][y-1] + 1,      # Inserir
                                          mat[x-1][y-1] + cost  # Substituir
                                      )
                    mat[x][y] = m
    #pmat(mat)
    print "São necessárias %s operações para sair de %s para %s" % (m,strO,strD)
    
print "Algorítimo de distância de edição"
if len(sys.argv) < 3:
    print "favor entre com as strings de origem e destino"
else:
    strO = sys.argv[1]
    strD = sys.argv[2]
    print "string de origem %s, e de destino %s" % (strO, strD)
    levenshteinDistance(strO, strD)


  
"""
Função LevenshteinDistance(Caracter : str1[1..lenStr1], Caracter : str2[1..lenStr2]) : INTEIRO
  Ínicio
   // tab é uma tabela com lenStr1+1 linhas e lenStr2+1 colunas
   Inteiro:  tab[0..lenStr1, 0..lenStr2]
   // X e Y são usados para interagir str1 e str2
   Inteiro:  X, Y, cost
 
   Para X de 0 até lenStr1
       tab[X, 0] <- X
   Para Y de 0 até lenStr2
       tab[0, Y] <- Y
 
   Para X de 1 até lenStr1
       Para Y de 1 até lenStr2
           Se str1[X] = str2[Y] Então cost <- 0
                                Se-Não cost <- 1
           d[X, Y] := menor(
                                tab[X-1, Y  ] + 1,     // Deletar
                                tab[X  , Y-1] + 1,     // Enserir
                                tab[X-1, Y-1] + cost   // Substituir
                            )
 
   LevenshteinDistance <- tab[lenStr1, lenStr2]
  Fim
  
"""