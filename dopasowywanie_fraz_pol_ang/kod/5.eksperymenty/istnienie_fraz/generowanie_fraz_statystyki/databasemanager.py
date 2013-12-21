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
    
   
    def get_sentence(self,pol_or_ang):
        query = "select "
        if pol_or_ang == "pol":
            query += "pol from translationPolAng"
        else:
            query += "ang from translationPolAng" 
        self.cur.execute(query)
	return self.cur.fetchall()

    def find_phrase(self,lista_slow,n,pol_or_ang):
        query = "select count(*) from "
        if pol_or_ang == "pol":
            query = query + "statistics_pol where "
        else:
            query = query + "statistics_pol where "
 
        comparison= ""
        i = 0
        while i < n : 
           comparison = comparison + "word"+str(i+1)+"='"+lista_slow[i]+"'"
           i = i + 1
           if i < n:
               comparison = comparison + " and "

        if n < 6:
            comparison +=  " and word%d is NULL" % (n+1)
            #comparison = " word"+str(n+1)+" is NULL and " + comparison
        query += comparison       
        self.cur.execute(query)
        amount = self.cur.fetchall()[0][0]
   
        if amount > 0: 
            return True
        else: 
            return False
  
    def get_all_phrases(self,n,pol_or_ang):
        query = "select * from "
        if pol_or_ang == "pol":
            query += "statistics_pol where "
        else:
            query += "statistics_ang where "
 
        comparison= ""
        i = 0
        while i < n : 
           comparison +=  "word%d is not NULL" % (i + 1)
           i = i + 1
           if i < n:
               comparison += " and "

        if n < 6:
            comparison = comparison  + " and word%d is NULL" % (n + 1)
        
        query = query + comparison  
        
        self.cur.execute(query)
        return self.cur.fetchall()

