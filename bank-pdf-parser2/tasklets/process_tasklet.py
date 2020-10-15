#Tasklet

__copyright__ = """\
(c). Copyright 1990-2008, Vyper Logix Corp., 

              All Rights Reserved.

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
import os, sys, types, logging

from vyperlogix.misc import _utils
from vyperlogix.pyAMF.hooks import data_hook
from vyperlogix.pyAMF import hooks
from vyperlogix import oodb

from tasklet_lib import tasklet_utils

def dummy(args):
    pass

def echo(data):
    """
    __pyAMF__
    """
    dpath = _metadata['_data_path'][0]
    logging.info('%s.1 :: _data_path=%s' % (_utils.funcName(),str(dpath)))
    return str(dpath)

def selected(data):
    """
    __pyAMF__
    """
    logging.info('%s.1 :: data=%s' % (_utils.funcName(),data))
    dpath = _metadata['_data_path'][0]
    logging.info('%s.2 :: os.path.exists(dpath)=%s' % (_utils.funcName(),os.path.exists(dpath)))
    if (os.path.exists(dpath)):
        pass
        #fname = tasklet_utils.dbx_name('context',dpath)
        #logging.info('%s.3 :: fname=%s' % (_utils.funcName(),fname))
        #dbx = oodb.PickledFastCompressedHash2(fname)
        #logging.info('%s.4 :: dbx.fileName=%s' % (_utils.funcName(),dbx.fileName))
        #try:
            #dbx['home'] = None
            #dbx['home'] = data
        #except Exception, details:
            #data = str(details)
        #finally:
            #dbx.sync()
            #dbx.close()
    return str(data)

from vyperlogix.hash import lists

_metadata = lists.HashedLists()
_metadata['_functions'] = None

for f in dir():
    x = eval(f)
    if (type(x) == types.FunctionType):
        s = '' if (x.__doc__ is None) else x.__doc__
        if (s.find('__pyAMF__') > -1):
            _metadata['_functions'] = x
pass

_metadata['_tasklet_name'] = __name__
_metadata['_data_path'] = os.path.abspath('.')

hooks._metadata = _metadata

if (__name__ == '__main__'):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
