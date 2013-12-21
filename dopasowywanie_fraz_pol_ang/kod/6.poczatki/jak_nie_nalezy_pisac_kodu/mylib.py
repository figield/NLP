#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
from string import * 


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

