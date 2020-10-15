class Dict(dict):
    '''
    This method requires no changes to any existing code that attempts to access what could be a missing key from a Python dict instance.
    
    Typically, Python will throw an exception whenever an attempt is made to access a missing key from a standard Python dict instance.
    
    To avoid this one can either use the get() method, as shown below, to provide defaults for each dict() access however doing this
    requires more code changes.
    '''
    def __init__(self, *args, **kwargs):
        self.__default__ = kwargs.get('default','')
        super(Dict, self).__init__(*args)
    
    def __getitem__(self, key):
        return super(Dict, self).__getitem__(key) if (super(Dict, self).has_key(key)) else self.default

    def __setitem__(self, key, value):
        if (super(Dict, self).has_key(key)):
            super(Dict, self).__delitem__(key)
        super(Dict, self).__setitem__(key,value)

    def default():
        doc = "Property idiom"
        def fget(self):
            return self.__default__
        def fset(self, value):
            self.__default__ = value
        return locals()
    default = property(**default())

if (__name__ == '__main__'):
    d1 = Dict()
    print 'Test missing key... if this works you will not see any exceptions.'
    assert d1[1] == '', 'Oops, something went wrong.'
    
    print 'Test existing key... if this work you will not see any exceptions.'
    d1[1] = 'a'
    assert d1[1] == 'a', 'Oops, something went wrong.'
    
    d2 = dict([(n,n) for n in xrange(0,10)])
    print 'Test dict recast to Dict(), if this work you will not see any exceptions.'
    assert d2[1] == 1, 'Oops, something went wrong.'

    _d2 = Dict(d2)
    assert _d2[1] == 1, 'Oops, something went wrong.'
    assert _d2[111] == '', 'Oops, something went wrong.'

    print 'Now lets look at the other method for handling missing keys.'
    try:
        assert d2[111] == '', 'As expected, this causes a problem.'
    except KeyError:
        print 'Yes, this caused an exception because the key was missing.'
    
    print 'Now lets look at the coding pattern that provides a default, this this work you will see no exception.'
    try:
        assert d2.get(111,'') == '', 'This will not cause an exception.'
    except KeyError:
        print 'No exception was noticed because a default was provided.'

    d1 = Dict(default='aa')
    print 'Test missing key with custom default rather than the provided default... if this works you will not see any exceptions.'
    assert d1[1] == 'aa', 'Oops, something went wrong.'
        
    _d2 = Dict(d2,default='bb')
    print 'Test missing key with custom default rather than the provided default for dict instance recast... if this works you will not see any exceptions.'
    assert _d2[1] == 1, 'Oops, something went wrong.'
    assert _d2[111] == 'bb', 'Oops, something went wrong.'

    print 'Test missing key with custom default that changes after dict() as been recast rather than the default behavior... if this works you will not see any exceptions.'
    _d2.default = 'ccc'
    assert _d2[111] == 'ccc', 'Oops, something went wrong.'
