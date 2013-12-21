#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from locale import *
from string import * 
from databasemanager import *


zbior_fraz = {}

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

def rozdziel_frazePL(fraza,n):
    lista_slow = re.compile("[ \t\n]+",re.L).split(fraza)
    lista_fraz_n = []
    if len(lista_slow)< n:
        return []
    else:
        i = 0
        while (i+n) <= len(lista_slow):
            e = i + n -1
            lista_nonsensow_na_poczatku = ['się','self','in','','i','a','ą','b','c','ć','d','e','ę','f','g','h','j','k','l','ł','m','n','ń','ó','p','r','s','ś','t','ż','ż','ź','x','y','v','vi','iv','iii','ii','ix','xi','vii','viii','x','xi','xii','xiii','xiv','xv','xvi']
            lista_nonsensow_na_koncu = ['','self','in','i','a','ą','b','c','ć','d','e','ę','f','g','h','j','k','l','ł','m','n','ń','ó','p','r','s','ś','t','ż','ż','ź','x','y','v','vi','iv','iii','ii','ix','xi','vii','viii','x','xi','xii','xiii','xiv','xv','xvi'] 
            if ((lista_slow[i] in lista_nonsensow_na_poczatku) or (lista_slow[e] in lista_nonsensow_na_koncu)): 
                i = i + 1
                continue    
            slowa = ""
            j = 0
            while j< n:
                if j== 0: 
                    slowa = lista_slow[i]
                else:
                    slowa = slowa + " " + lista_slow[i+j]
                j = j+1
            i = i+1
            if slowa != "": lista_fraz_n.append(slowa)
        return 	lista_fraz_n

def rozdziel_frazeAng(fraza,n):
    lista_slow = re.compile("[ \t\n]+",re.L).split(fraza)
    lista_fraz_n = []
    if len(lista_slow)< n:
        return []
    else:
        i = 0
        while (i+n) <= len(lista_slow):
            #if lista_slow[i] in ['s','d']: 
            #    i = i + 1
            #    continue    
            e = i + n -1
            lista_nonsensow_na_poczatku = ['selves','self','','b','c','d','e','f','g','h','j','k','l','m','n','o','p','r','s','t','u','w','z','x','y','v','vi','iv','iii','ii','ix','xi','vii','viii','x','xi','xii','xiii','xiv','xv','xvi']
            lista_nonsensow_na_koncu = ['selves','self','i','','the','a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','r','s','t','u','w','z','x','y','v','vi','iv','iii','ii','ix','xi','vii','viii','x','xi','xii','xiii','xiv','xv','xvi']
            if ((lista_slow[i] in lista_nonsensow_na_poczatku) or (lista_slow[e] in lista_nonsensow_na_koncu)): 
                i = i + 1
                continue    
            slowa = ""
            j = 0
            while j< n:
                if j== 0: 
                    slowa = lista_slow[i]
                else:
                    slowa = slowa + " " + lista_slow[i+j]
                j = j+1
            i = i+1
            if slowa != "": lista_fraz_n.append(slowa)
        return 	lista_fraz_n



    
def filtr_usuniecieNiewygodnychZnakow(tekst):
    tekst=tekst.replace('\\','')
    # usuniecie wielu spacji pod rzad
    p1 = re.compile('([ ]+|\n)') 
    tekst=p1.sub(' ',tekst)
    return tekst
     
def filtr_zamianaNaBezKropekAng(tekst):
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
    p8 = re.compile('(\'mrs.|\'Mrs.)')
    tekst=p8.sub('\'mrs',tekst)
    p9 = re.compile('( mrs.| Mrs.)')
    tekst=p9.sub(' mrs',tekst)
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
    #tekst=re.compile('\'re ').sub(' are ',tekst) # cholera! zapomnielismy o tym! zostawiam to juz tak ...
    return tekst

    

