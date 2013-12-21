#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from databasemanager import *
from myHash import *
from cPickle import dump


def formy_podstawowe_slowa_ang(dbm,slownik_ang,exceptions_ang,slowo,names):
    slowo = slowo.strip()
    bform_list = []
    #if slowo not in names:
    if True:
        lista_form_podst = []
        if slowo in exceptions_ang:
            lista_form_podst = dbm.get_exceptions_ang(slowo)
            if len(lista_form_podst) > 0:  
                for (r,) in lista_form_podst:
                    bform_list.append(r)
        else:
            if len(slowo) >= 4:
                if slowo[-3:] == 'ing' and len(slowo) > 4:
                    if slowo[-4] == slowo[-5]:
                        if (slowo[:-4],'v.') in slownik_ang:
                            bform_list.append(slowo[:-4]) #swim-ming
                            #print "\tadd:" + slowo[:-4] + " ("+ slowo + ")"
                    else:
                        if (slowo[:-3],'v.') in slownik_ang:
                            bform_list.append(slowo[:-3])
                            #print "\tadd:" + slowo[:-3] + " ("+ slowo + ")"
                        elif (slowo[:-3]+'e','v.') in slownik_ang:
                            bform_list.append(slowo[:-3] + 'e')
                            #print "\tadd:" + slowo[:-3] + 'e' + " ("+ slowo + ")"
                elif slowo[-2:] == 'ed':
                    if (slowo[:-2],'v.') in slownik_ang:
                        bform_list.append(slowo[:-2]) # work-ed
                        #print "\tadd:" + slowo[:-2] + " ("+ slowo + ")"
                    elif (slowo[:-1],'v.') in slownik_ang:
                        bform_list.append(slowo[:-1]) # notice-d
                        #print "\tadd:" + slowo[:-1] + " ("+ slowo + ")"
                elif slowo[-2:] == 'es':
                    if (slowo[:-2],'v.') in slownik_ang or (slowo[:-2],'n.') in slownik_ang:
                        bform_list.append(slowo[:-2]) # teach-es
                        #print "\tadd:" + slowo[:-2] + " ("+ slowo + ")"
                elif slowo[-2:] == 's':
                    if (slowo[:-1],'v.') in slownik_ang or (slowo[:-1],'n.') in slownik_ang: 
                        bform_list.append(slowo[:-1]) # work-s
                        #print "\tadd:" + slowo[:-1] + " ("+ slowo + ")"
                
        bform_list.append(slowo)
    else:
        bform_list.append("<name>")
    return bform_list


def formy_podstawowe_slowa_pl(dbm,_plp,slowo,names):
    slowo = slowo.strip()
    string = _plp.plp_rec(slowo)
    numery = string.split(':')
    ids = numery[1:]
    bform_list = []

    for nr in ids:
        i = int(nr)
        bform = _plp.plp_bform(i)	
        if len(bform) >= 1:
	    bform_list.append(bform)
        bform = ""

    if len(bform_list)==0:
        #if slowo not in names:
        if True:
            if len(slowo) > 4:
                bform_list = szukaj_synonimow(dbm,slowo)
        else: 
            bform_list.append("<name>")

    bform_list.append(slowo)
    return bform_list 
 

def szukaj_synonimow(dbm,slowo):
    lista_synonimow = []
    records = dbm.get_synonym_pol(slowo.strip())  
    for (w1,w2) in records:
        lista_synonimow.append(w1.strip())
        lista_synonimow.append(w2.strip())
    return lista_synonimow


def tlumacz_slowa_pol(dbm,zb_slow_postawowych,wyjatki_pol,slowo):
    zbior_slow_przetlumaczonych = set()
    for slowo_pl in zb_slow_postawowych:
        records = dbm.get_translation_pol2ang(slowo_pl)
        if len(records) == 0:
            zbior_slow_przetlumaczonych.add(slowo_pl)
        else:
            for (r,) in records:
                zbior_slow_przetlumaczonych.add(r.strip())

    if slowo in zbior_slow_przetlumaczonych and len(zbior_slow_przetlumaczonych) == 1:
        if wyjatki_pol.get(slowo_pl) == None:
            wyjatki_pol[slowo_pl] = 1        
        else:                    
            wyjatki_pol[slowo_pl] += 1

    return zbior_slow_przetlumaczonych


