__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
import os, sys
class MySQLConnectionSniffer():
    def __init__(self,host,port,db,username,password):
        self.__host__ = host
        self.__port__ = port
        self.__db__ = db
        self.__username__ = username
        self.__password__ = password
        
    def __str__(self):
        return self
        
    def exists(self):
        try:
            import MySQLdb
        except ImportError:
            print >> sys.stderr, 'ERROR: Cannot import MySQLdb and this is required.'
            return False
        results = True
        try:
            db = MySQLdb.connect(host=self.host, port=int(str(self.port)),
                                 user=self.username,
                                  passwd=self.password,
                                  db=self.db)
            print '#1 (%s:%s)-(%s)@(%s,%s)' % (self.host,self.port,self.db,self.username,self.password)
            db.close
        except:
            results = False
        return results
                
    def host():
        doc = "host is readonly"
        def fget(self):
            return self.__host__
        return locals()    
    host = property(**host())

    def port():
        doc = "port is readonly"
        def fget(self):
            return self.__port__
        return locals()    
    port = property(**port())

    def db():
        doc = "db is readonly"
        def fget(self):
            return self.__db__
        return locals()    
    db = property(**db())

    def username():
        doc = "username is readonly"
        def fget(self):
            return self.__username__
        return locals()    
    username = property(**username())

    def password():
        doc = "password is readonly"
        def fget(self):
            return self.__password__
        return locals()    
    password = property(**password())

