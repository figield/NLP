#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, re
from string import *
from cPickle import dump, load
import codecs

def main():

    filename = 'flex_pol_dict_sorted_utf8_small.txt'
    f_fleks = codecs.open(filename, 'rb', encoding='utf-8')
    fleksMap = {}
    for line in f_fleks.readlines():
        if (re.match(r'^\d+:', line)):            
            baseWord = line.split(':')[1].strip().lower()
        else:
            fleksWord = line.split('-')[1].strip().lower()
            fleksMap[fleksWord] = baseWord

    fleksMapFile = open('polfleksMap.pic','wb')
    dump(fleksMap, fleksMapFile, 2)
    fleksMapFile.close()

def test():
    fleksMapFile = open('polfleksMap.pic','rb')
    fleksMap = load(fleksMapFile)
    print fleksMap['mamy']
    print fleksMap[u'\u017cabie']
    #print fleksMap['niema']

if __name__ == '__main__':
    main()
    test()
