# vast - vyperlogix automatic synchronizer tool

import os, sys
import re
import traceback

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc import _utils

import models

from vyperlogix.enum.Enum import Enum

class methods(Enum):
    none = 0
    single = 2^0
    multi = 2^1

from vyperlogix.misc import threadpool
_Q1_ = threadpool.ThreadQueue(100)
_Q2_ = threadpool.ThreadQueue(10)

import Queue
_QQ_ = Queue.Queue(200000)

db_fpath = 'vast.sqlite3'

_issues_ = []

__re__ = None

######################################################################################
#
# pod
#
#
######################################################################################

def test_pod():
    print 'BEGIN...',
    db = models.pod.Db(file = db_fpath, dynamic_index = True)
    
    folder1  = models.Folder(name = 'top', some_attr = 'foo')
    folder2  = models.Folder(name = 'next', some_attr = ['bar', 'baz'])
    
    file1  = models.File(name = 'file1', age = 40, folder = folder1, random_attr = 10.23)
    file2  = models.File(name = 'file2', age = 35, folder = folder2, random_attr = {'key': ['value', (1, 2, 3)]})
    
    db.commit()
    print 'END !'

    print 'TESTING...',
    for aFolder in models.Folder:
	print '%s <%s>' % (aFolder.name, aFolder.some_attr)
    
    for aFolder in [f for f in models.Folder if f.name[0] == 't']:
	print '%s <%s>' % (aFolder.name, aFolder.some_attr)
    
    for aFolder in models.Folder.where.name[0] == 't':
	print '%s <%s>' % (aFolder.name, aFolder.some_attr)
    
    for aFile in models.File.where.age > 30:
	print '%s <%s>' % (aFile.name, aFile.age)

    for f in models.File:
	print '%s <%s>' % (f.name, f)
    
    for aFile in [f for f in models.File if f.folder.name == 'top']:
	print '%s <%s>' % (aFile.name, aFile)
	
    for aFile in [f for f in models.File if f.folder.name == 'next']:
	print '%s <%s>' % (aFile.name, aFile)
	
    print 'TESTING DONE !',
    
def __scan_source(top):
    top = top[0] if (misc.isList(top)) else top
    if (_isDb):
	db = models.pod.Db(file = db_fpath, dynamic_index = True)
    for root,dirs,files in _utils.walk(top):
	_root_ = _utils.ascii_only(root)
	if (len(_root_) != len(root)):
	    anIssue = 'WARNING: There is an issue with "%s".' % (root)
	    _issues_.append(anIssue)
	    print >>sys.stderr, anIssue
	for f in files:
	    _f_ = _utils.ascii_only(f)
	    if (len(_f_) != len(f)):
		anIssue = 'WARNING: There is an issue with "%s" in "%s".' % (f,root)
		_issues_.append(anIssue)
		print >>sys.stderr, anIssue
	    try:
		fname = os.sep.join([root,f])
		if (__isTransferingFiles):
		    statinfo = os.stat(fname)
		    fsize = statinfo.st_size
		    if (_isDb):
			models.File(name = fname,size=fsize,mtime=statinfo.st_mtime)
		    print '[%s] %s' % (fsize,fname)
		elif (__isSearchingForFiles):
		    if (_isRegex):
			try:
			    __re__
			except:
			    info_string = _utils.formattedException(details=e)
			    _issues_.append(info_string)
			pass
		    print '%s' % (fname)
	    except WindowsError, e:
		info_string = _utils.formattedException(details=e)
		_issues_.append(info_string)
	if (_isDb):
	    db.commit()
    if (_isDb):
	db.commit()

@threadpool.threadify(_Q2_)
def read_queue():
    db = models.pod.Db(file = db_fpath, dynamic_index = True)
    while (1):
	try:
	    print >>sys.stderr, '%s() :: _QQ_.get()' % (misc.funcName())
	    item = _QQ_.get()
	    print >>sys.stderr, '%s() :: item=%s' % (misc.funcName(),item)
	    if (item is None):
		print >>sys.stderr, '1. Terminating the %s() loop due termination signal.' % (misc.funcName())
		break
	    models.File(name = item['name'],size=item['size'],mtime=item['mtime'])
	    db.commit()
	except:
	    print >>sys.stderr, '2. Terminating the %s() loop due to an error.' % (misc.funcName())
	    break
    
@threadpool.threadify(_Q1_)
def _scan_source(top):
    top = top[0] if (misc.isList(top)) else top
    for root,dirs,files in _utils.walk(top):
	_root_ = _utils.ascii_only(root)
	if (len(_root_) != len(root)):
	    anIssue = 'WARNING: There is an issue with "%s".' % (root)
	    _issues_.append(anIssue)
	    print >>sys.stderr, anIssue
	for f in files:
	    _f_ = _utils.ascii_only(f)
	    if (len(_f_) != len(f)):
		anIssue = 'WARNING: There is an issue with "%s" in "%s".' % (f,root)
		_issues_.append(anIssue)
		print >>sys.stderr, anIssue
	    try:
		fname = os.sep.join([root,f])
		statinfo = os.stat(fname)
		fsize = statinfo.st_size
		_QQ_.put_nowait({'name':fname,'size':fsize,'mtime':statinfo.st_mtime})
		#print '[%s] %s' % (fsize,fname)
	    except WindowsError, e:
		info_string = _utils.formattedException(details=e)
		_issues_.append(info_string)
	pass
    pass

