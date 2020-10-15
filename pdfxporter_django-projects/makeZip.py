#!/usr/bin/env python
import zipfile
import os, sys
import re
from distutils import util

from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.misc import _utils

_root = os.path.dirname(sys.argv[0])
if (not os.path.exists(_root)):
    _root = os.path.abspath(os.curdir)

print '_root is "%s".' % (_root)

_root_ = _root

rx = re.compile('[.]svn')
rxLog = re.compile('log')
rxPop = re.compile('pop')
rxZip = re.compile('[.]zip')

skip_list = ['django-trunk','sample-site-with-templates']

def addFileToZip(top,_zip,filename,useNoPath=False):
    print 'ZIP Adding (%s) to (%s)' % (filename,_zip.filename)
    f_base = filename.replace('.pyo','.pyc').replace(top,'')
    _zip.write(filename,f_base if (not useNoPath) else os.path.basename(f_base))

dnames = [f for f in os.listdir(_root_) if (os.path.isdir(os.sep.join([_root_,f]))) and (f not in skip_list) ]
for dname in dnames:
    _zipName_prefix = '%s' % (dname)
    zipName = '%s.zip' % (_zipName_prefix)
    
    zipName = os.sep.join([_root_,zipName])
    if (os.path.exists(zipName)):
	os.remove(zipName)
    try:
	zp = zipfile.ZipFile( zipName, 'w', zipfile.ZIP_DEFLATED)
	top = os.path.abspath(dname)
	for root, dirs, files in os.walk(top):
	    if (rx.search(root) == None):
		py_files = [os.sep.join([root,f]) for f in files if (f.endswith('.py'))]
		print 'Compiling (%s) %s' % (root,py_files)
		util.byte_compile(py_files,optimize=2,force=1)
		compiled_file = lambda f:f.replace('.py','.pyo') if (os.path.exists(f.replace('.py','.pyo'))) else f
		py_files = [(f,compiled_file(f)) for f in py_files]
		d = dict(py_files)
		set_files = set(d.keys())
		for f,p in py_files:
		    addFileToZip(top,zp,p)
		s = set([f for f in files if (not f.endswith('.py')) and (not f.endswith('.pyc')) and (not f.endswith('.pyo')) and (not f.endswith('.cmd')) and (not f.endswith('.wpr')) and (f != 'Django-Commands.txt') ]) - set_files
		for f in list(s):
		    addFileToZip(top,zp,os.sep.join([root,f]))
    except Exception, details:
	print 'Error in ZIP processing. (%s)' % (str(details))
    finally:
	try:
	    zp.close()
	except Exception, details:
	    pass
print 'Done !'