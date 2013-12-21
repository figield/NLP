#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from locale import *
from string import *
from databasemanager import *
  
def add_exceptions(arg,dbm):
    wholeFile = open(arg,"r").read()
    listOfVerbs = re.compile('\n',re.L).split(wholeFile)
    p1 = re.compile('\t',re.L)
    p2 = re.compile(',',re.L)

    print "Przetwarzanie pliku \'%s\'  i wczytywanie do tabeli \'exceptions_ang\' " % arg
    for line in listOfVerbs:
        list1 = p1.split(line)
        if len(list1) == 4:
            verbAng1 = list1[0].strip()
            verbAng2 = list1[1].strip()
            verbAng3 = list1[2].strip()
            if verbAng1 != verbAng2:
                if dbm.getExceptionExist(verbAng2,verbAng1) < 1:
                    dbm.insertException(verbAng2,verbAng1,"v.","2")
            if verbAng1 != verbAng3:
                if dbm.getExceptionExist(verbAng3,verbAng1) < 1:
                    dbm.insertException(verbAng3,verbAng1,"v.","3")

def main():    
    file_name = sys.argv[1]
    dbm = DBmanager() 
    add_exceptions(file_name,dbm)


if __name__ == '__main__':
    main()
