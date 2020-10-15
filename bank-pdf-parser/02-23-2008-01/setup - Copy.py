from distutils.core import setup
import os
import sys
_files = []
for root, dirs, files in os.walk('lib', topdown=True):
    if (root != '.svn'):
        for f in files:
            if (f.endswith('.py')):
                _files.append(os.sep.join([root,f]))
setup(name='hal-lib',
      version='1.0',
      py_modules=_files,
      )

