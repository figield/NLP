# -*- coding: latin2 -*-
import sys
import MySQLdb
import re

class DBmanager:

    def __init__(self):
	self.con = MySQLdb.connect (host = "localhost",
                                    user = "polang",
                                    passwd = "polang",
                                    db = "polang",
                                    unix_socket = "/var/run/mysqld/mysqld.sock")
	self.cur = self.con.cursor()

    def insertTranslation(self, word, translation, id_description, id_gender):
        query = "INSERT INTO dictionary(word, translation, id_description, id_gender, label) VALUES ('" + word + "','" + translation + "', '" + id_description + "', '" + id_gender +"', 'B')" 
    	self.cur.execute(query)	  
	return 1

    def getTranslationExist(self, slowoPol,slowoAng):
        query="SELECT count(*) FROM dictionary WHERE word='"+slowoPol+"' and translation='"+slowoAng+"'"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def getExceptionExist(self, word_e,word):
        query="SELECT count(*) FROM exceptions_ang WHERE word_e ='"+word_e+"' and word='"+word+"'"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def insertIrregularVerb(self, verb1, verb2, verb3, word):
        query = "INSERT INTO irregularVerbs(verb1, verb2, verb3, word) VALUES ('" + verb1 + "','" + verb2 + "', '" + verb3 + "', '" + word +"')" 
    	self.cur.execute(query)	  
	return 1

    def insertException(self, word_e, word, desc, typ):
        query = "INSERT INTO exceptions_ang(word_e, word, des, typ) VALUES ('" + word_e + "','" + word + "', '" + desc + "', '" + typ +"')" 
    	self.cur.execute(query)	  
	return 1        

