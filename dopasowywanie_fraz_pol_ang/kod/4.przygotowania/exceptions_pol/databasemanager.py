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

    def insertExceptionPol(self, word1, word2, desc, typ):
        query = "INSERT INTO exceptions_pol(word1, word2, des, typ) VALUES ('" + word1 + "','" + word2 + "', '" + desc + "', '" + typ +"')" 
    	self.cur.execute(query)	  
	return 1  

    def getExceptionPol(self):
        query = "select word1,word2 from exceptions_pol" 
    	self.cur.execute(query)	  
	return self.cur.fetchall()
