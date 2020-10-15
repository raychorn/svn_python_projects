from vyperlogix.classes.CooperativeClass import Cooperative

import traceback
import zipfile

import __builtin__
import os,sys

from vyperlogix.crypto import Encryptors

from vyperlogix import misc
from vyperlogix.misc import _utils

class ZipImporterExtended(Cooperative):
    def __init__(self):
	sys.path_hooks.append(self.importHook)
	sys.path_importer_cache.clear()

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
    
    def find_egg_and_read(self,name,fromlist=[]):
	fr = fromlist[0] if (len(fromlist) > 0) else ''
	fname = os.path.basename(name)
	if (not fname.startswith('e')):
	    return None
	print '--> %s' % (name)
	toks = name.split(os.sep)
	r_toks = misc.reverseCopy(toks)
	r_path = ''
	for tok in r_toks:
	    r_path += '/' + tok
	    print '(?)--> %s' % (r_path)
	    for p in sys.path:
		files = self.open_egg(p)
		_name = r_path
		for f in files:
		    if (f.filename.find(_name) > -1):
			print 'Found "%s" in "%s".' % (_name,p),
			has_all = all([any([(_f.filename.find(fr) > -1) for _f in files if (_f.filename.find(fr) > -1)]) for fr in fromlist[1:]])
			print 'has_all=%s' % (has_all),
			if (has_all):
			    source = self.read_egg(p,f.filename)
			    print 'Source !'
			    return source
			else:
			    print 'No Source (1)'
	return None
    
    def importHook(self, name, globals={}, locals={}, fromlist=[]):
        globals = {} if (globals is None) else globals
        locals = {} if (locals is None) else locals
        fromlist = [] if (fromlist is None) else fromlist
        print 'Importing "%s" fromlist=%s.' % (name,fromlist)
	source = self.find_egg_and_read(name,fromlist)
	if (source is not None):
	    code = __builtin__.compile(source.replace('\r\n','\n'),'from %s in %s' % (name,','.join(fromlist)),'exec') # See PEP 302 for hints as to how code objects can be handled.
	    exec code in globals, locals
	else:
	    print 'WARNING: Cannot import "%s" from "%s".' % (name,fromlist)
    
if (__name__ == '__main__'):
    sys.path.insert(0,"Z:\python projects\pyEggs\@lib\VyperLogixLib-1.0-py2.5.egg")
    sys.path.append("Z:\python projects\pyEggs\@lib\eVyperLogixLib-1.0-py2.5.egg")
    print '\n'.join(sys.path)
    i = ZipImporterExtended()
    try:
        from vyperlogix.misc import ObjectTypeName
        print '(+)-->%s' % (ObjectTypeName.typeName(i))
    except Exception, _details:
        info_string = _utils.formattedException(details=_details)
        print >>sys.stderr, info_string
    try:
        import e.misc
        #print '(+)-->%s' % (ObjectTypeName.typeName(i))
    except Exception, _details:
        info_string = _utils.formattedException(details=_details)
        print >>sys.stderr, info_string
    pass
