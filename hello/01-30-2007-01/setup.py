from distutils.core import setup
import py2exe
import myPy2exe

import psyco
psyco.bind(setup)

setup(console=['hello.py'],cmdclass = {'py2exe': myPy2exe.Py2exe})
