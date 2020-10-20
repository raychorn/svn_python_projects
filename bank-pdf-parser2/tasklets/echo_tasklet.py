#Tasklet

__copyright__ = """\
(c). Copyright 1990-2020, Vyper Logix Corp., 

              All Rights Reserved.

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
import os, sys, types, logging

from vyperlogix.misc import _utils

def dummy(args):
  pass

def echo(data):
    """
    __pyAMF__
    """
    return data

from vyperlogix.hash import lists
from vyperlogix.pyAMF.hooks import data_hook
from vyperlogix.pyAMF import hooks

_metadata = lists.HashedLists()

_metadata['_tasklet_name'] = __name__
_metadata['_data_path'] = os.path.abspath('.')

_metadata['_functions'] = None

for f in dir():
    x = eval(f)
    if (type(x) == types.FunctionType):
        s = '' if (x.__doc__ is None) else x.__doc__
        if (s.find('__pyAMF__') > -1):
            _metadata['_functions'] = x
pass

hooks._metadata = _metadata

# BEGIN: METADATA
#import types
#for f in [k for k,v in vv.items() if (v) and (type(v) == types.FunctionType) and (v.__doc__.find('__pyAMF__') > -1)]:
  #_tasklet_name = v.__name__
  #_functions.append(v)
# END! METADATA

if (__name__ == '__main__'):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
    