from win32api import GetComputerName
try:
    import shelve
    __use_shelve__ = True
except ImportError:
    __use_shelve__ = False

from vyperlogix.json.jsonshelve import FlatShelf

class persistence(object):
    def __init__(self, fname, use__name__=False, use_shelve=False):
        self.__fname = fname
        self.__use__name__ = use__name__
        self.__use_shelve__ = use_shelve
        self.__isUsingSpecificFileName = False

    def set_isUsingSpecificFileName(self,bool):
        self.__isUsingSpecificFileName = bool
    
    def get_isUsingSpecificFileName(self):
        return self.__isUsingSpecificFileName
    
    def set_fname(self,fname):
        self.__fname = fname
        self.isUsingSpecificFileName = True
    
    def get_fname(self):
        return self.__fname
    
    def getShelvedFileName(self):
        if (self.isUsingSpecificFileName):
            return self.fname
        else:
            n = ''
            if (self.__use__name__):
                n = '_%s' % (__name__)
            return '%s%s_%s.dat' % (self.fname,n,GetComputerName())
    
    def shelveThis(self,key,value):
        if (__use_shelve__ and self.__use_shelve__):
            handle = shelve.open(self.getShelvedFileName())
            handle[key] = value
            handle.close()
        else:
            handle = FlatShelf(self.getShelvedFileName())
            handle.load()
            handle[key] = value
            handle.save()
            handle.close()
    
    def unShelveThis(self,key,value=''):
        fname = self.getShelvedFileName()
        try:
            if (__use_shelve__ and self.__use_shelve__):
                handle = shelve.open(fname)
                if (handle.has_key(key)):
                    try:
                        value = handle[key]
                    except Exception, details:
                        print 'Unable to un-shelve from "%s" due to "%s".' % (fname,str(details))
                    finally:
                        handle.close()
            else:
                handle = FlatShelf(fname)
                handle.load()
                if (handle.has_key(key)):
                    try:
                        value = handle[key]
                    except Exception, details:
                        print 'Unable to un-shelve from "%s" due to "%s".' % (fname,str(details))
                    finally:
                        handle.close()
        except:
            print 'Unable to un-shelve from "%s", probably due to a faulty path name.' % fname
        return value

    fname = property(get_fname, set_fname)
    isUsingSpecificFileName = property(get_isUsingSpecificFileName, set_isUsingSpecificFileName)
