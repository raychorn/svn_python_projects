from distutils.core import setup
import py2exe
import myPy2exe
import os

if (1):
	setup(
		console=['setupProduct.py'],
		name='setupProduct',
		scripts=['lib%sthreadpool.py' % os.sep,'lib%sreadYML.py' % os.sep,'lib%s_pyodbc.py' % os.sep],
		options={"py2exe":{"optimize":2}},
		cmdclass = {'py2exe': myPy2exe.Py2exe}
	)
else:
	options = {
		"py2exe": {
			"optimize":2,
			"ignores": "profileit"
		}
	}

	setup(
		console=['setupProduct'],
		name='setupProduct',
		scripts=['lib%sthreadpool.py' % os.sep,'lib%sreadYML.py' % os.sep,'lib%s_pyodbc.py' % os.sep],
		options=options
	)
