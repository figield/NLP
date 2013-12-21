#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from locale import *
from string import *
from databasemanager import *
  
p2 = re.compile('[ ]+',re.L)
exce_set = set()

def find_exceptions(arg):
    
    caly_slownik = open(arg,"r").read()
    lista_tlumaczen = re.compile('\n',re.L).split(caly_slownik)
   
    p1 = re.compile('=',re.L)
    value=""
    word=[]
    name=""
    num = 1  # 1,2
 
    for tlumaczenie in lista_tlumaczen:

        lista = p1.split(tlumaczenie)
        tag = lista[0].strip()
        
        if num == 1 and tag=="value":
            word=[]
            num = 2
            name = ""
            value = lista[1][1:-1]
            continue
           
        if num == 2 and tag=="word":          
            word.append(lista[1])
            continue   

        if num == 2 and tag=="name":          
            name= lista[1]
            num = 1   
        else:
            continue
          
        for w in word:
            sprawdz_i_zapisz(value,w,name)


def sprawdz_i_zapisz(value,w,descr):
      
    lista_slow = p2.split(w)
    if len(lista_slow) == 0 or len(lista_slow)>2:
        return 0
    
    if len(lista_slow)==2 and lista_slow[0]=="to":
        slowo = lista_slow[1]
        lista_slow = []
        lista_slow.append(slowo)
     
    descr = descr.strip()
 
    slowoAng = ""
    for s in lista_slow:
        if s[1:-1]=="s":
            slowoAng = slowoAng + "\\\'" + s[1:-1]
        else:
            if slowoAng == "": 
                slowoAng = s[1:-1]
                if slowoAng == "to" or slowoAng == "company"or slowoAng == "na" or slowoAng == "naked": return 1
            else:
                slowoAng = slowoAng + " " + s[1:-1]
    
    slowoAng = slowoAng.strip() 

    if descr == "pa" or 'ą' in slowoAng or 'ż' in slowoAng or 'ś' in slowoAng or 'ź' in slowoAng or 'ę' in slowoAng or 'ć' in slowoAng or 'ń' in slowoAng or 'ó' in slowoAng or 'ł' in slowoAng or (descr == '' and ('rz' in slowoAng or 'na' in slowoAng or 'ny' in slowoAng or 'sz' in slowoAng or 'cz' in slowoAng or 'dz' in slowoAng or 'ki' in slowoAng or 'ka' in slowoAng or 'owy' in slowoAng or 'owa' in slowoAng or 'ne' in slowoAng or 'ta' in slowoAng or 'owe' in slowoAng or 'te' in slowoAng or 'ty' in slowoAng or 'ne' in slowoAng)):    
        print value +" -> "+ slowoAng 
        exce_set.add((value,slowoAng))
    return 1
      
def main():     
    dbm = DBmanager() 
    find_exceptions(sys.argv[1])
    print str(len(exce_set))
    for (word1,word2) in exce_set:
        dbm.insertExceptionPol(word1, word2, "", "")

if __name__ == '__main__':
    main()
