#!/usr/bin/env python
import zipfile
import os
import re
from distutils import util

ignore = ['lib01.pyc','lib01.pyo','makeZip.py','makeZip.pyc','makeZip.pyo','myeval.py','pythonProcess.pyc','pythonProcess.pyo','Ruby-Python-Bridge.kpf','rubypythonlib.py','_compile.py','_compile.pyc','_compile.pyo','myeval.pyc','rubypythonlib.pyc']

try:
    execdict = { }
    execfile( '_compile.py', globals(), execdict)
except Exception, details:
    print 'Error running compilation. (%s)' % (str(details))

rx = re.compile('[.]svn')
rxZip = re.compile('[.]zip')

zipName = 'Ruby-Python-Bridge_0_1_0.zip'

try:
    if os.path.exists(zipName):
        os.remove(zipName)
except Exception, details:
    print 'WARNING in removing the old ZIP due to (%s)' % (str(details))

try:
    zip = zipfile.ZipFile( zipName, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk('.'):
        if (rx.search(root) == None):
            util.byte_compile(files,optimize=2,force=1)
            for f in ignore:
                try:
                    files.remove(f)
                except Exception, details:
                    print 'WARNING in ignoring files due to (%s)' % (str(details))
            for f in files:
                if (rxZip.search(f) == None):
                    print 'ZIP Adding (%s) to (%s)' % (f,zipName)
                    zip.write(f,f.replace('.pyo','.pyc'))
except Exception, details:
    print 'Error in ZIP processing. (%s)' % (str(details))
finally:
    try:
        zip.close()
    except Exception, details:
        pass