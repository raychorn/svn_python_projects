from vyperlogix.classes import SmartObject

class SampleObj(object):
    def __init__(self):
        self.__dict__ = {}
        
    def foo():
        doc = "property foo's doc string"
        def fget(self):
            return self.__dict__['foo']
        def fset(self, value):
            self.__dict__['foo'] = value
        def fdel(self):
            del self.__dict__['foo']
        return locals()
    foo = property(**foo())
    

if (__name__ == '__main__'):
    s = SampleObj()
    s.foo = '1'
    print s.foo
    
    so = SmartObject.SmartObject(s.__dict__)
    print so.foo
    print so['foo']
