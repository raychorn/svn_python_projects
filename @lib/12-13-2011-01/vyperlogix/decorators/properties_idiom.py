"""
Rather than defining your get/set/del methods at the class level, as is usually done, e.g.

class MyClass(object):
    def __init__(self):
        self._foo = "foo"

    def getfoo(self):
        return self._foo
    def setfoo(self, value):
        self._foo = value
    def delfoo(self):
        del self._foo
    foo = property(getfoo, setfoo, delfoo, "property foo's doc string")

I would like to suggest the following alternative idiom:
"""

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

class MyClass(object):
    def __init__(self):
        self._foo = "foo"
        self._bar = "bar"

    def foo():
        doc = "property foo's doc string"
        def fget(self):
            return self._foo
        def fset(self, value):
            self._foo = value
        def fdel(self):
            del self._foo
        return locals()
    foo = property(**foo())

    def bar():
        doc = "bar is readonly"
        def fget(self):
            return self._bar
        return locals()    
    bar = property(**bar())



