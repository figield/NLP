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
 
slowa1 = open('slowa1.txt','w')
slowo_1={}

for slowo in re.compile("[^a-zA-Z±¡êÊ¿¯¼¬æÆóÓ¶¦ñÑ³£]*[_\n]*",re.L).split(open(sys.argv[1],"r").read()):
    if not slowo:
        print slowo
        continue
    

    slowo = slowo.lower()
    if slowo_1.get(slowo)==None:
        slowo_1[slowo]= 1
    else:
        slowo_1[slowo]= slowo_1[slowo] + 1
    
    
       
k=slowo_1.keys()
k.sort()
for x in k:
    slowa1.write(x +" "+str(slowo_1[x]) + "\n")     
