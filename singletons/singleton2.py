class _Singleton(object):

    def __init__(self):
        # just for the sake of information
        self.instance = "Instance at %d" % self.__hash__()

_singleton = _Singleton()

def Singleton(): return _singleton

def test():
    s1 = Singleton()
    print __name__, id(s1)
    
    s2 = Singleton()
    print __name__, id(s2)

    s3 = _Singleton()
    print __name__, id(s3)

if (__name__ == '__main__'):
    test()
    