def dopasuj_krotki(krotka_pl,krotka_ang,zbior_fraz,roznica):
    dopasowane = False 
    if len(krotka_ang) <= (len(krotka_pl) + roznica) and len(krotka_ang) >= len(krotka_pl):               
        licznik = 0
        stop = len(krotka_pl)
        krotka_ang_copy = []
        for kang in krotka_ang:
            krotka_ang_copy.append(kang)
        fraza_pol = zamien_na_fraze_pol(krotka_pl)
        nr_krotka_pol = len(krotka_pl)
        nr_pol = 0
        while nr_pol < nr_krotka_pol:
            (slowo_pl, zb_slow_przetl_na_ang) = krotka_pl[nr_pol]
            nr_pol += 1
            znal = False
            nr_krotka_ang = len(krotka_ang_copy)
            if len(krotka_pl) > 2 and nr_pol == 1:
                nr_krotka_ang = len(krotka_ang_copy) - 1
            nr_ang = 0
            while nr_ang < nr_krotka_ang:
                kangc = krotka_ang_copy[nr_ang]
                nr_ang += 1
                (slowo_ang, zb_slow_przetl_ang) = kangc
                for slowo_pl2ang in zb_slow_przetl_na_ang:
                    for slowo_ang2ang in zb_slow_przetl_ang:       
                        if slowo_pl2ang == slowo_ang2ang:
                            znal = True
                            krotka_ang_copy.remove(kangc)
                            licznik +=1
                            break
                    if znal: break
                if znal: break
            if licznik == stop:
                dopasowane = True
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
    return dopasowane


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


def drukuj_dopasowane(dbm,dopasowania_wynik,hash_fraz,metoda,poczatki_ang,koncowki_ang,to_file,to_db,typ_db):   
    frazy_pol = hash_fraz.keys()    
    ilosc_fraz_pol = 0 
    ilosc_fraz_ang = 0
    hash_fraz_wynik = {}
    for fraza_pol in frazy_pol:
        if len(hash_fraz[fraza_pol]) > 0:
            zbior_fraz_end = set()
            if len(hash_fraz[fraza_pol]) == 1:
                zbior_fraz_end = hash_fraz[fraza_pol]
            else:
                # selekcja fraz na 4 sposoby do wyboru
                if metoda == 0:
                    # 0 - czyli wszystkie propozycje dopasowan
                    zbior_fraz_end = hash_fraz[fraza_pol]
                elif metoda == 1:
                    # 1 - na podstwie statystyk samych fraz
                    zbior_fraz_end = statystyka_fraz(hash_fraz[fraza_pol])
                elif metoda == 2:
                    # 2 - na podstawie przeciecia fraz
                    zbior_fraz_end = przeciecie_fraz(hash_fraz[fraza_pol])
                elif metoda == 3:
                    # 3 - na podstawie statystyk i przeciezia fraz.
                    zbior_fraz_end = statystyka_przciecie_fraz(hash_fraz[fraza_pol],poczatki_ang,koncowki_ang,len(fraza_pol.split()))

            if  len(zbior_fraz_end) > 0:
                if hash_fraz_wynik.get(fraza_pol)== None:
                    hash_fraz_wynik[fraza_pol] = zbior_fraz_end
                else:
                    print "Warning: powtorzenie frazy polskiej" 
                                
    frazy_pol = hash_fraz_wynik.keys() 
    if to_file:
        for fraza_pol in frazy_pol:
            ilosc_fraz_pol += 1
            zbior_fraz_end = hash_fraz_wynik[fraza_pol]
            dopasowania_wynik.write("\n%s:" % (fraza_pol))
            for r in zbior_fraz_end:
                ilosc_fraz_ang += 1
                dopasowania_wynik.write("\n\t%s\t%s" % (str(r.n),r.f))
                #dopasowania_wynik.write("\t%s" % (r.f))
        dopasowania_wynik.write("ilosc fraz ang.: %s\n" % (str(ilosc_fraz_ang)))
        dopasowania_wynik.write("ilosc fraz pol.: %s\n" % (str(ilosc_fraz_pol)))

    if to_db and typ_db == 'temp' and metoda == 3:
        dbm.clear_temp()
        for fraza_pol in frazy_pol:
            for r in hash_fraz_wynik[fraza_pol]:
                dbm.write_phrase_to_temp(len(fraza_pol.split()),re.compile('[\']+').sub('\\\'',fraza_pol),re.compile('[\']+').sub('\\\'',r.f))
                break
        
    if to_db and typ_db == 'allxxx' and metoda == 3:
        # warto miec kopie tabeli w razie utrady danych ... #1
        hash_fraz_db = dbm.get_all_phrases() # 2
        dbm.clear_all_phrases()
        for fraza_pol in frazy_pol:
            for r in hash_fraz_wynik[fraza_pol]:
                if hash_fraz_db.get(fraza_pol)== None:
                    hash_fraz_db[fraza_pol] = set()
                    hash_fraz_db[fraza_pol] = hash_fraz_wynik[fraza_pol]
                    print "znaleziono nowa fraze"
                else:
                    hash_fraz_db[fraza_pol] = merge_fraz_z_db(hash_fraz_db[fraza_pol],hash_fraz_wynik[fraza_pol]) # 3
                breakexceptions_ang

        frazy_pol_db = hash_fraz_db.keys()
        for fraza_pol in frazy_pol_db:
            for r in hash_fraz_db[fraza_pol]:
                 #dbm.write_phrase_all(len(fraza_pol.split()),fraza_pol,re.compile('[\']+').sub('\\\'',fraza_pol),"NULL",re.compile('[\']+').sub('\\\'',r.f)) # 4
                break

