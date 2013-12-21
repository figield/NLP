#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from locale import *
from string import *

def filtr_zamianaNaMaleLitery(tekst):
    tekst=tekst.lower()
    return tekst

def filtr_zamianaNaMaleLiteryPL(tekst):
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
    tekst=tekst.replace('....\"','')
    tekst=tekst.replace('...','.')
    
    p1 = re.compile('([ ]+|\n)') 
    tekst=p1.sub(' ',tekst)
    return tekst
     
def filtr_zamianaNaBezKropekAng(tekst):
    p1 = re.compile('(\'mrs.|\'Mrs.|\"mrs.|\"Mrs.| mrs.| Mrs.|^Mrs.|^mrs.)')
    #tekst=tekst.replace('(\'mrs.|\'Mrs.|\"mrs.|\"Mrs.| mrs.| Mrs.|^Mrs.|^mrs.)',' mrs')
    tekst=p1.sub(' mrs',tekst)
    
    p2 = re.compile('( mr.| Mr.|^Mr.|^mr.|\"mr.|\"Mr.|\'mr.|\'Mr.)')  # czemu to działa źle??????
    #tekst=tekst.replace('( mr.| Mr.|^Mr.|^mr.|\"mr.|\"Mr.|\'mr.|\'Mr.)',' mr')
    tekst=p2.sub(' mr',tekst) 
    
    p3 = re.compile('( ms.| Ms.|^Ms.|^ms.|\"ms.|\"Ms.|\'ms.|\'Ms.)')
    tekst=p3.sub(' ms',tekst)

    return tekst  

def filtr_zamianyNaFormyRozszerzoneAng(tekst):
    tekst=re.compile('haven\'t').sub('have not',tekst)
    tekst=re.compile('hasn\'t').sub('has not',tekst)
    tekst=re.compile('hadn\'t').sub('had not',tekst)
    tekst=re.compile('(can\'t|cannot)').sub('can not',tekst)
    tekst=re.compile('couldn\'t').sub('could not',tekst)
    tekst=re.compile('shouldn\'t').sub('should not',tekst)
    tekst=re.compile('won\'t').sub('will not',tekst)
    tekst=re.compile('wouldn\'t').sub('would not',tekst)
    tekst=re.compile('wasn\'t').sub('was not',tekst)
    tekst=re.compile('weren\'t').sub('were not',tekst)
    tekst=re.compile('(isn\'t|ain\'t)').sub('is not',tekst)
    tekst=re.compile('aren\'t').sub('are not',tekst)
    tekst=re.compile('mustn\'t').sub('must not',tekst)
    tekst=re.compile('mightn\'t').sub('might not',tekst)    
    tekst=re.compile('needn\'t').sub('need not',tekst)
    tekst=re.compile('don\'t').sub('do not',tekst)
    tekst=re.compile('doesn\'t').sub('does not',tekst)
    tekst=re.compile('didn\'t').sub('did not',tekst)
    tekst=re.compile('\'ll').sub(' will',tekst)
#    tekst=re.compile('\'s a ').sub(' is a ',tekst)
#    tekst=re.compile('\'s an ').sub(' is an ',tekst)
#    tekst=re.compile('\'s the ').sub(' is the ',tekst)
    tekst=re.compile('i\'m').sub('i am',tekst)
    tekst=re.compile('\'d better').sub(' had better',tekst)
    tekst=re.compile('\'d rather').sub(' would rather',tekst)
    tekst=re.compile('\'d sooner').sub(' would sooner',tekst)
    tekst=re.compile('\'ve ').sub(' have ',tekst)
    return tekst

    

def wydziel_zdania(flaga,plik):
    
    caly_tekst = open(plik,"r").read()
    caly_tekst = filtr_zamianaNaMaleLitery(caly_tekst)
    caly_tekst = filtr_usuniecieNiewygodnychZnakow(caly_tekst)
    if flaga=='pol':
        caly_tekst = filtr_zamianaNaMaleLiteryPL(caly_tekst)
    elif flaga=='ang':
        caly_tekst = filtr_zamianyNaFormyRozszerzoneAng(caly_tekst)
        caly_tekst = filtr_zamianaNaBezKropekAng(caly_tekst) 
    
    lista_zdan = re.compile("([0-9.:;/(){}_<>!?^%=*&$#\-\+\"\r\[\]]*)",re.L).split(caly_tekst)
    lista_zdan_oczyszczonych = []
    
    for zdanie in lista_zdan:
        p1 = re.compile('(^[ ,\'`]+|[ ,\'`]+$)')   
        p2 = re.compile('[\']+')
        p3 = re.compile('[ ]+')
        zdanie=p1.sub('',zdanie)
        #zdanie=p2.sub('\\\'',zdanie) # to jakby do bazy wpisaywal...
        zdanie=p3.sub(' ',zdanie) 

        if len(zdanie)<5:
            continue
        
        lista_zdan_oczyszczonych.append(zdanie)
	
	# czy nelezy sprowadzic kazde(...?) slowo do formy podstawowej przy uzyciu clp 2 etap
	# nalezy sie zastanowic ktora forme podstawowa brac pod uwage!
	            
    return lista_zdan_oczyszczonych

    
    
