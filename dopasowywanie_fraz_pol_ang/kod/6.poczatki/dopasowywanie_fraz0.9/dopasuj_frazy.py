#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from cPickle import load
from libs.library import *
from libs import _plp
from libs.databasemanager import *

def main():   
    kat = 'wyniki'
    dbm = DBmanager()
    _plp.plp_init()
    p1 = re.compile('[:;?!().,\-\t\n\r\'\"]+')
    p2 = re.compile('[ ]+')              
    koncowki = ['the','i','a','an','t','d']
    poczatki = ['s','d']
    zbior_fraz = {}
    lista_zdan_z_bazy = dbm.get_both_sentences()
    ilosc_zdan = len(lista_zdan_z_bazy)
    imiona = dbm.get_all_names()
    names = set()
    for (n,) in imiona:
        names.add(n.lower())  

    simple = True   
    method = "simple"
    if 'simple' not in sys.argv:
        simple = False
        method = "stat" 
    dopasowania_wynik = open(kat + '/' + method + '_dopasowanie_wynik.txt','w')
    rezultat = open(kat + '/' + method + '_rezultat.txt','w')
    rezultat.write("Pobrano %d zdan" % (ilosc_zdan))
    m = 2
    k = 6
    h = 1
    stat_set_pol2 = set()
    stat_set_pol3 = set()
    stat_set_pol4 = set()
    stat_set_pol5 = set()
    stat_set_pol6 = set()
    stat_set_ang2 = set()
    stat_set_ang3 = set()
    stat_set_ang4 = set()
    stat_set_ang5 = set()
    stat_set_ang6 = set()
    
    if not simple:
        for pol_or_ang in ['pol','ang']:
            n = m
            while n<=k:    
                print "Pobranie statystyk %d wyrazowych..." % (n)   
                if pol_or_ang == 'pol':
                    if n == 2:
                        stat_set_pol2 = load(open('statystyki/stat_pol2.pic','r')) 
                    elif n == 3:
                        stat_set_pol3 = load(open('statystyki/stat_pol3.pic','r'))
                    elif n == 4:
                        stat_set_pol4 = load(open('statystyki/stat_pol4.pic','r'))
                    elif n == 5:
                        stat_set_pol5 = load(open('statystyki/stat_pol5.pic','r'))
                    elif n == 6:
                        stat_set_pol6 = load(open('statystyki/stat_pol6.pic','r')) 
                else:
                    if n == 2:
                        stat_set_ang2 = load(open('statystyki/stat_ang2.pic','r'))
                    elif n == 3:
                        stat_set_ang3 = load(open('statystyki/stat_ang3.pic','r'))
                    elif n == 4:
                        stat_set_ang4 = load(open('statystyki/stat_ang4.pic','r'))
                    elif n == 5:
                        stat_set_ang5 = load(open('statystyki/stat_ang5.pic','r'))
                    elif n == 6:
                        stat_set_ang6 = load(open('statystyki/stat_ang6.pic','r'))
                n+=1 
            
    for (zdanie_pol,zdanie_ang,) in lista_zdan_z_bazy:
        if h % 100 == 0: print "> " + str(h)
        h += 1         
        lista_znalezionych_krotek_pol = []
        lista_znalezionych_krotek_ang = []
        rezultat.write("\n\n-----------------------------------------------------")
        rezultat.write("\nZ. pol: %s\nZ. ang: %s" % (zdanie_pol,zdanie_ang))            

        for pol_or_ang in ['pol','ang']:
            if pol_or_ang == 'pol':      
                #przeksztalcenie zdania na formy bez apostrfow -
                #zdania i statystyki byly juz poddane tej operacji
                zdanie = p1.sub(' ',zdanie_pol)
            else:
                # - // -     
                zdanie = p1.sub(' ',zdanie_ang)
            zdanie = p2.sub(' ', zdanie.strip())  

            slowa = re.compile("[ \t\n]+",re.L).split(zdanie)
            slowa_krot = [] 
            if pol_or_ang == 'pol':          
                for slowo in slowa:
                    rezultat.write("\n\nOrg:%s\nPodst:" % slowo)
                    zb_slow_podstawowych = set(formy_podstawowe_slowa_pl(dbm,_plp,slowo,names))
                    for sp in zb_slow_podstawowych:
                        rezultat.write("%s," % sp)
                    zb_slow_przetl_na_ang = (slowo, tlumacz_slowa_pol(dbm,zb_slow_podstawowych))
                    rezultat.write("\nPol2Ang:")
                    s,angs = zb_slow_przetl_na_ang
                    for spa in angs:
                        rezultat.write("%s," % spa)
                    slowa_krot.append(zb_slow_przetl_na_ang)
            else:
                for slowo in slowa:
                    rezultat.write("\n\nOrg(ang):%s\nPodst:" % slowo)
                    zb_slow_postawowych = set(formy_podstawowe_slowa_ang(dbm,slowo,names))
                    for sp in zb_slow_postawowych:
                        rezultat.write("%s," % sp)
                    zb_slow_przetl_ang = (slowo, zb_slow_postawowych)
                    slowa_krot.append(zb_slow_przetl_ang)

            n = m
            while n <= k:                
                krotki = []
                if n == 2:                    
                    krotki = zip(slowa[:-1], slowa[1:])      
                    pary_krot = zip(slowa_krot[:-1], slowa_krot[1:])
                    y = len(krotki)
                    x = 0
                    while x < y:
                        if selekcja_krotek(poczatki,koncowki,krotki[x]):     
                            if pol_or_ang == 'pol':
                                if simple:
                                    lista_znalezionych_krotek_pol.append(pary_krot[x])
                                else:
                                    if krotki[x] in stat_set_pol2: # czy szukać w statystykach form po przeksztalceniu??...
                                        lista_znalezionych_krotek_pol.append(pary_krot[x])
                            else:
                                if simple:
                                    lista_znalezionych_krotek_ang.append(pary_krot[x])
                                else:
                                    if krotki[x] in stat_set_ang2:
                                        lista_znalezionych_krotek_ang.append(pary_krot[x])
                        x += 1  
                elif n == 3:    
                    krotki = zip(slowa[:-1], slowa[1:], slowa[2:])
                    pary_krot = zip(slowa_krot[:-1], slowa_krot[1:], slowa_krot[2:])
                    y = len(krotki)
                    x = 0
                    while x < y:
                        if selekcja_krotek(poczatki,koncowki,krotki[x]):
                            if pol_or_ang == 'pol':
                                if simple:
                                    lista_znalezionych_krotek_pol.append(pary_krot[x])
                                else:
                                    if krotki[x] in stat_set_pol3:
                                        lista_znalezionych_krotek_pol.append(pary_krot[x])
                            else:
                                if simple:
                                    lista_znalezionych_krotek_ang.append(pary_krot[x])
                                else:
                                    if krotki[x] in stat_set_ang3:
                                        lista_znalezionych_krotek_ang.append(pary_krot[x])  
                        x += 1
                elif n == 4:          
                    krotki = zip(slowa[:-1], slowa[1:], slowa[2:], slowa[3:])
                    pary_krot = zip(slowa_krot[:-1], slowa_krot[1:], slowa_krot[2:], slowa_krot[3:])
                    y = len(krotki)
                    x = 0
                    while x < y:
                        if selekcja_krotek(poczatki,koncowki,krotki[x]):
                            if pol_or_ang == 'pol':
                                if simple:
                                    lista_znalezionych_krotek_pol.append(pary_krot[x])
                                else:
                                    if krotki[x] in stat_set_pol4:
                                        lista_znalezionych_krotek_pol.append(pary_krot[x])
                            else:
                                if simple:
                                    lista_znalezionych_krotek_ang.append(pary_krot[x])
                                else:
                                    if krotki[x] in stat_set_ang4:
                                        lista_znalezionych_krotek_ang.append(pary_krot[x])  
                        x += 1
                elif n == 5:          
                    krotki = zip(slowa[:-1], slowa[1:], slowa[2:], slowa[3:], slowa[4:])
                    pary_krot = zip(slowa_krot[:-1], slowa_krot[1:], slowa_krot[2:], slowa_krot[3:], slowa_krot[4:])
                    y = len(krotki)
                    x = 0
                    while x < y:
                        if selekcja_krotek(poczatki,koncowki,krotki[x]):
                            if pol_or_ang == 'pol':
                                if simple:
                                    lista_znalezionych_krotek_pol.append(pary_krot[x])
                                else:
                                    if krotki[x] in stat_set_pol5:
                                        lista_znalezionych_krotek_pol.append(pary_krot[x])
                            else:
                                if simple:
                                    lista_znalezionych_krotek_ang.append(pary_krot[x])
                                else:
                                    if krotki[x] in stat_set_ang5:
                                        lista_znalezionych_krotek_ang.append(pary_krot[x])  
                        x += 1
                elif n == 6:          
                    krotki = zip(slowa[:-1], slowa[1:], slowa[2:], slowa[3:], slowa[4:], slowa[5:])
                    pary_krot = zip(slowa_krot[:-1], slowa_krot[1:], slowa_krot[2:], slowa_krot[3:], slowa_krot[4:], slowa_krot[5:])
                    y = len(krotki)
                    x = 0
                    while x < y:
                        if selekcja_krotek(poczatki,koncowki,krotki[x]):
                            if pol_or_ang == 'pol':
                                if simple:
                                    lista_znalezionych_krotek_pol.append(pary_krot[x])
                                else:
                                    if krotki[x] in stat_set_pol6:
                                        lista_znalezionych_krotek_pol.append(pary_krot[x])
                            else:
                                if simple:
                                    lista_znalezionych_krotek_ang.append(pary_krot[x])
                                else:
                                    if krotki[x] in stat_set_ang6:
                                        lista_znalezionych_krotek_ang.append(pary_krot[x])  
                        x += 1
                n+=1

        for krotka_pl in lista_znalezionych_krotek_pol:
            for krotka_ang in lista_znalezionych_krotek_ang:
                dopasuj_krotki(dbm,krotka_pl,krotka_ang,zbior_fraz)               
                               
    rezultat.write("\n\nZnalezionych fraz: %d " % len(zbior_fraz)) 
    drukuj_dopasowane(dopasowania_wynik,zbior_fraz)        
    dopasowania_wynik.close()
    rezultat.close()


if __name__ == '__main__':
    main()
