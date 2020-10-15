import sys

useConsole = True
useFolder = False

print >>sys.stderr, 'HOMEPATH=(%s)' % HOMEPATH

a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), 'XMLSocketServer2.py'], pathex=['Z:\\python projects\\adobe-air-deployment-system'])
pyz = PYZ(a.pure)
if (not useFolder):
	exe = EXE( pyz,
		a.scripts,
		a.binaries,
		name='server2.exe',
		debug=False,
		strip=False,
		upx=True,
		console=useConsole )
else:
	exe = EXE(pyz,
		a.scripts,
		exclude_binaries=1,
		name='buildserver2/server2.exe',
		debug=False,
		strip=False,
		upx=True,
		console=useConsole )
	coll = COLLECT( exe,
		a.binaries,
		strip=False,
		upx=True,
		name='distserver2')
