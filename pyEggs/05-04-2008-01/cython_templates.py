template1 = """
import glob

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[ 
"""

template2 = """
Extension("%s",       ["%s"]),
"""

template3 = """
]

setup(
  name = '%s',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
)
"""

cmd_template = """
@echo off

set PYTHONPATH=%s
python Setup.py build_ext --inplace -c mingw32
"""
