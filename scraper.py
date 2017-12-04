import urllib2
import time

class Scraper(object):
    def __init__(self, query, globalId = 'EBAY-GB'):
        self.endpoint = 'http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords'
        self.serviceName = '&SERVICE-NAME=FindingService'
        self.serviceVersion = '&SERVICE-VERSION=1.0.0'
        self.globalId = '&GLOBAL-ID=' + globalId
        self.appName = '&SECURITY-APPNAME=JanKapus-retrogam-PRD-45d80d3bd-81ede79d'
        self.format = '&RESPONSE-DATA-FORMAT=XML'
        self.keywords = '&keywords=' + query

    def requestXML(self):
        URL = self.endpoint + self.serviceName + self.serviceVersion + self.globalId + self.appName + self.format + self.keywords
        print URL
        try:
            request = urllib2.urlopen(URL)
            XML = request.read()
        except Exception:
            print 'something went wrong'

        print XML

    def populateDB(self):
        pass

class Messanger(object):
    def __init__(self):
        pass



def main():
    lastQuery = int(time.time())

    while True:
        time.sleep(3)
        curTime = int(time.time())
        if curTime - lastQuery >= 600:
            lastQuery = curTime
            a = Scraper('commodore+64')
            a.requestXML()

if __name__ == "__main__":
    main()
