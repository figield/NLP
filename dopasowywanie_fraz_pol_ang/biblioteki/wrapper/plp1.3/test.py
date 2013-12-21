#!/usr/bin/python
# -*- coding: latin2 -*-
import _plp, os, sys, re 
from string import *

print "init..."
_plp.plp_init()
print "after init"
print _plp.plp_ver()
print "Aby zakonczyc wpisz: q, exit lub quit"

while 1:
    print "\npodaj wyraz:" 
    slowo = sys.stdin.readline()
    slowo = slowo.strip()
    if slowo == 'q' or slowo =='exit' or slowo=='quit':
        break
    string = _plp.plp_rec(slowo)
    numery = string.split(':')
    ile = int(numery[0])
    ids = numery[1:]

    for nr in ids:
        i = int(nr)
        label = _plp.plp_label(i)
        bform = _plp.plp_bform(i)	
        forms = _plp.plp_forms(i)
        vec_id = _plp.plp_vec(i,slowo)
        
        print "\nid: "+ str(i)
        if len(label) >= 1:
	    print "1)label: " + label
	
        if len(bform) >= 1:
	    print "2)bform: " + bform
	
        if len(forms) >= 1:
	    print "3)forms: " + forms
	
        if len(vec_id) >= 1:
	    print "4)vec_id: " + vec_id
		
        label = ""
        bform = ""
        forms = ""
        vec_id= ""
