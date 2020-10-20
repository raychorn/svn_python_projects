from vyperlogix import misc
from vyperlogix.hash import lists

__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

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

def post_from_sqlalchemy(request):
    d = lists.HashedLists()
    for k,v in request.POST.iteritems():
	toks = k.split('-')
	_d_ = d
	for t in toks[0:-1]:
	    _d = _d_[t]
	    if (_d is None):
		_d = lists.HashedLists2()
		_d_[t] = _d
	    else:
		_d = _d[0] if (misc.isList(_d)) else _d
	    _d_ = _d
	_d_[toks[-1]] = v[0] if (misc.isList(v)) else v
    return d
