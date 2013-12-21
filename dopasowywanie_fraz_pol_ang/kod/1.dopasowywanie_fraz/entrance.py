#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from locale import *
from init.myArgv import *
from libs.dopasuj_frazy import *

def main(): 

    args = myArgv()
    flaga = False
    p1 = re.compile('=',re.L)
    listOflines = []

    try:
        settingsFile = open("settings","r").read()
        flaga = True
    except:
        print "ustawienia domyslne"
        flaga = False        
    
    if flaga:
        listOflines = re.compile('\n',re.L).split(settingsFile)
   
    for line in listOflines:
        if len(line) < 3: continue
        if line[0] == '#' or line[0] == '' or line[0] == ' ' or ('=' not in line):
            continue  
        else:
            list1 = p1.split(line.strip())
            param = list1[0].strip()
            print param + " = " + list1[1].strip()
            if param == 'logs':
                if list1[1].strip() == 'True':
                    args.logs = True
                else:              
                    args.logs = False
            elif param == 'track':
                if list1[1].strip() == 'True':
                    args.track = True
                else:              
                    args.track = False
            elif param == 'synchronization_method':
                args.synchronization_method = list1[1].strip()
            elif param == 'radius':
                args.radius = int(list1[1].strip())            
            elif param == 'chunk':
                args.chunk = int(list1[1].strip()) 
            elif param == 'margin':
                args.margin = int(list1[1].strip()) 
            elif param == 'separator_pol':
                args.split_pol = list1[1].strip() 
            elif param == 'separator_ang':
                args.split_ang = list1[1].strip() 
            elif param == 'ngram_min':
                args.ngram_min = int(list1[1].strip()) 
            elif param == 'ngram_max':
                args.ngram_max = int(list1[1].strip()) 
            elif param == 'diff':
                args.diff = int(list1[1].strip()) 
            elif param == 'selection_method_number':
                args.selection_method_number = int(list1[1].strip()) 
            elif param == 'generation_method':
                args.generation_method = list1[1].strip() 
            elif param == 'data_source':
                args.texts = list1[1].strip() 
            elif param == 'to_file':
                if list1[1].strip() == 'True':
                    args.to_file = True
                else:              
                    args.to_file = False
            elif param == 'to_db':
                if list1[1].strip() == 'True':
                    args.to_db = True
                else:              
                    args.to_db = False
            elif param == 'data_target':
                args.typ_db = list1[1].strip()
            elif param == 'frozen_phrases_write':
                if list1[1].strip() == 'True':
                    args.frozen_phrases_write = True
                else:              
                    args.frozen_phrases_write = False 
            elif param == 'frozen_phrases_read':
                if list1[1].strip() == 'True':
                    args.frozen_phrases_read = True
                else:              
                    args.frozen_phrases_read = False 

    run(args)  
 

if __name__ == '__main__':
    main()
