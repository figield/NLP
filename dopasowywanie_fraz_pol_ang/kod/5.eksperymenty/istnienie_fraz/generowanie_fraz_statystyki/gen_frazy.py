#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from databasemanager import *

def main():   
    kat = 'wyniki'
    pol_or_ang = sys.argv[1]
    dbm = DBmanager()
    p1 = re.compile('[.,;?!\-\'\"]+')       
  
    lista_zdan_z_bazy = dbm.get_sentence(pol_or_ang)
    ilosc_zdan = len(lista_zdan_z_bazy)
    print "Przetwarzanie %d zdan" % (ilosc_zdan) 
    
    n=2
    while n<7:
        print "Pobranie statystyk %d wyrazowych..." % (n)   
        statystyki = dbm.get_all_phrases(n,pol_or_ang)
        print "Pobrano %d fraz\n" % (len(statystyki))
        stat_set = set(wiersz[2:n+2] for wiersz in statystyki)        
        Znalezione = 0
        Nie_znalezione = 0
        frazy_wynik = open(kat+'/frazy_'+pol_or_ang+"_"+str(n)+'.txt','w')
        for (zdanie,) in lista_zdan_z_bazy:
            zdanie=p1.sub('',zdanie)
            slowa = re.compile("[ \t\n]+",re.L).split(zdanie)
            pary = []
            if n == 2:
                pary = zip(slowa[:-1], slowa[1:])
            elif n == 3:          
                pary = zip(slowa[:-1], slowa[1:], slowa[2:])
            elif n == 4:          
                pary = zip(slowa[:-1], slowa[1:], slowa[2:], slowa[3:])
            elif n == 5:          
                pary = zip(slowa[:-1], slowa[1:], slowa[2:], slowa[3:], slowa[4:])
            elif n == 6:          
                pary = zip(slowa[:-1], slowa[1:], slowa[2:], slowa[3:], slowa[4:], slowa[5:])

            frazy_wynik.write(zdanie + "\n")
            for para in pary:
                wynik = ""
                if para in stat_set:
                    wynik = '\t+ '
                    Znalezione+=1                
                else:
                    wynik = '\t- '
                    Nie_znalezione+=1

                for p in para:
                    wynik+= '%s ' % (p)
                wynik+="\n"
                frazy_wynik.write('%s' % (wynik))
        n+=1
        frazy_wynik.write('Znalezione:%d\nNie znalezione:%d' % (Znalezione,Nie_znalezione))
        frazy_wynik.close()
        
 
if __name__ == '__main__':
    main()
