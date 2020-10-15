class A(object):
    def __init__(self):
        print "A"

class B(object):
    def __init__(self):
        print "B"

class C(A):
    def __init__(self, arg):
        print "C","arg=",arg
        A.__init__(self)

class D(B):
    def __init__(self, arg):
        print "D", "arg=",arg
        B.__init__(self)

class E(C,D):
    def __init__(self, arg):
        print "E", "arg=",arg 
        C.__init__(self, arg)
        D.__init__(self, arg)

E(10)
