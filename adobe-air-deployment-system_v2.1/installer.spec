_toc = []
if (os.path.exists('buildtime.txt')):
	_toc.append(('buildtime.txt', 'buildtime.txt', 'DATA'))
_root = 'air'
if (os.path.exists(_root)):
	files = os.listdir(_root)
	for f in files:
		t = (f,_root+os.sep+f,'DATA')
		_toc.append(t)
pkg1 = PKG(_toc, name='air.pkg', exclude_binaries=0)

useTk = True
useConsole = False

import os
import sys

_toc = []

_root = 'distserver'
if (os.path.exists(_root)):
	files = os.listdir(_root)
	for f in files:
		t = (f,_root+os.sep+f,'DATA')
		_toc.append(t)
else:
	t = ('server.exe','server.exe','DATA')
	_toc.append(t)

pkg2 = PKG(_toc, name='server.pkg', exclude_binaries=0)

print >>sys.stderr, 'HOMEPATH=(%s)' % HOMEPATH

if (not useTk):
	a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), 'installer.py'],pathex=['Z:\\python projects\\adobe-air-deployment-system'])
	pyz = PYZ(a.pure)
	exe = EXE( pyz, pkg1, pkg2,
		a.scripts,
		a.binaries,
		name='installer.exe',
		debug=False,
		strip=False,
		upx=True,
		console=useConsole )
else:
	a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\unpackTK.py'), os.path.join(HOMEPATH,'support\\useTK.py'), 'installer.py', os.path.join(HOMEPATH,'support\\removeTK.py')],
		pathex=['Z:\\python projects\\adobe-air-deployment-system'])
	pyz = PYZ(a.pure)
	exe = EXE(TkPKG(), pyz, pkg1, pkg2,
		a.scripts,
		a.binaries,
		name='installer.exe',
		debug=False,
		strip=False,
		upx=True,
		console=useConsole )
