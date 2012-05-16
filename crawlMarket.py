#!/usr/bin/env python
# coding: utf-8

"""
Google Android Market Crawler
For the sake of research
1) database file name
2 through n) all the types we want to explore
"""

import sys
import re
import urllib2
import urlparse
import sqlite3 as sqlite
import threading
import logging
#from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) < 2:
    sys.exit("usage: [source] [category]");
else:
    source = sys.argv[1]
    argLen = len(sys.argv) - 1

    categories = [x.upper() for x in sys.argv[2::]]

import codecs
f = codecs.open(source, "w", "utf-8")

class MarketCrawler(threading.Thread):
    #mainURL = "https://market.android.com"
    #topfreeURL = "https://market.android.com/details?id=apps_topselling_free&num=24&cat="
    #toppaidURL = "https://market.android.com/details?id=apps_topselling_paid&num=24&cat="

    mainURL = "https://play.google.com"

    pageIncrements = 24;

    """
    run()
    This will be the entry point for the thread and it will loop through every
    category provided by the user
    crawl process
    """
    def run(self):
        logging.debug("Running new crawler thread")
        for cat in categories:
            print cat
            topfreeURL = "http://play.google.com/store/apps/category/" + cat + "/collection/topselling_free"
            toppaidURL = "http://play.google.com/store/apps/category/" + cat + "/collection/topselling_paid"
            self.crawlAppsForCategory(cat, topfreeURL)
            self.crawlAppsForCategory(cat, toppaidURL)

    def crawlAppsForCategory(self, cat, url):

        pageIndex = 0

        curl = url + "?start="
        # logging.debug("curl:" + curl);
        currentURL = curl + str(pageIndex) + "&num=" + str(self.pageIncrements)
        logging.debug("current URL:" + currentURL);
        

        while True:
            try:
                request = urllib2.Request(currentURL)
                #request.add_header("User-Agent", "PermissionCrawler; en-us")
                request.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.3 (KHTML, like Gecko)  QtWeb Internet Browser/3.7 http://www.QtWeb.net")
                request.add_header("Accept-Language", "en-US") # powtorka kodu na dole
                handle = urllib2.build_opener()
                content = handle.open(request).read()
                soup = BeautifulSoup(content)

                appURLS = self.extractAppUrls(soup)

                # for item in appURLS:
                #     logging.debug("appURLs:" + item);
                
                extractor = Extractor(appURLS, cat)
                extractor.start()
                logging.debug("Running thread")
                #self.extractPermissionsIntoDB(appURLS, cat)

                pageIndex+=self.pageIncrements
                currentURL = curl + str(pageIndex) + "&num=" + str(self.pageIncrements)

            except urllib2.HTTPError, error:
                if error.code == 404:
                    print >> sys.stderr, "404 ERROR: %s -> %s" % (error, error.url)
                if error.code == 403:
                    print >> sys.stderr, "403 (NO MORE APP PAGES FOR THIS CATEGORY)ERROR: %s -> %s" % (error, error.url)
                else:
                    print >> sys.stderr, "ERROR: %s" % error
                break
            except Exception, e:
                print >> sys.stderr, "iSERROR: %s" % e
    

    """
    From the page the lists a page of 24 apps of the particular category,
    extract the links to those apps
    """
    def extractAppUrls(self, soup):
        logging.debug("exctracing urls?")
        tags = soup('a')
        #to get rid of duplicates since the href get returns links twice
        # skip = False         

        appURLS = []
        for tag in tags:
            clazz = tag.get("class")
            if clazz == "title":
                href = tag.get("href")
                if href is not None: # byc moze potrzebne bedzie wiecej zabezpieczen. Zminifikowany kod playmarketu ma malo wspolnego z czytelnoscia
                    # logging.debug(self.mainURL + href)
                    appURLS.append(self.mainURL+href)

        # for tag in  tags:
        #     href = tag.get("href")
        #     if skip:
        #         skip = False
        #         continue
        #     if href is not None and re.match('/details', href) and not re.search('apps_editors_choice', href):
        #         #print href
        #         appURLS.append(self.mainURL+href)
        #         skip = True
        
        return appURLS


    """
    Fetch all the URLS in appURLS
    """
