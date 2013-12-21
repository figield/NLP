#!/usr/bin/env python

def n_tuples(n, lst):
    for i in xrange(len(lst) - n + 1):
        yield lst[i:i+n]

for words in n_tuples(4, 'ala ma kota i psa i chomika, krowe kota psa i koguta'.split()):
    print words
