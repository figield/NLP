#!/usr/bin/python
# coding: latin-1
import sys,re
import string
from locale import *
from string import *

#setlocale(LC_ALL,'pl_PL')
#setlocale(LC_ALL,'pl_PL.latin-1')
#setlocale(LC_ALL,'pl_PL.ISO8859-2')
setlocale(LC_ALL,'pl_PL.utf8')
 
frazy = open('frazy.txt','w')
zbior_fraz={}

def toLowerCasePL(fraza):
    fraza = fraza.strip().lower()
    fraza=fraza.replace('¡','±')
    fraza=fraza.replace('Ê','ê')
    fraza=fraza.replace('Æ','æ')
    fraza=fraza.replace('¯','¿')
    fraza=fraza.replace('¬','¼')
    fraza=fraza.replace('Ó','ó')
    fraza=fraza.replace('¦','¶')
    fraza=fraza.replace('Ñ','ñ')
    return fraza


for fraza in re.compile("[0-9:;,./(){}_<>!?^%=*&$#\-\+\"\'\n\b\r\[\]]*",re.L).split(open(sys.argv[1],"r").read()):
    if not fraza:
        continue
   
    fraza = toLowerCasePL(fraza)    
    
    if zbior_fraz.get(fraza)==None:
        zbior_fraz[fraza]= 1
    else:
        zbior_fraz[fraza]= zbior_fraz[fraza] + 1
    
    
       
k=zbior_fraz.keys()
k.sort()
for x in k:
    frazy.write(x +" "+str(zbior_fraz[x]) + "\n")     
    
