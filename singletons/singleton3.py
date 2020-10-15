class Singleton(object):
    __single = None # the one, true Singleton

    def __new__(classtype, *args, **kwargs):
        # Check to see if a __single exists already for this class
        # Compare class types instead of just looking for None so
        # that subclasses will create their own __single objects
        if classtype != type(classtype.__single):
            classtype.__single = object.__new__(classtype, *args, **kwargs)
        return classtype.__single

    def __init__(self,name=None):
        self.name = name

    def display(self):
        print self.name,id(self),type(self)

class Subsingleton(Singleton):
    pass

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
