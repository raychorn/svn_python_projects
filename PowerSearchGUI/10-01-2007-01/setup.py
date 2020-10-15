from distutils.core import setup
import py2exe
import myPy2exe

import psyco
psyco.bind(setup)

if (0):
	setup(
		console=['main.py'],
		name='powerSearch',
		scripts=['lib\misc.py'],
		options={"py2exe":{"optimize":2}},
		cmdclass = {'py2exe': myPy2exe.Py2exe}
	)
else:
	setup(
		console=['main.py'],
		name='powerSearch',
		scripts=['lib\misc.py'],
		options={"py2exe":{"optimize":2}}
	)
