#!/usr/bin/python
# -*- coding: latin2 -*-
import _plp,os,sys,re
import string
from databasemanager import *
from cPickle import load
from gen_patterns import label_set

def main():   
    kat = 'wyniki'
    pol_or_ang = sys.argv[1]
    dbm = DBmanager()
    _plp.plp_init()
    p1 = re.compile('[.,;?!\-\'\"]+')       
  
    lista_zdan_z_bazy = dbm.get_sentence(pol_or_ang)
    ilosc_zdan = len(lista_zdan_z_bazy)
    print "Przetwarzanie %d zdan" % (ilosc_zdan) 
    
    n=2
    while n<4:
        print "Pobranie wzorcow statystyk %d wyrazowych z pliku" % (n)   
        frazy_stat_clp_pic  = open('frazy_clp_'+str(n)+'.pic','r')
        set_of_tuples = load(frazy_stat_clp_pic)
        print "Pobrano %d wzorcow\n" % (len(set_of_tuples))                  
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
                tuples =()
                if n == 2:
                    w1, w2 = para
                    tuples = (label_set(w1), label_set(w2))
                    #print "%s,%s: %s" % (w1,w2,str(tuples))
                elif n == 3:
                    w1, w2, w3 = para
                    tuples = (label_set(w1), label_set(w2), label_set(w3))
                elif n == 4:
                    w1, w2, w3, w4 = para
                    tuples = (label_set(w1), label_set(w2), label_set(w3), label_set(w4))
                elif n == 5:
                    w1, w2, w3, w4, w5 = para
                    tuples = (label_set(w1), label_set(w2), label_set(w3), label_set(w4), label_set(w5))
                elif n == 6:
                    w1, w2, w3, w4, w5, w6 = para
                    tuples = (label_set(w1), label_set(w2), label_set(w3), label_set(w4), label_set(w5), label_set(w6))

                if tuples in set_of_tuples:
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
