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

    def insertTranslationPolAng(self, pol, pol_org, ang, ang_org, flag):
        query = "INSERT INTO translationPolAng(pol,pol_org, ang, ang_org, flag) VALUES ('" + pol + "','" + pol_org + "','" + ang + "','" + ang_org + "', '" + flag +"')" 
    	self.cur.execute(query)	  
	return 1
   

    def deleteTranslationPolAng(self):
        query = "DELETE FROM translationPolAng"
        query2 = "ALTER TABLE translationPolAng AUTO_INCREMENT=1" 
    	self.cur.execute(query)	
        self.cur.execute(query2)  
	return 1
    
