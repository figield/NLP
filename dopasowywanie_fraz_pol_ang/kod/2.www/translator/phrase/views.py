# -*- coding: ISO-8859-2 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse
from libs.databasemanager import *
from libs.record import *
from libs.translation import *
from simplemethod.pol2ang import tlumacz_slowa
from clpmethod.pol2ang import tlumacz_slowa_clp
from phrasemethod.pol2ang import tlumacz_slowa_phrase
from pbmtmethod.ang2pol import tlumacz_text_pbmt
from libs.transWord import *
from libs.parseText import *
import time

#---------------------------------------------------------------------------
def main_page(request):
    return render_to_response('main_page.html', {})

#---------------------------------------------------------------------------    
def translate(request):
    return render_to_response('translate.html', {})

#---------------------------------------------------------------------------    
def translate_ang(request):
    return render_to_response('translate_ang.html', {})

#---------------------------------------------------------------------------    
def dictionary(request):
    return render_to_response('dictionary.html', {})

#---------------------------------------------------------------------------    
def phrase(request):
    return render_to_response('phrase.html', {})

#---------------------------------------------------------------------------    
def go_and_translate(request):
    tekst = ""
    try:
        tekst = request.POST['text_to_translate']
    except:     
        return render_to_response('translate.html',{})
    
    level1 = request.POST.get('level1', False)
    level2 = request.POST.get('level2', False)
    level3 = request.POST.get('level3', False)
    level4 = request.POST.get('level4', False)
    translation = tekst.encode('latin2')
    dbm = DBmanager() 
    lista_slow = wydziel_slowa(translation)
    lista_fraz = wydziel_frazy(translation)
    wynik1 = ""
    wynik2 = ""
    wynik3 = ""
    wynik4 = ""
    show1 = False
    show2 = False
    show3 = False
    show4 = False
    nr = 0

    if level1:
        show1 = True
        [wynik1,nr] = generate_results_to_html(tlumacz_slowa(dbm,lista_slow),nr)
    
    if level2:
        show2 = True
        [wynik2,nr] = generate_results_to_html(tlumacz_slowa_clp(dbm,lista_slow),nr)
    
    if level3:
        show3 = True
        [wynik3,nr] = generate_results_to_html(tlumacz_slowa_phrase(dbm,lista_fraz,0),nr)
        
    if level4:
        show4 = True
        [wynik4,nr] = generate_results_to_html(tlumacz_slowa_phrase(dbm,lista_fraz,1),nr)

    return render_to_response('translate.html',{'translation1':wynik1,'wynik1':show1,
                                                    'translation2':wynik2,'wynik2':show2,
                                                    'translation3':wynik3,'wynik3':show3,
                                                    'translation4':wynik4,'wynik4':show4,
                                                    'text_to_translate':tekst.strip(),'show_trans':True})


#---------------------------------------------------------------------------  
def go_and_translate_ang(request):
    tekst = ""
    try:
        tekst = request.POST['text_to_translate']
    except:     
        return render_to_response('translate_ang.html',{})
    
    level1 = request.POST.get('level1', False)
    translation = tekst.encode('latin2')
    dbm = DBmanager() 
    wynik1 = ""
    show1 = False
    nr = 0

    if level1:
        show1 = True
        [wynik1,nr] = generate_results_to_html(tlumacz_text_pbmt(dbm,translation),nr)
   
    return render_to_response('translate_ang.html',{'translation1':wynik1,'wynik1':show1,
                                                    'text_to_translate':tekst.strip(),'show_trans':True})

#---------------------------------------------------------------------------  
#---------------------------------------------------------------------------  

def wrappcolor(color,w):
    return "<font color= \"" + color + "\">" + w + "</font>"

def wrappselect_alternatives(value_id,w):
    if w == '-Del-':
        return "<li><span onClick=\"cT('""','sp"+str(value_id)+"')\">"+w+"</span></li>"    
    else:
        return "<li><span onClick=\"cT('"+w+"','sp"+str(value_id)+"')\">"+w+"</span></li>"

