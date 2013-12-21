#!/usr/bin/python
# coding: latin-1
import os,sys,re
import string
from locale import *
from string import *

#setlocale(LC_ALL,'pl_PL')
#setlocale(LC_ALL,'pl_PL.latin-1')
#setlocale(LC_ALL,'pl_PL.ISO8859-2')
setlocale(LC_ALL,'pl_PL.utf8')
 

def filtr_zamianaNaMaleLiteryPL(tekst):
    tekst=tekst.lower()
    tekst=tekst.replace('¡','±')
    tekst=tekst.replace('Ê','ê')
    tekst=tekst.replace('Æ','æ')
    tekst=tekst.replace('¯','¿')
    tekst=tekst.replace('¬','¼')
    tekst=tekst.replace('Ó','ó')
    tekst=tekst.replace('¦','¶')
    tekst=tekst.replace('Ñ','ñ')
    tekst=tekst.replace('£','³')
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
    
          
def wydziel_frazy_zdaniowe(arg,kat):
    sciezka = arg.split('/')
    nazwa_pliku = sciezka[-1]
    frazy_alfabet = open(kat+'/zdania_alfabet_'+nazwa_pliku,'w')
    frazy_kolejno = open(kat+'/zdania_kolejno_'+nazwa_pliku,'w')
    
    zbior_fraz={}
 
    caly_tekst = open(arg,"r").read()
    caly_tekst = filtr_zamianaNaMaleLiteryPL(caly_tekst)
    caly_tekst = filtr_usuniecieNiewygodnychZnakow(caly_tekst)

    lista_fraz = re.compile("[0-9:;./(){}_<>!?^%=*&$#\-\+\"\r\[\]]*",re.L).split(caly_tekst)
    ilosc_fraz = len(lista_fraz)
    nr_frazy =0
    
    while nr_frazy < ilosc_fraz:
        fraza = lista_fraz[nr_frazy]
        nr_frazy = nr_frazy + 1
          
        # usuniecie np przecinka z poczatku frazy
        p1 = re.compile('^[ ,\'`]+')   
        # usuniecie np przecinka z konca frazy
        p2 = re.compile('[ ,\'`]+$') 
        
        fraza = fraza.strip()
        fraza=p1.sub('',fraza)
        fraza=p2.sub('',fraza)
        
        if len(fraza)<=1:
            continue
     
        frazy_kolejno.write(fraza + "\n")
          
        if zbior_fraz.get(fraza)==None:
            zbior_fraz[fraza]= 1
        else:
            zbior_fraz[fraza]= zbior_fraz[fraza] + 1
        
        
    k=zbior_fraz.keys()
    k.sort()
    for x in k:
        frazy_alfabet.write(x +" "+str(zbior_fraz[x]) + "\n")     
        
    frazy_alfabet.close()
    frazy_kolejno.close()
    
    
def main():
    katalog_z_wynikami = 'wyniki'
    #os.mkdir(katalog_z_wynikami)
    for arg in sys.argv[1:]: 
        wydziel_frazy_zdaniowe(arg,katalog_z_wynikami)
                
main()
