#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
import time 
from databasemanager import *
from mylib import rozdziel_frazePL, rozdziel_frazeAng
from pickle import load

# etapy:
#
# 1. Pobranie zdania polskiego z bazy
# 2. Znalezienie w bazie statystyk części zdania n-wyrazowego
# 3. Zapisanie wyników w osobnych plikach.

def main():   
    kat = 'wyniki'
    n=int(sys.argv[1])
    pol_or_ang = sys.argv[2]
    dbm = DBmanager()
    nr = 1
    ilosc_zdan = 0
    Znalezione = 0
    Nie_znalezione = 0
    frazy_wynik = open(kat+'/frazy_'+pol_or_ang+"_"+str(n)+'2.txt','w')

    print "Pobranie statystyk %d wyrazowych..." % (n)   
    stat_set = load(file('stat2.pickle'))
    print "Pobrano %d fraz" % (len(stat_set)) 

    print "Pobieranie zdan z bazy..."
    lista_zdan_z_bazy = dbm.get_sentence(pol_or_ang)
    ilosc_zdan = len(lista_zdan_z_bazy)
    print "Przetwarzanie %d zdan..." % (ilosc_zdan) 

    for (zdanie,) in lista_zdan_z_bazy:
        slowa = zdanie.split()
        pary = zip(slowa[:-1], slowa[1:])
        frazy_wynik.write(zdanie + '\n')
        for para in pary:
            if para in stat_set:
                frazy_wynik.write('\t+ %s %s\n' % (para[0], para[1]))
            else:
                frazy_wynik.write('\t- %s %s\n' % (para[0], para[1])) 
    
if __name__ == '__main__':
	main()
