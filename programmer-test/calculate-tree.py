'''
#1
'''
__data__ = {
    'nodes': ['-', 1, 2, 3],
    'child': {
        'nodes':['+', 1, 2, 3],
        'child': {
            'nodes':['*', 1, 2, 3],
            'child': {
                'nodes':['/', 100, 2, 2],
                },
            },
        },
}

__value__ = None
_op_ = None

__add__ = lambda a, b:a + b
__subr__ = lambda a, b:a - b
__mult__ = lambda a, b:a * b
__div__ = lambda a, b:a / b

__operands__ = {
    '+': __add__,
    '-': __subr__,
    '*': __mult__,
    '/': __div__,
}

def calculate(root):
    global __value__, _op_
    _keys_ = __operands__.keys()
    for k, v in root.iteritems():
        if (k == 'nodes'):
            _op_ = None
            for op in v:
                if (op in _keys_):
                    _op_ = op
                elif (str(op).isdigit()):
                    if (__operands__.has_key(_op_)):
                        if (__value__ is None):
                            __value__ = op
                        else:
                            print '%s %s %s' % (__value__, _op_, op)
                            __value__ = __operands__[_op_](__value__, op)
                            print '= %s' % (__value__)
                    else:
                        print 'WARNING: Cannot perform the "%s" operation.' % (op)
        elif (k == 'child'):
            print '%s --> %s' % (_op_, __value__)
            __value__ = None
            calculate(v)

if (__name__ == '__main__'):
    __value__ = None
    calculate(__data__)
    print '%s --> %s' % (_op_, __value__)