def drukuj_wyjatki_pol(wyjatki_pol,wyjatki_pol_hash):
    wyjatki = wyjatki_pol_hash.keys() 
    wyjatki.sort()
    for w in wyjatki:
        wyjatki_pol.write("%s\t%d\n" % (w,wyjatki_pol_hash[w]))


def merge_fraz_z_db(zb_fraz_db,zb_fraz_wynik):

    return set()


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
    tekst=re.compile('\'re ').sub(' are ',tekst)
    return tekst
   

def zamiana_na_bez_kropek_ang(tekst):
    tekst = tekst.replace('^ms.','^ms')
    tekst = tekst.replace(' ms.',' ms') 
    tekst = tekst.replace('^mrs.','^mrs')
    tekst = tekst.replace(' mrs.',' mrs')
    tekst = tekst.replace('^mr.','^mr')
    tekst = tekst.replace(' mr.',' mr')
    tekst = tekst.replace('\"mr.','\"mr')
    tekst = tekst.replace('\"ms.','\"ms') 
    tekst = tekst.replace('\'mr.','\'mr')
    tekst = tekst.replace('\'ms.','\'ms')
    tekst = tekst.replace('\'mrs.','\'mrs')
    tekst = tekst.replace(' e.g.',' for example')
    tekst = tekst.replace(' etc.',' et cetera')
    return tekst  


def zamiana_na_bez_kropek_pol(tekst):
    tekst = tekst.replace(' p.n.e.',' przed naszą erą ') 
    tekst = tekst.replace(' n.e.',' naszej ery ') 
    tekst = tekst.replace(' np.',' na przykład ')
    tekst = tekst.replace(' godz.',' godzina ') 
    tekst = tekst.replace(' tel.',' telefon ')
    tekst = tekst.replace(' itd.',' i tak dalej ')
    tekst = tekst.replace(' itp.',' i tym podobnie ')
    tekst = tekst.replace(' z o.o.',' z ograniczoną odpowiedzialnością ')
    tekst = tekst.replace(' sp.',' spółka ')
    tekst = tekst.replace(' nt.',' na temat ')
    tekst = tekst.replace(' s.a.',' spółka akcyjna ')
    tekst = tekst.replace(' r.',' rok ')
    tekst = tekst.replace(' art.',' artykuł ')
    tekst = tekst.replace('^art.','^artykuł ')
    tekst = tekst.replace(' ust.',' ustawa ')
    tekst = tekst.replace(' w.',' wiek ')
    return tekst 


def zamiana_na_male_litery_pol(tekst):
    tekst = tekst.replace('Ą','ą')
    tekst = tekst.replace('Ę','ę')
    tekst = tekst.replace('Ć','ć')
    tekst = tekst.replace('Ż','ż')
    tekst = tekst.replace('Ź','ź')
    tekst = tekst.replace('Ó','ó')
    tekst = tekst.replace('Ś','ś')
    tekst = tekst.replace('Ń','ń')
    tekst = tekst.replace('Ł','ł')
    return tekst.lower()


def zamiana_na_male_litery(tekst):
    tekst=tekst.lower()
    return tekst


def usuniecie_niewygodnych_znakow(tekst):
    tekst = tekst.replace('\\','')
    #tekst = tekst.replace('-',' ')
    return re.compile('[ \n\t\r]+').sub(' ',tekst)


