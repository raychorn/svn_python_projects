'''
Riddle me this:  When are tuples not tuples ?
'''
def inject(instance):
    '''
    Python method injection only if the method does not already exist.
    '''
    def decorator(f):
        import new
        f = new.instancemethod(f, instance, instance.__class__)
        try:
            value = getattr(instance, f.func_name)
        except AttributeError:
            setattr(instance, f.func_name, f)
        return f
    return decorator

# create a simple tuple
t = (1,2,3)
print type(t)
assert str(type(t)).find('tuple') > -1, 'Better be a tuple !!!'

# create a list...
l = [3,4,5]
print type(l)
assert str(type(l)).find('list') > -1, 'Better be a list !!!'

class MyList(list):
    pass

class MyTuple(tuple):
    def __setattr__(self, value):
        pass

    def __setitem__(self, index, value):
        __n__, val = value
        l = list(self)
        try:
            l[index] = val
        except TypeError:
            pass
        globals()[__n__] = MyTuple(tuple([2])) + self[1:]

    def __set__(self, value):
        pass

tt = MyTuple(t)
tt[0] = ('tt',2)
assert tt[0] == 2, 'Better be the value I expect !'

ttt = tuple(t)

def __setitem__(self, index, value):
    __n__, val = value
    l = list(self)
    l[index] = val
    globals()[__n__] = MyTuple(tuple([2])) + self[1:]

tttt = MyTuple(ttt)
tttt['__setitem___'] = ('tttt',__setitem__)

ttt = tuple(tttt)
ttt[0] = ('ttt',2)
assert ttt[0] == 2, 'Better be the value I expect !'
