#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from locale import *
from string import *
  
def select(arg):
    FileIn = open(arg,"r").read()
    FileIn = FileIn.replace('\"','')
    FileOut = open("selected_" + arg ,"w")
    listOfLines = re.compile('\n',re.L).split(FileIn)
    #p1 = re.compile('\t',re.L)
    #p2 = re.compile(',',re.L)
    Len = len(listOfLines)
    print Len
    diff = Len / 250
    print diff    

    print "Przetwarzanie pliku"
    i = 0
    while i < Len:
        FileOut.write(listOfLines[i]+"\n")
        i = i + diff

def main():    
    file_name = sys.argv[1] 
    select(file_name)


if __name__ == '__main__':
    main()
