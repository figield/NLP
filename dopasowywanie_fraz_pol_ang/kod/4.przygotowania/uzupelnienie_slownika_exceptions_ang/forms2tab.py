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
    p2 = re.compile(',',re.L)

    print "Przetwarzanie pliku \'%s\'  i wczytywanie do tabeli \'irregularVerbs\' " % arg
    for line in listOfVerbs:
        list1 = p1.split(line)
        if len(list1) == 4:
            verbAng1 = list1[0].strip()
            verbAng2 = list1[1].strip()
            verbAng3 = list1[2].strip()
            verbsPl = list1[3].strip()
            verbsListPl = p2.split(verbsPl)
            verbsListPl2 = set()
        
            for verbPl in verbsListPl:
                verbsListPl2.add(verbPl.strip())
        
            for verbPl in verbsListPl2:
                if len(verbPl) > 2 :
                    dbm.insertIrregularVerb(verbAng1,verbAng2,verbAng3,verbPl)

def main():    
    file_name = sys.argv[1]
    dbm = DBmanager() 
    add_forms(file_name,dbm)


if __name__ == '__main__':
    main()
