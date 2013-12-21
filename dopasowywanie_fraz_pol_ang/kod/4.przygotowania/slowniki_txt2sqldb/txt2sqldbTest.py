#!/usr/bin/python
# -*- coding: latin2 -*-
import os,sys,re
import string
from locale import *
from string import *
from databasemanager import *


      
def main():
    
    dbm = DBmanager() 
    print " Czyszczenie tabeli \'dictionary\'"
    dbm.clearTranslation()
    dbm.insertTranslationTest()
    
    
    print "ok"
	
main()