def get_lista_zdan(tekst):
    return re.compile("[0-9:;.,/(){}_<>!?^%=*&$#\+\"\r\[\]]*",re.L).split(tekst)#[:-1]         


def oczysc_zdanie(zdanie):      
    zdanie = re.compile('(^[ \'`]+|[ \'`]+$|[]+)').sub('',zdanie)
    #zdanie = re.compile('[\']+').sub('\\\'',zdanie)
    zdanie = re.compile('[ \'`]+').sub(' ',zdanie)
    return zdanie

# metoda 1
def statystyka_fraz(zbior_fraz):
    zbior_fraz_new = []
    maxi = 0
    for r1 in zbior_fraz:
        if r1.n > maxi:
            maxi = r1.n
    for r in zbior_fraz:
        if r.n == maxi:
            zbior_fraz_new.append(r)
    return zbior_fraz_new

# metoda 2
def przeciecie_fraz(zbior_fraz):
    zbior_fraz_new = set()
    lista_fraz = list(zbior_fraz)
    S1 = set(((zbior_fraz.pop()).f).split())

    for r1 in zbior_fraz:
        S2 = set((r1.f).split())
        S1 = S1 & S2

    # rekonstrukcja zdania
    if len(S1) > 0:
        F = ""
        for r in lista_fraz:
            L = (r.f).split()
            S = set(L)
            if S1.issubset(S):
                for slowo in L:
                    if slowo in S1: 
                        F += slowo + " " 
                break 
        zbior_fraz_new.add(MyHash(F.strip(),1))
        return zbior_fraz_new
    else:
        return zbior_fraz_new

# brzuchu w:
#	1	stomach in
#	1	his stomach in bed
#	1	on his stomach
#	1	czasami nic co pasuje       
#	1	lying on his stomach
#	1	his stomach in
#	1	on his stomach in
#	1	stomach in bed

# powinno zostac: "stomach in".

# metoda 3
def statystyka_przciecie_fraz(zbior_fraz,poczatki_ang,koncowki_ang,len_pol):
    zbior_fraz_new_temp = set()
    # dlaczego dla trzech najwiekszych? sprawdzic dla innych wartosci tez
    maxi1 = 0
    maxi2 = 0
    maxi3 = 0
    for r1 in zbior_fraz:
        if r1.n > maxi1:
            maxi3 = maxi2
            maxi2 = maxi1
            maxi1 = r1.n
        elif r1.n > maxi2 and r1.n < maxi1:
            maxi3 = maxi2
            maxi2 = r1.n
        elif r1.n > maxi3 and r1.n <  maxi2:
            maxi3 = r1.n

    for r in zbior_fraz:
        if r.n <= maxi1 and r.n >= maxi3:
            zbior_fraz_new_temp.add(r)
     
    return znajdz_najczesciej_wystepujacy_fragment_frazy(zbior_fraz_new_temp,poczatki_ang,koncowki_ang,len_pol)

