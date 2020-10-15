from distutils.core import setup
import py2exe

from vyperlogix import misc
from vyperlogix.misc import _utils
import os, sys, traceback

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from vyperlogix.daemon.daemon import Log

_stdOut = sys.stdout

sys.stdout = Log(StringIO())

_console=[os.sep.join([os.getcwd(),'windows_sleep_runner.py'])]
_packages = [[f for f in sys.path if (f.endswith('@lib'))][0]]
_includes = ['win32api','win32file','win32con']
_excludes = []
#_excludes = ['Crypto.PublicKey._fastmath','Crypto.Util.winrandom','_pybsddb','bsddb3.dbutils', 'r_hmac', 'testdata', 'tests']

_root = os.path.abspath('.')
print >>sys.stderr, '_root is "%s" from "%s".' % (_root,sys.argv[0])

print >>sys.stderr, '_packages is "%s".' % (_packages)

while (1):
    _len_packages = len(_packages)
    try:
	try:
	    _root_ = os.path.abspath('.')
	    print >>sys.stderr, 'Building...\n\tconsole is "%s"\n\tpackages is "%s"\n\tincludes is "%s"\n\texcludes is "%s".' % (_console,_packages,_includes,_excludes)
	    setup(
		    console=_console,
		    packages=_packages,
		    options = {"py2exe": {"compressed": 1,
					  "optimize": 2,
					  "ascii": 1,
					  "bundle_files": 1,
					  "includes": _includes,
					  "excludes": _excludes,
	                                  "dll_excludes": ["mswsock.dll", "MSWSOCK.dll", "powrprof.dll"],
					  }
			       },
		    zipfile = None,
		)
	except ImportError, details:
	    print >>sys.stderr, 'ImportError: %s' % (details)
	except Exception, details:
	    print >>sys.stderr, 'ERROR: %s' % (details)
	    exc_info = sys.exc_info()
	    info_string = _utils.asMessage('\n'.join(traceback.format_exception(*exc_info)))
	    print >>sys.stderr, info_string
    except Exception, details:
	print >>sys.stderr, 'ERROR: %s' % (details)
	exc_info = sys.exc_info()
	info_string = _utils.asMessage('\n'.join(traceback.format_exception(*exc_info)))
	print >>sys.stderr, info_string
    finally:
	_stdout_log = os.sep.join([_root_,'stdout_%s.txt' % (_utils.timeStampForFileName())])
	_utils.writeFileFrom(_stdout_log,sys.stdout.f.getvalue())
    
	if (0):
	    _lines = sys.stdout.f.getvalue().split('\n')
	    
	    sys.stdout = Log(StringIO())
	    
	    _collecting = False
	    _collection = []
	    for _l in _lines:
		if (_l.find('The following modules appear to be missing') > -1):
		    _collecting = True
		    continue
		if (_collecting):
		    if (len(_l.strip()) == 0):
			break
		    _collection.append(_l)
	
	    names = []
	    print >>sys.stderr, '\tBEGIN:'
	    for c in _collection:
		print >>sys.stderr, '\t\t"%s"' % (c)
		names = eval(c)
		if (isinstance(names,list)):
		    for name in names:
			print >>sys.stderr, '\t\t(%s)' % (name)
	    print >>sys.stderr, '\tEND!'
	    
	    d = {}
	    for name in names:
		d[name] = ''
		for p in sys.path:
		    if (p.find(name) > -1):
			d[name] = p
	    
	    #print >>sys.stderr, '\n'
	    #print >>sys.stderr, '\tBEGIN:'
	    #for p in sys.path:
		#print >>sys.stderr, '\t\t(%s)' % (p)
	    #print >>sys.stderr, '\tEND!'
	    #print >>sys.stderr, '\n'
	    
	    print >>sys.stderr, '\t%s' % (str(d))
	    
	    from vyperlogix.hash import lists
	    if (len(d) > 0):
		lists.prettyPrint(d,title='Name to Path Item.',fOut=sys.stderr)
		
		from vyperlogix.zip import eggs
		for k,v in d.iteritems():
		    if (len(v) > 0):
			_eggs_root = _utils.safely_mkdir(fpath='eggs',dirname='')
			print >>sys.stderr, '\t\tUnEgg module "%s" from "%s" into "%s".' % (k,v,_eggs_root)
			eggs.unEgg(k,v,_eggs_root)
			# locate the __init__.py? and use that folder name for the _eggs_root
			_real_eggs_root = _utils.searchForFileNamed('__init__.py', top=_eggs_root)
			if (len(_real_eggs_root) == 0):
			    _real_eggs_root = _utils.searchForFileNamed('__init__.pyc', top=_eggs_root)
			if (len(_real_eggs_root) == 0):
			    _real_eggs_root = _utils.searchForFileNamed('__init__.pyo', top=_eggs_root)
			if (os.path.exists(_real_eggs_root)):
			    if (os.path.isfile(_real_eggs_root)):
				_real_eggs_root = os.path.dirname(_real_eggs_root)
			    if (misc.findInListSafely(_packages,_real_eggs_root) == -1):
				print >>sys.stderr, '\t\tReal Egg Folder is "%s".' % (_real_eggs_root)
				_packages.append(_real_eggs_root)
			else:
			    print >>sys.stderr, '\t\tCannot locate the root for the Egg named "%s".' % (k)
		
    if (_len_packages == len(_packages)):
	print >>sys.stderr, '\t\tNothing to UnEgg therefore nothing more to do, except enjoy the rest of the process.'
	break # get out of the loop because there was no change to the list of packages.
    #else:
	#for f in ['build','dist']:
	    #_f = os.sep.join([_root,f])
	    #print >>sys.stderr, '\t\tRemoving "%s".' % (_f)
	    #_utils.removeAllFilesUnder(_f)
	#print >>sys.stderr, '\t\tBack to repeat the Build.'
    
sys.stdout = _stdOut
sys.exit()
    
_fpath = os.sep.join([_root_,'dist'])
_fpath2 = os.sep.join([_root_,'svnHotBackups'])

_utils.safely_mkdir(_fpath2,dirname='')
_files = os.listdir(_fpath)
_root = _fpath if (os.path.isdir(_fpath)) else os.path.dirname(_fpath)
print '_fpath=%s, _root=%s' % (_fpath,_root)
_root2 = _fpath2 if (os.path.isdir(_fpath2)) else os.path.dirname(_fpath2)
print '_fpath2=%s, _root2=%s' % (_fpath2,_root2)
for f in _files:
    _f = os.sep.join([_root,f])
    _f2 = os.sep.join([_root2,f])
    print '_utils.copyFile(%s,%s)' % (_f,_f2)
    _utils.copyFile(_f,_f2)