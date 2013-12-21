#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string


def get_text(dbm,argv):
    if 'dane' in argv:
        lista_tekstow_rownoleglych = []
        lista_plikow = os.listdir(sys.argv[1]+"/pol")   
        for fname in lista_plikow:
            lista_tekstow_rownoleglych.append((open(sys.argv[1]+"/pol/"+fname,"r").read(),open(sys.argv[1]+"/ang/"+fname,"r").read()))
        return lista_tekstow_rownoleglych
    else:
        return dbm.get_both_sentences()


def init_stat(kat,simple,m,k):
    stat_pol2 = set()
    stat_pol3 = set()
    stat_pol4 = set()
    stat_pol5 = set()
    stat_pol6 = set()
    stat_ang2 = set()
    stat_ang3 = set()
    stat_ang4 = set()
    stat_ang5 = set()
    stat_ang6 = set()
    
    if not simple:
        for pol_or_ang in ['pol','ang']:
            n = m
            while n<=k:    
                print "Pobranie statystyk %d wyrazowych..." % (n)   
                if pol_or_ang == 'pol':
                    if n == 2:
                        stat_pol2 = load(open(kat+'/stat_pol2.pic','r')) 
                    elif n == 3:
                        stat_pol3 = load(open(kat+'/stat_pol3.pic','r'))
                    elif n == 4:
                        stat_pol4 = load(open(kat+'/stat_pol4.pic','r'))
                    elif n == 5:
                        stat_pol5 = load(open(kat+'/stat_pol5.pic','r'))
                    elif n == 6:
                        stat_pol6 = load(open(kat+'/stat_pol6.pic','r')) 
                else:
                    if n == 2:
                        stat_ang2 = load(open(kat+'/stat_ang2.pic','r'))
                    elif n == 3:
                        stat_ang3 = load(open(kat+'/stat_ang3.pic','r'))
                    elif n == 4:
                        stat_ang4 = load(open(kat+'/stat_ang4.pic','r'))
                    elif n == 5:
                        stat_ang5 = load(open(kat+'/stat_ang5.pic','r'))
                    elif n == 6:
                        stat_ang6 = load(open(kat+'/stat_ang6.pic','r'))
                n+=1 
    return ([stat_pol2,stat_pol3,stat_pol4,stat_pol5,stat_pol6],[stat_ang2,stat_ang3,stat_ang4,stat_ang5,stat_ang6])


def get_all_names(dbm):
    imiona = dbm.get_all_names()
    names = set()
    for (n,) in imiona:
        names.add(n.lower())  
    return names


def lista_nonsensow_na_poczatku_pol():
    return ['się', 'self', 'in','i', 'a','ą','b','c','ć','d','e', 'ę','f','g','h','j','k','l','ł','m','n','ń','ó','p', 'r','s','ś','t','ż','ż', 'ź','x',   'y','v','vi','iv','iii','ii','ix','xi','vii','viii','x','xi','xii','xiii','xiv','xv','xvi']


def lista_nonsensow_na_koncu_pol():    
    return ['self','in','i','a','ą','b','c','ć','d','e','ę','f','g','h','j','k','l','ł','m','n','ń','ó','p','r','s','ś', 't','ż','ż','ź','x','y','v','vi','iv','iii','ii','ix','xi','vii','viii','x','xi','xii','xiii','xiv','xv','xvi'] 
  

def lista_nonsensow_na_poczatku_ang():
    return ['selves','self','b','c','d','e','f','g','h','j','k','l','m','n','o','p','r','s','t','u','w','z','x', 'y','v','vi','iv','iii','ii','ix','xi','vii','viii','x','xi','xii','xiii','xiv','xv','xvi']


def lista_nonsensow_na_koncu_ang():
    return ['selves','self','i','the','a','an','b','c','d','e','f','g','h','j','k','l','m','n','o','p','r', 's','t','u','w','z','x','y','v','vi','iv','iii','ii','ix','xi','vii','viii','x','xi','xii','xiii','xiv','xv','xvi']

