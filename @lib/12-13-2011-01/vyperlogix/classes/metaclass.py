from vyperlogix.misc import ObjectTypeName

class CooperativeAbstract(type):
    """Metaclass implementing cooperative methods. Works
    well for methods returning None, such as __init__"""
    def __init__(cls,name,bases,dic):
        for meth in getattr(cls,'__cooperative__',[]): 
            setattr(cls,meth,cls.coop_method(meth,dic.get(meth)))
    def coop_method(cls,name,method): # method can be None
        """Calls both the superclass method and the class method (if the 
        class has an explicit method). Implemented via a closure"""
        def _(self,*args,**kw):
            getattr(super(cls,self),name)(*args,**kw) # call the supermethod
            if method: method(self,*args,**kw) # call the method
        return _

class CooperativeBase(object):
    __metaclass__=CooperativeAbstract
    __cooperative__=['__init__']
