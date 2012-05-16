import sys
import re
import urllib2
import urlparse
import sqlite3 as sqlite
import logging
import json 
import codecs

logging.basicConfig(level=logging.DEBUG)

dbfilename = "defaultExport.db"

connection = sqlite.connect(dbfilename)
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS apps           (id INTEGER PRIMARY KEY, 
															appname VARCHAR(256), 
															category VARCHAR(256), 
															rating REAL,
															downloads VARCHAR(256),
															content_rating VARCHAR(256),
															file_size REAL)""")
#cursor.execute('CREATE TABLE IF NOT EXISTS urls_to_crawl (category VARCHAR(256), url VARCHAR(256))')

connection.commit()



def exportToSqlite(entry):
	appName = entry['appName']
	category = entry['category']
	rating = entry['rating']
	downloads = entry['downloads']
	contentRating = entry['contentRating']
	fileSize = entry['fileSize']
	
	cursor.execute("INSERT INTO apps VALUES ((?), (?), (?), (?), (?), (?), (?))", (None, appName, category, rating, downloads, contentRating, fileSize))
	connection.commit()
	#print fileSize

if __name__ == "__main__":
    logging.debug("Export to SQLite Started!")
    f = codecs.open("export.txt", "r", "UTF-8")
    for line in f.readlines():
    	entry = json.loads(line)
    	exportToSqlite(entry)
    f.close()
    connection.close()

    
