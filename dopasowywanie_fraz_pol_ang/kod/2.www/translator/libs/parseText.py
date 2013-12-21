#!/usr/bin/python
# -*- coding: ISO-8859-2 -*-
import os,sys,re
import string
from locale import *
from string import *


def filtr_zamianaNaMaleLiteryPL(tekst):
    tekst=tekst.lower()
    tekst=tekst.replace('Ą','ą')
    tekst=tekst.replace('Ę','ę')
    tekst=tekst.replace('Ć','ć')
    tekst=tekst.replace('Ż','ż')
    tekst=tekst.replace('Ź','ź')
    tekst=tekst.replace('Ó','ó')
    tekst=tekst.replace('Ś','ś')
    tekst=tekst.replace('Ń','ń')
    tekst=tekst.replace('Ł','ł')
    return tekst

def filtr_usuniecieNiewygodnychZnakow(tekst):
    tekst=tekst.replace('\\','')
    # usuniecie wielu spacji pod rzad
    p1 = re.compile('([ ]+|\n)') 
    tekst=p1.sub(' ',tekst)
    # zastapic mr. -> mr  ...itp
    p2 = re.compile('( mr.| Mr.|^Mr.|^mr.)')
    tekst=p2.sub(' mr',tekst) 
    p3 = re.compile('( ms.| Ms.|^Ms.|^ms.)')
    tekst=p3.sub(' ms',tekst) 
    p4 = re.compile('(\"mr.|\"Mr.)')
    tekst=p4.sub('\"mr',tekst)
    p5 = re.compile('(\"ms.|\"Ms.)')
    tekst=p5.sub('\"ms',tekst) 
    p6 = re.compile('(\'mr.|\'Mr.)')
    tekst=p6.sub('\'mr',tekst)
    p7 = re.compile('(\'ms.|\'Ms.)')
    tekst=p7.sub('\'ms',tekst)
    return tekst  
    

def wydziel_slowa(caly_tekst):
   
    caly_tekst = filtr_zamianaNaMaleLiteryPL(caly_tekst)
    caly_tekst = filtr_usuniecieNiewygodnychZnakow(caly_tekst)

    lista_slow1 = re.compile("[ 0-9:;.,/(){}_<>!?^%=*&$#\-\+\"\r\[\]]*",re.L).split(caly_tekst)
    lista_slow2 = []    
 
    for slowo in lista_slow1:
          
        # usuniecie apostrofu z poczatku/konca frazy
        p1 = re.compile('[\'`]+')    	
        slowo=p1.sub('',slowo)

        if len(slowo)<1:
            continue
        	
        lista_slow2.append(slowo)
        	
    return lista_slow2

# slowo1 slowo2 slowo3 slowo4
# 
#lista_fraz = [(slowo1,[[slowo1,slowo2],[slowo1,slowo2,slowo3]),
#              (slowo2,[[slowo2,slowo3]]),
#              ...]
def wydziel_frazy(caly_tekst):
    lista_fraz = []
    caly_tekst = filtr_zamianaNaMaleLiteryPL(caly_tekst)
    caly_tekst = filtr_usuniecieNiewygodnychZnakow(caly_tekst)

    lista_zdan1 = re.compile("[0-9:;.,/(){}_<>!?^%=*&$#\-\+\"\r\[\]]*",re.L).split(caly_tekst)
    lista_zdan2 = []    
 
    for z in lista_zdan1:
        p1 = re.compile('[\'`]+')    	
        zdanie = p1.sub('',z)
        if len(zdanie)<1:
            continue
        lista_zdan2.append(zdanie)

    for zd in lista_zdan2:
        lista_slow = zd.split()
        print lista_slow 
        dl = len(lista_slow)
        nr = 0
        while nr < dl:
            lista_list_slow = []
            slowo = lista_slow[nr]
            if (dl - nr) > 1: # frazy n = 2
                lista_list_slow.append([lista_slow[nr],lista_slow[nr+1]])

            if (dl - nr) > 2: # frazy n = 3
                lista_list_slow.append([lista_slow[nr],lista_slow[nr+1],lista_slow[nr+2]])

            if (dl - nr) > 3: # frazy n = 4
                lista_list_slow.append([lista_slow[nr],lista_slow[nr+1],lista_slow[nr+2],lista_slow[nr+3]])

            if (dl - nr) > 4: # frazy n = 5
                lista_list_slow.append([lista_slow[nr],lista_slow[nr+1],lista_slow[nr+2],lista_slow[nr+3],lista_slow[nr+4]])

            if (dl - nr) > 5: # frazy n = 6
                lista_list_slow.append([lista_slow[nr],lista_slow[nr+1],lista_slow[nr+2],lista_slow[nr+3],lista_slow[nr+4],lista_slow[nr+5]])
           
            nr += 1
            lista_fraz.append((slowo,lista_list_slow))
            
    print lista_fraz
    return lista_fraz




