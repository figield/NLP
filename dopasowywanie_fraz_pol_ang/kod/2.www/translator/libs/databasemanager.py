# -*- coding: utf8 -*-
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

    
    def findTranslation(self, words, limit):
        query = "select * from translationPolAng where pol like \"%"+words+"%\" or ang like \"%"+words+"%\" limit " + limit
        self.cur.execute(query)
	return self.cur.fetchall()
  
    def findPhrase(self, words, limit):
        query = "select phrase_pol, phrase_ang from phrase_dictionary_temp where phrase_pol like \"%"+words+"%\" or phrase_ang like \"%"+words+"%\" limit " + limit
        self.cur.execute(query)
	return self.cur.fetchall()

    def findWord(self, words, limit):
        query = "select word,translation,id_description from dictionary where word like \"%"+words+"%\" or translation like \"%"+words+"%\" limit " + limit
        self.cur.execute(query)
	return self.cur.fetchall()


    def get_sentence(self,pol_or_ang):
        query = "select "
        if pol_or_ang == "pol":
            query += "pol from translationPolAng"
        else:
            query += "ang from translationPolAng" 
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_both_sentences(self):
        query = "select pol, ang from translationPolAng"#" where id = 2806"    
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_both_sentences_test(self):
        query = "select pol, ang from translationPolAng where id = 2806"    
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def get_translation_pol2ang(self,word_pol): 
        query = "select translation from dictionary where word ='%s'" % word_pol     
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
        
        query = query + comparison #+ " limit 50" 
        
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_exceptions_ang(self,word_e):
        query = "select word from exceptions_ang where word_e = '" + word_e + "'"
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_synonym_pol(self,word):
        query = "select word1, word2 from exceptions_pol where word1 like \"%" + word + "%\" or word2 like \"%" + word + "%\""
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_all_names(self):
        self.cur.execute("SELECT name FROM names")
        return self.cur.fetchall()


    def clear_temp(self):
        query1 = "DELETE FROM phrase_dictionary_temp"
        query2 = "ALTER TABLE phrase_dictionary_temp AUTO_INCREMENT=1"
        self.cur.execute(query1)
        self.cur.execute(query2)	
        return 1  

    def write_phrase_to_temp(self,dl,fraza_pol,fraza_ang):
        query = "INSERT INTO phrase_dictionary_temp(phrase_pol, phrase_ang,len) VALUES ('" + fraza_pol + "','" + fraza_ang + "'," +  str(dl) + ")" 
        self.cur.execute(query)	  
        return 1

    def get_all_phrases(self):
        return {}

    def clear_all_phrases(self):
        query1 = "DELETE FROM phrase_dictionary_all"
        query2 = "ALTER TABLE phrase_dictionary_all AUTO_INCREMENT=1"
        self.cur.execute(query1)
        self.cur.execute(query2)	
        return 1

    def get_phrase_ang(self,dl,fraza_pol): 
        query = "select phrase_ang from phrase_dictionary_temp where phrase_pol like '" + fraza_pol + "' and len >= " + str(dl)
        self.cur.execute(query)
        return self.cur.fetchall()
        
    def tlumacz_slowo_ang(self,slowo_ang):
        query = "select word from dictionary where translation = \'"+ slowo_ang+"\'"
        self.cur.execute(query)
        return self.cur.fetchall()


    def find_phrase_pbmt(self,fraza,N,G,C):
        query = ""
        fraza_pol = ""
        find = False
        if not find:
            query = "select C"+str(C)+",NG from NP where S = \'"+ fraza +"\'"
            self.cur.execute(query)
            records = self.cur.fetchall()
            if len(records) > 0:
                for (fraza_pol,NG) in records:
                    N = int(NG[0])
                    G = int(NG[1])
                    find = True
                    break

        if not find:
            query = "select NG"+str(N)+str(G)+",C from VP where S = \'"+ fraza +"\'"
            self.cur.execute(query)
            records = self.cur.fetchall()
            if len(records) > 0:
                for (fraza_pol,C_str) in records:
                    C = int(C_str)
                    find = True
                    break

        if not find:
            query = "select T from P where S = \'"+ fraza +"\'"
            self.cur.execute(query)
            records = self.cur.fetchall()
            if len(records) > 0:
                for (fraza_pol,) in records:
                    find = True
                    break
                    
        return (fraza_pol,N,G,C)

