import httplib, urllib

import os, sys

import time
import uuid

import threading

import Queue

from vyperlogix.enum.Enum import Enum

from vyperlogix.misc  import ioTimeAnalysis

from vyperlogix.misc import threadpool

from vyperlogix.daemon import daemon

from vyperlogix import misc
from vyperlogix.misc  import _utils

from vyperlogix.hash import lists

from vyperlogix.classes import SmartObject

_Q_ = threadpool.ThreadQueue(1,isDaemon=False)

_Q2_ = threadpool.ThreadQueue(1,isDaemon=False)

_Q3_ = threadpool.ThreadQueue(1,isDaemon=False)

_max_count = 100

_timeout = 10

_q_ = Queue.Queue(_max_count)

#_host = 'rhorn-srv.centos.magma-da.com'

_host = 'pyeggs.dyn-o-saur.com'

_count = 0

_count_failures = 0

_interval = 10

_total_requests_per_second = 0.0
_average_requests_per_second = 0.0
_count_requests_per_second = 0

_isRunning = False

d_responses = lists.HashedLists()

threadLock = threading.Lock()

StringIO = _utils.stringIO

class Modes(Enum):
    none = 0
    gets = 2**0
    posts = 2**1
    single = 2**2
    multi = 2**3
    
#_run_mode = Modes.gets | Modes.single
_run_mode = Modes.gets | Modes.multi
#_run_mode = Modes.posts | Modes.single
#_run_mode = Modes.posts | Modes.multi

#_url = '/contact/login_form' if ((_run_mode & Modes.gets).value) else '/contact/login'

_url = '/' if ((_run_mode & Modes.gets).value) else '/'

def accessor(host,url,callback=None):
    global _count
    global _count_failures
    global _q_
    
    _uuid = uuid.uuid4()
    
    conn = httplib.HTTPConnection(host)
    if ((_run_mode & Modes.gets).value):
        print >>logger, '%s :: GET' % (_uuid)
        conn.request("GET", url)
    elif ((_run_mode & Modes.posts).value):
        print >>logger, '%s :: POST' % (_uuid)
        params = urllib.urlencode({'email': 'rhorn@magma-da.com', 'password': 'Peek@b99'})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}        
        conn.request("POST", url, params, headers)
    isError = False
    try:
        print >>logger, '%s :: GET_RESPONSE' % (_uuid)
        response = conn.getresponse()
    except:
        isError = True
	response = None
    if (response is not None):
	d_responses[response.status] = response
	if ( (isError == False) and (response.status in [200,302]) and (response.reason in ['OK','Found','Moved Temporarily']) ):
	    print >>logger, '%s :: READ_RESPONSE, isError=%s, response.status=%s, response.reason=%s' % (_uuid,isError,response.status,response.reason)
	    try:
		data1 = response.read()
	    except:
		data1 = ''
	    _count += 1
	    print >>logger, '%s :: SUCCESS: %s' % (_uuid,_count)
	    if ((_count % _interval) == 0):
		threadLock.acquire()
		if (callable(callback)):
		    callback(_count)
		threadLock.release()
	    #print >>logger, data1
	else:
	    threadLock.acquire()
	    _count_failures += 1
	    print >>logger, '%s :: FAILURE: %s, isError=%s, response.status=%s, response.reason=%s' % (_uuid,_count_failures,isError,response.status,response.reason)
	    threadLock.release()
    s = SmartObject.SmartFuzzyObject(args={'uuid':_uuid,'ts':time.time()})
    _q_.put_nowait(s)
    #print >>logger, '%s :: %s' % (_uuid,'-'*40)
    #print >>logger, '\n'

@threadpool.threadify(_Q_)
def main_threaded(host,url,callback=None):
    return accessor(host,url,callback=callback)

def main_single(host,url,callback=None):
    return accessor(host,url,callback=callback)

def main(host,url,callback=None):
    if ((_run_mode & Modes.single).value):
        main_single(host,url,callback=callback)
    elif ((_run_mode & Modes.multi).value):
        main_threaded(host,url,callback=callback)

def report_requests_per_second(count):
    global _average_requests_per_second
    global _count_requests_per_second
    global _total_requests_per_second
    
    now = time.time()
    et = max(now,_beginTime) - min(now,_beginTime)
    rps = count / et
    
    _count_requests_per_second += 1
    _total_requests_per_second += rps
    _average_requests_per_second = _total_requests_per_second / _count_requests_per_second
    
    print >>logger, '\t%4.2f (requests per second)' % (rps)
    print >>logger, '\t%4.2f (average requests per second)' % (_average_requests_per_second)

