import thread

class Singleton(object):
    '''Implement Pattern: SINGLETON'''

    __lockObj = thread.allocate_lock()  # lock object
    __instance = None  # the unique instance

    def __new__(cls, *args, **kargs):
        return cls.getInstance(cls, *args, **kargs)

    def __init__(self):
        pass

    def getInstance(cls, *args, **kargs):
        '''Static method to have a reference to **THE UNIQUE** instance'''
        # Critical section start
        cls.__lockObj.acquire()
        try:
            if cls.__instance is None:
                # (Some exception may be thrown...)
                # Initialize **the unique** instance
                cls.__instance = object.__new__(cls, *args, **kargs)

                '''Initialize object **here**, as you would do in __init__()...'''

        finally:
            #  Exit from critical section whatever happens
            cls.__lockObj.release()
        # Critical section end

        return cls.__instance
    getInstance = classmethod(getInstance)
    
if __name__ == "__main__":
    o1 = Singleton('foo')
    o1.display()
    o2 = Singleton('bar')
    o2.display()
    o3 = Subsingleton('foobar')
    o3.display()
    o4 = Subsingleton('barfoo')
    o4.display()
    print 'o1 = o2:',o1 == o2
    print 'o1 = o3:',o1 == o3
    print 'o3 = o4:',o3 == o4
    print 'o1 is a singleton?',isinstance(o1,Singleton)
    print 'o3 is a singleton?',isinstance(o3,Singleton)
    print 'o1 is a subsingleton?',isinstance(o1,Subsingleton)
    print 'o3 is a subsingleton?',isinstance(o3,Subsingleton)
