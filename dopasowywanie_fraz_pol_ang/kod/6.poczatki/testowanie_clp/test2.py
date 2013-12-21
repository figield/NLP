#!/usr/bin/python
# -*- coding: latin2 -*-
import _plp,os,sys,re
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




def analiza_slowa(slowo):
    slowo = slowo.strip()
    string = _plp.plp_rec(slowo)
    numery = string.split(':')
    ile = int(numery[0])
    ids = numery[1:]
    wynik = ""     

    for nr in ids:
        i = int(nr)
        label = _plp.plp_label(i)
        bform = _plp.plp_bform(i)	
        forms = _plp.plp_forms(i)
        vec_id = _plp.plp_vec(i,slowo)
        
        wynik = wynik + "\nid: "+ str(i) + "\n"
        if len(label) >= 1:
	    wynik = wynik + "1)label: " + label + "\n"
	
        if len(bform) >= 1:
	     wynik = wynik + "2)bform: " + bform + "\n"
	
        if len(forms) >= 1:
	     wynik = wynik + "3)forms:" + forms + "\n"
	
        if len(vec_id) >= 1:
	     wynik = wynik + "4)vec_id: " + vec_id + "\n"
		
        label = ""
        bform = ""
        forms = ""
        vec_id= ""
    return wynik

def main(): 
    kat = 'wyniki'
    wyniki = open(kat+'/wynik.txt','w')
    lista_plikow= os.listdir(sys.argv[1])
    print "init..."
    _plp.plp_init()
    print "after init"
    print _plp.plp_ver()


    wstep = "Poczatki identyfikujace czesc mowy i rodzaj: \n AA - rzeczownik meski osobowy\n AB - rzeczownik meski zywotny\n AC - rzeczownik meski niezywotny\n AD - rzeczownik zenski\n AE - rzeczownik nijaki\n AF - rzeczownik plurale tantum osobowy\n AG - rzeczownik plurale tantum nieosobowy\n B - czasownik\n C - przymiotnik\n D - liczebnik\n E - zaimek\n G - nieodmienny\n"


    for arg in lista_plikow: 
        lista_slow = wydziel_slowa(sys.argv[1]+"/"+arg)
        wyniki.write(arg + "\n")
        wyniki.write("------------------------\n")
        wyniki.write(wstep)
        wyniki.write("------------------------\n")
        for s in lista_slow:
            wyniki.write(s + ", ")
        for slowo in lista_slow:
            wyniki.write("\n------------------------\n")
            wyniki.write("oryginalnie: " + slowo + "\n")
            wyniki.write(analiza_slowa(slowo))  
	    
    wyniki.close()    
	
main()
