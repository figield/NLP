#!/usr/bin/python
# -*- coding: latin2 -*-
import _plp
import string
from locale import *
from string import *


def zasieg(): 
    i = 1000000
    while i < 1118830:
        forms = _plp.plp_forms(i)
        if len(forms)< 2:
            i+=1
            continue
        myhash = {}
        slowa = forms.split(':')
        for slowo in slowa:
            vec_id = _plp.plp_vec(i,slowo)
            numery = vec_id.split(':')[1:]
            for nr in  numery:
                myhash[int(nr)] = slowo
        indeksy = myhash.keys()
        indeksy.sort()
        print "%s: %s" % (str(i),_plp.plp_label(i))
        for ind in indeksy:
            print " %d - %s" % (ind,myhash[ind])
        i += 1

def main(): 
    print "init..."
    _plp.plp_init()
    zasieg()
	
main()
