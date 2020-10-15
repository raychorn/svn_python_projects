import glob

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[ 
    Extension("coder",       ["coder.pyx"]),
]

setup(
  name = 'crypto',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
)