def scan_source(top):
    if (_method == methods.single):
	__scan_source(top)
    else:
	read_queue()
	top = top[0] if (misc.isList(top)) else top
	dirs = [os.sep.join([top,d]) for d in os.listdir(top) if (os.path.isdir(os.sep.join([top,d])))]
	for d in dirs:
	    _scan_source(d)
	print >>sys.stderr, 'Waiting for _Q1_ !'
	_Q1_.join()
	print >>sys.stderr, 'Terminate _QQ_ !'
	_QQ_.put_nowait(None)
	print >>sys.stderr, 'Waiting for _Q2_ !'
	_Q2_.join()
	pass

def test_db():
    num = 0
    db = models.pod.Db(file = db_fpath, dynamic_index = True)
    for f in models.File:
	num += 1
	print '%s' % (f.name)
    print >>sys.stderr, 'There are %d files.' % (num)
    
if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--db':'use pod db.',
	    '--debug':'debug some stuff.',
	    '--profile':'profille some stuff.',
	    '--analysis':'analyze some stuff.',
	    '--method=?':'[single,multi,]',
	    '--clear':'clear the database.',
	    '--test':'test db only.',
	    '--source=?':'name the source folder tree.',
	    '--dest=?':'name the dest folder tree.',
	    '--search=?':'filespec to search for... (this can be a regex-like spec in the form of "blah|blah")',
	    }
    _argsObj = Args.Args(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = _argsObj.programName
	_isVerbose = False
	try:
	    if _argsObj.booleans.has_key('isVerbose'):
		_isVerbose = _argsObj.booleans['isVerbose']
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print info_string
	    _isVerbose = False
	    
	_isDebug = False
	try:
	    if _argsObj.booleans.has_key('isDebug'):
		_isDebug = _argsObj.booleans['isDebug']
	except:
	    pass
	
	_isDb = False
	try:
	    if _argsObj.booleans.has_key('isDb'):
		_isDb = _argsObj.booleans['isDb']
	except:
	    pass
	
	_isHelp = False
	try:
	    if _argsObj.booleans.has_key('isHelp'):
		_isHelp = _argsObj.booleans['isHelp']
	except:
	    pass
	
	_isProfile = False
	try:
	    if _argsObj.booleans.has_key('isProfile'):
		_isProfile = _argsObj.booleans['isProfile']
	except:
	    pass
	
	_isAnalysis = False
	try:
	    if _argsObj.booleans.has_key('isAnalysis'):
		_isAnalysis = _argsObj.booleans['isAnalysis']
	except:
	    pass
	
	_isClear = False
	try:
	    if _argsObj.booleans.has_key('isClear'):
		_isClear = _argsObj.booleans['isClear']
	except:
	    pass
	
	_isTest = False
	try:
	    if _argsObj.booleans.has_key('isTest'):
		_isTest = _argsObj.booleans['isTest']
	except:
	    pass
	
	if (_isHelp):
	    ppArgs()
	    sys.exit()
	
	if (_isTest):
	    _isClear = False
	
	if (_isClear):
	    import glob
	    print 'Clear DB !'
	    for f in glob.glob('%s*' % (db_fpath)):
		try:
		    os.unlink(f)
		except WindowsError, e:
		    pass
	
	_source = None
	try:
	    __source = _argsObj.arguments['source'] if _argsObj.arguments.has_key('source') else _source
	    try:
		if (os.path.exists(__source)):
		    _source = __source
	    except:
		pass
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print info_string
	
	print '_source=%s' % (_source)
	    
	_dest = None
	try:
	    __dest = _argsObj.arguments['dest'] if _argsObj.arguments.has_key('dest') else _dest
	    try:
		if (os.path.exists(__dest)):
		    _dest = __dest
	    except:
		pass
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print info_string
	
	print '_dest=%s' % (_dest)
	    
	_isRegex = False
	_search = None
	try:
	    __search = _argsObj.arguments['search'] if _argsObj.arguments.has_key('search') else _search
	    _search = __search
	    ioBuf = _utils.stringIO()
	    print >>ioBuf, "(?P<name>%s)" % (_search)
	    print ioBuf.getvalue()
	    __re__ = re.compile(ioBuf.getvalue())
	    _isRegex = (ObjectTypeName.typeClassName(__re__).lower().find('re.SRE_Pattern'.lower()) > -1)
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print info_string
	
	print '_search=%s [%s]' % (_search,'REGEX' if (_isRegex) else 'Literal')
	    
	_method = methods.single
	try:
	    __method = _argsObj.arguments['method'] if _argsObj.arguments.has_key('method') else _method
	    _method = methods.single if (__method == methods.single) else methods.multi if (__method == methods.multi) else methods.single
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print info_string
	
	if (_source is not None):
	    __isTransferingFiles = (_dest is not None) and (_source != _dest)
	    __isSearchingForFiles = (_source is not None) and (len(_search) > 0)
	    from vyperlogix.misc import _psyco
	    _psyco.importPsycoIfPossible(func=[scan_source,_scan_source,read_queue,__scan_source])
	    #test_pod()
	    if (os.path.isdir(_source)):
		if (not _isTest):
		    if (_isProfile):
			import cProfile
			cProfile.run('scan_source("%s")' % (_source))
		    elif (_isAnalysis):
			from vyperlogix.analysis import ioTimeAnalysis
			ioTimeAnalysis.runWithAnalysis(func=scan_source,args=[_source])
		    else:
			scan_source(_source)
		    if (len(_issues_) > 0):
			for anIssue in _issues_:
			    print >>sys.stderr, anIssue
		    else:
			print >>sys.stderr, 'There are NO issues.'
		else:
		    test_db()
	    else:
		print 'WARNING: Cannot perform synchronization at this time, source must be a directory or folder...'
	    pass
	else:
	    print 'WARNING: Cannot perform synchronization at this time, please adjust your inputs and try again...'
sys.exit(1)