#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from locale import *
from string import *
from databasemanager import *
  
def add_forms(arg,dbm):
    wholeFile = open(arg,"r").read()
    listOfAdj = re.compile('\n',re.L).split(wholeFile)
    p1 = re.compile('\t',re.L)

    print "Przetwarzanie pliku \'%s\'  i wczytywanie do tabeli \'irregularAdjectiv\' " % arg
    for line in listOfAdj:
        list1 = p1.split(line)
        if len(list1) == 3:
            adjAng1 = list1[0].strip()
            adjAng2 = list1[1].strip()
            adjAng3 = list1[2].strip()
            dbm.insertIrregularAdj(adjAng1,adjAng2,adjAng3)

def main():    
    file_name = sys.argv[1]
    dbm = DBmanager() 
    add_forms(file_name,dbm)

if __name__ == '__main__':
    main()
