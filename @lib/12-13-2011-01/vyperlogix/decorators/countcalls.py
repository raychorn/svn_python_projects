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

class countcalls(object):
    "Decorator that keeps track of the number of times a function is called."
    
    __instances = {}
    
    def __init__(self, f):
        self.__f = f
        self.__numCalls = 0
        countcalls.__instances[f] = self
    
    def __call__(self, *args, **kwargs):
        self.__numCalls += 1
        return self.__f(*args, **kwargs)
    
    @staticmethod
    def count(f):
        "Return the number of times the function f was called."
        return countcalls.__instances[f].__numCalls
    
    @staticmethod
    def counts():
        "Return a dict of {function: # of calls} for all registered functions."
        return dict([(f, countcalls.count(f)) for f in countcalls.__instances])
