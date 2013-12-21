#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
import time 
from databasemanager import *
from mylib import rozdziel_frazePL, rozdziel_frazeAng
from pickle import dump

def main():   
    kat = 'wyniki'
    n=int(sys.argv[1])
    pol_or_ang = sys.argv[2]
    dbm = DBmanager()
    nr = 1
    ilosc_zdan = 0
    Znalezione = 0
    Nie_znalezione = 0

    print "Pobranie statystyk %d wyrazowych..." % n   
    statystyki = dbm.get_all_phrases(n,pol_or_ang)
    stat_set = set(wiersz[2:4] for wiersz in statystyki)
    dump(stat_set, file('stat2.pickle', 'w'))
 
if __name__ == '__main__':
	main()