def main():
    kat = 'wyniki'
    lista_zdan_pol=[]
    lista_zdan_ang=[]
    lista_zdan_pol_synch=[]
    lista_zdan_ang_synch=[]
    
    if sys.argv[1]=='-pol':
        lista_zdan_pol=wydziel_zdania('pol',sys.argv[2])
        lista_zdan_ang=wydziel_zdania('ang',sys.argv[4])
    
    if sys.argv[1]=='-ang':
        lista_zdan_ang=wydziel_zdania('ang',sys.argv[2]) 
        lista_zdan_pol=wydziel_zdania('pol',sys.argv[4])   
      
      
    #---synchronizacja na podstwie ilosci slow---#
    DELTA = 35 # % dluzszego zdania
    nr_p = 0
    nr_a = 0
    koniec_listy_ang = False
    koniec_listy_pol = False
    
    while True:
        diff = abs(len(lista_zdan_pol[nr_p])-len(lista_zdan_ang[nr_a]))
        diff2 = 0.0
        if len(lista_zdan_pol[nr_p])>len(lista_zdan_ang[nr_a]):
            diff2 = (1.0 * diff / len(lista_zdan_pol[nr_p]))*100
        else:
            diff2 = (1.0 * diff / len(lista_zdan_ang[nr_a]))*100
        
        if diff2 >= DELTA:
            print diff2
            if len(lista_zdan_pol[nr_p])> len(lista_zdan_ang[nr_a]):
                lista_zdan_pol_synch.append(lista_zdan_pol[nr_p])
                if(nr_a+1)<len(lista_zdan_ang):
                    lista_zdan_ang_synch.append(lista_zdan_ang[nr_a]+ " # " + lista_zdan_ang[nr_a+1])
                    nr_a = nr_a + 1
                else:
                    lista_zdan_ang_synch.append(lista_zdan_ang[nr_a])
                    koniec_listy_ang = True
            else:
                lista_zdan_ang_synch.append(lista_zdan_ang[nr_a])
                if(nr_p+1)<len(lista_zdan_pol):
                    lista_zdan_pol_synch.append(lista_zdan_pol[nr_p]+ " # " + lista_zdan_pol[nr_p+1])
                    nr_p = nr_p + 1
                else:
                    lista_zdan_pol_synch.append(lista_zdan_pol[nr_p])
                    koniec_listy_pol = True
        else:
            lista_zdan_pol_synch.append(lista_zdan_pol[nr_p])
            lista_zdan_ang_synch.append(lista_zdan_ang[nr_a])
        
        nr_p = nr_p + 1
        nr_a = nr_a + 1
        
        if nr_p == len(lista_zdan_pol):
            koniec_listy_pol = True
        
        if nr_a == len(lista_zdan_ang):
            koniec_listy_ang = True
        
        if koniec_listy_pol:
            while nr_a < len(lista_zdan_ang):
                lista_zdan_ang_synch.append(lista_zdan_ang[nr_a])
                nr_a = nr_a + 1
            break
            
        if koniec_listy_ang:
            while nr_p < len(lista_zdan_pol):
                lista_zdan_pol_synch.append(lista_zdan_pol[nr_p])
                nr_p = nr_p + 1
            break
                         
    print "Ilosc zdan polskich:" + str(len(lista_zdan_pol))  
    print "Ilosc zdan angielskich:" + str(len(lista_zdan_ang))   
    print "Ilosc zdan polskich po synchronizacji:" + str(len(lista_zdan_pol_synch))  
    print "Ilosc zdan angielskich po synchronizacji:" + str(len(lista_zdan_ang_synch))      
 
      
    zdania_pol_ang = open(kat+'/zdania_pol_ang.txt','w')  
    if len(lista_zdan_pol_synch)> len(lista_zdan_ang_synch):
        nr = 0
        while nr < len(lista_zdan_ang_synch):
            zdania_pol_ang.write(lista_zdan_pol_synch[nr]+"\n")
            zdania_pol_ang.write(lista_zdan_ang_synch[nr]+"\n\n")
            nr = nr + 1
        while nr < len(lista_zdan_pol_synch):
            zdania_pol_ang.write(lista_zdan_pol_synch[nr]+"\n")
            nr = nr + 1
    else:
        nr = 0
        while nr < len(lista_zdan_pol_synch):
            zdania_pol_ang.write(lista_zdan_pol_synch[nr]+"\n")
            zdania_pol_ang.write(lista_zdan_ang_synch[nr]+"\n\n")
            nr = nr + 1
        while nr < len(lista_zdan_ang_synch):
            zdania_pol_ang.write(lista_zdan_ang_synch[nr]+"\n")
            nr = nr + 1
                     
    zdania_pol_ang.close()      
    print "koniec"        
main()
