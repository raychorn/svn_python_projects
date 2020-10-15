import glob

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[ 
Extension("str_replace2a", ["str_replace2a.pyx"]),
]

setup(
  name = 'str_replace2a',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
)
