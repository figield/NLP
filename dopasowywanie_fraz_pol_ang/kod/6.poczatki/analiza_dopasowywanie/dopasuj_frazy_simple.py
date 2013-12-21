#!/usr/bin/python
# -*- coding: latin2 -*-
import _plp,os,sys,re
import string
from databasemanager import *
from library import *

def main():   
    kat = 'wyniki'
    dbm = DBmanager()
    _plp.plp_init()      
    zbior_fraz = {}   
    p1 = re.compile('[.,;?!\-\'\"]+')        
    dopasowania_wynik = open(kat+'/dopasowanie_wynik.txt','w')
    rezultat = open(kat+'/rezultat.txt','w')
    lista_zdan_z_bazy = dbm.get_both_sentences()
    ilosc_zdan = len(lista_zdan_z_bazy)
    rezultat.write("Pobrano %d zdan" % (ilosc_zdan)) 
    m = 2
    k = 4
    h = 1
    for (zdanie_pol,zdanie_ang,) in lista_zdan_z_bazy:
        print str(h)
        h += 1         
        lista_znalezionych_krotek_pol = []
        lista_znalezionych_krotek_ang = []
        rezultat.write("\n\n-----------------------------------------------------")
        rezultat.write("\nZ. pol: %s\nZ. ang: %s" % (zdanie_pol,zdanie_ang))            

        for pol_or_ang in ['pol','ang']:
            if pol_or_ang == 'pol':          
                zdanie = p1.sub('',zdanie_pol)
            else:
                zdanie = p1.sub('',zdanie_ang)  
            slowa1 = re.compile("[ \t\n]+",re.L).split(zdanie)
            slowa = []
            if pol_or_ang == 'pol':          
                for slowo in slowa1:
                    rezultat.write("\n\nOrg: %s\nPodst: " % slowo)
                    zb_slow_postawowych = set(formy_podstawowe_slowa_pl(_plp,slowo))
                    for sp in zb_slow_postawowych:
                        rezultat.write("%s, " % sp)
                    zb_slow_przetl_na_ang = (slowo, tlumacz_slowa_pol(dbm,zb_slow_postawowych))
                    rezultat.write("\nAng: ")
                    s,angs = zb_slow_przetl_na_ang
                    for spa in angs:
                        rezultat.write("%s, " % spa)
                    slowa.append(zb_slow_przetl_na_ang)
            else:
                slowa = slowa1 

            n = m
            while n <= k:
                pary = []
                if n == 2:
                    pary = zip(slowa[:-1], slowa[1:])
                    for para in pary:
                        if pol_or_ang == 'pol':
                            lista_znalezionych_krotek_pol.append(para) 
                        else:
                            lista_znalezionych_krotek_ang.append(para)  
                elif n == 3:          
                    pary = zip(slowa[:-1], slowa[1:], slowa[2:])
                    for para in pary:
                        if pol_or_ang == 'pol':
                            lista_znalezionych_krotek_pol.append(para)
                        else:
                            lista_znalezionych_krotek_ang.append(para)  
                elif n == 4:          
                    pary = zip(slowa[:-1], slowa[1:], slowa[2:], slowa[3:])
                    for para in pary:
                        if pol_or_ang == 'pol':
                            lista_znalezionych_krotek_pol.append(para)
                        else:
                            lista_znalezionych_krotek_ang.append(para)  
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
