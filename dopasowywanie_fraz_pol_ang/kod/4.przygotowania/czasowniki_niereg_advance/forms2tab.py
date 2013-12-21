#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from locale import *
from string import *
from databasemanager import *
  
def add_forms(arg,dbm):
    wholeFile = open(arg,"r").read()
    listOfVerbs = re.compile('\n',re.L).split(wholeFile)
    p1 = re.compile('\t',re.L)

    print "Przetwarzanie pliku \'%s\'  i wczytywanie do tabeli \'irregularVerbsAdvance\' " % arg
    for line in listOfVerbs:
        list1 = p1.split(line)
        if len(list1) == 5:
            verbAng1 = list1[0].strip().lower()
            verbAng2 = list1[1].strip().lower()
            verbAng3 = list1[2].strip().lower()
            verbAng4 = list1[3].strip().lower()
            verbAng5 = list1[4].strip().lower()
            
            dbm.insertIrregularVerbAdvance(verbAng1,verbAng2,verbAng3,verbAng4,verbAng5)

def main():    
    file_name = sys.argv[1]
    dbm = DBmanager() 
    add_forms(file_name,dbm)


if __name__ == '__main__':
    main()
