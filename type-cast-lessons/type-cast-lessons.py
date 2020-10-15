class Parent(object):
    def __set__(self,key,value):
        self.__dict__[key] = value

    def __get__(self,key):
        return self.__dict__[key]

    def __delete__(self,key):
        del self.__dict__[key]

    def __setattr__(self,key,value):
        self.__dict__[key] = value

    def __getattr__(self,key):
        return self.__dict__[key]

    def __delattr__(self,key):
        del self.__dict__[key]
        
    def __setitem__(self,key,value):
        self.__dict__[key] = value

    def __getitem__(self,key):
        return self.__dict__[key]

    def __delitem__(self,key):
        del self.__dict__[key]
        
    def __repr__(self):
        import StringIO
        ioBuf = StringIO.StringIO()
        print >> ioBuf, '{',
        items = []
        for k,v in self.__dict__.iteritems():
            items.append('%s=%s' % (k,v))
        print >> ioBuf, ', '.join(items),
        print >> ioBuf, '}'
        return ioBuf.getvalue()
        
class A(Parent):
    pass

class B(Parent):
    pass

class C(A):
    pass

_a_ = A()

print _a_.__dict__

print '{',
for k,v in _a_.__dict__.iteritems():
    print '%s=%s' % (k,v),
print '}'

print "There won't be any key/value pairs in _a_ at this time.\n"

_a_['foo'] = 'bar'
_a_['animal'] = 'cat'

print "Now there are key/value pairs in _a_.\n"

print '{',
items = []
for k,v in _a_.__dict__.iteritems():
    items.append('%s=%s' % (k,v))
print ', '.join(items),
print '}'

print
print 'Now I will make _a_ into an instance of B()\n'

_b_ = B()

print '{',
for k,v in _b_.__dict__.iteritems():
    print '%s=%s' % (k,v),
print '}'

print "There won't be any key/value pairs in _b_ at this time.\n"

for k,v in _a_.__dict__.iteritems():
    _b_[k] = v

print '{',
items = []
for k,v in _b_.__dict__.iteritems():
    items.append('%s=%s' % (k,v))
print ', '.join(items),
print '}'

print
print 'Now _b_ has become an instance of _a_ because _b_ has the data from _a_.\n'

print

print 'Now I show the representation of _a_\n%s\n' % (_a_)

print 'Now I show the representation of _b_\n%s\n' % (_b_)

print 'Both representations are the same, right ?\n'

print 'This means I have successfully type-cast the instance of A() into an instance of B().\n'
