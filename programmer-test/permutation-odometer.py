#from vyperlogix import oodb
#from vyperlogix.decorators import properties_idiom
from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash.lists import HashedLists
from vyperlogix.lists.ListWrapper import CircularList

d = {
    '2': ['A', 'B', 'C'],
    '3': ['D', 'E', 'F'],
    '4': ['G', 'H', 'I'],
    '5': ['J', 'K', 'L'],
    '6': ['M', 'N', 'O'],
    '7': ['P', 'Q', 'R', 'S'],
    '8': ['T', 'U', 'V'],
    '9': ['W', 'X', 'Y', 'Z'],
}

class CircularOdometer(CircularList):
    def callback():
        doc = "callback"
        def fget(self):
            callback = None
            try:
                callback = self.__callback__
            except AttributeError:
                callback = None
            return current
        def fset(self, callback):
            self.__callback__ = callback
        return locals()
    callback = property(**callback())

    def current():
        doc = "current"
        def fget(self):
            current = 0
            try:
                current = self.__current__
            except AttributeError:
                current = 0
            return current
        def fset(self, current):
            self.__current__ = current
        return locals()
    current = property(**current())

    def siblings():
        doc = "siblings"
        def fget(self):
            siblings = []
            try:
                siblings = self.__siblings__
            except AttributeError:
                siblings = []
            return current
        def fset(self, siblings):
            self.__siblings__ = siblings
        return locals()
    siblings = property(**siblings())

    def next(self):
        try:
            self.current += 1
            if (self.current >= len(self)):
                if (callable(self.callback)):
                    try:
                        self.callback(self)
                        self.__has_rolled__ = True
                        self.current = 0
                    except:
                        pass
            return self.__cycler__.next()
        except AttributeError:
            import itertools 
            self.__cycler__ = itertools.cycle(self)
            self.current -= 1
            return self.next()

    def has_rolled():
        doc = "has_rolled"
        def fget(self):
            has_rolled = False
            try:
                has_rolled = self.__has_rolled__
            except AttributeError:
                has_rolled = False
            return has_rolled
        return locals()
    has_rolled = property(**has_rolled())

def __init__(_d_, callback=None):
    if (misc.isDict(_d_)):
        for k, v in _d_.iteritems():
            if (misc.isList(v)):
                _v_ = CircularOdometer(initlist=v)
                _v_.callback = callback
            else:
                _v_ = v
            _d_[k] = _v_

def __transform__(s):
    l = []
    if (misc.isString(s)):
        for ch in s:
            v = d[ch] if (d.has_key(ch)) else None
            l.append(v)
        for i in xrange(0, len(l)):
            c = l[i]
            c.siblings = l[i + 1:]
            pass
    return l

def callback(self):
    try:
        self.siblings[0].next()
    except:
        pass
    pass

if (__name__ == '__main__'):
    __init__(d, callback=callback)
    target = '234'
    target = __transform__(target)
    _count_ = 1
    __d__ = HashedLists()
    print 'BEGIN:'
    try:
        while (not target[-1].has_rolled):
            word = ''.join([i[i.current] for i in target])
            __d__[word] = word
            _is_repeated_ = False
            if (any([len(i) > 1 for i in __d__.values() if (misc.isList(i))])):
                _is_repeated_ = True
            print '%s :: %s%s' % (_count_, word, ' (R)' if (_is_repeated_) else '')
            if (_is_repeated_):
                break
            target[0].next()
            _count_ += 1
    except Exception, ex:
        print _utils.formattedException(details = ex)
    print 'END!'
