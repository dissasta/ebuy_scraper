from urllib.request import urlopen
import time
import psycopg2
from datetime import datetime

dbname = 'ebuy_scraper'
user = 'ebuy_scraper'
host = 'localhost'
password = 'Kapuston123'

currentDate = datetime.today().day

class User(object):
    users = []
    def __init__(self, name, email, dailyUpdate = None):
        self.name = name
        self.email = email
        self.dailyUpdate = dailyUpdate
        self.dailyMailSent = False
        User.users.append(self)
        
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
            if query[0] == 3:
                print(XML)
        except Exception:
            print('something went wrong')

    def parseXML(self, data):
       pass
        

class DBManager(object):
    def __init__(self):
        pass
        
    def pullData(self, table):
        cur = self.conn.cursor()
        cur.execute("""SELECT * FROM %s""" % table)
        rows = cur.fetchall()
        cur.close()
        return rows
    
    def updateLastScraped(self, queryID, curTime):
        cur = self.conn.cursor()
        cur.execute("""UPDATE queries SET lastscraped = %s WHERE id = %s""" % (curTime, queryID)) 
        self.conn.commit()
        cur.close()
    
    def pushData(self, table, column, newvalue, criteria, id):
        cur = self.conn.cursor()
        cur.execute("""UPDATE $s SET %s = %s WHERE $s = %s""" % (table, column, newvalue, criteria, id))
        self.conn.commit()
        cur.close()
    
    def manageResults(self, query):
        #update old results
        pass
        #add new results
        
        #remove dead results
        
    def connect(self):
        try:
            self.conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (dbname, user, host, password))
        except Exception:
            print('Failed to establish connection to the DB')

    def updateUsers(self):
        userList = self.pullData('users')
        if len(userList) != len(User.users):
            if User.users:
                for name in userList:
                    found = False
                    for present in User.users:
                        if name[0] == present.name:
                            found = True
                            break
                    
                    if not found:
                        User(name[0], name[2], name[3])
            else:
                for name in userList:
                    User(name[0], name[2], name[3])
        
        for present in User.users:
            for user in userList:
                if user[0] == present.name:
                    present.dailyUpdate = user[3]
                    break

                                            
class Messanger(object):
    def __init__(self):
        pass


def main():
    global currentDate
    dbmanager = DBManager()
    dbmanager.connect()
    scraper = Scraper()
    
    while True:
        dbmanager.updateUsers()           
        
        time.sleep(3)
        
        queries = dbmanager.pullData('queries')
        
        for query in queries:
            curTime = time.time()
            if curTime - query[6] >= query[5]:
                dbmanager.updateLastScraped(query[0], curTime)
                allResults = scraper.requestXML(query)
                if allResults:
                    newResults = dbmanager.manageResults(query, allResults)
                    if newResults and query[8]:
                        pass
                        #messanger send mail
            else:
                print('current difference =' + str(curTime - query[6])) 
        
        #wyslanie emaila z wynikami wyszukania
        for user in User.users:
            if not user.dailyMailSent:
                if time.time() >= user.dailyUpdate:
                    print('wysylam maila')
                    user.dailyMailSent = True
            else:
                if datetime.today().day - currentDate != 0:
                    user.dailyUpdate += 86400
                    user.dailyMailSent = False
                    currentDate = datetime.today().day
                    
if __name__ == "__main__":
    main()
