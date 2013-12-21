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


def rozdziel_fraze(fraza,n):
    lista_slow = re.compile("[ ]+",re.L).split(fraza)
    lista_fraz_n = []
    if len(lista_slow)< n:
	return []
    else:
	i = 0
	while (i+n) <= len(lista_slow):
	    slowa = ""
	    j = 0
	    while j< n:
		if j== 0: 
		    slowa = lista_slow[i]
		else:
		    slowa = slowa + " " + lista_slow[i+j]
		j= j+1
	    i = i+1
	    if slowa != "": lista_fraz_n.append(slowa)
	return 	lista_fraz_n
    
    

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
    

def wydziel_frazy(arg,zbior_fraz,n):
    
    caly_tekst = open(arg,"r").read()
    caly_tekst = filtr_zamianaNaMaleLiteryPL(caly_tekst)
    caly_tekst = filtr_usuniecieNiewygodnychZnakow(caly_tekst)

    lista_zdan = re.compile("[0-9:;.,/(){}_<>!?^%=*&$#\-\+\"\r\[\]]*",re.L).split(caly_tekst)
    
    for zdanie in lista_zdan:
          
        # usuniecie np apostrofu z poczatku/konca frazy
        p1 = re.compile('^[ \'`]+')   
        p2 = re.compile('[ \'`]+$') 
	
        zdanie=p1.sub('',zdanie)
        zdanie=p2.sub('',zdanie) 

        if len(zdanie)<1:
            continue
        
	# trzeba rozdzielic fraze na fraze n-wyrazowa i dopiero wtedy robic statystyke 
    	# pol:
	# nelezy sprowadzic kazde(...?) slowo do formy podstawowej przy uzyciu clp 2 etap
	# nalezy sie zastanowic ktora forme podstawowa brac pod uwage!
	
	lista_fraz_n = rozdziel_fraze(zdanie,n)
	for f in lista_fraz_n:
	    if zbior_fraz.get(f)==None:
    		zbior_fraz[f]= 1
    	    else:
    		zbior_fraz[f]= zbior_fraz[f] + 1
            
    return zbior_fraz

    
def main():
    
    kat = 'wyniki'
    #os.mkdir(katalog_z_wynikami)
    lista_plikow= os.listdir(sys.argv[1])

    n=6
    i=1
    
    while i<=n:
	zbior_fraz = {}
	print "---------------------------------------------"
	print "Frazy " + str(i) + "-wyrazowe:"
	print "---------------------------------------------"
	frazy_stat = open(kat+'/frazy_'+str(i)+'.txt','w')
	frazy_stat_id = open(kat+'/frazy_'+str(i)+'_id.txt','w')
	
	for arg in lista_plikow: 
	    zbior_fraz = wydziel_frazy(sys.argv[1]+"/"+arg,zbior_fraz,i)
	    print " "+ arg + ": "+ str(len(zbior_fraz))
	
	k=zbior_fraz.keys()
	k.sort(lambda y,x: zbior_fraz[x]!=zbior_fraz[y] and cmp(zbior_fraz[x],zbior_fraz[y])or strcoll(x,y))
        
        nr = 1	
	for x in k:
    	    frazy_stat.write(str(zbior_fraz[x]) + "\t" + x + "\n")
    	    frazy_stat_id.write(str(nr)+"\t"+str(zbior_fraz[x]) + "\n")
            nr = nr + 1
	frazy_stat.close()    
	frazy_stat_id.close()    
        i = i + 1
	
main()
