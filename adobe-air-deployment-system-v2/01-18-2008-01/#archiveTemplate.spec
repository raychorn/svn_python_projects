import os
import sys
from lib import shelved

fname = 'archiveSpec.txt'
if (os.path.exists(fname)):
	exec open(fname, 'r').read()+'\n'

	print >>sys.stderr, 'buildPath=(%s)' % buildPath
	print >>sys.stderr, 'toc1=(%s)' % str(toc1)
	print >>sys.stderr, 'useConsole=(%s)' % useConsole
	print >>sys.stderr, 'useShelved=(%s)' % useShelved

	print >>sys.stderr, 'HOMEPATH=(%s)' % HOMEPATH

	if (useShelved):
		print >>sys.stderr, 'shelvedFname=(%s)' % shelvedFname
		
		persisted = shelved.persistence(shelvedFname)
		persisted.isUsingSpecificFileName = True
		pyz = persisted.unShelveThis('pyz')
		a_scripts = persisted.unShelveThis('a.scripts')
		a_binaries = persisted.unShelveThis('a.binaries')
	
	print >>sys.stderr, 'exeName=(%s)' % exeName
	exe = EXE( pyz, toc1,
					a_scripts,
					a_binaries,
					name=exeName,
					debug=False,
					strip=False,
					upx=False,
					console=useConsole )
