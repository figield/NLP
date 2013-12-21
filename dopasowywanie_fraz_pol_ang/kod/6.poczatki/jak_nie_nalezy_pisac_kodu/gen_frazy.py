#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from locale import *
from string import * 
from databasemanager import *
from mylib import rozdziel_frazePL, rozdziel_frazeAng

# etapy:
#
# 1. Pobranie zdania polskiego z bazy
# 2. Znalezienie w bazie statystyk części zdania n-wyrazowego
# 3. ...zapisanie wyników w osobnych plikach cdn.

zbior_fraz_zdania = {}


# jak to przyśpieszyc? (przefiltrować bazę (pomniejszyć ją))Załadowac wszystko do pamieci! ];>
# jak uwspólnić biblioteki ? 

def wydziel_frazy_ze_zdania(dbm, zdanie, n, pol_or_ang):
    p1 = re.compile('[.,;?!\-\'\"]+') 
    zdanie=p1.sub(' ',zdanie)
    lista_fraz_ze_zdania = [] 
    lista_fraz_ze_zdania_po_selekcji = []   
    zna = 0
    nie_zna =0    

    if pol_or_ang == "pol": 
        lista_fraz_ze_zdania = rozdziel_frazePL(zdanie,n)
    else:
        lista_fraz_ze_zdania = rozdziel_frazeAng(zdanie,n)      

    for fz in lista_fraz_ze_zdania:
       lista_slow = re.compile("[ ]+",re.L).split(fz)         
       if len(lista_slow)!= n:
           print "ERROR: Dlgosc listy slow jest nieodpowiednia!!"
           continue 

       if dbm.find_phrase(lista_slow,n,pol_or_ang)==True:
           lista_fraz_ze_zdania_po_selekcji.append("+ "+fz)
           zna = zna + 1
       else:
           lista_fraz_ze_zdania_po_selekcji.append("- "+fz)
           nie_zna = nie_zna + 1

    if zbior_fraz_zdania.get(zdanie)==None:
        zbior_fraz_zdania[zdanie]= []
        for fraza_n in lista_fraz_ze_zdania_po_selekcji:
            zbior_fraz_zdania[zdanie].append(fraza_n)
       
    return (zna,nie_zna)        
    
def main():   
    kat = 'wyniki'
    n=int(sys.argv[1])
    pol_or_ang = sys.argv[2]
    dbm = DBmanager()
    nr = 1
    ilosc_zdan = 0
    Znalezione = 0
    Nie_znalezione = 0

    print "Pobieranie zdan z bazy..."
    lista_zdan_z_bazy = dbm.get_sentence(pol_or_ang)
    ilosc_zdan = len(lista_zdan_z_bazy)
    print "Przetwarzanie "+str(ilosc_zdan) +" zdan..." 
     
    for r in lista_zdan_z_bazy:
        zdanie =  r[0]
        print str(nr)
        (zna,nie_zna)=wydziel_frazy_ze_zdania(dbm, zdanie, n, pol_or_ang)
        Znalezione = Znalezione + zna
        Nie_znalezione = Nie_znalezione + nie_zna
        nr = nr + 1
    
    print "Zapisywanie danych do plikow"
    
    frazy_wynik = open(kat+'/frazy_'+pol_or_ang+"_"+str(n)+'.txt','w')
    frazy_wynik.write("Znalezionych: " +str(Znalezione)+", nie znalezionych: " + str(Nie_znalezione)+"\n")
    
    keys = zbior_fraz_zdania.keys()
    for key_zd in keys:
        frazy_wynik.write(key_zd + "\n")
        for fr in zbior_fraz_zdania[key_zd]:
            frazy_wynik.write("\t" + fr + "\n")  
       
    frazy_wynik.close()    
 
main()
