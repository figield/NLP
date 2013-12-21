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

    print "Przetwarzanie pliku \'%s\'  i wczytywanie do tabeli \'dictionary\' " % arg
    for line in listOfVerbs:
        list1 = p1.split(line)
        if len(list1) == 4:
            verbAng = list1[0].strip()
            print "Ang: " + verbAng
            verbsPl = list1[3].strip()
            verbsListPl = p2.split(verbsPl)
            verbsListPl2 = set()
        
            for verbPl in verbsListPl:
                verbsListPl2.add(verbPl.split()[0].strip())
        
            for verbPl in verbsListPl2:
                if len(verbPl) > 2 :
                    print "Pol: " + verbPl
                    checkAndWrite(verbAng,verbPl,dbm)


def checkAndWrite(verbAng,verbPl,dbm):    
    if dbm.getTranslationExist(verbPl,verbAng) == 0:
        print "dodanie: %s - %s" % (verbPl,verbAng)
        dbm.insertTranslation(verbPl,verbAng,"v.","")

          
def main():    
    file_name = sys.argv[1]
    dbm = DBmanager() 
    add_forms(file_name,dbm)


if __name__ == '__main__':
    main()
