#!/usr/bin/python
# -*- coding: latin2 -*-
import _plp,os,sys,re
import string
from databasemanager import *


def analiza_slowa_ang(file,slowo):
    slowo = slowo.strip()
    bform_list = []
    bform_list.append(slowo)
    return bform_list


def analiza_slowa_pl(file,slowo):
    slowo = slowo.strip()
    string = _plp.plp_rec(slowo)
    numery = string.split(':')
    ile = int(numery[0])
    ids = numery[1:]
    wynik = ""     
    bform_list = []

    for nr in ids:
        i = int(nr)
        label = _plp.plp_label(i)
        bform = _plp.plp_bform(i)	
        #forms = _plp.plp_forms(i)
        #vec_id = _plp.plp_vec(i,slowo) 
        
        wynik = wynik + "\nid: "+ str(i) + "\n"
        if len(label) >= 1:
	    wynik = wynik + "1)label: " + label + "\n"
	
        if len(bform) >= 1:
	     wynik = wynik + "2)bform: " + bform + "\n"
	     bform_list.append(bform) 

        #if len(forms) >= 1:
	#     wynik = wynik + "3)forms:" + forms + "\n"
	
        #if len(vec_id) >= 1:
	#     wynik = wynik + "4)vec_id: " + vec_id + "\n"
	
        file.write(wynik)
        label = ""
        bform = ""
        #forms = ""
        #vec_id= ""

    return bform_list 



def main():   
    kat = 'wyniki'
    dbm = DBmanager()
    _plp.plp_init()
    p1 = re.compile('[.,;?!\-\'\"]+')       
  
    lista_zdan_z_bazy = dbm.get_both_sentences()
    ilosc_zdan = len(lista_zdan_z_bazy)
    print "Przetwarzanie %d zdan" % (ilosc_zdan) 
     
    frazy_wynik = open(kat+'/dopasowanie.txt','w')
    for (zdanie_pol,zdanie_ang) in lista_zdan_z_bazy:
        zdanie_pol = p1.sub('',zdanie_pol)
        slowa_pol = re.compile("[ \t\n]+",re.L).split(zdanie_pol)
        zdanie_ang = p1.sub('',zdanie_ang)
        slowa_ang = re.compile("[ \t\n]+",re.L).split(zdanie_ang)

        frazy_wynik.write(zdanie_pol + "\n")    
        for slowo_pol in slowa_pol:
            bform_list_pol = analiza_slowa_pl(frazy_wynik,slowo_pol)
            frazy_wynik.write("lista form podstawowych dla %s: %s\n" % (slowo_pol,str(bform_list_pol)))
            frazy_wynik.write("tlumaczenia:\n")
            for bform in bform_list_pol:
                records = dbm.get_translation_pol2ang(bform)
                for record in records:
                    frazy_wynik.write("\t%s\n" % str(record))    

        frazy_wynik.write(zdanie_ang + "\n")    
        for slowo_ang in slowa_ang:
            bform_list_ang = analiza_slowa_ang(frazy_wynik,slowo_ang)
            frazy_wynik.write("lista form podstawowych dla %s: %s\n" % (slowo_ang,str(bform_list_ang)))


    frazy_wynik.close()
        
 
if __name__ == '__main__':
    main()
