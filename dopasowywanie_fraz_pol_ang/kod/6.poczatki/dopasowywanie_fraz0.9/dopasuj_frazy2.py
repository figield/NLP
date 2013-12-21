#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from cPickle import load
from libs.library import *
from libs import _plp
from init.init import *
from libs.databasemanager import *


def main():   
    kat = 'wyniki'
    dbm = DBmanager()
    _plp.plp_init() 
    koncowki_pol = lista_nonsensow_na_koncu_pol()
    poczatki_pol = lista_nonsensow_na_poczatku_pol()
    koncowki_ang = lista_nonsensow_na_koncu_ang()
    poczatki_ang = lista_nonsensow_na_poczatku_ang()
    zbior_fraz = {}

    teksty_rownolegle = get_text(dbm,sys.argv)
    names = get_all_names(dbm)   

    simple = True   
    method = "simple"
    if 'simple' not in sys.argv:
        simple = False
        method = "stat" 

    dopasowania_wynik = open(kat + '/' + method + '_dopasowanie_wynik.txt','w')
    rezultat = open(kat + '/' + method + '_rezultat.txt','w')
    m = 2
    k = 6
    h = 1

    (stat_pol,stat_ang) = init_stat('stat', simple,m,k)
                
    for (tekst_pol,tekst_ang) in teksty_rownolegle:
        lista_znalezionych_krotek_pol = []
        lista_znalezionych_krotek_ang = []        

        for pol_or_ang in ['pol','ang']:
            tekst = ""
            if pol_or_ang == 'pol':
                tekst = zamiana_na_male_litery_pol(tekst_pol)
                tekst = usuniecie_niewygodnych_znakow(tekst)
            else:
                tekst = zamiana_na_male_litery(tekst_ang) 
                tekst = zamiana_na_formy_rozszerzone_ang(tekst) 
                tekst = zamiana_na_bez_kropek_ang(tekst)
                tekst = usuniecie_niewygodnych_znakow(tekst)

            lista_zdan = get_lista_zdan(tekst)
            
            for zdanie in lista_zdan:
                zdanie = oczysc_zdanie(zdanie)
                rezultat.write("\n\nZdanie: %s" % zdanie)
                slowa = re.compile("[ ]+",re.L).split(zdanie)
                slowa_krot = [] 
                if pol_or_ang == 'pol':          
                    for slowo in slowa:
                        zb_slow_podstawowych = set(formy_podstawowe_slowa_pl(dbm,_plp,slowo,names))
                        zb_slow_przetl_na_ang = (slowo, tlumacz_slowa_pol(dbm,zb_slow_podstawowych))
                        slowa_krot.append(zb_slow_przetl_na_ang)
                        # - print -
                        rezultat.write("\n\nOrg:%s\nPodst:" % slowo)                        
                        for sp in zb_slow_podstawowych:
                            rezultat.write("%s," % sp)                        
                        rezultat.write("\nPol2Ang:")
                        s,angs = zb_slow_przetl_na_ang
                        for spa in angs:
                            rezultat.write("%s," % spa)
                else:
                    for slowo in slowa:
                        zb_slow_postawowych = set(formy_podstawowe_slowa_ang(dbm,slowo,names))
                        zb_slow_przetl_ang = (slowo, zb_slow_postawowych)
                        slowa_krot.append(zb_slow_przetl_ang)
                        # - print -
                        rezultat.write("\n\nOrg(ang):%s\nPodst:" % slowo)
                        for sp in zb_slow_postawowych:
                            rezultat.write("%s," % sp)

                n = m
                while n <= k:                
                    krotki = []
                    if n == 2 and len(slowa) >= 2:                    
                        krotki = zip(slowa[:-1], slowa[1:])      
                        pary_krot = zip(slowa_krot[:-1], slowa_krot[1:])
                    elif n == 3 and len(slowa) >= 3:
                        krotki = zip(slowa[:-1], slowa[1:], slowa[2:])
                        pary_krot = zip(slowa_krot[:-1], slowa_krot[1:], slowa_krot[2:])
                    elif n == 4 and len(slowa) >= 4:                
                        krotki = zip(slowa[:-1], slowa[1:], slowa[2:], slowa[3:])
                        pary_krot = zip(slowa_krot[:-1], slowa_krot[1:], slowa_krot[2:], slowa_krot[3:])
                    elif n == 5 and len(slowa) >= 5:
                        krotki = zip(slowa[:-1], slowa[1:], slowa[2:], slowa[3:], slowa[4:])
                        pary_krot = zip(slowa_krot[:-1], slowa_krot[1:], slowa_krot[2:], slowa_krot[3:], slowa_krot[4:])
                    elif n == 6 and len(slowa) >= 6:
                        krotki = zip(slowa[:-1], slowa[1:], slowa[2:], slowa[3:], slowa[4:], slowa[5:])
                        pary_krot = zip(slowa_krot[:-1], slowa_krot[1:], slowa_krot[2:], slowa_krot[3:], slowa_krot[4:], slowa_krot[5:])

                    y = len(krotki)
                    x = 0
                    while x < y:
                        if pol_or_ang == 'pol':
                            if selekcja_krotek(poczatki_pol,koncowki_pol,krotki[x]):                            
                                if simple:
                                    lista_znalezionych_krotek_pol.append(pary_krot[x])
                                else:
                                    if krotki[x] in stat_pol[n-2]:
                                        lista_znalezionych_krotek_pol.append(pary_krot[x])
                        else:
                            if selekcja_krotek(poczatki_ang,koncowki_ang,krotki[x]):
                                if simple:
                                    lista_znalezionych_krotek_ang.append(pary_krot[x])
                                else:
                                    if krotki[x] in stat_ang[n-2]:
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
