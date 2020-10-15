from vyperlogix.classes.CooperativeClass import Cooperative

import os,sys
import traceback

# To-Do:
# 
# (1) Make Encrypted Egg to test this process.

class ZipImporterEncrypted(Cooperative):
    def __init__(self, path):
        self.__path__ = path
    
    def path():
        doc = "path"
        def fget(self):
            return self.__path__
        def fset(self, path):
            self.__path__ = path
        return locals()    
    path = property(**path())
    
if (__name__ == '__main__'):
    i = ZipImporterEncrypted()
    try:
        from vyperlogix.misc import ObjectTypeName
        print '(+++) %s' % ObjectTypeName.typeName(i)
    except ImportError:
        # To import from an exotic source we leave the source out of the normal path list and then notice when we cannot do the import.
        # Perform the import by reading the source and then do an "exec" to execute the source.
        pass
    except:
        exc_info = sys.exc_info()
        info_string = '\n'.join(traceback.format_exception(*exc_info))
        print >>sys.stderr, info_string
    pass
