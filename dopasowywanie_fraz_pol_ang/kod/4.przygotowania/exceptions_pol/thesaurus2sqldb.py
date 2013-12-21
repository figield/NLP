#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from locale import *
from string import *
from databasemanager import *
  
p2 = re.compile('[ ]+',re.L)
exce_set = set()

def find_exceptions(dbm,arg):
    
    caly_slownik = open(arg,"r").read()
    lista_list_synonimow = re.compile('\n',re.L).split(caly_slownik)
   
    p1 = re.compile(';',re.L)
    lista_istniejacych_juz_synonimow = dbm.getExceptionPol()

    for lista_synonimow_str in lista_list_synonimow:

        lista = p1.split(lista_synonimow_str)
        syn1 = lista[0].strip()

        for w in lista[1:]:
            if (syn1,w) in lista_istniejacych_juz_synonimow:
                print (syn1,w)
            else:
                exce_set.add((syn1,w))
  
def main():     
    dbm = DBmanager() 
    find_exceptions(dbm,sys.argv[1])
    print str(len(exce_set))
    for (word1,word2) in exce_set:
        dbm.insertExceptionPol(word1, word2, "", "")

if __name__ == '__main__':
    main()
