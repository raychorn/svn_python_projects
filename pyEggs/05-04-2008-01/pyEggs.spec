import os, sys

useConsole = True
useFolder = False

def findFilesInModules(top,toc=[],filter='.py'):
	for root, dirs, files in os.walk(top, topdown=True):
		for name in files:
			if (name.endswith(filter)):
				toc.append(os.sep.join([root, name]))
		
print >>sys.stderr, 'HOMEPATH=(%s)' % HOMEPATH
toc = [os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'pyEggs.py']
findFilesInModules('Z:\python projects\@lib\lib',toc,'.py')
print 'toc=[%s]' % (toc)
a = Analysis(toc, pathex=['Z:\\python projects\\pyEggs'])
pyz = PYZ(a.pure)
if (not useFolder):
	exe = EXE( pyz,
		a.scripts,
		a.binaries,
		name='pyEggs.exe',
		debug=False,
		strip=False,
		upx=True,
		console=useConsole )
else:
	exe = EXE(pyz,
		a.scripts,
		exclude_binaries=1,
		name='build_pyEggs/pyEggs.exe',
		debug=False,
		strip=False,
		upx=True,
		console=useConsole )
	coll = COLLECT( exe,
		a.binaries,
		strip=False,
		upx=True,
		name='dist_pyEggs')
