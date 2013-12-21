#!/usr/bin/python
# -*- coding: ISO-8859-2 -*-
from libs.databasemanager import *
from libs.transWord import *
from libs.library import zamiana_na_male_litery,usuniecie_niewygodnych_znakow # okresl konkretnie co!

# ang -> pol
def tlumacz_text_pbmt(dbm, tekst_ang):
    tekst = zamiana_na_male_litery(tekst_ang)
    #tekst = zamiana_na_formy_rozszerzone_ang(tekst) 
    #tekst = zamiana_na_bez_kropek_ang(tekst)
    tekst = usuniecie_niewygodnych_znakow(tekst)
    lista_zdan = get_lista_zdan_pbmt(tekst)
    print lista_zdan
    tekst_pol = ""
    lista_tekst_pol = []
    print "1. START"
    for zdanie_ang in lista_zdan:
        print "2. Wczytaj nowe <zdanie> z tlumaczonego <tekstu>"
        print "<zdanie> := <%s> " % zdanie_ang
        lista_slow = zdanie_ang.split()
        lista_slow_temp = zdanie_ang.split()
        print "3. Przypisz <przypadek>:=1"
        C = 1
        print "4. Przypisz <fraza>:=<zdanie>"
        fraza = zdanie_ang
        koniec_zdania = False
        N = 1
        G = 1
        while not koniec_zdania:
            print "5. Czy odnaleziono <fraze> == <%s> w lingwistycznej bazie danych?" % fraza
            (fraza_pol,N,G,C) = dbm.find_phrase_pbmt(fraza,N,G,C)        
            if fraza_pol != "":
                print "TAK, przejscie do pkt 6"
                print "6. Tlumaczenie <frazy>\n%s" % fraza_pol
                tekst_pol += fraza_pol + " "
                print "7. Ustawienie aktualnych wartosci atrybutow <przypadek>:= 1, <liczba>:= %d, <rodzaj>:=%d " % (N,G)
                print "8. Przejscie do kroku nr 14."
                
                print "14. Czy przetlumaczono juz cale zdanie?"
                (fraza,koniec_zdania,lista_slow,lista_slow_temp) = redukcja_zdania(lista_slow_temp,lista_slow)                
                if koniec_zdania == True:
                    print "TAK przejscie do kroku 17.(Jezeli to bylo ostantnie zdanie to petla zakonczy dzialanie)"
                    lista_tekst_pol.append((tekst_pol.strip()+".",[tekst_pol.strip()+"."]))
                    tekst_pol = ""
                else:
                    print "NIE, przejscie do kroku 15.(kolejny obieg petli dla nowej frazy)"
            else:
                print "NIE, przejscie do pkt 9."
                print "9. Czy <fraza> jest <pojedynczym wyrazem>?"
                print lista_slow_temp
                if len(lista_slow_temp) == 1:
                    print "TAK, przejscie do kroku 10."
                    print "10. Wypisanie jako tlumaczenia <frazy> rozwazany <pojedynczy wyraz> == %s" % lista_slow_temp[0] 
                    lista_tekst_pol.append((tekst_pol.strip(),[tekst_pol.strip()]))
                    tekst_pol = ""

                    slowa_pol = dbm.tlumacz_slowo_ang(lista_slow_temp[0])
                    if len(slowa_pol) == 0:
                        print "<NIE_przetlumaczony_wyraz>:= <%s>" % lista_slow_temp[0]
                        lista_tekst_pol.append((lista_slow_temp[0],[lista_slow_temp[0]]))
                    else:
                        print "<tlumaczony_wyraz> == <%s> :" % lista_slow_temp[0]
                        lista_temp = []
                        for (slowo_pol,) in slowa_pol:
                            lista_temp.append(slowo_pol)    
                        lista_tekst_pol.append((lista_slow_temp[0],lista_temp))

                    print "11. Przejscie do kroku 14."

                    print "14(2). Czy przetlumaczono juz cale zdanie?"
                    (fraza,koniec_zdania,lista_slow,lista_slow_temp) = redukcja_zdania(lista_slow_temp,lista_slow)
                    if koniec_zdania == True:
                        print "TAK przejscie do kroku 17.(Jezeli to bylo ostantnie zdanie to petla zakonczy dzialanie 18. jeżeli nie to krok 2.)"
                        lista_tekst_pol.append((tekst_pol.strip()+".",[tekst_pol + '.']))
                        tekst_pol = ""
                    else:
                        print "NIE, przejscie do kroku 15.(kolejny obieg petli dla nowej frazy)"
                else:
                    print "NIE, przejscie do kroku 12."
                    print "12. Przypisanie <fraza>:= <fraza> minus <ostatni wyraz frazy>"
                    fraza = obciecie_wyrazu(lista_slow_temp)
                    print "13. Przejscie do kroku 5."
                    
    print "18. STOP"        

    return slowa_do_listy(lista_tekst_pol)


def obciecie_wyrazu(lista_slow_temp):
    fraza = ""
    lista_slow_temp.pop()
    for s in lista_slow_temp:
        fraza += s + " "
    return fraza.strip()


def redukcja_zdania(lista_slow_temp,lista_slow):
    lista_slow_new = []
    fraza_new = ""
    dl = len(lista_slow)
    dlt = len(lista_slow_temp)
    #print "*** dl = %d, dlt = %d" % (dl, dlt)
    #print lista_slow
    #print lista_slow_temp
    lista_slow_temp = []
    koniec_zdania = False
    if dl == dlt:
        koniec_zdania = True
    else:
        i = dlt
        while i < dl:
             lista_slow_new.append(lista_slow[i])
             lista_slow_temp.append(lista_slow[i])
             fraza_new += lista_slow[i] + " "
             i += 1    
    #print "*** Redukcja : " + fraza_new
    return (fraza_new.strip(),koniec_zdania,lista_slow_new,lista_slow_temp)


def slowa_do_listy(lista_slow):
    wynik = list()
    for (slowo,lista_tl) in lista_slow:
        trans = TransWord()
        if len(lista_tl) == 1 and (slowo in lista_tl):
            trans.word_in = slowo
            trans.flag = 'false'
        else:
            trans.word_in = slowo
            trans.flag = 'true' 
            for r in lista_tl:
                trans.list_of_words.append(r)
        wynik.append(trans) 
        del trans  
    return wynik


def get_lista_zdan_pbmt(tekst):
    tekst = tekst.replace('\'','\\\'')
    lista_zdan = re.compile("[.]*",re.L).split(tekst)
    if lista_zdan[-1].strip() == "":
        lista_zdan = lista_zdan[:-1]
    return lista_zdan        