@threadpool.threadify(_Q2_)
def monitor():
    global _q_
    global _isRunning
    
    while (_isRunning):
        try:
            print >>logger, '\t%s :: _q_.get()' % (misc.funcName())
            x = _q_.get(block=True,timeout=_timeout)
            print >>logger, '\t%s :: x=%s' % (misc.funcName(),x)
        except Exception, _details:
            print >>logger, _utils.formattedException(details=_details)
            _isRunning = False
            print >>logger, '\t%s :: _isRunning=%s' % (misc.funcName(),_isRunning)
            break
            
    if ((_run_mode & Modes.multi).value):
	print >>logger, '\t_Q_.join()'
	_Q_.join()
    
    d_responses.prettyPrint(fOut=logger)
    
    ioTimeAnalysis.ioTimeAnalysisReport(iters=_max_count,fOut=logger)
    
    report_requests_per_second(_count)
    report_requests_per_second(_count)

    sys.exit(1)
    sys.exit(1)

@threadpool.threadify(_Q3_)
def runTest():
    from vyperlogix.process import Popen

    buf = StringIO()
    cmd = r'"Z:\python projects\molten_hammer\run-once.cmd"'
    shell = Popen.Shell([cmd],isExit=True,isWait=True,isVerbose=True,fOut=buf)
    #print buf.getvalue()

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)
    
    from vyperlogix.misc import Args
    from vyperlogix.misc import PrettyPrint

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--host=?':'specify the host or IP address.',
	    '--max_count=?':'specify the max number of requests.',
	    '--threads=?':'specify the number of threads.',
	    '--mode=?':'["gets","posts","single","multi"]',
	    '--timeout=?':'specify the timeout for the primary Q loop.',
	    '--procs=?':'specify the number of child procs.',
	    '--url=?':'specify the URL to use when issuing the GET or POST per the --mode= setting.',
	    }
    _argsObj = Args.Args(args)

    _progName = _argsObj.programName
    _isVerbose = False
    try:
	if _argsObj.booleans.has_key('isVerbose'):
	    _isVerbose = _argsObj.booleans['isVerbose']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_isVerbose = False
    
    if (_isVerbose):
	print '_argsObj=(%s)' % str(_argsObj)
	
    _isHelp = False
    try:
	if _argsObj.booleans.has_key('isHelp'):
	    _isHelp = _argsObj.booleans['isHelp']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_isHelp = False
	
    _host = ''
    try:
	if _argsObj.arguments.has_key('host'):
	    _host = _argsObj.arguments['host']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_host = ''
	
    _max_count = 0
    try:
	if _argsObj.arguments.has_key('max_count'):
	    _max_count = int(_argsObj.arguments['max_count'])
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_max_count = 0
	
    _threads = 0
    try:
	if _argsObj.arguments.has_key('threads'):
	    _threads = int(_argsObj.arguments['threads'])
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_threads = 0
	
    _timeout = 0
    try:
	if _argsObj.arguments.has_key('timeout'):
	    _timeout = int(_argsObj.arguments['timeout'])
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_timeout = 0
	
    _procs = 0
    try:
	if _argsObj.arguments.has_key('procs'):
	    _procs = int(_argsObj.arguments['procs'])
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_procs = 0
	
    _run_mode = Modes.none
    try:
	if _argsObj.arguments.has_key('mode'):
	    modes = _argsObj.arguments['mode'].split('|')
	    _run_mode = Modes.none
	    for mode in modes:
		_run_mode |= Modes(mode)
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_run_mode = Modes.none
	
    _url = '/'
    try:
	if _argsObj.arguments.has_key('url'):
	    _url = _argsObj.arguments['url']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_url = '/'
	
    if (_isHelp):
	ppArgs()
    else:
	fname = os.path.join(os.path.dirname(__file__),'report_%s.txt' % (_utils.timeStampForFileName()))
	fOut = open(fname,'w')
	logger = daemon.EchoLog(fOut)
	
	if (_threads > 0):
	    _Q_ = threadpool.ThreadQueue(_threads,isDaemon=False)
	    
	if (_procs == 0):
	    ioTimeAnalysis.initIOTime('main')
	    
	    _isRunning = True
	    monitor()
	    
	    _beginTime = time.time()
	    ioTimeAnalysis.ioBeginTime('main')
	    for i in xrange(0,_max_count):
		main(_host,_url,callback=report_requests_per_second)
	    ioTimeAnalysis.ioEndTime('main')
	    
	    while _isRunning:
		time.sleep(1)
		print >>logger, '\t(+) _isRunning=%s' % (_isRunning)
	else:
	    _Q3_ = threadpool.ThreadQueue(_procs,isDaemon=False)
	    import time
	    for i in xrange(0,_procs+1):
		print 'Proc # %s' % (i+1)
		runTest()
		time.sleep(5)
	    pass
	
