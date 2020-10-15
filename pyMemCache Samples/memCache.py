from vyperlogix.misc import _utils
from vyperlogix.hash import proxies

from vyperlogix.misc import ObjectTypeName

from vyperlogix.misc.GenPasswd import GenPasswd

from vyperlogix.analysis import ioTimeAnalysis

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix.misc import threadpool

import os, sys
import time
import uuid

__Q__ = threadpool.ThreadQueue(1)

__Test1_Writes__ = 'Test1-Writes'
__Test1_Reads__ = 'Test1-Reads'

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()
	
    oBuf = _utils.stringIO()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
            '--diags1':'perform some diagnostics - shows results from reads.',
            '--memcache':'use memcache rather than umemcache.',
            '--umemcache':'use umemcache rather than memcache.',
            '--threaded=?':'threading with pool size set to ?.',
	    '--server=?':'url or address of server end-point.',
            '--records=?':'number of records to create/test.',
	    }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = __args__.programName

	_stdout = sys.stdout

	_isVerbose = __args__.get_var('isVerbose',Args._bool_,False)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isVerbose=%s' % (_isVerbose)
	_isDebug = __args__.get_var('isDebug',Args._bool_,False)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isDebug=%s' % (_isDebug)
	_isDiags1 = __args__.get_var('isDiags1',Args._bool_,False)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isDiags1=%s' % (_isDiags1)

	_isMemcache = __args__.get_var('isMemcache',Args._bool_,True)
	_isUmemcache = __args__.get_var('isUmemcache',Args._bool_,False)
	if (not _isMemcache):
	    _isMemcache = (not _isUmemcache)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isMemcache=%s' % (_isMemcache)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isUmemcache=%s' % (_isUmemcache)

	_isHelp = __args__.get_var('isHelp',Args._bool_,False)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: _isHelp=%s' % (_isHelp)

	if (_isHelp):
	    ppArgs()
	    sys.exit()

	__server__ = __args__.get_var('server',Args._str_,'127.0.0.1:11211')
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: __server__=%s' % (__server__)

	__records__ = __args__.get_var('records',Args._int_,1)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: __records__=%s' % (__records__)

	__threaded__ = __args__.get_var('threaded',Args._int_,0)
	if (_isVerbose):
	    print >>_stdout, 'DEBUG: __threaded__=%s' % (__threaded__)

	is_memcachable = True
	if (_isMemcache):
	    try:
		import memcache
	    except ImportError:
		is_memcachable = False
	if (_isUmemcache):
	    try:
		import umemcache as memcache
	    except ImportError:
		is_memcachable = False
	    
	if (is_memcachable):
	    try:
		mc = memcache.Client([__server__], debug=0 if (_isDebug) else 1)
		is_memcachable = all([s.connect() for s in mc.servers])
	    except:
		mc = memcache.Client(__server__)
	
	if (is_memcachable):
	    if (__threaded__ > 0):
		__Q__ = threadpool.ThreadQueue(100)
	    ioTimeAnalysis.init_AnalysisDataPoint(__Test1_Writes__)
	    ioTimeAnalysis.init_AnalysisDataPoint(__Test1_Reads__)
	    
	    def _cache_this(d,mc):
		global __bytes__
		k = str(uuid.uuid4())
		d[k] = GenPasswd(length=128)
		__bytes__ += len(str(k)) + len(str(d[k]))
		mc.set(k,d[k])
    
	    @threadpool.threadify(__Q__)
	    def cache_this(d,mc):
		_cache_this(d,mc)
	    
	    __bytes__ = 0
	    try:
		d = {}
		ioTimeAnalysis.begin_AnalysisDataPoint(__Test1_Writes__)
		for i in xrange(0,__records__):
		    if (__threaded__ > 0):
			cache_this(d,mc)
		    else:
			_cache_this(d,mc)
		if (__threaded__ > 0):
		    __Q__.join()
		ioTimeAnalysis.end_AnalysisDataPoint(__Test1_Writes__)
		t1 = ioTimeAnalysis.ioTimeAnalysis.ioTimeAnalysis(__Test1_Writes__)
		print
		print 't1=%s, __bytes__=%s (%-10.2f, %s bytes/sec)' % (t1,__bytes__,__bytes__/t1,"{:10,.2}".format(__bytes__/t1))
		print
		print 'stats is %s' % (mc.stats)
		n = 1
		__bytes__ = 0
		ioTimeAnalysis.begin_AnalysisDataPoint(__Test1_Reads__)
		for k in d.keys():
		    foo = mc.get(k)
		    if (_isDiags1):
			print '%d :: %s --> %s' % (n,k,foo)
		    __bytes__ += len(str(k)) + len(str(foo))
		    n += 1
		ioTimeAnalysis.end_AnalysisDataPoint(__Test1_Reads__)
		t2 = ioTimeAnalysis.ioTimeAnalysis.ioTimeAnalysis(__Test1_Reads__)
		print
		print 't2=%s, __bytes__=%s (%-10.2f, %s bytes/sec)' % (t2,__bytes__,__bytes__/t2,"{:10,.2}".format(__bytes__/t2))
		print
		print ioTimeAnalysis.ioTimeAnalysis.ioTimeAnalysisReport()
	    except Exception, details:
		info_string = _utils.formattedException(details=details)
		print >>sys.stderr, info_string
	else:
	    print 'ERROR cannot run the test.'
	    
    from vyperlogix.process.killProcByPID import killProcByPID
    pid = os.getpid()
    killProcByPID(pid)
