#!/usr/bin/python
import os,sys,re
import string
from locale import *
from string import *
from databasemanager import *
  
p1 = re.compile('=',re.L)
p2 = re.compile('[ ]+',re.L)
p3 = re.compile('[\'`\"]+')   
      
# popracowac nad przyspieszeniem algorytmu.

def wydziel_tlumaczenia(arg,dbm):
    
    id_descr=""
    id_gen ="" 
    slowoPol=""
    slowoAng=""
    caly_slownik = open(arg,"r").read()
    lista_tlumaczen = re.compile('\n',re.L).split(caly_slownik)
    
    print "1) Przetwarzanie slownka '"+ arg +"' i wczytywanie do tabeli \'dictionary\' "

    for tlumaczenie in lista_tlumaczen:

        if len(tlumaczenie)<5:
            continue

        tlumaczenie = p3.sub('',tlumaczenie)  
        lista1 = p1.split(tlumaczenie)
        lista2 = p2.split(lista1[0])
        slowoAng=lista1[1].strip() 
        slowoPol=lista2[0].strip()
        if len(lista2)==2:
            id_descr=lista2[1][1:-1]
        else:
            id_gen=lista2[1][1:-1]
            id_descr=lista2[2][1:-1]
         
        dbm.insertTranslation(slowoPol,slowoAng,id_descr,id_gen)


def wydziel_tlumaczenia2(arg,dbm):
    
    caly_slownik = open(arg,"r").read()
    lista_tlumaczen = re.compile('\n',re.L).split(caly_slownik)
   
    p1 = re.compile('=',re.L)
    value=""
    word=[]
    name=""
    num = 1  # 1,2
  
    print "2) Przetwarzanie slownka '"+ arg +"' i wczytywanie do tabeli \'dictionary\' "
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
            sprawdz_i_zapisz(value,w,name,dbm)


def sprawdz_i_zapisz(value,w,descr,dbm):
       
    plec = ""
    lista_slow = p2.split(w)
    if len(lista_slow) == 0 or len(lista_slow)>2:
        return 0
    
    if len(lista_slow)==2 and lista_slow[0]=="to":
        slowo = lista_slow[1]
        lista_slow = []
        lista_slow.append(slowo)
     
    if len(descr)> 30:
        descr = ""
    descr = descr.strip()
  
    if descr =="f" or descr =="m" or descr =="pl" or descr =="n":
        plec = descr
        descr = ""

    slowoAng = ""
    for s in lista_slow:
        if s[1:-1]=="s":
            slowoAng = slowoAng + "\\\'" + s[1:-1]
        else:
            if slowoAng == "": 
                slowoAng = s[1:-1]
            else:
                slowoAng = slowoAng + " " + s[1:-1]
    
    slowoAng = slowoAng.strip() 
    if dbm.getTranslationExist(value,slowoAng) == 0:
        dbm.insertTranslation(value,slowoAng,descr,plec)
    
    return 1
      
def main():
    
    lista_plikow= os.listdir(sys.argv[1]) 
    lista_plikow2= os.listdir(sys.argv[2]) 
   
    dbm = DBmanager() 
    print " Czyszczenie tabeli \'dictionary\'"
    dbm.clearTranslation()
        
    for arg in lista_plikow:
        wydziel_tlumaczenia(sys.argv[1]+"/"+arg,dbm)

    for arg in lista_plikow2:
        wydziel_tlumaczenia2(sys.argv[2]+"/"+arg,dbm)

main()
