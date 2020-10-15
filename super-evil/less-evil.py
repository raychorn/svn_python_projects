class A(object):
    def __init__(self,*args,**kwargs):
        print "A","args=",','.join([str(a) for a in args])

class B(object):
    def __init__(self,*args,**kwargs):
        print "B","args=",','.join([str(a) for a in args])

class C(A):
    def __init__(self,*args,**kwargs):
        print "C","args=",','.join([str(a) for a in args])
        super(A, self).__init__(self)

class D(B):
    def __init__(self,*args,**kwargs):
        print "D", "args=",','.join([str(a) for a in args])
        super(B, self).__init__(self)

class E(C,D):
    def __init__(self,*args,**kwargs):
        print "E", "args=",','.join([str(a) for a in args])
        super(C, self).__init__(self,args,kwargs)
        super(D, self).__init__(self,args,kwargs)

E(10)

#from vyperlogix import oodb

#E arg= 10
#C arg= 10
#A
#D arg= 10
#B
