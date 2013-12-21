#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from cPickle import load
 
def get_text(dbm,texts,wielkosc_chunka,rozdzielnik_pol,rozdzielnik_ang,margin):
    if texts == 'dane':
        lista_tekstow_rownoleglych = []
        lista_plikow = os.listdir(texts+"/pol") 
        # pobranie samych nazw plikow
        # w obu kat. pliki nazywaja sie tak samo
        for fname in lista_plikow:
            tekst_pol = open(texts + "/pol/"+fname,"r").read()
            tekst_ang = open(texts +"/eng/"+fname,"r").read()
            ilosc_chunkow = len(tekst_pol) / wielkosc_chunka
            print str(ilosc_chunkow)
            tekst_pol_def = defragmentuj_tekst_pol(ilosc_chunkow,tekst_pol,rozdzielnik_pol)
            tekst_ang_def = defragmentuj_tekst_ang(ilosc_chunkow,tekst_ang,rozdzielnik_ang,margin)
            if len(tekst_pol_def) == len(tekst_ang_def):
                i = 0
                ile = len(tekst_pol_def)  
                while i < ile: 
                    lista_tekstow_rownoleglych.append((tekst_pol_def[i],tekst_ang_def[i],fname))
                    i+=1
            else:
                print fname
                print "ilosc fragmentow z obu tekstow nie zgadza sie!"
        print "Ilosc chunkow: %d" % len(lista_tekstow_rownoleglych)
    else:
        for (t1,t2) in dbm.get_both_sentences():
            lista_tekstow_rownoleglych.append((t1,t2,"database"))
    return lista_tekstow_rownoleglych


def defragmentuj_tekst_pol(ilosc_chunkow,tekst,rozdzielnik):
    lista_frag = []
    lista_tekstow = re.compile(rozdzielnik,re.L).split(tekst)
    if ilosc_chunkow == 0: 
        ilosc_chunkow = 1
    for fragment_tekstu in lista_tekstow[1:]:
        size = len(fragment_tekstu)/ilosc_chunkow
        i = 1
        id_p = 0
        while i <= ilosc_chunkow:
            (chunk,id_p) = tnij_po_zdaniach_pol(fragment_tekstu,size,i,id_p)
            lista_frag.append(chunk)
            i+=1
    return lista_frag


def defragmentuj_tekst_ang(ilosc_chunkow,tekst,rozdzielnik,M):
    lista_frag = []
    lista_tekstow = re.compile(rozdzielnik,re.L).split(tekst)
    if ilosc_chunkow == 0: 
        ilosc_chunkow = 1
    for fragment_tekstu in lista_tekstow[1:]:
        size = len(fragment_tekstu)/ilosc_chunkow
        i = 1
        while i <= ilosc_chunkow:
            chunk = tnij_po_zdaniach_ang(fragment_tekstu,size,i,M)
            lista_frag.append(chunk)
            i+=1
    return lista_frag


def tnij_po_zdaniach_pol(fragment_tekstu,size,i,id_p):
    id_k_temp = 0
    chunk = ""
    
    id_k_temp = (i * size) - 1
    
    while fragment_tekstu[id_k_temp] not in ['.',';',',','\n\n']:
        id_k_temp += 1
        if id_k_temp >= len(fragment_tekstu):
            id_k_temp = len(fragment_tekstu) - 1 
            break

    if id_k_temp + 1 == len(fragment_tekstu):
        None 
    else:
        id_k_temp = id_k_temp + 1
    
    chunk = fragment_tekstu[id_p:id_k_temp]

    return (chunk,id_k_temp)


def tnij_po_zdaniach_ang(fragment_tekstu,size,i,M):
    id_k_temp = 0
    id_p_temp = 0
    chunk = ""

    if i == 1:
        id_p_temp = 0
        id_k_temp = size + M + 1
    else:
        id_p_temp = ((i-1) * size) - M + 1 
        id_k_temp = (i * size) + M + 1
        if id_k_temp >= len(fragment_tekstu):
            id_k_temp = len(fragment_tekstu) - 1 
        
    while fragment_tekstu[id_p_temp] not in ['.',';',',','\n\n']:
        id_p_temp -= 1
        if id_p_temp < 0:
            id_p_temp = 0 
            break
    id_p_temp += 1

    dl_frag = len(fragment_tekstu)
    while id_k_temp < dl_frag and fragment_tekstu[id_k_temp] not in ['.',';',',','\n\n']:
        id_k_temp += 1
        if id_k_temp >= len(fragment_tekstu):
            id_k_temp = len(fragment_tekstu)
            break
    id_k_temp += 1
  
    chunk = fragment_tekstu[id_p_temp:id_k_temp]

    return chunk