def wydziel_frazy(arg,n):
    
    caly_tekst = open(arg,"r").read()
    caly_tekst = filtr_zamianaNaMaleLitery(caly_tekst)
    caly_tekst = filtr_usuniecieNiewygodnychZnakow(caly_tekst)
    if 'pol' in sys.argv:
        caly_tekst = filtr_zamianaNaMaleLiteryPL(caly_tekst)
    elif 'ang' in sys.argv:
        caly_tekst = filtr_zamianyNaFormyRozszerzoneAng(caly_tekst)
        caly_tekst = filtr_zamianaNaBezKropekAng(caly_tekst) 
    
    lista_zdan = re.compile("[0-9:;.,/(){}_<>!?^%=*&$#\-\+\"\r\[\]]*",re.L).split(caly_tekst)
    
    for zdanie in lista_zdan:
        p1 = re.compile('(^[ \'`]+|[ \'`]+$|[]+)')  
        #p2 = re.compile('[]+')  
        p3 = re.compile('[\']+')
        p4 = re.compile('[ ]+')        
	zdanie=p1.sub('',zdanie)
        #zdanie=p2.sub('',zdanie)
        zdanie=p3.sub('\\\'',zdanie)
        zdanie=p4.sub(' ',zdanie)

        if len(zdanie)<6:
            continue
 	
        if 'pol' in sys.argv:
            lista_fraz_n = rozdziel_frazePL(zdanie,n)
        elif 'ang' in sys.argv:
	    lista_fraz_n = rozdziel_frazeAng(zdanie,n)  
	      
        for f in lista_fraz_n:
            if zbior_fraz.get(f)==None:
                zbior_fraz[f]= 1
            else:
                zbior_fraz[f]= zbior_fraz[f] + 1
            

    
def main():
    
    kat = 'wyniki'
    lista_plikow= os.listdir(sys.argv[1])

    n=int(sys.argv[4])
    i=n
    dbm = DBmanager() 
    if 'clean' in sys.argv:   
        if 'pol' in sys.argv:
            print "Czyszczenie tabeli statystyk dla jezyka polskiego"
            dbm.clearStatisticsPol()
        elif 'ang' in sys.argv:   
            print "Czyszczenie tabeli statystyk dla jezyka angielskiego"
            dbm.clearStatisticsAng()
    
    
    while i<=n:
        print "---------------------------------------------"
        print "Frazy " + str(i) + "-wyrazowe:"
        print "---------------------------------------------"
        nr_ksiazki = 1
        for arg in lista_plikow: 
            wydziel_frazy(sys.argv[1]+"/"+arg,i)
            print str(nr_ksiazki) + " "+ arg + ": "+ str(len(zbior_fraz))
	    nr_ksiazki = nr_ksiazki + 1
 
        k=zbior_fraz.keys()
        #k.sort(lambda y,x: zbior_fraz[x]!=zbior_fraz[y] and cmp(zbior_fraz[x],zbior_fraz[y])or strcoll(x,y))
        
        if 'totxt'in sys.argv:    
            print "Zapisywanie danych do plików"
            frazy_stat = open(kat+'/frazy_'+str(i)+'.txt','w')
            frazy_stat_id = open(kat+'/frazy_'+str(i)+'_id.txt','w')
          
            nr = 1	
            for x in k:
                frazy_stat.write(str(zbior_fraz[x]) + "\t" + x + "\n")
                frazy_stat_id.write(str(nr)+"\t"+str(zbior_fraz[x]) + "\n")
                nr = nr + 1
            frazy_stat.close()    
            frazy_stat_id.close()    
        
        if 'todb' in sys.argv: 
            print "Wprowadzanie danych do bazy"  
            if 'pol' in sys.argv:
                f = dbm.insertStatisticsPol
            elif 'ang' in sys.argv:
                f = dbm.insertStatisticsAng
            for x in k:
               if zbior_fraz[x]>1:
                   words = re.compile("[ ]+",re.L).split(x)
                   if len(words)!= i: print "Uwaga! nie zgadza się ilość słów: " + x         
                   f(str(zbior_fraz[x]),words)
        i = i + 1   
	
main()
