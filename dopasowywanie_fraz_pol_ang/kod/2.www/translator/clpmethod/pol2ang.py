#!/usr/bin/python
# -*- coding: ISO-8859-2 -*-
import _plp
from libs.databasemanager import *
from libs.transWord import *
from libs.library import formy_podstawowe_slowa_pl, szukaj_synonimow, tlumacz_slowa_pol

def tlumacz_slowa_clp(dbm,lista_slow):
    _plp.plp_init()
    lista_slow_podst = do_fromy_podstawowej(dbm,_plp,lista_slow)
    return slowa_do_listy(lista_slow_podst)


def do_fromy_podstawowej(dbm,_plp,lista_slow):
    lista_slow_podst = []    
    for slowo in lista_slow:
        zb_slow_podstawowych = set(formy_podstawowe_slowa_pl(dbm,_plp,slowo,[]))
        #print str(zb_slow_podstawowych)
        zb_slow_przetl_na_ang = (slowo, tlumacz_slowa_pol(dbm,zb_slow_podstawowych))
        lista_slow_podst.append(zb_slow_przetl_na_ang)
    return lista_slow_podst   


def slowa_do_listy(lista_slow):
    wynik = list()
    for (slowo,lista_tl) in lista_slow:
        trans = TransWord()
        if len(lista_tl) == 1 and (slowo in lista_tl):
            trans.word_in = slowo
            trans.flag = 'false'
        else:
            trans.word_in = slowo
            trans.flag = 'true' 
            for r in lista_tl:
                trans.list_of_words.append(r)
        wynik.append(trans) 
        del trans  
    return wynik



