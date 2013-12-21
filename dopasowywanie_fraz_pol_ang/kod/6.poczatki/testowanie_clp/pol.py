#!/usr/bin/python
# coding: latin-1
import _plp,os,sys,re
import string
from locale import *
from string import *

setlocale(LC_ALL,'pl_PL.utf8')
 
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


def doFromyPodstawowej(lista_slow,wyniki):
    
    for slowo in lista_slow:
        string = _plp.plp_rec(slowo)
        numery = string.split(':')
        ile = int(numery[0])
        ids = numery[1:]
        if ile < 1:
            wyniki.write(slowo + "- ??\n" )
        else:    
            for nr in ids:
                i = int(nr)
                bform = _plp.plp_bform(i)
                wyniki.write(slowo +" -> "+ bform + "\n")
    return 1

def main(): 
    kat = 'wyniki'
    wyniki = open(kat+'/wynik.txt','w')
    lista_plikow= os.listdir(sys.argv[1])
    print "init..."
    _plp.plp_init()
    print "after init"
    print _plp.plp_ver()

    for arg in lista_plikow: 
        print "Tekst: " + sys.argv[1]+"/"+arg
        lista_slow = wydziel_slowa(sys.argv[1]+"/"+arg)
        wyniki.write(arg + "\n")
        wyniki.write("------------------------\n")
        doFromyPodstawowej(lista_slow,wyniki)  
	    
    wyniki.close()    
	
main()
