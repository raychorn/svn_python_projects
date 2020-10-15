from util import exceptions
from util import ioTimeAnalysis

def isInteger(s):
    return (isinstance(s,int))

def isFloat(s):
    return (isinstance(s,float))

def __exec__(source,__locals__,__globals__):
    try:
        exec(source,__locals__,__globals__)
    except Exception, ex:
        print exceptions.formattedException(details=ex)
    return __globals__.get('val',None)

def analyze(reason):
    '''
    Usage:
    
    @analyze(reason)
    def method(item):
        print item
    '''
    def decorator(func):
        def proxy(*args, **kwargs):
            normalize = lambda a:str(a) if (isInteger(a) or isFloat(a)) else '"%s"'%(a)
            __args__ = ','.join([normalize(a) for a in args])
            __kwargs__ = ','.join(['%s=%s'%(k,normalize(v)) for k,v in kwargs.iteritems()])
            ioTimeAnalysis.initIOTime(reason)
            ioTimeAnalysis.ioBeginTime(reason)
            val = __exec__('val = func(%s%s%s)' % (__args__,',' if (len(kwargs) > 0) else '',__kwargs__),{'func':func},{})
            ioTimeAnalysis.ioEndTime(reason)
            return val
        return proxy
    return decorator
