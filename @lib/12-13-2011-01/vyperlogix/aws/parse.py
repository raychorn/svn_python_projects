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

from vyperlogix import misc
from vyperlogix.misc import _utils

import math
from vyperlogix.classes.SmartObject import SmartFuzzyObject

def is_valid_file(fname):
    _isString_ =  misc.isString(fname)
    _fname_ =  os.path.abspath(fname) if (_isString_) else fname
    return  _fname_ if (_isString_ and os.path.exists(_fname_) and  os.path.isfile(_fname_)) else None

def _parseAws(data):
    __data__ = []
    try:
	_lines_ =  [l for l in data.split('\n') if (len(l) > 0)]
	_guide_ =  _lines_[0].split('+')
	_columns_ =  _lines_[1].split('|')
	_num_columns_ =  len(_columns_)
	if (len(_guide_) == _num_columns_):
	    _columns_ =  [c.strip() for c in _columns_]
	    _num_lines_ = len(_lines_)
	    _width_ = int(math.floor(math.log10(_num_lines_)))
	    _fmt_ = '#%' + ('0%d' % (_width_ + 1)) + 'd'
	    for lineNum in xrange(3, _num_lines_-1):
		aLine =  _lines_[lineNum]
		_aLine_ =  [c.strip() for c in aLine.split('|')]
		if (_num_columns_ == len(_aLine_)):
		    _tt_ = []
		    for i in xrange(0, len(_aLine_)):
			if (len(_columns_[i]) > 0):
			    _tt_.append(tuple([_columns_[i], _aLine_[i]]))
		    __data__.append(SmartFuzzyObject(args=dict(_tt_)))
		else:
		    print >> sys.stderr, 'WARNING: Looks like "%s" is not a valid aws ls file at line #%d.' % (__path__, lineNum)
    except:
	pass
    return __data__

def parseAws(__path__):
    __data__ = []
    if (os.path.exists(__path__)):
	if (os.path.isfile(__path__)):
	    __data__ = _parseAws(_utils.readFileFrom(__path__, noCRs=False))
	else:
	    print >> sys.stderr, 'WARNING: Looks like "%s" is not a file.' % (__path__)
    else:
	print >> sys.stderr, 'WARNING: Cannot determine the location of "%s".' % (__path__)
    return __data__

def _find_in_aws(data, target):
    __is_found__ = False
    __data__ =  _parseAws(data)
    for  item in  __data__:
	try:
	    if item.key.find(target) >  -1:
		__is_found__ = True
		break
	except:
	    pass
    return __is_found__

def find_in_aws(__path__, target):
    __is_found__ = False
    __data__ =  parseAws(__path__)
    for  item in  __data__:
	try:
	    if item.key.find(target) >  -1:
		__is_found__ = True
		break
	except:
	    pass
    return __is_found__
