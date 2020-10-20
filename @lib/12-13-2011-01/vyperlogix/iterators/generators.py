from __future__ import print_function

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
def dot_product_generator(*args):
    var_names = [chr(i+ord('a')) for i in xrange(0,len(args))]
    s_varnames = ','.join(var_names)
    pairs = []
    ii = 0
    for v in var_names:
        pairs.append('for %s in %s' % (v, args[ii]))
        ii += 1
    source = '((%s) %s)' % (s_varnames, ' '.join(pairs))
    return eval(source)    


if (__name__ == '__main__'):
    import itertools

    a = [1,2,3]
    b = ['A', 'B', 'C']
    c = ['a', 'b', 'c']

    __ab__ = [a,b,c]
    __dot__ = itertools.product(*__ab__)
    list_ab = list(__dot__)
    print('BEGIN: list_ab')
    for item in list_ab:
        print(item)
    print('END!!! list_ab')
    
    print('-'*30)
    
    __ab__ = dot_product_generator(a, b, c)
    
    list_ab2 = [ab for ab in __ab__]
    
    print('BEGIN: list_ab2')
    for item in list_ab2:
        print(item)
    print('END!!! list_ab2')
    
    print('-'*30)
    
    s = set(list_ab) - set(list_ab2)
    assert len(s) == 0, 'WARNING, they not equal !!!!'

