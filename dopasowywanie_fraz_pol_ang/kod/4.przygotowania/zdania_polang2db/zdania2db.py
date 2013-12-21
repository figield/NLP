#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
import time 
from locale import *
from string import *
from databasemanager import *
  
p1e = re.compile('[\']+',re.L)
p2e = re.compile('[\"]+',re.L)  
p3e = re.compile(' \| ',re.L) 
      
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
#    tekst=re.compile('\'re ').sub(' are ',tekst) # cholera! całes statstyki trzeba zmienić!
    return tekst

def load_sentences(arg,flag,nr_pol,dbm):
    file_sentences = open(arg,"r").read()
    list_oftranslation = re.compile('\n\n',re.L).split(file_sentences)
    nr = 0
    print "flag:" + flag
    for trans_polang in list_oftranslation:
        lang_lang = p3e.split(trans_polang)
        nr = nr + 2
        if len(lang_lang) < 2:
           print flag +"nr: " + str(nr) +", len:" + str(len(lang_lang)) + ", " + trans_polang
        lang1org = lang_lang[0].strip()
        lang2org = lang_lang[1].strip()
        if nr_pol == 1:
            lang1 = filtr_zamianaNaMaleLiteryPL(lang1org)
            lang1org =  p1e.sub('\\\'',lang1org)
            lang1org =  p2e.sub('\\\'',lang1org)
            lang1 = filtr_zamianaNaMaleLitery(lang1)
            lang2 = filtr_zamianaNaMaleLitery(lang2org)
            lang2org =  p1e.sub('\\\'',lang2org)
            lang2org =  p2e.sub('\\\'',lang2org)
            lang2 = filtr_usuniecieNiewygodnychZnakow(lang2)
            lang2 = filtr_zamianyNaFormyRozszerzoneAng(lang2)
            lang1 = p1e.sub('\\\'',lang1) 
            lang1 = p2e.sub('\\\"',lang1) 
            lang2 = p1e.sub('\\\'',lang2) 
            lang2 = p2e.sub('\\\"',lang2)
            dbm.insertTranslationPolAng(lang1,lang1org,lang2,lang2org,flag)
        else:
            lang2 = filtr_zamianaNaMaleLiteryPL(lang2org)
            lang2org =  p1e.sub('\\\'',lang2org)
            lang2org =  p2e.sub('\\\'',lang2org)  
            lang2 = filtr_zamianaNaMaleLitery(lang2)
            lang1 = filtr_zamianaNaMaleLitery(lang1org)
            lang1org =  p1e.sub('\\\'',lang1org)
            lang1org =  p2e.sub('\\\'',lang1org)
            lang1 = filtr_usuniecieNiewygodnychZnakow(lang1)
            lang1 = filtr_zamianyNaFormyRozszerzoneAng(lang1) 
            lang1 = p1e.sub('\\\'',lang1) 
            lang1 = p2e.sub('\\\"',lang1) 
            lang2 = p1e.sub('\\\'',lang2) 
            lang2 = p2e.sub('\\\"',lang2)
            dbm.insertTranslationPolAng(lang2,lang2org,lang1,lang1org,flag)
            
def main():
    lista_plikow= os.listdir(sys.argv[1])
    dbm = DBmanager() 
    if "rm" in sys.argv:
        print "Czyszczenie tabeli translationPolAng\n"
        dbm.deleteTranslationPolAng()
        time.sleep(0.5)
    for arg in lista_plikow:
        load_sentences(sys.argv[1]+"/"+arg,sys.argv[2],int(sys.argv[3]),dbm)

main()
