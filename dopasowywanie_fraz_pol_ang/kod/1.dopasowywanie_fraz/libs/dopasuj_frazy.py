#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from libs import _plp
from libs.library import *
from init.init import *
from libs.databasemanager import *
from init.myArgv import *


def run(args):   
    #---------------------------------
    loguj = args.logs
    trackuj = args.track
    wielkosc_chunka = args.chunk
    rozdzielnik_pol = args.split_pol 
    rozdzielnik_ang = args.split_ang
    m = args.ngram_min
    k = args.ngram_max
    roznica = args.diff 
    metoda = args.selection_method_number
    method = args.generation_method
    dane = args.texts
    to_file = args.to_file
    to_db = args.to_db
    typ_db = args.typ_db
    margines = args.margin
    radius = args.radius
    synchronization_method = args.synchronization_method    
    frozen_phrases_read = args.frozen_phrases_read
    frozen_phrases_write = args.frozen_phrases_write

    #---------------------------------
    dbm = DBmanager()
    _plp.plp_init() 
    koncowki_pol = lista_nonsensow_na_koncu_pol()
    poczatki_pol = lista_nonsensow_na_poczatku_pol()
    koncowki_ang = lista_nonsensow_na_koncu_ang()
    poczatki_ang = lista_nonsensow_na_poczatku_ang()
    slownik_ang  = zbior_slow_ang(dbm)
    exceptions_ang = zbior_wyjatkow_ang(dbm)
    zbior_fraz = wczytaj_zamrozone_frazy(frozen_phrases_read)
    wyjatki_pol_hash = {}
    teksty_rownolegle = get_text(dbm,dane,wielkosc_chunka,rozdzielnik_pol,rozdzielnik_ang,margines)
    names = [] #get_all_names(dbm)   
   
    #---------------------------------
    simple = True   
    if method != 'simple':
        simple = False
        method = "stat" 

    dopasowania_wynik = open('wyniki/' + method + '_dopasowanie_wynik.txt','w')
    if loguj:
        logs = open('logs/' + method + '_rezultat.txt','w')
        chunks_pol_file = open('logs/' + 'chunks_pol.txt','w')
        chunks_ang_file = open('logs/' + 'chunks_ang.txt','w')
    wyjatki_pol = open('logs/wyjatki_pol.txt','w')
    if trackuj: tracks = open('logs/' + method + '_postep.txt','w')

    (stat_pol,stat_ang) = init_stat('stats', simple, m, k)

    ilosc_tesktow = len(teksty_rownolegle)
    nr_analizowanego = 1
    file_name2 = ""    
        
    for (tekst_pol,tekst_ang,fname) in teksty_rownolegle:
        if loguj: 
            chunks_pol_file.write("\n"+ 50 * '*' +"\nchunk %d: \n %s" % (nr_analizowanego,tekst_pol))
            chunks_ang_file.write("\n"+ 50 * '*' +"\nchunk %d: \n %s" % (nr_analizowanego,tekst_ang))  

        lista_znalezionych_krotek_pol = []
        lista_znalezionych_krotek_ang = []
         
        if file_name2 != fname:
            file_name2 = fname
            print file_name2      

        for pol_or_ang in ['pol','ang']:
            tekst = ""
            if pol_or_ang == 'pol':
                tekst = zamiana_na_male_litery_pol(tekst_pol)
                tekst = zamiana_na_bez_kropek_pol(tekst)
                tekst = usuniecie_niewygodnych_znakow(tekst)
            else:
                tekst = zamiana_na_male_litery(tekst_ang) 
                tekst = zamiana_na_formy_rozszerzone_ang(tekst) 
                tekst = zamiana_na_bez_kropek_ang(tekst)
                tekst = usuniecie_niewygodnych_znakow(tekst)

            lista_zdan = get_lista_zdan(tekst)
            
            for zdanie in lista_zdan:
                zdanie = oczysc_zdanie(zdanie)
                if len(zdanie) < 5: continue
                if loguj: logs.write("\n\nZdanie: %s" % zdanie)
                slowa = re.compile("[ ]+",re.L).split(zdanie)
                slowa_krot = [] 
                if pol_or_ang == 'pol':          
                    for slowo in slowa:
                        zb_slow_podstawowych = set(formy_podstawowe_slowa_pl(dbm,_plp,slowo,names))
                        zb_slow_przetl_na_ang = (slowo, tlumacz_slowa_pol(dbm,zb_slow_podstawowych,wyjatki_pol_hash,slowo))
                        slowa_krot.append(zb_slow_przetl_na_ang)
                        if loguj:
                            logs.write("\n\nOrg:%s\nPodst:" % slowo)                        
                            for sp in zb_slow_podstawowych:
                                logs.write("%s," % sp)                        
                            logs.write("\nPol2Ang:")
                            s,angs = zb_slow_przetl_na_ang
                            for spa in angs:
                                logs.write("%s," % spa)
                else:
                    for slowo in slowa:
                        zb_slow_postawowych = set(formy_podstawowe_slowa_ang(dbm,slownik_ang,exceptions_ang,slowo,names))
                        zb_slow_przetl_ang = (slowo, zb_slow_postawowych)
                        slowa_krot.append(zb_slow_przetl_ang)
                        if loguj:
                            logs.write("\n\nOrg(ang):%s\nPodst:" % slowo)
                            for sp in zb_slow_postawowych:
                                logs.write("%s," % sp)

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
        print "%s>>ilosc krotek pol: %s; ilosc krotek ang: %s;" % (str(nr_analizowanego), str(len(lista_znalezionych_krotek_pol)), str(len(lista_znalezionych_krotek_ang)))
        if trackuj: tracks.write("%s>>ilosc krotek pol: %s; ilosc krotek ang: %s\n" % (str(nr_analizowanego), str(len(lista_znalezionych_krotek_pol)), str(len(lista_znalezionych_krotek_ang))))
         
        zrownoleglanie = True
        if synchronization_method == 'chunks':
            zrownoleglanie = False
 
        if zrownoleglanie:
            dl_listy_kr_pol = len(lista_znalezionych_krotek_pol)
            dl_listy_kr_ang = len(lista_znalezionych_krotek_ang)
        
            R = radius
            if dl_listy_kr_ang < 2*R:
               R = 50

            nr_kr_pol = 0
            sr_kr_ang = 0
            lista_id_znalezionych_kr = []  
            while nr_kr_pol < dl_listy_kr_pol:
                sr_kr_ang = srednia_arytm(lista_id_znalezionych_kr,sr_kr_ang)

                pa = sr_kr_ang - R
                if pa < 0:
                    pa = 0

                ka = sr_kr_ang  + R
                if ka > dl_listy_kr_ang:
                    ka = dl_listy_kr_ang 
               
                lista_id_znalezionych_kr = []
                while pa < ka:     
                    if dopasuj_krotki(lista_znalezionych_krotek_pol[nr_kr_pol],lista_znalezionych_krotek_ang[pa],zbior_fraz,roznica):
                        lista_id_znalezionych_kr.append(pa)
                    pa += 1 
                
                if len(lista_id_znalezionych_kr) == 0:
                    sr_kr_ang += nr_kr_pol % 2

                nr_kr_pol += 1
        else:
            for krotka_pl in lista_znalezionych_krotek_pol:
                for krotka_ang in lista_znalezionych_krotek_ang:
                    dopasuj_krotki(krotka_pl,krotka_ang,zbior_fraz,roznica)                


        nr_analizowanego += 1           
                    
    if loguj: logs.write("\n\nZnalezionych fraz: %d " % len(zbior_fraz)) 
    
    drukuj_dopasowane(dbm,dopasowania_wynik,zbior_fraz,metoda,poczatki_ang,koncowki_ang,to_file,to_db,typ_db)       
    dopasowania_wynik.close()
    zamroz_frazy(zbior_fraz,frozen_phrases_write)
    drukuj_wyjatki_pol(wyjatki_pol,wyjatki_pol_hash)
    wyjatki_pol.close()
    if loguj: 
        logs.close()
        chunks_pol_file.close()
        chunks_ang_file.close()
    if trackuj: 
        tracks.close()

