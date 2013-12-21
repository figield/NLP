#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from databasemanager import *

def main():   
    kat = 'wyniki'
    dbm = DBmanager()    

    for pol_or_ang in ['pol','ang']:
        n = 2
        while n < 7:
            statystyki = []
            statystyki2 = []
            print "Pobranie statystyk %d wyrazowych..." % (n) 
            if pol_or_ang == 'pol': 
                if n == 2: 
                    statystyki = dbm.get_2_phrases_pol()
                elif n == 3:
                    statystyki = dbm.get_3_phrases_pol()
                elif n == 4:
                    statystyki = dbm.get_4_phrases_pol()
                elif n == 5:
                    statystyki = dbm.get_5_phrases_pol()
                elif n == 6:
                    statystyki = dbm.get_6_phrases_pol()
            elif pol_or_ang == 'ang': 
                if n == 2: 
                    statystyki = dbm.get_2_phrases_ang()
                elif n == 3:
                    statystyki = dbm.get_3_phrases_ang()
                elif n == 4:
                    statystyki = dbm.get_4_phrases_ang()
                elif n == 5:
                    statystyki = dbm.get_5_phrases_ang()
                elif n == 6:
                    statystyki = dbm.get_6_phrases_ang()
            
            stat_wynik = open(kat+'/stat_'+pol_or_ang+"_"+str(n)+'.txt','w')
            nr = 1
            for (r,) in statystyki:
                statystyki2.append(r)
            statystyki2.reverse() 
            for r in statystyki2:
                stat_wynik.write("%d\t%s\n" % (nr,r))
                #print "%d\t%s" % (nr,r) 
                nr += 1
                if nr == 50000: break
            stat_wynik.close()
            n += 1
 
if __name__ == '__main__':
    main()
