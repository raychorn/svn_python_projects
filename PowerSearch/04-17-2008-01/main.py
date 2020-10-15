import sys
from vyperlogix import misc
import os
from os import path
import re
import psyco

_dirName = ''
_isVerbose = False

def powerSearchFor(dname, fname):
	print 'powerSearchFor(%s) at: [%s]' % (fname,dname)
	for dirpath, dirnames, filenames in os.walk(dname):
		if (_isVerbose):
			print 'dirpath=(%s)' % (dirpath)
		#print 'misc.containsWildcard(%s)=(%s)' % (fname,misc.containsWildcard(fname))
		if (misc.containsWildcard(fname)):
			#print 'misc.isSimpleWildcard(%s)=(%s)' % (fname,misc.isSimpleWildcard(fname))
			if (misc.isSimpleWildcard(fname)):
				r = misc.regularExpressionFromWildCard(fname)
				for ff in filenames:
					mo = r.search(ff)
					if (mo != None):
						print '%s%s%s' % (dirpath,os.sep,ff)
		elif (fname in filenames):
			print 'Found "%s" in "%s".' % (fname,dirpath)
			break

def testIt():
	powerSearchFor("c:\\","benchmark.rb")

if ( (len(sys.argv) == 1) or (sys.argv[1] == '--help') ):
	print '--help             ... displays this help text.'
	print '--verbose          ... output more stuff during search.'
	print '--dir=dir_name     ... begin search here.'
	print '--search=file_name ... search for the file name.'
else:
	for i in xrange(len(sys.argv)):
		if (sys.argv[i].find('--dir=') > -1):
			toks = sys.argv[i].split('=')
			_dirName = toks[i]
		elif (sys.argv[i].find('--verbose') > -1):
			_isVerbose = True
		elif (sys.argv[i].find('--search=') > -1):
			toks = sys.argv[i].split('=')
			if (len(toks) == 2):
				psyco.bind(powerSearchFor)
				psyco.bind(misc.isSimpleWildcard)
				psyco.bind(misc.containsWildcard)
				psyco.bind(misc.regularExpressionFromWildCard)
				#import cProfile
				#cProfile.run("testIt()")
				powerSearchFor(_dirName,toks[1])

