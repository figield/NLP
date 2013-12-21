#!/usr/bin/python
# -*- coding: latin2 -*-
import _plp,os,sys,re
import string
from locale import *
from string import *
from databasemanager import *

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
    tekst=tekst.replace(' -',' ')
    tekst=tekst.replace('- ',' ')
    
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
    
    lista_zdan = re.compile("([0-9.:;/(){}_<>!?^%=*&$#\+\"\r\[\]]*)",re.L).split(caly_tekst)
    lista_zdan_oczyszczonych = []
    
    for zdanie in lista_zdan:
        p1 = re.compile('(^[ ,\'`\-]+|[ ,\'`\-]+$)')   
        p2 = re.compile('[\']+')
        p3 = re.compile('[ ]+')
        zdanie=p1.sub('',zdanie)
        #zdanie=p2.sub('\\\'',zdanie) # to jakby do bazy wpisaywal...
        zdanie=p3.sub(' ',zdanie) 

        if len(zdanie)<5:
            continue
        
        lista_zdan_oczyszczonych.append(zdanie)
	            
    return lista_zdan_oczyszczonych



def tlumacz_slowa_na_ang(dbm,lista_slow):
    lista_slow_podst = doFormyPodstawowej(lista_slow)
    lista_rekordow_tlumaczen = []
    
    for slowo in lista_slow_podst:
        records = dbm.getEnglishWord(slowo)
        if len(records) > 0 :
            lista_rekordow_tlumaczen.append(records) 
        else:
            slowo_rec = []
            slowo_rec.append(slowo)
            slowo_rec.append(slowo)
            slowo_rec_list = []
            slowo_rec_list.append(slowo_rec)
            lista_rekordow_tlumaczen.append(slowo_rec_list)
    
    return lista_rekordow_tlumaczen
    
    
def doFormyPodstawowej(lista_slow):
    lista_slow_podst = []
    slowa_str = "\nBASE FORM: "
    no_replay = ""
    
    for slowo in lista_slow:
        string = _plp.plp_rec(slowo)
        numery = string.split(':')
        ile = int(numery[0])
        ids = numery[1:]
        if ile < 1:
            slowa_str = slowa_str + ", #" + slowo
            lista_slow_podst.append(slowo)
        else:    
            for nr in ids:
                i = int(nr)
                bform = _plp.plp_bform(i)
                if no_replay != bform:
                    lista_slow_podst.append(bform)
                    slowa_str = slowa_str + ", " + bform
                no_replay = bform
    
    print slowa_str
    return lista_slow_podst
    
    
def wydziel_slowa_pol(tekst):
    lista_slow1 = re.compile("[ ,]*",re.L).split(tekst)
    lista_slow2 = []    
    slowa_str = "\nORGINAL: "
 
    for slowo in lista_slow1:
        if len(slowo)<1:
            continue
        slowa_str = slowa_str + ", " +  slowo    
        lista_slow2.append(slowo)
        	
    print slowa_str    	
    return lista_slow2
    
    
    
def main():
    kat = 'wyniki'
    lista_zdan_pol=[]
    lista_zdan_ang=[]
    lista_zdan_pol_synch=[]
    lista_zdan_ang_synch=[]
    
    print "init data base connector"
    dbm = DBmanager()
    print "init CLP"
    _plp.plp_init()
    print _plp.plp_ver()
    
    
    if sys.argv[1]=='-pol':
        lista_zdan_pol=wydziel_zdania('pol',sys.argv[2])
        lista_zdan_ang=wydziel_zdania('ang',sys.argv[4])
    
    if sys.argv[1]=='-ang':
        lista_zdan_ang=wydziel_zdania('ang',sys.argv[2]) 
        lista_zdan_pol=wydziel_zdania('pol',sys.argv[4])   
      
      
    #---synchronizacja przy uzyciu slownika pol-ang ---#
    
    nr_p = 0
    nr_a = 0
    koniec_listy_ang = False
    koniec_listy_pol = False
    
    
    while True:
        tlumaczenia_str = "\nTRANSLATE: "
        lista_recordow_tlumaczen=tlumacz_slowa_na_ang(dbm,wydziel_slowa_pol(lista_zdan_pol[nr_p]))
        #szukaj_slow_w_zdaniu_ang(lista_recordow_tlumaczen,lista_zdan_ang[nr_a]) 
        print "\nANG: " + lista_zdan_ang[nr_a]
        
        for records in lista_recordow_tlumaczen:
            for r in records:
                tlumaczenia_str = tlumaczenia_str + ", "+ r[1] 
        
          
        print tlumaczenia_str    
        
        
        nr_p = nr_p + 1
        nr_a = nr_a + 1
        
        if nr_p == len(lista_zdan_pol):
            koniec_listy_pol = True
        
        if nr_a == len(lista_zdan_ang):
           koniec_listy_ang = True
        
        if koniec_listy_pol:
            while nr_a < len(lista_zdan_ang):
                #lista_zdan_ang_synch.append(lista_zdan_ang[nr_a])
                nr_a = nr_a + 1
            break
            
        if koniec_listy_ang:
            while nr_p < len(lista_zdan_pol):
                #lista_zdan_pol_synch.append(lista_zdan_pol[nr_p])
                nr_p = nr_p + 1
            break
     
    
    
    if False:                    
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
