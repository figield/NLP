#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from databasemanager import *
from levenshtein import *
from myHash import *


def formy_podstawowe_analiza_slowa_ang(slowo):
    slowo = slowo.strip()
    bform_list = []
    bform_list.append(slowo)
    return bform_list


def formy_podstawowe_slowa_pl(_plp,slowo):
    slowo = slowo.strip()
    string = _plp.plp_rec(slowo)
    numery = string.split(':')
    ids = numery[1:]
    bform_list = []
    for nr in ids:
        i = int(nr)
        label = _plp.plp_label(i)
        bform = _plp.plp_bform(i)	
        if len(bform) >= 1:
	    bform_list.append(bform)
        bform = ""
    if len(bform_list)==0:
        bform_list.append(slowo)
    return bform_list 
 

def tlumacz_slowa_pol(dbm,zb_slow_postawowych):
    zbior_slow_przetlumaczonych = set()
    for slowo_pl in zb_slow_postawowych:
        records = dbm.get_translation_pol2ang(slowo_pl)
        if len(records) == 0:
            zbior_slow_przetlumaczonych.add(slowo_pl)
        else:
            for (r,) in records:
                zbior_slow_przetlumaczonych.add(r.strip())
    return zbior_slow_przetlumaczonych


def dopasuj_krotki(dbm,krotka_pl,krotka_ang,zbior_fraz):
    licznik = 0
    stop = len(krotka_pl)
    fraza_pol = ""
    for (slowo_pl,z) in krotka_pl:
        fraza_pol += "%s " %  slowo_pl
    fraza_pol = fraza_pol.strip()
    for (slowo_pl, zb_slow_przetl_na_ang) in krotka_pl:
        znal = False
        for slowo_ang in krotka_ang:
            for slowo_pl2ang in zb_slow_przetl_na_ang:       
               if slowo_pl2ang[:-1] == slowo_ang[:-1]:#levenshtein(slowo_pl2ang,slowo_ang)< 2:
                   znal = True
                   licznik +=1
                   break
            if znal: break
        if licznik == stop:
            fraza_ang = zamien_na_fraze(krotka_ang)
            if zbior_fraz.get(fraza_pol)==None:
                zbior_fraz[fraza_pol] = set()
                zbior_fraz[fraza_pol].add(MyHash(fraza_ang,1))
            else:
                exist = False
                for r in zbior_fraz[fraza_pol]:
                    if r.f == fraza_ang:
                        r.n += 1
                        exist = True
                        break
                if not exist:
                    zbior_fraz[fraza_pol].add(MyHash(fraza_ang,1))
            break
               
def zamien_na_fraze(krotka):
    fraza = ""
    for k in krotka:
        fraza += '%s ' % (k)
    return fraza.strip()

def drukuj_dopasowane(dopasowania_wynik,zbior_fraz):   
    frazy_pol = zbior_fraz.keys()     
    for fraza_pol in frazy_pol:
        dopasowania_wynik.write("\n"+fraza_pol + ":\n")
        for r in zbior_fraz[fraza_pol]:
            if r.n > 0 :
                dopasowania_wynik.write("\t"+ str(r.n) + "\t" + r.f + "\n")