def generate_results_to_html(lista_rekordow,nr):
    wynik = ""
    for d in lista_rekordow:
        if d.flag == 'true': 
            if len(d.list_of_words) == -1:
                #slowo = d.list_of_words[0].decode('latin2').encode('utf-8')
                #wynik = wynik + wrappcolor("black",slowo) + " "
                nr = nr + 1
                for s in d.list_of_words:
                    wynik = wynik + "<a class = \"choice\" id=\"sp"+str(nr)+"\"><span class=\"before\">"+ s.decode('latin2').encode('utf-8') +"</span><ul>"
                wynik = wynik +wrappselect_alternatives(nr,"-Del-")+" "+"</ul></a>" + " "
            else:  
                nr = nr + 1
                first = 'true' 
                for s in d.list_of_words:
                    if first=='true':
                        wynik = wynik + "<a class = \"choice\" id=\"sp"+str(nr)+"\"><span class=\"before\">"+ s.decode('latin2').encode('utf-8') +"</span><ul>"
                    first = 'false' 
                    wynik = wynik + wrappselect_alternatives(nr,s.decode('latin2').encode('utf-8'))+" "
                wynik = wynik +wrappselect_alternatives(nr,"-Del-")+" "+"</ul></a>" + " "
        else:
            slowo = d.word_in.decode('latin2').encode('utf-8')
            if slowo == '.':
                wynik = wynik[:-1] + wrappcolor("blue",slowo) + " "
            else:
                wynik = wynik + wrappcolor("blue",slowo) + " " 
    return [wynik,nr]

#---------------------------------------------------------------------------      
#---------------------------------------------------------------------------
def return_to_translation(request):
    tekst = ""
    try:
        tekst = request.POST['text_to_translate'] 
    except:     
        return render_to_response('translate.html',{})

    return render_to_response('translate.html',{'text_to_translate':tekst.strip()})


#---------------------------------------------------------------------------
def sentence(request):       
    return render_to_response('sentence.html', {})

#---------------------------------------------------------------------------
def find_sentence(request):
    sentences_list = []
    words = ""
    if request.method == "POST" and request.POST["words"]:
        words = request.POST["words"].encode('latin2')
    
    dbm = DBmanager()
    limit = '100'
    records = dbm.findTranslation(words.strip(),limit)
    for r in records:
        t = Translation()
        t.pol = r[2].decode('latin2').encode('utf-8')    
        t.ang = r[4].decode('latin2').encode('utf-8')
        t.flag = r[5]        
        sentences_list.append(t)

    if "_inline" in request.POST:
        return render_to_response("all_sentences.html", {'all_sentences': sentences_list, 'rows':"hello word!"})
    else:
        return render_to_response("all_sentences.html", {'all_sentences': sentences_list})
     
#---------------------------------------------------------------------------
def find_phrase(request):
    sentences_list = []
    words = ""
    if request.method == "POST" and request.POST["words"]:
        words = request.POST["words"].encode('latin2')
    
    dbm = DBmanager()
    limit = '100'
    records = dbm.findPhrase(words.strip(),limit)
    for r in records:
        t = Translation()
        t.pol = r[0].decode('latin2').encode('utf-8')    
        t.ang = r[1].decode('latin2').encode('utf-8')
        #t.flag = r[5]        
        sentences_list.append(t)

    if "_inline" in request.POST:
        return render_to_response("all_phrases.html", {'all_sentences': sentences_list, 'rows':"hello word!"})
    else:
        return render_to_response("all_phrases.html", {'all_sentences': sentences_list})

#---------------------------------------------------------------------------
def find_word(request):
    sentences_list = []
    words = ""
    if request.method == "POST" and request.POST["words"]:
        words = request.POST["words"].encode('latin2')
    
    dbm = DBmanager()
    limit = '100'
    records = dbm.findWord(words.strip(),limit)
    for r in records:
        t = Translation()
        t.pol = r[0].decode('latin2').encode('utf-8')    
        t.ang = r[1].decode('latin2').encode('utf-8')
        t.flag = r[2]        
        sentences_list.append(t)

    if "_inline" in request.POST:
        return render_to_response("all_words.html", {'all_sentences': sentences_list, 'rows':"hello word!"})
    else:
        return render_to_response("all_words.html", {'all_sentences': sentences_list})


#---------------------------------------------------------------------------
def credits(request):
    return render_to_response('credits.html', {})

#---------------------------------------------------------------------------
