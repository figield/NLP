#!/usr/bin/python
# -*- coding: latin2 -*-
import _plp,os,sys,re
import string
from locale import *
from string import *
from databasemanager import *

 
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
    

def wydziel_slowa(arg):
   
    caly_tekst = open(arg,"r").read()
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


def tlumacz_slowa(dbm,lista_slow,wyniki):
    znalezione = 0
    nieznalezione = 0
    lista_slow_podst = doFromyPodstawowej(lista_slow)
    print "Ilość słów w formie podstawowej: "+str(len(lista_slow_podst))
    for slowo in lista_slow_podst:
        records = dbm.getEnglishWord(slowo)
        if len(records) < 1 :
            wyniki.write(slowo+" - 0\n")
            nieznalezione = 1 + nieznalezione  
        else:
            znalezione = 1 + znalezione 
            for r in records:
                wyniki.write(r[0]+" -> "+ r[1] +"\n")   
    print "Przetłumaczono: " + str(znalezione) + " słów ("+str((100.0*znalezione/len(lista_slow_podst))) +"%)"
    print "Nie znaleziono: " + str(nieznalezione) + " słów ("+str((100.0*nieznalezione/len(lista_slow_podst)))+"%)"

def doFromyPodstawowej(lista_slow):
    lista_slow_podst = []
    
    for slowo in lista_slow:
        string = _plp.plp_rec(slowo)
        numery = string.split(':')
        ile = int(numery[0])
        ids = numery[1:]
        if ile < 1:
            lista_slow_podst.append(slowo)
        else:    
            for nr in ids:
                i = int(nr)
                bform = _plp.plp_bform(i)
                lista_slow_podst.append(bform)

    return lista_slow_podst

def main(): 
    kat = 'wyniki'
    wyniki = open(kat+'/wynik.txt','w')
    lista_plikow= os.listdir(sys.argv[1])
    dbm = DBmanager()
    print "init..."
    _plp.plp_init()
    print "after init"
    print _plp.plp_ver()

    for arg in lista_plikow: 
        print "Tłumaczony tekst: " + sys.argv[1]+"/"+arg
        lista_slow = wydziel_slowa(sys.argv[1]+"/"+arg)
        print "Ilość słów oryginalnych: "+str(len(lista_slow))
        wyniki.write("\nPlik: " + arg + "\n")
        wyniki.write("--------------------------\n")
        tlumacz_slowa(dbm,lista_slow,wyniki)  
	    
    wyniki.close()    
	
main()
