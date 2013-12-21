#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from locale import *
from string import *
from databasemanager import *
  

def main():     
    dbm = DBmanager() 
    caly_plik = open(sys.argv[1],"r").read()
    typ = sys.argv[2]
    lista_wierszy = re.compile('\n',re.L).split(caly_plik)  
    p1 = re.compile(',',re.L)
    
    for wiersz in lista_wierszy:
        dane = p1.split(wiersz)
        if len(dane) > 1:
            if typ == "NP":
                print dane[0][1:-1] + "; " + dane[1][1:-1] + "; " + dane[2][1:-1] + "; " + dane[3][1:-1] + "; " + dane[4][1:-1] + "; " + dane[5][1:-1] + "; " + dane[6][1:-1] + "; " + dane[7][1:-1]
                dbm.insertNP(dane)
            elif typ == "VP":
                print dane[0][1:-1] + "; " + dane[1][1:-1] + "; " + dane[2][1:-1] + "; " + dane[3][1:-1] + "; " + dane[4][1:-1] + "; " + dane[5][1:-1] + "; " + dane[6][1:-1] + "; " + dane[7][1:-1]
                dbm.insertVP(dane)
            elif typ == "P":
                print dane[0][1:-1] + "; " + dane[1][1:-1]
                dbm.insertP(dane)

if __name__ == '__main__':
    main()
