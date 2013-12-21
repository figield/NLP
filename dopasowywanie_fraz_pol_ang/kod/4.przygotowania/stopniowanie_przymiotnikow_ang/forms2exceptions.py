#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from locale import *
from string import *
from databasemanager import *
  
def add_exceptions(arg,dbm):
    wholeFile = open(arg,"r").read()
    listOfadjs = re.compile('\n',re.L).split(wholeFile)
    p1 = re.compile('\t',re.L)

    print "Przetwarzanie pliku \'%s\'  i wczytywanie do tabeli \'exceptions_ang\' " % arg
    for line in listOfadjs:
        list1 = p1.split(line)
        if len(list1) == 3:
            adjAng1 = list1[0].strip()
            adjAng2 = list1[1].strip()
            adjAng3 = list1[2].strip()
            if adjAng1 != adjAng2:
                if dbm.getExceptionExist(adjAng2,adjAng1) < 1:
                    dbm.insertException(adjAng2,adjAng1,"adi.","2")
            if adjAng1 != adjAng3:
                if dbm.getExceptionExist(adjAng3,adjAng1) < 1:
                    dbm.insertException(adjAng3,adjAng1,"adi.","3")

def main():    
    file_name = sys.argv[1]
    dbm = DBmanager() 
    add_exceptions(file_name,dbm)


if __name__ == '__main__':
    main()
