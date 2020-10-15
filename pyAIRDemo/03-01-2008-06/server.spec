useTk = False
useConsole = True

import os
import sys

print >>sys.stderr, 'HOMEPATH=(%s)' % HOMEPATH

if (not useTk):
	a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), 'XMLSocketServer2.py'],pathex=['Z:\\python projects\\pyAIRDemo'])
	pyz = PYZ(a.pure)
	exe = EXE( pyz,
		a.scripts,
		a.binaries,
		name='pyAIRDemoServer.exe',
		debug=False,
		strip=False,
		upx=True,
		console=useConsole )
else:
	a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\unpackTK.py'), os.path.join(HOMEPATH,'support\\useTK.py'), 'zipBackups.py', os.path.join(HOMEPATH,'support\\removeTK.py')],
		pathex=['Z:\\python projects\\pyAIRDemo'])
	pyz = PYZ(a.pure)
	exe = EXE(TkPKG(), pyz,
		a.scripts,
		a.binaries,
		name='pyAIRDemoServer.exe',
		debug=False,
		strip=False,
		upx=True,
		console=useConsole )
