from win32api import *
import shelve

class persistence(object):
    def __init__(self):
        pass

    def getShelvedFileName(self):
        return '%s_%s.dat' % (__name__,GetComputerName())
    
    def shelveThis(self,key,value):
        handle = shelve.open(self.getShelvedFileName())
        handle[key] = value
        handle.close()
    
    def unShelveThis(self,key):
        value = ''
        handle = shelve.open(self.getShelvedFileName())
        if (handle.has_key(key)):
            try:
                value = handle[key]
            except Exception:
                pass
            finally:
                handle.close()
        return value

