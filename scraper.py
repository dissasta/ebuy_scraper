from urllib.request import urlopen
import time
import psycopg2

dbname = 'ebuy_scraper'
user = 'ebuy_scraper'
host = 'localhost'
password = 'Kapuston123'

class Scraper(object):
    def __init__(self):
        self.endpoint = 'http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords'
        self.serviceName = '&SERVICE-NAME=FindingService'
        self.serviceVersion = '&SERVICE-VERSION=1.0.0'
        self.globalId = '&GLOBAL-ID='
        self.appName = '&SECURITY-APPNAME=JanKapus-retrogam-PRD-45d80d3bd-81ede79d'
        self.format = '&RESPONSE-DATA-FORMAT=XML'
        self.keywords = '&keywords='
        self.category = ''
        self.filters = ''
        
    def requestXML(self, query):
        queryText = query[1].replace(" ", "%20")
        queryCategory = query[2]
        queryGlobalID = query[3]
        queryFilters = query[4]
        
        URL = (self.endpoint + self.serviceName + self.serviceVersion + self.globalId + '%s' + self.appName + self.format + self.keywords + '%s') % (queryGlobalID, queryText)

        try:
            request = urlopen(URL)
            XML = request.read()
            self.parseXML(XML)
        
        except Exception:
            print('something went wrong')

    def parseXML(self):
        pass
        

class DBManager(object):
    def __init__(self):
        pass
        
    def checkQueries(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT * FROM queries""")
        rows = cur.fetchall()
        cur.close()

        return rows
    
    def updateLastScraped(self, queryID, curTime):
        cur = self.conn.cursor()
        cur.execute("""UPDATE queries SET lastscraped = %s WHERE id = %s""" % (curTime, queryID)) 
        cur.close()
        
    def connect(self):
        try:
            self.conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (dbname, user, host, password))
        except Exception:
            print('Failed to establish connection to the DB')


class Messanger(object):
    def __init__(self):
        pass


def main():
    dbmanager = DBManager()
    dbmanager.connect()
    scraper = Scraper()
    
    while True:
        time.sleep(3)
        queries = dbmanager.checkQueries()
        for query in queries:
            curTime = time.time()
            if curTime - query[6] >= query[5]:
                dbmanager.updateLastScraped(query[0], curTime)
                scraper.requestXML(query)
                
            else:
                print('current difference =' + str(curTime - query[6])) 
        

if __name__ == "__main__":
    main()
