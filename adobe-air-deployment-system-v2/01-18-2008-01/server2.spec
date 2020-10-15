import os
import sys
from lib import shelved

buildPath = 'Z:\\python projects\\adobe-air-deployment-system'

toc1 = [('foo1.PKG', '@archive\\134\\foo1.PKG', 'DATA')]

useConsole = True
useFolder = False
useShelved = True

shelvedFname = 'archive-template.dat'

exeName = 'server2.exe'

print >>sys.stderr, 'buildPath=(%s)' % buildPath
print >>sys.stderr, 'toc1=(%s)' % str(toc1)
print >>sys.stderr, 'useConsole=(%s)' % useConsole
print >>sys.stderr, 'useFolder=(%s)' % useFolder
print >>sys.stderr, 'useShelved=(%s)' % useShelved

print >>sys.stderr, 'HOMEPATH=(%s)' % HOMEPATH

if (useShelved):
	print >>sys.stderr, 'shelvedFname=(%s)' % shelvedFname
	
	persisted = shelved.persistence(shelvedFname)
	persisted.isUsingSpecificFileName = True
	pyz = persisted.unShelveThis('pyz')
	a_scripts = persisted.unShelveThis('a.scripts')
	a_binaries = persisted.unShelveThis('a.binaries')
else:
	a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), 'XMLSocketServer2.py'], pathex=[buildPath])
	pyz = PYZ(a.pure)
	a_scripts = a.scripts
	a_binaries = a.binaries
	persisted.shelveThis('pyz',pyz)
	persisted.shelveThis('a.scripts',a_scripts)
	persisted.shelveThis('a.binaries',a_binaries)

print >>sys.stderr, 'exeName=(%s)' % exeName
if (not useFolder):
	exe = EXE( pyz, toc1,
		a_scripts,
		a_binaries,
		name=exeName,
		debug=False,
		strip=False,
		upx=False,
		console=useConsole )
else:
	exe = EXE(pyz,
		a_scripts,
		exclude_binaries=1,
		name='buildserver2/' + exeName,
		debug=False,
		strip=False,
		upx=True,
		console=useConsole )
	coll = COLLECT( exe,
		a_binaries,
		strip=False,
		upx=True,
		name='distserver2')
