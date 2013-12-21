#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from locale import *
from string import *
from databasemanager import *
  
def add_names(arg,dbm,sex):
    wholeFile = open(arg,"r").read()
    listOfVerbs = re.compile('\n',re.L).split(wholeFile)

    print "Przetwarzanie pliku \'%s\'  i wczytywanie do tabeli \'names\' " % arg
    for line in listOfVerbs:
        name = line.replace('\'','\\\'').strip()
        dbm.insertNames(name,sex)

def main():    
    file_name = sys.argv[1]
    sex = sys.argv[2]
    dbm = DBmanager() 
    add_names(file_name,dbm,sex)


if __name__ == '__main__':
    main()
