__hunts__ = '__hunts__'
__hunted_by__ = '__huntedBy__'

class Animal(object):
    def __init__(self):
        self.__dict__ = {}
        
    def __repr__(self):
        return self.className
    
    def __str__(self):
        return self.className
        
    def __getattr__(self,key):
        __key__ = '__%s__' % (key.replace('_',''))
        return '%s.%s --> "%s"' % (self,key,', '.join([c.className for c in self.__dict__[__key__]])) if (self.__dict__.has_key(__key__)) else '%s.%s --> %s' % (self,key,None)
    
    def __hunts__(self,prey):
        if (not self.__dict__.has_key(__hunts__)):
            self.__dict__[__hunts__] = []
        if (prey not in self.__dict__[__hunts__]):
            self.__dict__[__hunts__].append(prey)
        try:
            if (not prey.__dict__.has_key(__hunted_by__)):
                prey.__dict__[__hunted_by__] = []
            if (self not in prey.__dict__[__hunted_by__]):
                prey.__dict__[__hunted_by__].append(self)
        except:
            i = 0
            while (i < len(self.__dict__[__hunts__])):
                if (self.__dict__[__hunts__][i] == prey):
                    del self.__dict__[__hunts__][i]
                    break
                
    def className():
        doc = "className"
        def fget(self):
            return str(self.__class__).split()[-1].split("'")[1]
        return locals()    
    className = property(**className())

                    
class Lion(Animal):
    def __init__(self):
        super(Animal, self).__init__()
        self.__dict__['__class__'] = self.className
        
class Tiger(Animal):
    def __init__(self):
        super(Animal, self).__init__()
        self.__dict__['__class__'] = self.className
        
_lion_ = Lion()

_tiger_ = Tiger()

_lion_.__hunts__(_tiger_)

print 'BEGIN:'
print _lion_.hunts
print _tiger_.hunts

print _lion_.huntedBy
print _tiger_.huntedBy
print 'END !'
