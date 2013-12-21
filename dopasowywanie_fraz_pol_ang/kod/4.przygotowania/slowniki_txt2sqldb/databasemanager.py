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
	
    def testQuery(self):
	self.cur.execute("select version()")
	print self.cur.fetchone()[0]
		
    def getVerb(self, verb):
	self.cur.execute("SELECT * FROM verbs WHERE verb = '" + verb + "'")
	return self.cur.fetchone()
		
    def getEnglishVerb(self, word):
	self.cur.execute("SELECT translation FROM dictonary d, verbs v WHERE v.verb = '" + word + "' AND d.word = v.id_verb")
	return self.cur.fetchall()
	    
    def getCategoryOfEnglishVerb(self, verb):		
	self.cur.execute("SELECT category FROM english_verbs WHERE verb = '" + verb + "'")
	return  self.cur.fetchall()

    def getVerbsWithCategories(self):
	self.cur.execute("SELECT * FROM verbs WHERE category IS NOT NULL")
	return self.cur.fetchall() #self.cur.fetchone()[0]
    
    def getVerbsByCategory(self, category, limit):
	self.cur.execute("SELECT * FROM verbs WHERE category = " + category + " AND amount != 0 order by rand() LIMIT " + str(limit))
	return self.cur.fetchall() #self.cur.fetchone()[0]
    
    def getVerbs(self):
	self.cur.execute("SELECT * FROM verbs")
	return self.cur.fetchall() #self.cur.fetchone()[0]

    def getNumRows(self, id_word, id_verb):
	#params = (id_verb, id_word)
    	self.cur.execute("SELECT count(*) FROM words_frequency WHERE id_verb = " + str(id_verb) + " AND id_word = " + str(id_word))
	return self.cur.fetchone()[0]
	
    def insertTranslation(self, word, translation, id_description, id_gender):
        query = "INSERT INTO dictionary(word, translation, id_description, id_gender) VALUES ('" + word + "','" + translation + "', '" + id_description + "', '" + id_gender +"')" 
    	self.cur.execute(query)	  
	return 1

    def getTranslation(self, slowoPol,slowoAng):
        query="SELECT * FROM dictionary WHERE word='"+slowoPol+"' and translation='"+slowoAng+"'"
        self.cur.execute(query)
        return self.cur.fetchall()

    def getTranslationExist(self, slowoPol,slowoAng):
        query="SELECT count(*) FROM dictionary WHERE word='"+slowoPol+"' and translation='"+slowoAng+"'"
        self.cur.execute(query)
        return self.cur.fetchone()[0]


    def insertTranslationTest(self):
        query = "INSERT INTO dictionary(word, translation, id_description, id_gender) VALUES ('śźćńłóćąęż' , 'ĄŻŁÓĘŚĆŹŃ', 1,1)" 
        print query
    	self.cur.execute(query)	  
	return 1
	
    def insertGender(self, id_gender, gender):
        query = "INSERT INTO gender(id_gender,gender) VALUES (" + str(id_gender) + ",'" + gender +"')" 
        self.cur.execute(query)	  
        return 1
	
    def insertDescription(self, id_description, description):
        query = "INSERT INTO description(id_description, description) VALUES (" + str(id_description) + ",'" + description  +"')" 
        self.cur.execute(query)	  
        return 1

    def insertStatisticsPol(self, frequency, words):
        query = "INSERT INTO statistics_pol(frequency,"
        i = 1
        for w in words:
            query = query + "word" + str(i)
            if i == len(words):
                query = query + ") VALUES ("
            else:
                query = query + ","
            i = i + 1
        i = 1
        query = query + str(frequency) + ","
        for v in words:
            query = query + "'" + v + "'"
            if i == len(words):
                query = query + ")"
            else:
                query = query + ","
            i = i + 1
        self.cur.execute(query)	
        return 1
    
    def insertStatisticsAng(self,frequency, words):
        query = "INSERT INTO statistics_ang(frequency,"
        i = 1
        for w in words:
            query = query + "word" + str(i)
            if i == len(words):
                query = query + ") VALUES ("
            else:
                query = query + ","
            i = i + 1
        i = 1
        query = query + str(frequency) + ","
        for v in words:
            query = query + "'" + v + "'"
            if i == len(words):
                query = query + ")"
            else:
                query = query + ","
            i = i + 1
        self.cur.execute(query)	
        return 1
    

    def clearDescription(self):
        query = "DELETE FROM description"
        self.cur.execute(query)	
        return 1

    def clearGender(self):
        query = "DELETE FROM gender"
        self.cur.execute(query)	
        return 1

    def clearTranslation(self):
        query1 = "DELETE FROM dictionary"
        query2 = "ALTER TABLE dictionary AUTO_INCREMENT=1"
        self.cur.execute(query1)
        self.cur.execute(query2)	
        return 1  
     
    def clearStatisticsPol(self):
        query1 = "DELETE FROM statistics_pol"
        query2 = "ALTER TABLE statistics_pol AUTO_INCREMENT=1"
        self.cur.execute(query1)
        self.cur.execute(query2)	
        return 1  
    
    def clearStatisticsAng(self):
        query3 = "DELETE FROM statistics_ang"
        query4 = "ALTER TABLE statistics_ang AUTO_INCREMENT=1"
        self.cur.execute(query3)
        self.cur.execute(query4)	
        return 1  
    

    def getEnglishWord(self, slowo):
        query = "SELECT word, translation FROM dictionary WHERE word='"+slowo+"'"
        self.cur.execute(query)
        return self.cur.fetchall()
	
    def updateWord(self, id_verb, id_word,num):
	#params = (id_word, id_verb)
    	self.cur.execute("UPDATE words_frequency SET amount = amount + " + str(num) + " WHERE id_word = " + str(id_word) + " AND id_verb = " + str(id_verb))	  
	return #self.con.commit()
    
    def getWordsByVerbId(self, ids):
	self.cur.execute("SELECT id_word, amount, form FROM words_frequency WHERE " + ids + " AND (form = 1) ORDER BY amount DESC LIMIT 2000")
	return self.cur.fetchall()
    		
    def getWordsByVerbId2(self, ids):
	self.cur.execute("SELECT id_word, sum(amount) s, form FROM words_frequency WHERE " + ids + " AND (form = 1) GROUP BY id_word ORDER BY s DESC")
	return self.cur.fetchall()
    
    def removeEntry(self, id_verb, id_word):
	self.cur.execute("DELETE FROM words_frequency WHERE id_word = " + str(id_word) + " AND id_verb = " + str(id_verb))
	return 1
	
    def getVerbId(self, verb):
	self.cur.execute("SELECT id_verb FROM verbs WHERE verb = '" + str(verb) + "'")	  
	return self.cur.fetchone()
	
    def updateNumWords(self, id_verb, amount):
	self.cur.execute("UPDATE verbs SET amount = amount + " + str(amount) + " WHERE id_verb = " + str(id_verb))	  
	return 1

    