def init_stat(kat,simple,m,k):
    stat_pol2 = set()
    stat_pol3 = set()
    stat_pol4 = set()
    stat_pol5 = set()
    stat_pol6 = set()
    stat_ang2 = set()
    stat_ang3 = set()
    stat_ang4 = set()
    stat_ang5 = set()
    stat_ang6 = set()
    
    if not simple:
        for pol_or_ang in ['pol','ang']:
            n = m
            while n<=k:    
                print "Pobranie statystyk %d wyrazowych..." % (n)   
                if pol_or_ang == 'pol':
                    if n == 2:
                        stat_pol2 = load(open(kat+'/stat_pol2.pic','r')) 
                    elif n == 3:
                        stat_pol3 = load(open(kat+'/stat_pol3.pic','r'))
                    elif n == 4:
                        stat_pol4 = load(open(kat+'/stat_pol4.pic','r'))
                    elif n == 5:
                        stat_pol5 = load(open(kat+'/stat_pol5.pic','r'))
                    elif n == 6:
                        stat_pol6 = load(open(kat+'/stat_pol6.pic','r')) 
                else:
                    if n == 2:
                        stat_ang2 = load(open(kat+'/stat_ang2.pic','r'))
                    elif n == 3:
                        stat_ang3 = load(open(kat+'/stat_ang3.pic','r'))
                    elif n == 4:
                        stat_ang4 = load(open(kat+'/stat_ang4.pic','r'))
                    elif n == 5:
                        stat_ang5 = load(open(kat+'/stat_ang5.pic','r'))
                    elif n == 6:
                        stat_ang6 = load(open(kat+'/stat_ang6.pic','r'))
                n+=1 
    return ([stat_pol2,stat_pol3,stat_pol4,stat_pol5,stat_pol6],[stat_ang2,stat_ang3,stat_ang4,stat_ang5,stat_ang6])


def wczytaj_zamrozone_frazy(frozen_phrases_read):
    zbior_fraz = {}
# dorzuc try!
    if frozen_phrases_read:
        lista_plikow = os.listdir("frozen_phrases") 
        if len(lista_plikow) == 1:
            for zbf in lista_plikow:
                zbior_fraz = load(open('frozen_phrases/'+ zbf ,'r'))
                break
    return zbior_fraz 

def get_all_names(dbm):
    imiona = dbm.get_all_names()
    names = set()
    for (n,) in imiona:
        names.add(n.lower())  
    return names

def zbior_slow_ang(dbm):
    records = dbm.get_verb_and_noun()
    slownik_ang = set()
    for (s,t) in records:
        slownik_ang.add((s,t))
    return slownik_ang


def zbior_wyjatkow_ang(dbm):
    zb_ex = set()
    lista_ex = dbm.get_exceptions_ang_all()
    for (ex,) in lista_ex:
        zb_ex.add(ex)
    return zb_ex

def lista_nonsensow_na_poczatku_pol():
    return ['-','i', 'oraz','lub','albo','się', 'self', 'in','i', 'a','ą','b','c','ć','d','e', 'ę','f','g','h','j','k','l','ł','m','n','ń','ó','p', 'r','s','ś','t','ż','ż', 'ź','x','y','v','vi','iv','iii','ii','ix','xi','vii','viii','x','xi','xii','xiii','xiv','xv','xvi']


def lista_nonsensow_na_koncu_pol():    
    return ['na','-','z','oraz','lub','w','self','in','i','a','ą','b','c','ć','d','e','ę','f','g','h','j','k','l','ł','m','n','ń','ó','p','r','s','ś', 't','ż','ż','ź','x','y','v','vi','iv','iii','ii','ix','xi','vii','viii','x','xi','xii','xiii','xiv','xv','xvi'] 
  

def lista_nonsensow_na_poczatku_ang():
    return ['-','and','or','b','c','d','e','f','g','h','j','k','l','m','n','o','p','r','s','t','u','w','z','x', 'y','v','vi','iv','iii','ii','ix','xi','vii','viii','x','xi','xii','xiii','xiv','xv','xvi']


def lista_nonsensow_na_koncu_ang():
    return ['and','-','or','i','the','a','an','b','c','d','e','f','g','h','j','k','l','m','n','o','p','r', 's','t','u','w','z','x','y','v','vi','iv','iii','ii','ix','xi','vii','viii','x','xi','xii','xiii','xiv','xv','xvi']

