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

import time

class datetime(object):
    def __init__(self, *argv):
        self.t = time.struct_time(argv+(0,)*(9-len(argv)))    # append to length 9 
    def __getattr__(self, name):
        try:
            i = ['year', 'month', 'day', 'hour', 'minute', 'second', 'weekday'].index(name)
            return self.t[i]
        except:
            return getattr(self.t, name)
    def __len__(self): return len(self.t)
    def __getitem__(self, key): return self.t[key]
    def __repr__(self): return repr(self.t)
    def now(self=None):
        return datetime(*time.localtime())
    now = staticmethod(now)
    def strftime(self, fmt="%Y-%m-%d %H:%M:%S"):
        return time.strftime(fmt, self.t)
