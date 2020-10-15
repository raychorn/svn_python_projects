from distutils.core import setup
import os
import sys
import re
import compileall

def copyFile(src,dst):
    if (os.path.exists(src)):
        fIn = open(src,'rb')
        fOut = open(dst,'wb')
        _lines = fIn.readlines()
        fOut.writelines(_lines)
        fOut.flush()
        fOut.close()
        fIn.close()
    else:
        print 'ERROR :: Cannot find the file named "%s".' % src

_destFolder = 'c:/@1/@lib'
_files = []
_dirs = []
compileall.compile_dir('lib/', rx=re.compile('/[.]svn'), force=True)
for root, dirs, files in os.walk(_destFolder, topdown=False):
    for f in files:
        os.remove(os.sep.join([root,f]))
if (not os.path.exists(_destFolder)):
    os.mkdir(_destFolder)
for root, dirs, files in os.walk('lib', topdown=True):
    if (root.find('.svn') == -1):
        _dname = os.sep.join([_destFolder,root])
        _dirs.append(_dname)
        if (not os.path.exists(_dname)):
            os.mkdir(_dname)
        for f in files:
            if (f.endswith('.pyc')):
                _fnameIn = os.sep.join([root,f])
                _fnameOut = os.sep.join([_destFolder,_fnameIn])
                _files.append(_fnameOut)
                copyFile(_fnameIn,_fnameOut)
if (0):
    setup(name='sorting',
          version='1.0',
          description='Python Sorting Sample',
          author='Ray C. Horn',
          author_email='raychorn@hotmail.com',
          url='http://raychorn.phpnet.us/',
          py_modules=['sorting'],
          packages=_dirs,
          )

