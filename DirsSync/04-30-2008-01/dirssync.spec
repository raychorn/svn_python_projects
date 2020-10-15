useTk = False
useConsole = False

import os
import sys

print >>sys.stderr, 'HOMEPATH=(%s)' % HOMEPATH

if (not useTk):
	a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), 'dirssync.py'],pathex=['Z:\\python projects\\dirssync'])
	pyz = PYZ(a.pure)
	exe = EXE( pyz,
		a.scripts,
		a.binaries,
		name='dirssync.exe',
		debug=False,
		strip=False,
		upx=True,
		console=useConsole )
else:
	a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\unpackTK.py'), os.path.join(HOMEPATH,'support\\useTK.py'), 'dirssync.py', os.path.join(HOMEPATH,'support\\removeTK.py')],
		pathex=['Z:\\python projects\\dirssync'])
	pyz = PYZ(a.pure)
	exe = EXE(TkPKG(), pyz,
		a.scripts,
		a.binaries,
		name='dirssync.exe',
		debug=False,
		strip=False,
		upx=True,
		console=useConsole )
