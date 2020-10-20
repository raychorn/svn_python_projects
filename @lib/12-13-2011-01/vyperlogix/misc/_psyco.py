from os import environ
from vyperlogix.misc import _utils
from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName

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

def importPsycoIfPossible(func=None,isVerbose=False):
    '''func can be a function or a list of functions'''
    import sys
    import types
    import platform
    if (not _utils.isBeingDebugged):
        try:
            _bits = -1
            _isMachineBits32 = False
            _bits = ''.join([[ch for ch in t if (ch.isdigit())] for t in list(platform.architecture()) if (t.find('bit') > -1)][0])
            if (len(_bits) > 0):
                _bits = int(_bits)
                _isMachineBits32 = (_bits == 32)
            if (sys.platform == 'win32'):
                import psyco
            elif (_isMachineBits32):
                import psyco_linux
            else:
                print '%s :: psyco cannot be imported because target machine has %s bits and is not a Windows box !' % (misc.funcName(),_bits)
                return
            if (isVerbose):
                print '%s :: psyco has been imported !' % (misc.funcName())
            if (func):
                if (misc.isList(func)):
                    for f in func:
                        if (callable(f)):
                            psyco.bind(f)
                        else:
                            _utils.print_stderrout('%s :: Cannot bind psyco to "%s" because the bind target is not a function or a list of functions !' % (misc.funcName(),str(f)))
                elif (callable(func)):
                    psyco.bind(func)
                else:
                    _utils.print_stderrout('%s :: Cannot bind psyco to "%s" because the bind target is not a function or a list of functions !' % (misc.funcName(),str(func)))
            else:
                psyco.full()
        except Exception, details:
            if (isVerbose):
                print '%s :: psyco has not been imported because "%s" !' % (misc.funcName(),str(details))
    else:
        if (isVerbose):
            print '%s :: psyco has not been imported because Wing IDE is Active and psyco does not run with Wing !' % (misc.funcName())
