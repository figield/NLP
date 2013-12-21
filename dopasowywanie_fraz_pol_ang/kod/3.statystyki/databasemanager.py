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
    

    def get_2_phrases_ang(self):
        query = "select frequency from statistics_ang where word2 is not NULL and word3 is NULL order by frequency"
        self.cur.execute(query)
	return self.cur.fetchall()

    def get_3_phrases_ang(self):
        query = "select frequency from statistics_ang where word3 is not NULL and word4 is NULL order by frequency"
        self.cur.execute(query)
	return self.cur.fetchall()

    def get_4_phrases_ang(self):
        query = "select frequency from statistics_ang where word4 is not NULL and word5 is NULL order by frequency"
        self.cur.execute(query)
	return self.cur.fetchall()

    def get_5_phrases_ang(self):
        query = "select frequency from statistics_ang where word5 is not NULL and word6 is NULL order by frequency"
        self.cur.execute(query)
	return self.cur.fetchall()

    def get_6_phrases_ang(self):
        query = "select frequency from statistics_ang where word6 is not NULL order by frequency"
        self.cur.execute(query)
	return self.cur.fetchall()

    def get_2_phrases_pol(self):
        query = "select frequency from statistics_pol where word2 is not NULL and word3 is NULL order by frequency"
        print "query..."
        self.cur.execute(query)
        print "after execution ..."
	return self.cur.fetchall()

    def get_3_phrases_pol(self):
        query = "select frequency from statistics_pol where word3 is not NULL and word4 is NULL order by frequency"
        self.cur.execute(query)
	return self.cur.fetchall()

    def get_4_phrases_pol(self):
        query = "select frequency from statistics_pol where word4 is not NULL and word5 is NULL order by frequency"
        self.cur.execute(query)
	return self.cur.fetchall()

    def get_5_phrases_pol(self):
        query = "select frequency from statistics_pol where word5 is not NULL and word6 is NULL order by frequency"
        self.cur.execute(query)
	return self.cur.fetchall()

    def get_6_phrases_pol(self):
        query = "select frequency from statistics_pol where word6 is not NULL order by frequency"
        self.cur.execute(query)
	return self.cur.fetchall()




