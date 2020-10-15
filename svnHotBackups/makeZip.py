#!/usr/bin/env python
import zipfile
import os, sys
import re
from distutils import util

from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.misc import _utils

bool_skip_project_root = False

l_files_to_ignore = ListWrapper(['findfile.py','makeZip.py','setup_sftp.py','setup_svnHotBackups.py','test.py','zipper.py'])

l_folders_to_not_really_ignore = ListWrapper([''])

l_folders_to_ignore = ListWrapper(['@magma', 'data', 'sftp', 'svnHotBackups'])

l_entry_points = ListWrapper([])

l_data = ListWrapper([])

d_entry_folders = {}

for item in l_entry_points:
    d_entry_folders[os.path.dirname(item)] = item

_root = os.path.dirname(sys.argv[0])

_root_ = _root

ignore_folders = dict([(k,1) for k in list(l_folders_to_ignore.asSet())])

l_entry_folders = ListWrapper(d_entry_folders.keys())

_l_entry_folders = ListWrapper(l_entry_folders.copy())

l_files_to_ignore = ListWrapper(l_files_to_ignore.asSet())

l_folders_to_ignore = ListWrapper(ignore_folders.keys())

rx = re.compile('[.]svn')
rxLog = re.compile('log')
rxPop = re.compile('pop')
rxZip = re.compile('[.]zip')

_zipName_prefix = '%s' % (os.path.abspath('.').split(os.sep)[-1])
zipName = '%s.zip' % (_zipName_prefix)
zipName2 = '%s.egg' % (_zipName_prefix)

zipName = os.sep.join([_root_,zipName])
zipName2 = os.sep.join([_root_,zipName2])

def addFileToZip(top,_zip,filename,useNoPath=False):
    print 'ZIP Adding (%s) to (%s)' % (filename,_zip.filename)
    f_base = filename.replace('.pyo','.pyc').replace(top,'')
    _zip.write(filename,f_base if (not useNoPath) else os.path.basename(f_base))

try:
    zip = zipfile.ZipFile( zipName, 'w', zipfile.ZIP_DEFLATED)
    zip2 = zipfile.ZipFile( zipName2, 'w', zipfile.ZIP_DEFLATED)
    top = os.path.abspath(_root_)
    for root, dirs, files in os.walk(top):
        if (rx.search(root) == None) and (rxLog.search(root) == None) and (rxPop.search(root) == None) and (not any([root.find(l) > -1 for l in l_folders_to_ignore if (top.split(os.sep)[-1] != l)])):
            py_files = [os.sep.join([root,f]) for f in files if (f.endswith('.py')) and (l_files_to_ignore.find(f) == -1)]
	    print 'Compiling (%s) %s' % (root,py_files)
	    util.byte_compile(py_files,optimize=2,force=1)
	    compiled_file = lambda f:f.replace('.py','.pyo') if (os.path.exists(f.replace('.py','.pyo'))) else f
	    py_files = [compiled_file(f) for f in py_files]
            for f in py_files:
		addFileToZip(top,zip,f)
    for f in l_entry_points:
        top = os.sep.join([_root_,os.path.dirname(f)])
        for root, dirs, files in os.walk(top):
            if (rx.search(root) == None) and (rxLog.search(root) == None) and (rxPop.search(root) == None):
                py_files = [os.sep.join([root,f]) for f in files if (f.endswith('.py') and (l_entry_points.findFirstContaining(f) > -1))]
                print 'Compiling (%s) %s' % (root,py_files)
                util.byte_compile(py_files,optimize=2,force=1)
                _files = [f.replace('.py','.pyo') for f in py_files]
                for f in _files:
                    if (rxZip.search(f) == None):
                        addFileToZip(top,zip2,f)
    for f in l_data:
        top = os.sep.join([_root_,os.path.dirname(f)])
        _f = os.sep.join([_root_,f])
	addFileToZip(os.path.dirname(top),zip2,_f)
except Exception, details:
    print 'Error in ZIP processing. (%s)' % (str(details))
finally:
    try:
        zip.close()
        zip2.close()
    except Exception, details:
        pass
    finally:
	if (_utils.fileSize(zipName) == 0):
	    os.remove(zipName)
	if (_utils.fileSize(zipName2) == 0):
	    os.remove(zipName2)
