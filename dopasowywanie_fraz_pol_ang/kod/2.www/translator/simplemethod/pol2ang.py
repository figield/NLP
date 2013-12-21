#!/usr/bin/python
# -*- coding: ISO-8859-2 -*-
from libs.transWord import * 


def tlumacz_slowa(dbm,lista_slow):
    wynik = list()
    for slowo in lista_slow:
        records = dbm.get_translation_pol2ang(slowo.strip())
        trans = TransWord()
        if len(records) < 1 :
            trans.word_in = slowo
            trans.flag = 'false'
        else:
            trans.word_in = slowo
            trans.flag = 'true' 
            for r in records:
                trans.list_of_words.append(r[0])
        wynik.append(trans) 
        del trans  
    return wynik
	        
	
