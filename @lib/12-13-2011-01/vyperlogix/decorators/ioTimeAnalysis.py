import functools

from vyperlogix.misc import ioTimeAnalysis

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

def analyze(reason):
    '''
    Usage:

    @analyze(reason)
    def method(item):
        print item
    '''
    def decorator(func):
        def proxy(*args, **kwargs):
            ioTimeAnalysis.initIOTime(reason)
            ioTimeAnalysis.ioBeginTime(reason)
            val = None
            try:
                val = func(*args,**kwargs)
            except Exception, ex:
                ioTimeAnalysis.ioEndTime(reason)
                raise ex
            ioTimeAnalysis.ioEndTime(reason)
            return val
        return proxy
    return decorator

def Analyze(reason):
    class _Analyze(object):
        def __init__(self, fn):
            self.fn = fn

        def __get__(self, obj, type=None):
            return functools.partial(self, obj)

        def __call__(self, *args, **kwargs):
            ioTimeAnalysis.initIOTime(reason)
            ioTimeAnalysis.ioBeginTime(reason)
            val = None
            try:
                val = self.fn(*args, **kwargs)
            except Exception, ex:
                ioTimeAnalysis.ioEndTime(reason)
                raise ex
            ioTimeAnalysis.ioEndTime(reason)
            return val

    return _Analyze
