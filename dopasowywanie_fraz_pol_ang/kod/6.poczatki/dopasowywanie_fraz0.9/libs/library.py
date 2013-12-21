#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from databasemanager import *
#from levenshtein import *
from myHash import *


def formy_podstawowe_slowa_ang(dbm,slowo,names):
    slowo = slowo.strip()
    bform_list = []
    if slowo not in names:
        lista_form_podst = dbm.get_exceptions_ang(slowo)    
        for (r,) in lista_form_podst:
            bform_list.append(r)
# odetnij -s , ed , ing oraz inne przypadki. sprawdz czy sa takie same jak w statystykach ...lub nie 
# co zrobic z tymi apostrofami ??
    bform_list.append(slowo)
    return bform_list


def formy_podstawowe_slowa_pl(dbm,_plp,slowo,names):
    slowo = slowo.strip()
    string = _plp.plp_rec(slowo)
    numery = string.split(':')
    ids = numery[1:]
    bform_list = []
    for nr in ids:
        i = int(nr)
        label = _plp.plp_label(i)
        bform = _plp.plp_bform(i)	
        if len(bform) >= 1:
	    bform_list.append(bform)
        bform = ""
    if len(bform_list)==0:
        if len(slowo) > 2 and slowo not in names:
            bform_list = szukaj_synonimow(dbm,slowo)
        bform_list.append(slowo)
        #if slowo in names: 
        #    print "name: " + slowo
    return bform_list 
 

def szukaj_synonimow(dbm,slowo):
    lista_synonimow = []
    records = dbm.get_synonym_pol(slowo.strip())
    #print "?> " + slowo +": "  
    for (w1,w2) in records:
        #print  w1 +", " + w2 + ", "
        lista_synonimow.append(w1.strip())
        lista_synonimow.append(w2.strip())
    return lista_synonimow


def tlumacz_slowa_pol(dbm,zb_slow_postawowych):
    zbior_slow_przetlumaczonych = set()
    for slowo_pl in zb_slow_postawowych:
        records = dbm.get_translation_pol2ang(slowo_pl)
        if len(records) == 0:
            zbior_slow_przetlumaczonych.add(slowo_pl)
        else:
            for (r,) in records:
                zbior_slow_przetlumaczonych.add(r.strip())
    return zbior_slow_przetlumaczonych


def dopasuj_krotki(dbm,krotka_pl,krotka_ang,zbior_fraz):
    if (len(krotka_ang) - 1) <= len(krotka_pl):  
        licznik = 0
        stop = len(krotka_pl)
        fraza_pol = zamien_na_fraze_pol(krotka_pl)
        for (slowo_pl, zb_slow_przetl_na_ang) in krotka_pl:
            znal = False
            for (slowo_ang, zb_slow_przetl_ang) in krotka_ang:
                for slowo_pl2ang in zb_slow_przetl_na_ang:
                    for slowo_ang2ang in zb_slow_przetl_ang:       
                        if slowo_pl2ang[:-1] == slowo_ang2ang[:-1]:#levenshtein(slowo_pl2ang,slowo_ang)< 2:
                            znal = True
                            licznik +=1
                            break
                    if znal: break
                if znal: break
            if licznik == stop:
                fraza_ang = zamien_na_fraze(krotka_ang)
                if zbior_fraz.get(fraza_pol)==None:
                    zbior_fraz[fraza_pol] = set()
                    zbior_fraz[fraza_pol].add(MyHash(fraza_ang,1))
                else:
                    exist = False
                    for r in zbior_fraz[fraza_pol]:
                        if r.f == fraza_ang:
                            r.n += 1
                            exist = True
                            break
                    if not exist:
                        zbior_fraz[fraza_pol].add(MyHash(fraza_ang,1))
                break


def zamien_na_fraze(krotka):
    fraza = ""
    for (k,s) in krotka:
        if k in ['s','d']:
            fraza += '\'%s' % (k)
        else:
            fraza += ' %s' % (k)
    return fraza.strip()

               
def zamien_na_fraze_pol(krotka):
    fraza = ""
    for (k,s) in krotka:
        fraza += ' %s' % (k)
    return fraza.strip()


def drukuj_dopasowane(dopasowania_wynik,zbior_fraz):   
    frazy_pol = zbior_fraz.keys()     
    for fraza_pol in frazy_pol:
        dopasowania_wynik.write("\n"+fraza_pol + ":\n")
        for r in zbior_fraz[fraza_pol]:
            if r.n > 0 :
                dopasowania_wynik.write("\t"+ str(r.n) + "\t" + r.f + "\n")


def zakazane_koncowki(zb_koncowek,sk):
    if sk in zb_koncowek:
        return True
    else: 
        return False


def selekcja_krotek(poczatki,koncowki,krotka):      
    if zakazane_koncowki(koncowki,krotka[-1]) or zakazane_koncowki(poczatki,krotka[0]):
        return False
    else:
        return True    


def zamiana_na_formy_rozszerzone_ang(tekst):
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
    tekst=re.compile('i\'m').sub('i am',tekst)
    tekst=re.compile('\'d better').sub(' had better',tekst)
    tekst=re.compile('\'d rather').sub(' would rather',tekst)
    tekst=re.compile('\'d sooner').sub(' would sooner',tekst)
    tekst=re.compile('\'ve ').sub(' have ',tekst)
    tekst=re.compile('\'re ').sub(' are ',tekst) # cholera! cale statstyki trzeba zmienic!
    return tekst
   

def zamiana_na_bez_kropek_ang(tekst):
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


def zamiana_na_male_litery_pol(tekst):
    tekst=tekst.replace('Ą','ą')
    tekst=tekst.replace('Ę','ę')
    tekst=tekst.replace('Ć','ć')
    tekst=tekst.replace('Ż','ż')
    tekst=tekst.replace('Ź','ź')
    tekst=tekst.replace('Ó','ó')
    tekst=tekst.replace('Ś','ś')
    tekst=tekst.replace('Ń','ń')
    tekst=tekst.replace('Ł','ł')
    return tekst.lower()


def zamiana_na_male_litery(tekst):
    tekst=tekst.lower()
    return tekst


def usuniecie_niewygodnych_znakow(tekst):
    tekst = tekst.replace('\\','')
    return re.compile('[ \n\t\r]+').sub(' ',tekst)


def get_lista_zdan(tekst):
    return re.compile("[0-9:;.,/(){}_<>!?^%=*&$#\-\+\"\r\[\]]*",re.L).split(tekst)[:-1]         


def oczysc_zdanie(zdanie):      
    zdanie = re.compile('(^[ \'`]+|[ \'`,.]+$|[,.]+)').sub('',zdanie)
    zdanie = re.compile('[\']+').sub('\\\'',zdanie)
    zdanie = re.compile('[ ]+').sub(' ',zdanie)
    return zdanie


#---------------------------------------------------------------------------------------------

