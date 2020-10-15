import MySQLdb
import sqlite3

if (__name__ == '__main__'):
    aConnection = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="peekab00",db="geonosis")
    aCursor = aConnection.cursor()
    
    aCursor.execute('''SHOW TABLES''')
    
    __tables__ = {}
    
    for i in xrange(0,aCursor.rowcount):
        anItem = aCursor.fetchone()
        aTableName = list(anItem)[0]
        print aTableName
        __tables__[aTableName] = {}
        
    for t in __tables__:
        aCursor.execute('''DESCRIBE %s''' % (t))
        for i in xrange(0,aCursor.rowcount):
            anItem = list(aCursor.fetchone())
            __tables__[t][anItem[0]] = anItem
    
    aConnection.close()