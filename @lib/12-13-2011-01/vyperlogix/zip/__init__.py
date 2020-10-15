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
from vyperlogix.enum import Enum

class EntityType(Enum.Enum):
    none = 0
    folder = 2^0
    file = 2^1

def getZipFilesAnalysis(_zip,prefix='',_acceptable_types=[]):
    import os
    from vyperlogix.misc import ObjectTypeName
    from vyperlogix.hash import lists

    _analysis = lists.HashedLists()
    try:
	iterable = None
	if (ObjectTypeName.typeClassName(_zip) == 'zipfile.ZipFile'):
	    iterable = (f.filename for f in _zip.filelist)
	elif (lists.isDict(_zip)):
	    iterable = (f for f in _zip.keys())
	for f in iterable:
	    toks = os.path.splitext(f)
	    if (len(_acceptable_types) == 0) or (toks[-1].split('.')[-1] in _acceptable_types) or ( (len(prefix) > 0) and (toks[0].startswith(prefix)) ):
		_analysis[toks[0]] = toks[-1] if (len(toks) > 1) else ''
    except:
	pass
    return _analysis

def getZipFilesAnalysis2(_zip):
    import os
    from vyperlogix.misc import ObjectTypeName
    from vyperlogix.hash import lists

    _analysis = lists.HashedLists2()
    try:
	iterable = None
	if (ObjectTypeName.typeClassName(_zip) == 'zipfile.ZipFile'):
	    iterable = (f.filename for f in _zip.filelist)
	elif (lists.isDict(_zip)):
	    iterable = (f for f in _zip.keys())
	for f in iterable:
	    _analysis[f] = f
    except:
	pass
    return _analysis

def unZipInto(_zip,target,isVerbose=False,callback=None):
    import os
    from vyperlogix.misc import ObjectTypeName
    from vyperlogix.hash import lists
    from vyperlogix.misc import _utils

    try:
	iterable = None
	typ = ObjectTypeName.typeClassName(_zip)
	if (typ == 'zipfile.ZipFile'):
	    iterable = (f.filename for f in _zip.filelist)
	else:
	    raise AttributeError('Invalid _zip attribute cann be of type "%s".' % (typ))
	if (isVerbose):
	    print '*** iterable = %s' % (str(iterable))
	if (iterable):
	    for f in iterable:
		_f_ = f.replace('/',os.sep)
		fname = os.path.join(target,_f_)
		if (f.endswith('/')):
		    if (not os.path.exists(fname)):
			os.makedirs(fname)
		    if (callable(callback)):
			try:
			    callback(EntityType.folder,f)
			except:
			    pass
		else:
		    __bytes__ = _zip.read(f)
		    if (isVerbose):
			print '%s -> %s [%s]' % (f,fname,__bytes__)
		    _utils.writeFileFrom(fname,__bytes__,mode='wb')
		    if (callable(callback)):
			try:
			    callback(EntityType.file,f,fname)
			except:
			    pass
    except Exception, _details:
	if (isVerbose):
	    print _utils.formattedException(details=_details)
