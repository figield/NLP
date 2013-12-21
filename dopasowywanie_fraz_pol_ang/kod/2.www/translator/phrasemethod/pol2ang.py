#!/usr/bin/python
# -*- coding: ISO-8859-2 -*-
import _plp
from libs.databasemanager import *
from libs.transWord import *
from libs.library import formy_podstawowe_slowa_pl, szukaj_synonimow, tlumacz_slowa_pol

def tlumacz_slowa_phrase(dbm,lista_fraz,sub_method):
    _plp.plp_init()
    lista_fraz = tlumacz_frazy(dbm,_plp,lista_fraz,sub_method)
    return frazy_do_listy(lista_fraz)

#lista_fraz = [(slowo1,[[slowo1,slowo2],[slowo1,slowo2,slowo3]),
#              (slowo2,[[slowo2,slowo3]]),
#              ...]
def tlumacz_frazy(dbm,_plp,lista_fraz,sub_method):
    lista_fraz_podst = []    
    for (slowo,listy_list_slow) in lista_fraz:
        lista_fraz_od_slowa = []
        for lista_slow in listy_list_slow:
            fraza_pol = ""
            dl = len(lista_slow)
            for s in lista_slow:
                fraza_pol += s + " "
            fraza_pol = fraza_pol.strip()
            frazy_ang = dbm.get_phrase_ang(dl,fraza_pol) 
            for (fraza_ang,) in frazy_ang:
                lista_fraz_od_slowa.append(fraza_ang)
        if len(lista_fraz_od_slowa) == 0:
            if sub_method == 0: # phrase
                lista_fraz_od_slowa.append(slowo)
            else:               #clp + phrase
                lista_fraz_od_slowa = tlumacz_slowa_pol(dbm,set(formy_podstawowe_slowa_pl(dbm,_plp,slowo,[])))
        lista_fraz_podst.append((slowo,lista_fraz_od_slowa))
    return lista_fraz_podst   


def frazy_do_listy(lista_fraz):
    wynik = list()
    for (slowo,lista_tl) in lista_fraz:
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



