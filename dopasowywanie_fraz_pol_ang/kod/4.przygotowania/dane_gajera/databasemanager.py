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

    def insertNP(self,dane):
        query = "INSERT INTO NP(S, C1, C2, C3, C4, C5, C6, NG) VALUES ('" + dane[0][1:-1].strip() + "','" + dane[1][1:-1].strip() + "','" + dane[2][1:-1].strip() + "','" + dane[3][1:-1].strip() + "','" + dane[4][1:-1].strip() + "','" + dane[5][1:-1].strip() + "','" + dane[6][1:-1].strip() + "','" + dane[7][1:-1].strip() + "')" 
    	self.cur.execute(query)	  
	return 1  

    def insertVP(self,dane):
        query = "INSERT INTO VP(S, NG11, NG12, NG13, NG21, NG22, NG23, C) VALUES ('" + dane[0][1:-1].strip() + "','" + dane[1][1:-1].strip() + "','" + dane[2][1:-1].strip() + "','" + dane[3][1:-1].strip() + "','" + dane[4][1:-1].strip() + "','" + dane[5][1:-1].strip() + "','" + dane[6][1:-1].strip() + "','" + dane[7][1:-1].strip() + "')" 
    	self.cur.execute(query)	  
	return 1  

    def insertP(self,dane):
        query = "INSERT INTO P(S, T) VALUES ('" + dane[0][1:-1].strip() + "','" + dane[1][1:-1].strip() + "')" 
    	self.cur.execute(query)	  
	return 1  

