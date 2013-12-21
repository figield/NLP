#!/usr/bin/python
# -*- coding: latin2 -*-

class myArgv:
      # zapisywanie do pliku informacji o zdaniu i tlumaczeniu slow
    logs = True
      # zapisywanie do pliku postepu parsowania fragmentow ksiazki
    track = True
      # mozliwe wartosci:
      # chunks - ilosc kawalkow = chunk, zakladka = margin
      # adaptive - dopasowanie dynamiczne w obszarze o ustalonym promieniu poszukiwan 
      # chunks_adaptive - polaczenie metody 'chunks' i 'adaptive' 
    synchronization_method = 'chunks'
      # promien poszukiwan dla metody 'adaptive' 
    radius = 200
      # ilosc fragmentow na ktore zostanie podzielony rozdzial
    chunk = 20
      # ilosc znakow, kt�ra jest dodawana na poczatku i na koncu fragmentu tekstu angielskiego
    margin = 100
      # tag rozdzielajacy rozdzialy polskich ksiazek
    split_pol = "CHAPTER_POL" 
      # tag rozdzielajacy rozdzialy angielskich ksiazek   
    split_ang = "CHAPTER_ANG"
      # uwzglednianie fraz od ngram_min do ngram_max wyrazowych
    ngram_min = 4
      # maksymalna wartosc to 6
    ngram_max = 6
      # roznica dlugosci frazy pol i ang, ang <= pol + diff && ang >= pol - diff
    diff = 2
      # drukowanie i selekcja fraz na 4 sposoby do wyboru (wsp. metoda):      
      # 0 - czyli wszystkie propozycje dopasowan
      # 1 - na podstwie statystyk samych fraz
      # 2 - na podstawie przeciecia fraz
      # 3 - na podstawie statystyk podfraz.
    selection_method_number = 3
      # do wyboru simple/stat
    generation_method = 'simple'
      # katalog z danymi - tekstami. teksty polskie musza byc w podkatalogu pol. 
      # Teksty angielskie w podkatalogu ang. Teksty polskie i angielskie musz�
      # nazywac sie tak samo oraz ich ilosc musi byc rowna.
      # wartosc inna niz 'dane' spowoduje odczyt z bazy
    texts = 'dane'
      # zapisywanie wynikow do pliku wyniki/simple_dopasowanie_wynik.txt
    to_file = True
      # zapisywanie danych do tabeli
    to_db = True
      # rodzaj tabeli przechowujacej wniki (temp|all)
      # temp - tymczasowa tabela - analiza wynikow itp
      # all - zbiorcza tabela danych - wyniki sa mergowane z poprzednimi
    typ_db = "temp"
      # zapisanie na dysku fraz z ich wszystkimi dopasowaniami, w celu dalszego powi�kszania zbioru.
      # True - zapisz zbi�r, False - nie zapisuj zbioru.
    frozen_phrases_write = True
      # wczytywanie z dysku fraz z ich wszystkimi dopasowaniami, w celu dalszego powi�kszania zbioru.
      # True - wczytaj zbi�r z dysku o ile taki istnieje, False - tw�rz zb�r od nowa.
    frozen_phrases_read = True
