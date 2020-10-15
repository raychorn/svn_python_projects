# http://www.djangosnippets.org/snippets/564/
from hashlib import sha1
from django.core.cache import cache as _djcache

from vyperlogix import misc

from vyperlogix.misc import ObjectTypeName

from vyperlogix.classes import SmartObject

try:
    from cPickle import Pickler, Unpickler
except ImportError:
    from pickle import Pickler, Unpickler

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def unPickleItem(glob):
    return Unpickler(StringIO(glob)).load()

def pickleItem(glob):
    io = StringIO()
    Pickler(io, -1).dump(glob)
    return io.getvalue()

def cache(seconds = 900):
    """
        Cache the result of a function call for the specified number of seconds, 
        using Django's caching mechanism.
        Assumes that the function never returns None (as the cache returns None to indicate a miss), and that the function's result only depends on its parameters.
        Note that the ordering of parameters is important. e.g. myFunction(x = 1, y = 2), myFunction(y = 2, x = 1), and myFunction(1,2) will each be cached separately. 

        Usage:

        @cache(600)
        def myExpensiveMethod(parm1, parm2, parm3):
            ....
            return expensiveResult
`
    """
    def doCache(f):
        def x(*args, **kwargs):
            key = sha1(str(f.__module__) + str(f.__name__) + str(args) + str(kwargs)).hexdigest()
            result = _djcache.get(key)
            if (result is None):
                result = f(*args, **kwargs)
                _result = [item if (not SmartObject.isSmartObject(item)) else item.asPythonDict() for item in result]
                _result = pickleItem(_result)
                _djcache.set(key, _result, seconds)
            else:
                result = unPickleItem(result)
                if (misc.isList(result)):
                    if (all([misc.isString(item) for item in result])):
                        result = ''.join(result)
                else:
                    pass
            return result
        return x
    return doCache