class Extractor(threading.Thread):
    def __init__(self, appURLS, cat):
        threading.Thread.__init__(self)
        self.sites = appURLS
        self.category = cat
        logging.debug("Created Extractor")
    
    def run(self):
        self.conn = sqlite.connect(source)
        self.curs = self.conn.cursor()
        #we can put this URL stuff into its own object /code repetition
        for site in self.sites:
            request = urllib2.Request(site)
            #request.add_header("User-Agent", "PyCrawler; en-us") #TODO: Wyjebac ta powtorke ^^
            request.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.3 (KHTML, like Gecko)  QtWeb Internet Browser/3.7 http://www.QtWeb.net")
            request.add_header("Accept-Language", "en-US")
            handle = urllib2.build_opener()
            content = handle.open(request).read()
            soup = BeautifulSoup(content)
            
            appName = soup.find('h1','doc-banner-title').contents[0]
            permissions = soup.findAll('div','doc-permission-description')

            # firebug masakra => dragonfly much betta
            
            # liczba ocen: <div class="votes">17 701</div>
            # <div class="votes">1 465</div>
            #votes = int((soup.find('div','votes').contents[0]).replace(' ', ''))
            
            # oceny (gwiazdki) : <div class="average-rating-value">4,6</div>
            rating = float(soup.find('div','average-rating-value').contents[0].replace(',', '.')) # masakra te przecinkokropki
            
            # cena: <meta itemprop="price" content="0"/>
            #price = soup.find('meta',attrs={"itemprop" : "price"}).get('content') #AttributeError: 'NoneType' object has no attribute 'contents'
            #splittedPrice = price.split(" ")
            #price = float(splittedPrice[0].replace(',', '.'))

            # aktualizacja: <time itemprop="datePublished">23 luty 2012</time>
            actualization = soup.find('time',attrs={"itemprop" : "datePublished"}).contents[0]
            
            # liczba pobran: <dd itemprop="numDownloads">1 000 000 - 5 000 000
            downloads = soup.find('dd',attrs={"itemprop" : "numDownloads"}).contents[0]
            
            # wykres sciagniec 
                #<div class="normalized-daily-installs-chart" style="width: 105px;">
                #   <img src="https://chart.googleapis.com/chart?cht=lxy&chd=e:AACIERGZIiKqMzO7RETMVVXdZmbud3f.iIkQmZohqqsyu7xDzM1U3d5l7u92,OoQdP2OoOBNaNaOoP2QdOoOBOBOBOoP2REQdP2P2S5d3oOrRnnj9g6gTg688&chds=0.0,1.0&chs=105x75&chma=1,0,1,1&chco=42b6c9ff&chls=2.5,1.0,0.0&chxl=0:%7C%7C1:%7C%7C2:%7C"/>
                # parametr chs opisuje wielkosc zadanego wykresu (max 3k px^2 ?)
            chart = soup.find('div', 'normalized-daily-installs-chart').contents[0].get('src')
            
            # Ocena tresci: <dd itemprop="contentRating">Dla wszystkich</dd>
            contentRating =  soup.find('dd', attrs={"itemprop" : "contentRating"}).contents[0]
            
            # wymaga androida: 
                #<dt itemprop="operatingSystems" content="Android">Wymaga Androida:</dt>
                #   <dd>2.1 lub nowszy</dd>
            version = soup.find('dd',attrs={"itemprop" : "softwareVersion"}).contents[0]
            
            # wielkosc : <dd itemprop="fileSize">6,5M</dd>
            fileSize = soup.find('dd', attrs={"itemprop" : "fileSize"}).contents[0]
            fileSize = fileSize.replace(',','.')
            if fileSize[-1] == 'M':
                fileSizeFloat = float(fileSize[:-1])
            elif fileSize[-1] == 'k':
                fileSizeStrpd = fileSize.rstrip('k')
                if len(fileSizeStrpd) == 3:
                    fileSizeFloat = float("0." + fileSizeStrpd)
                elif len(fileSizeStrpd) == 2:
                    fileSizeFloat = float("0.0" + fileSizeStrpd)
                elif len(fileSizeStrpd) == 1:
                    fileSizeFloat = float("0.00" + fileSizeStrpd)

            logging.debug("AppName: "       + appName)
            logging.debug("Category: "      + self.category)
            #logging.debug("Votes: "         + str(votes))
            logging.debug("Rating: "        + str(rating))
            #logging.debug("Price: "         + str(price))
            logging.debug("Actualization: " + actualization)
            logging.debug("Downloads: "     + downloads)
            logging.debug("Chart: "         + chart)
            logging.debug("ContentRating: " + contentRating)
            logging.debug("Version: " + version)
            logging.debug("File size: "     + str(fileSizeFloat))

            self.pushToFile(appName, self.category, rating, downloads, contentRating, fileSizeFloat, site)

    def pushToFile(self, appName, category, rating, downloads, contentRating, fileSize, site):
        logging.debug("Pushing to file app: " + appName)
        f.write("{")
        f.write("\"appName\" :"       + " \"" + appName       + "\"" + ",")
        f.write("\"category\" :"      + " \"" + category      + "\"" + ",")
        f.write("\"rating\" :"        + " "   + str(rating)          + ",")
        f.write("\"downloads\" :"     + " \"" + downloads     + "\"" + ",")
        f.write("\"contentRating\" :" + " \"" + contentRating + "\"" + ",")
        f.write("\"fileSize\" :"      + " "   + str(fileSize)        + "")
        #f.write("site :"          + " \"" + site          + "\"" + "\n") #UWAGA NA BRAK PRZECINKA
        f.write("}")

if __name__ == "__main__":
    logging.debug("Started!")
    #run the crawler thread
    MarketCrawler().run()
