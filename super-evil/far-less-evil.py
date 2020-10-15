import inspect

def second_arg(func):
    args = inspect.getargspec(func)[0]
    if len(args) >= 2: return args[1]

class _Cooperative(type):
    def __init__(cls, name, bases, dic):
        for n,func in dic.iteritems():
            setattr(cls, n, func)
    def __setattr__(cls, name, func):
        set = super(_Cooperative, cls).__setattr__
        if inspect.isfunction(func) and second_arg(func) == "super":
            set(name, lambda self, *args, **kw : 
                func(self, super(cls, self), *args, **kw))
        else:
            set(name, func)

class Cooperative:
    __metaclass__ = _Cooperative

class A(object):
    def __init__(self,*args,**kwargs):
        print "A","args=",','.join([str(a) for a in args])

class B(object):
    def __init__(self,*args,**kwargs):
        print "B","args=",','.join([str(a) for a in args])

class C(A):
    def __init__(self,*args,**kwargs):
        print "C","args=",','.join([str(a) for a in args])
        super().__init__(self,args,kwargs)

class D(B):
    def __init__(self,*args,**kwargs):
        print "D", "args=",','.join([str(a) for a in args])
        super().__init__(self,args,kwargs)

class E(C,D):
    def __init__(self,*args,**kwargs):
        print "E", "args=",','.join([str(a) for a in args])
        super().__init__(self,args,kwargs)
        #super(E, self).__init__(self,args,kwargs)

E(10)


