import time
import sys

__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., All Rights Reserved.

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

_ioTime = {}
_ioElapsedTime = 0

def initIOTime(reason):
    global _ioTime
    if (_ioTime.has_key(reason) == False):
        _ioTime[reason] = [0.0]

def ioBeginTime(reason):
    global _ioTime
    initIOTime(reason)
    _ioTime[reason].append(time.time())

def ioEndTime(reason):
    global _ioTime
    initIOTime(reason)
    d = _ioTime[reason]
    d.append(time.time())
    diff = d.pop() - d.pop()
    d[0] += diff
    _ioTime[reason] = d

def ioElapsedTime():
    return _ioElapsedTime

def ioTimeAnalysis(iters=None):
    global _ioTime
    global _ioElapsedTime

    _ioElapsedTime = 0
    for k in _ioTime.keys():
        d = _ioTime[k]
        _tpi = ''
        if ( (iters) and (isinstance(iters,int)) ):
            _tpi = ' time/iters=(%2.10f)' % (d[0]/iters)
        try:
            print '(ioTimeAnalysis) :: "%s" --> (%s secs)%s' % (k,d[0],_tpi)
        except Exception, details:
            from vyperlogix import misc
            info_string = misc.formattedException(details=details)
            print >>sys.stderr, info_string
        _ioElapsedTime += d[0]
    return _ioElapsedTime

def ioTimeAnalysisReport(iters=None,fOut=None):
    ioAnalysis = ioTimeAnalysis(iters)
    _msg = "\n\nTime spent doing I/O :: (%s secs)" % (str(ioAnalysis))
    print >>fOut, _msg
    return _msg

