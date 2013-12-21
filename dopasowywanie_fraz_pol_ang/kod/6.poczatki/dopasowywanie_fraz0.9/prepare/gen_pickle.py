#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from libs.databasemanager import *
from cPickle import dump

def main():   
    dbm = DBmanager()
    m = 2
    k = 6

    for pol_or_ang in ['pol','ang']:
        n = m
        while n<=k:    
            print "Pobranie statystyk %d wyrazowych..." % (n)   
            statystyki = dbm.get_all_phrases(n,pol_or_ang)
            stat = set(wiersz[2:n+2] for wiersz in statystyki)
            stat_n = open('stat_'+pol_or_ang+ str(n)+'.pic','w')
            print "Zapisywanie do pliku stat_"+pol_or_ang+str(n)+".pic"
            dump(stat,stat_n,2)
            stat_n.close() 
            n+=1 
   
 
if __name__ == '__main__':
    main()
