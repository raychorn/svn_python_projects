from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName
from vyperlogix.hash import lists

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

class memoized(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """
    def __init__(self, func):
        self.func = func
        self.cache = lists.HashedLists2()
        self.objType = ObjectTypeName.typeName(self)
        
    def __call__(self, *args):
        _name = misc.callersName()
        _l = ['_'.join(str(c).split()) for c in args if ObjectTypeName.typeName(c).find('.') == -1]
        _key = '_'.join(_l)
        if (self.cache[_name] == None):
            self.cache[_name] = {}
        try:
            return self.cache[_name][_key]
        except KeyError:
            self.cache[_name][_key] = value = self.func(*args)
            return value
        except TypeError, e:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)
        
    def __repr__(self):
        """Return the function's docstring."""
        return '(%s.%s) :: %s' % (self.objType,misc.funcName(),self.func.__doc__)
