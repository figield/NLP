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

    def insertNames(self, name, sex):
        query = "INSERT INTO names(name, sex) VALUES ('" + name + "','" + sex + "')" 
    	self.cur.execute(query)	  
	return 1        

    def getAllNames(self):
        self.cur.execute("SELECT name FROM names")
        return self.cur.fetchall()

