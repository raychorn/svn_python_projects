import sys

useConsole = True
useFolder = False

print >>sys.stderr, 'HOMEPATH=(%s)' % HOMEPATH

a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'Z:\\python projects\\@lib\\lib\\Args.py', 'Z:\\python projects\\@lib\\lib\\PrettyPrint.py', 'Z:\\python projects\\@lib\\lib\\handlers\\ExceptionHandler.py', 'mySQLBackups.py'], pathex=['Z:\\python projects\\mySQLBackups'])
pyz = PYZ(a.pure)
if (not useFolder):
	exe = EXE( pyz,
		a.scripts,
		a.binaries,
		name='mySQLBackups.exe',
		debug=False,
		strip=False,
		upx=True,
		console=useConsole )
else:
	exe = EXE(pyz,
		a.scripts,
		exclude_binaries=1,
		name='build_mySQLBackups/mySQLBackups.exe',
		debug=False,
		strip=False,
		upx=True,
		console=useConsole )
	coll = COLLECT( exe,
		a.binaries,
		strip=False,
		upx=True,
		name='dist_mySQLBackups')
