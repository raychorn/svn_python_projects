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

def dummy(args):
    pass

const_shutdown_command = '___SHUTDOWN___'

_callback = dummy

def shutdown(data):
    """
    __pyAMF__
    """
    logging.info('%s.1 :: %s' % (_utils.funcName(),data))
    if (data == const_shutdown_command):
        logging.info('%s.2 :: %s' % (_utils.funcName(),data))
        logging.info('%s.3 :: type(_callback)=%s' % (_utils.funcName(),type(_callback)))
        if (type(_callback) == types.FunctionType):
            try:
                logging.info('%s.4 :: Issuing callback !' % (_utils.funcName()))
                _callback(data)
            except:
                exc_info = sys.exc_info()
                info_string = '\n'.join(traceback.format_exception(*exc_info))
                logging.error(info_string)
    return data

def echo(data):
    """
    __pyAMF__
    """
    logging.info('%s.1 :: %s' % (_utils.funcName(),data))
    return const_shutdown_command

def callback_hook(callback_func):
    global _callback
    logging.info('%s.1 :: %s' % (_utils.funcName(),type(callback_func)))
    if (type(callback_func) == types.FunctionType):
        logging.info('%s.2 :: %s' % (_utils.funcName(),type(callback_func)))
        _callback = callback_func

from vyperlogix.hash import lists
from vyperlogix.pyAMF.hooks import data_hook
from vyperlogix.pyAMF import hooks

_metadata = lists.HashedLists()

_metadata['_tasklet_name'] = __name__
_metadata['callback_hook'] = callback_hook
_metadata['shutdown_command'] = const_shutdown_command
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

if (__name__ == '__main__'):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
