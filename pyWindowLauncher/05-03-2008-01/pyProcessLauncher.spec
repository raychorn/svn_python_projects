import sys

useConsole = True
useFolder = False

print >>sys.stderr, 'HOMEPATH=(%s)' % HOMEPATH

a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'Z:\\python projects\\@lib\\_utils.py', 'Z:\\python projects\\@lib\\Args.py', 'Z:\\python projects\\@lib\\PrettyPrint.py', 'pyProcessLauncher.py'], pathex=['Z:\\python projects\\pyWindowLauncher'])
pyz = PYZ(a.pure)
if (not useFolder):
	exe = EXE( pyz,
		a.scripts,
		a.binaries,
		name='pyProcessLauncher.exe',
		debug=False,
		strip=False,
		upx=True,
		console=useConsole )
else:
	exe = EXE(pyz,
		a.scripts,
		exclude_binaries=1,
		name='build_pyProcessLauncher/pyProcessLauncher.exe',
		debug=False,
		strip=False,
		upx=True,
		console=useConsole )
	coll = COLLECT( exe,
		a.binaries,
		strip=False,
		upx=True,
		name='dist_pyProcessLauncher')
