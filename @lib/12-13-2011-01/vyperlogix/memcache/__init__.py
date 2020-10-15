__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
import os, sys
class MemcacheConnectionSniffer():
    def __init__(self,host,port,timeout):
        self.__host__ = host
        self.__port__ = port
        self.__timeout__ = timeout
        
    def __str__(self):
        return self
        
    def exists(self):
        from vyperlogix.memcache import tester

        results = False

        try:
            uri = '%s:%s'%(self.host,self.port)
            tester.__test_using_umemcache__(uri,timeout=self.timeout)
            print '#1 (%s)' % (uri)
            results = True
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

    def timeout():
        doc = "timeout is readonly"
        def fget(self):
            return self.__timeout__
        return locals()    
    timeout = property(**timeout())


