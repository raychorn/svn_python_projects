# SalesForce Alchemy - provides an ORM-type interface for SalesForce via pyax and pyax_utils.

import os,sys
import zipfile
import __builtin__

from vyperlogix.crypto import Encryptors

from vyperlogix.classes.MagicObject import MagicObject2

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.classes.SmartObject import SmartObject2

from vyperlogix.classes.CooperativeClass import Cooperative

__copyright__ = """\
(c). Copyright 1990-2014, Vyper Logix Corp., All Rights Reserved.

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

class ZipImporterExtended(Cooperative):
    def __init__(self):
	pass

    def open_egg(self,fpath):
	files = []
	try:
	    _zip = zipfile.ZipFile(fpath,'r')
	    try:
		files = _zip.filelist
	    finally:
		_zip.close()
	except IOError:
	    pass
	return files
    
    def read_egg(self,fpath,fname):
	_zip = zipfile.ZipFile(fpath,'r')
	try:
	    bytes = _zip.read(fname)
	    try:
		sig = _zip.read('EGG-INFO/signature')
		if (str(Encryptors.Encryptors.simple.value) == sig):
		    source = Encryptors.decryptSimple(bytes)
		    return source
	    except:
		return bytes
	finally:
	    _zip.close()
	return None
    
    def find_egg_and_read(self,eggname,module={}):
	print '--> %s' % (eggname)
	files = self.open_egg(eggname)
	for k,modules in module['module'].iteritems():
	    for module in modules[0]:
		_name = module = '/'.join(module.split('.'))
		toks = [t for t in os.path.splitext(_name) if (len(t) > 0)]
		toks2 = misc.copy(toks)
		if (len(toks) == 1):
		    toks.append('__init__.py')
		_name = '/'.join(toks)
		toks2.append('.py')
		_name2 = '/'.join(toks2).replace('/.','.')
		_names = [_name,_name2]
		for f in files:
		    for _name in _names:
			if (f.filename.find(_name) > -1):
			    print 'Found "%s" in "%s".' % (_name,eggname),
			    source = self.read_egg(eggname,f.filename)
			    try:
				self.__module_name__ = f.filename
			    except:
				pass
			    print 'Source !'
			    return source.replace('\r\n','\n')
	return None
    
    def __import__(self,source,globals={},locals={}):
	if (source is not None):
	    name = ''
	    try:
		name = self.__module_name__
	    except:
		pass
	    try:
		self.__source__ = source
	    except:
		pass
	    code = __builtin__.compile(source,'from %s' % (name),'exec') # See PEP 302 for hints as to how code objects can be handled.
	    exec code in globals, locals
	else:
	    print 'WARNING: Cannot import "%s" from "%s".' % (name,fromlist)
    
class SecureEgg(MagicObject2,ZipImporterExtended):
    def __init__(self,egg=None,globals={},locals={}):
        self.__egg__ = egg
        self.__module__ = {}
        self.__module_name__ = ''
        self.__source__ = ''
        self.__globals__ = {}
        self.__locals__ = {}
        self.__reset_magic__()
	
    def module_names(self):
	name = []
	try:
	    if (self.__module__.has_key('module')):
		for k,modules in self.__module__['module'].iteritems():
		    for module in modules[0]:
			name.append(module)
	except:
	    pass
	return ','.join(name)
    
    def __str__(self):
	return '%s from %s' % (self.module_names(),self.__egg__)
        
    def __call__(self,*args,**kwargs):
        super(SecureEgg, self).__call__(*args,**kwargs)
        n = self.n.pop()
        a = list(args)
        a.append(kwargs)
        if (n == '_import_'):
            source = self.find_egg_and_read(self.__egg__,module=self.__module__)
	    if (kwargs.has_key('globals')):
		self.__globals__ = kwargs['globals']
	    if (kwargs.has_key('locals')):
		self.__locals__ = kwargs['locals']
	    self.__import__(source,globals=self.__globals__,locals=self.__locals__)
	    g = SmartObject2()
	    for k,v in self.__globals__.iteritems():
		g[k] = v
	    self.__globals__ = g
	    l = SmartObject2()
	    for k,v in self.__locals__.iteritems():
		l[k] = v
	    self.__locals__ = l
        elif (n == 'module'):
            _name = args[0]
	    self.__module__ = self.__magic__
        self.__reset_magic__()
        return self

if (__name__ == '__main__'):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
    
    eggname = r'Z:\python projects\pyEggs\@lib\eVyperLogixLib-1.0-py2.5.egg'
    e = SecureEgg(egg=eggname).module('e.misc')._import_(globals={},locals={})
    print str(e)

    try:
	e.module('e.misc._utils')._import_(globals={},locals={})
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
    print str(e)
 