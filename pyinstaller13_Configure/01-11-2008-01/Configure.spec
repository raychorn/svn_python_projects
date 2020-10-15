import sys

useConsole = True

print >>sys.stderr, 'HOMEPATH=(%s)' % HOMEPATH

a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), 'Configure.py'], pathex=['Z:\\python projects\\pyinstaller13_Configure'])
pyz = PYZ(a.pure)
exe = EXE( pyz,
	a.scripts,
	a.binaries,
	name='Configure.exe',
	debug=False,
	strip=False,
	upx=True,
	console=useConsole )
