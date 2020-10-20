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
import uuid
from vyperlogix.hash import lists

from vyperlogix.classes import CooperativeClass

__is_memcachable__ = True
try:
    import memcache
except ImportError:
    __is_memcachable__ = False

class MemCacheMixin(CooperativeClass.Cooperative):
    '''
    This object seeks to provide an interface to memcache in a generic manner however memcache is so weak it is best used
    as it was designed to be used - simply as a way to cache key,value pairs and nothing more.
    '''
    def __init__(self,mc_servers=['127.0.0.1:11211'],mc_debug=0):
        global __is_memcachable__
        self.__mc_servers__ = mc_servers
        self.__mc_debug__ = mc_debug
        self.__d__ = lists.HashedLists2()
        if (__is_memcachable__):
            self.__memcache_client__ = memcache.Client(self.mc_servers, debug=self.mc_debug)
            __is_memcachable__ = all([s.connect() for s in self.__memcache_client__.servers])
            
    def set_item(self,key,value,time=0):
        global __is_memcachable__
        if (__is_memcachable__):
            proxy_key = str(uuid.uuid4())
            self.__d__[key] = proxy_key
            self.__memcache_client__.set(proxy_key,value,time=time)
            
    def get_item(self,key):
        global __is_memcachable__
        if (__is_memcachable__):
            proxy_key = self.__d__[key]
            if (proxy_key is not None):
                value = self.__memcache_client__.get(proxy_key)
                if (value is None):
                    del self.__d__[key]
                return value
        return None
            
    def get_keys(self):
        return self.__d__.keys()
            
    def mc_servers():
        doc = "mc_servers"
        def fget(self):
            return self.__mc_servers__
        return locals()
    mc_servers = property(**mc_servers())    

    def mc_debug():
        doc = "mc_debug"
        def fget(self):
            return self.__mc_debug__
        return locals()
    mc_debug = property(**mc_debug())    
