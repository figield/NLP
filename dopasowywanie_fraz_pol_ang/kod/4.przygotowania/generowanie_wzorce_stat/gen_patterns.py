#!/usr/bin/python
# -*- coding: latin2 -*-
import _plp,os,sys,re
import string
from databasemanager import *


def label_set(slowo):
    slowo = slowo.strip()
    string = _plp.plp_rec(slowo)
    numery = string.split(':')
    ile = int(numery[0])
    ids = numery[1:]
    return frozenset(_plp.plp_label(int(nr)) for nr in ids)


def main():
    kat = 'wyniki'
    pol_or_ang = sys.argv[1]
    dbm = DBmanager()       
    _plp.plp_init()
    n = int(sys.argv[3])

    hash_of_tuples = {}
    print "\nPobranie statystyk %d wyrazowych..." % n   
    statystyki = dbm.get_all_phrases(n, pol_or_ang)
    print "Pobrano %d fraz" % len(statystyki)
    stat_set = set(wiersz[2:n+2] for wiersz in statystyki)            
    print "N = %d" % (n)        

    if n ==2 :
        for w1, w2 in stat_set:
            lw1 = label_set(w1)    
            lw2 = label_set(w2)
            if not lw1 or not lw2:
                continue
            tuples = (lw1, lw2)
            if hash_of_tuples.get(tuples)==None:
                hash_of_tuples[tuples]=1
            else:
                hash_of_tuples[tuples]+=1
        print len(hash_of_tuples)
        if 'totxt'in sys.argv: 
            k=hash_of_tuples.keys()
            k.sort(lambda y,x: cmp(hash_of_tuples[x], hash_of_tuples[y]))
            print "Zapisywanie danych do plików"
            frazy_stat_clp  = open(kat+'/frazy_clp_'+str(n)+'.txt','w')
            frazy_stat_clp_id = open(kat+'/frazy_clp_'+str(n)+'_id.txt','w')
            nr = 1      
            for x in k:
                if hash_of_tuples[x] > 2 :
                    (s1,s2)=x
                    frazy_stat_clp.write(str(hash_of_tuples[x]) + "\t" + str([y1 for y1 in s1])+", "+str([y2 for y2 in s2]) + "\n")
                    frazy_stat_clp_id.write(str(nr)+"\t"+str(hash_of_tuples[x]) + "\n")
                    nr = nr + 1
            frazy_stat_clp.close()    
            frazy_stat_clp_id.close()    
    elif n == 3:
        for w1, w2, w3 in stat_set:
            lw1 = label_set(w1)    
            lw2 = label_set(w2)
            lw3 = label_set(w3)
            if not lw1 or not lw2 or not lw3:
                continue
            tuples = (lw1, lw2, lw3)
            #print "%s,%s,%s: %s" % (w1,w2,w3,str(tuples))
            if hash_of_tuples.get(tuples)==None:
                hash_of_tuples[tuples]=1
            else:
                hash_of_tuples[tuples]+=1
        print len(hash_of_tuples)
        if 'totxt'in sys.argv:    
            k=hash_of_tuples.keys()
            k.sort(lambda y,x: cmp(hash_of_tuples[x], hash_of_tuples[y]))
            print "Zapisywanie danych do plików"
            frazy_stat_clp  = open(kat+'/frazy_clp_'+str(n)+'.txt','w')
            frazy_stat_clp_id = open(kat+'/frazy_clp_'+str(n)+'_id.txt','w')
            nr = 1      
            for x in k:
                if hash_of_tuples[x] > 2 :
                    (s1,s2,s3)=x
                    frazy_stat_clp.write(str(hash_of_tuples[x]) + "\t" + str([y1 for y1 in s1])+", "+str([y2 for y2 in s2])+", "+str([y3 for y3 in s3]) + "\n")
                    frazy_stat_clp_id.write(str(nr)+"\t"+str(hash_of_tuples[x]) + "\n")
                    nr = nr + 1
            frazy_stat_clp.close() 
            frazy_stat_clp_id.close()
    elif n == 4:
        for w1, w2, w3, w4 in stat_set:
            lw1 = label_set(w1)    
            lw2 = label_set(w2)
            lw3 = label_set(w3)
            lw4 = label_set(w4)
            if not lw1 or not lw2 or not lw3 or not lw4:
                continue
            tuples = (lw1, lw2, lw3, lw4)
            if hash_of_tuples.get(tuples)==None:
                hash_of_tuples[tuples]=1
            else:
                hash_of_tuples[tuples]+=1

        print len(hash_of_tuples)
        if 'totxt'in sys.argv:    
            k=hash_of_tuples.keys()
            k.sort(lambda y,x: cmp(hash_of_tuples[x], hash_of_tuples[y]))
            print "Zapisywanie danych do plików"
            frazy_stat_clp  = open(kat+'/frazy_clp_'+str(n)+'.txt','w')
            frazy_stat_clp_id = open(kat+'/frazy_clp_'+str(n)+'_id.txt','w')
            nr = 1      
            for x in k:
                if hash_of_tuples[x] > 2 :
                    (s1,s2,s3,s4)=x
                    frazy_stat_clp.write(str(hash_of_tuples[x]) + "\t" + str([y1 for y1 in s1])+", "+str([y2 for y2 in s2])+", "+str([y3 for y3 in s3])+", "+str([y4 for y4 in s4]) + "\n")
                    frazy_stat_clp_id.write(str(nr)+"\t"+str(hash_of_tuples[x]) + "\n")
                    nr = nr + 1
            frazy_stat_clp.close()
            frazy_stat_clp_id.close()
    elif n == 5:
        for w1, w2, w3, w4, w5 in stat_set:
            lw1 = label_set(w1)    
            lw2 = label_set(w2)
            lw3 = label_set(w3)
            lw4 = label_set(w4)
            lw5 = label_set(w5)
            if not lw1 or not lw2 or not lw3 or not lw4 or not lw5:
                continue
            tuples = (lw1, lw2, lw3, lw4, lw5)
            if hash_of_tuples.get(tuples)==None:
                hash_of_tuples[tuples]=1
            else:
                hash_of_tuples[tuples]+=1
        print len(hash_of_tuples)
        if 'totxt'in sys.argv:  
            k=hash_of_tuples.keys()
            k.sort(lambda y,x: cmp(hash_of_tuples[x], hash_of_tuples[y])) 
            print "Zapisywanie danych do plików"
            frazy_stat_clp  = open(kat+'/frazy_clp_'+str(n)+'.txt','w')
            frazy_stat_clp_id = open(kat+'/frazy_clp_'+str(n)+'_id.txt','w')
            nr = 1      
            for x in k:
                if hash_of_tuples[x] > 2 :
                    (s1,s2,s3,s4,s5)=x
                    frazy_stat_clp.write(str(hash_of_tuples[x]) + "\t" + str([y1 for y1 in s1])+", "+str([y2 for y2 in s2])+", "+str([y3 for y3 in s3])+", "+str([y4 for y4 in s4])+", "+str([y5 for y5 in s5]) + "\n")
                    frazy_stat_clp_id.write(str(nr)+"\t"+str(hash_of_tuples[x]) + "\n")
                    nr = nr + 1
            frazy_stat_clp.close()
            frazy_stat_clp_id.close()
    elif n == 6:
        for w1, w2, w3, w4, w5, w6 in stat_set:
            lw1 = label_set(w1)    
            lw2 = label_set(w2)
            lw3 = label_set(w3)
            lw4 = label_set(w4)
            lw5 = label_set(w5)
            lw6 = label_set(w6)
            if not lw1 or not lw2 or not lw3 or not lw4 or not lw5 or not lw6:
                continue
            tuples = (lw1, lw2, lw3, lw4, lw5, lw6)
            if hash_of_tuples.get(tuples)==None:
                hash_of_tuples[tuples]=1
            else:
                hash_of_tuples[tuples]+=1
        print len(hash_of_tuples)
        if 'totxt'in sys.argv:   
            k=hash_of_tuples.keys()
            k.sort(lambda y,x: cmp(hash_of_tuples[x], hash_of_tuples[y])) 
            print "Zapisywanie danych do plików"
            frazy_stat_clp  = open(kat+'/frazy_clp_'+str(n)+'.txt','w')
            frazy_stat_clp_id = open(kat+'/frazy_clp_'+str(n)+'_id.txt','w')
            nr = 1      
            for x in k:
                if hash_of_tuples[x] > 2 :
                    (s1,s2,s3,s4,s5,s6)=x
                    frazy_stat_clp.write(str(hash_of_tuples[x]) + "\t" + str([y1 for y1 in s1])+", "+str([y2 for y2 in s2])+", "+str([y3 for y3 in s3])+", "+str([y4 for y4 in s4])+", "+str([y5 for y5 in s5])+", "+str([y6 for y6 in s6]) + "\n")
                    frazy_stat_clp_id.write(str(nr)+"\t"+str(hash_of_tuples[x]) + "\n")
                    nr = nr + 1
            frazy_stat_clp.close()
            frazy_stat_clp_id.close()
    if 'pic' in sys.argv:
        k=hash_of_tuples.keys()
        print "Sortowanie,"
        k.sort(lambda y,x: cmp(hash_of_tuples[x], hash_of_tuples[y]))
        set_of_tuples = set()
        print "Tworzenie zbioru,"
        cut = int(sys.argv[4])
        for x in k:
            if hash_of_tuples[x] >= cut:
                set_of_tuples.add(x)
        print "Wielkosc zbioru : %d" % len(set_of_tuples)
        frazy_stat_clp_pic  = open('frazy_clp_'+str(n)+'.pic','w')
        print "Zapisywanie do pliku,"
        from cPickle import dump
        dump(set_of_tuples,frazy_stat_clp_pic,2)
        frazy_stat_clp_pic.close() 
 

if __name__ == '__main__':
    main()
