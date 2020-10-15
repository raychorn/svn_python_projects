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

import os, sys
import traceback

from vyperlogix import misc
from vyperlogix.misc import ioTimeAnalysis

import types

def dummy():
    pass

def init_AnalysisDataPoint(name):
    ioTimeAnalysis.initIOTime(name)

def begin_AnalysisDataPoint(name):
    ioTimeAnalysis.ioBeginTime(name)

def end_AnalysisDataPoint(name):
    ioTimeAnalysis.ioEndTime(name)
    
def runWithAnalysis(func=dummy,args=[],_ioElapsedTime=dummy,num_iters=None):
    caller = misc.callersName()
    ioTimeAnalysis.initIOTime('%s::%s' % (__name__,caller)) 
    ioTimeAnalysis.ioBeginTime('%s::%s' % (__name__,caller))
    val = None
    try:
        if (len(args) == 0):
            val = func()
        else:
            val = func(args)
    except:
        exc_info = sys.exc_info()
        info_string = '\n'.join(traceback.format_exception(*exc_info))
        print >>sys.stderr, '(%s) Reason: %s' % (misc.funcName(),info_string)
    ioTimeAnalysis.ioEndTime('%s::%s' % (__name__,caller))
    ioTimeAnalysis.ioTimeAnalysisReport()

    _et = 0
    _key_list = [k for k in ioTimeAnalysis._ioTime.keys()]
    for _key in _key_list:
        _et += (0 if (len(_key) == 0) else ioTimeAnalysis._ioTime[_key][0])
    if (_et > 0) and (num_iters is not None):
        _per_sec = num_iters / _et
        if (_per_sec > 0):
            _ms_per_soql = 1000 / _per_sec
    else:
        print >>sys.stderr, '(%s) 1.0 Cannot correctly report ms per iteration because there is no reported elapsed time from activities.' % (misc.funcName())

    return val