# metoda ta modyfikuje znalezione frazy, 'statystyki samogenerujace sie' !! ;] 
def znajdz_najczesciej_wystepujacy_fragment_frazy(zbior_fraz,poczatki_ang,koncowki_ang,len_pol):
    hash_fraz = {}
    for r in zbior_fraz:
        slowa = (r.f).split()
        k = len(slowa)
        # odrzucic frazy krotsze od frazy polskiej.(uwaga! trochu to ogranicza takie przypadki jak "panna mloda" -> "bride")
        n = len_pol
        while n <= k:
            krotki = []
            if n == 2 and len(slowa) >= 2:                    
                krotki = zip(slowa[:-1], slowa[1:])      
            elif n == 3 and len(slowa) >= 3:
                krotki = zip(slowa[:-1], slowa[1:], slowa[2:])
            elif n == 4 and len(slowa) >= 4:                
                krotki = zip(slowa[:-1], slowa[1:], slowa[2:], slowa[3:])
            elif n == 5 and len(slowa) >= 5:
                krotki = zip(slowa[:-1], slowa[1:], slowa[2:], slowa[3:], slowa[4:])
            elif n == 6 and len(slowa) >= 6:
                krotki = zip(slowa[:-1], slowa[1:], slowa[2:], slowa[3:], slowa[4:], slowa[5:])
            y = len(krotki)
            x = 0
            while x < y:
                fraza = ""
                # odrzucenie frazy z bezsensowynymi litrekami na koncu 
                if selekcja_krotek(poczatki_ang,koncowki_ang,krotki[x]): 
                    for s in krotki[x]:
                        fraza += s + " "
                    fraza = fraza.strip()
                    if hash_fraz.get(fraza) == None:
                        hash_fraz[fraza] = 1
                    else:
                        hash_fraz[fraza] += 1
                x += 1
            n += 1    
    frazy_keys = hash_fraz.keys()    
    # statystyka fraz 2-6 wyrazowych
    n_f = [0,0,0,0,0]                
    # frazy 2-6 wyrazowe 
    fraza_final = ['','','','','']    
    for key in frazy_keys: 
        length = len(key.split())
        if length > 1 and length <= 6:
            val = hash_fraz[key]          
            if n_f[length-2] < val:
                fraza_final[length-2] = key
                n_f[length-2] = val       
        else:
            print "cos jest nie tak..."

    zbior_fraz_new = set()
    d = 0 
    while d < 5:
        if n_f[d] > 0:
            zbior_fraz_new.add(MyHash(fraza_final[d],n_f[d]))  
        d += 1            

    zbior_fraz_new2 = statystyka_fraz(zbior_fraz_new)
    zbior_fraz_new3 = set()
    len2 = len(zbior_fraz_new2)  
    if len2 == 0:
        print "Info: nie znaleziono dopasowania dla frazy polskiej" 
        None       
    elif len2 == 1:
        zbior_fraz_new3 = zbior_fraz_new2
    else:
        ff = ''
        max_len = 0
        for r in zbior_fraz_new2:
            len_rf = len((r.f).split())
            if max_len < len_rf:
                max_len = len_rf
                ff = r.f
        zbior_fraz_new3.add(MyHash(ff,max_len))
#        min_len = 10
#        for r in zbior_fraz_new2:
#            len_rf = len((r.f).split())
#            if min_len > len_rf:
#                min_len = len_rf
#                ff = r.f
#        zbior_fraz_new3.add(MyHash(ff,min_len))


    return zbior_fraz_new3


def srednia_arytm(lista_id_znalezionych_kr,sr_def):
    dl_kr = len(lista_id_znalezionych_kr)
    sr = 0
    if dl_kr == 0:
        sr = sr_def
    else:
        for nr in lista_id_znalezionych_kr:
            sr += nr
        sr = sr / dl_kr  
    return sr


def zamroz_frazy(zbior_fraz,frozen_phrases_write):
    if frozen_phrases_write:
        file_frozen = open('frozen_phrases/zbior_fraz.pic','w')
        print "Zapisywanie do pliku frozen_phrases/zbior_fraz.pic"
        dump(zbior_fraz,file_frozen,2)
        file_frozen.close() 
    return 1

#---------------------------------------------------------------------------------------------

# pomysly/pytania:
# + (zrezygnowano)jezeli imie jest w jednej frazie a nie ma w drugie to odrzucic przypadek!
# + wykluczajace sie frazy angielskie np. "if he" vs "of it" dla "to ich" ... jak ? | done
# + dodac do wyjatkow przymiotniki 'nieregularne' takie jak 'good' -> 'best', 'better' | done
# + odetnij -s , -es oraz inne przypadki 
# + (nic) co zrobic z tymi apostrofami ?
# + czemu polskie literki w wyrazach nie zamieniaja sie na male!?
# - dorobic funkcjonalnosc ktora pozwoli na uzupelnianie slownika w bazie
# - wykorzsytac slownik w translatorze na webie
# + dorobic odczyt danych z bazy albo pliku
# + dorobic logi dla nierozpoznanych slow
# + dorzucic synonimy z sourceforge
# + poprawic "clp" angielskie
# + przeszukiwanie krotek po promieniu
# + przeanalizowanie buga z "ich dzieci"
# + rozwiazac problem z myslnikiem i slowami laczonymi
# + (zrezygnowano)przefiltrowac krotki polskie przed wydrukiem(??) (wyrzucenie krotszych krotek polskich dla ktorych zostala dopasowana taka sama fraza ang)
# + wrzucenie exceptionow do pamieci
# + wrzucenie do conf 'margin'
# + czemu 'będzie' nie jest rozpoznawane
# + problem z indeksami koncowymi chunkow
# - do pliku konfiguracyjnego dodac reguly filtrujace
# + dodac promien porownywania krotek
# + dodac wybor metody zrownoleglania tekstow
# + poprawic algorytm Gajera
# + dlaczego niektore pliki polskie nie maja krotek
