import socket,asyncore
import types
import os, sys
import re
import time
from threading import Thread
import threading
import traceback

import simplejson

from vyperlogix import misc
from vyperlogix.misc import _utils

logger = None

def addto(instance):
    def decorator(f):
        import new
        f = new.instancemethod(f, instance, instance.__class__)
        setattr(instance, f.func_name, f)
        return f
    return decorator

def decodeUnicode(value):
    import codecs
    import encodings
    if (isinstance(value,unicode)):
        return ((codecs.getencoder('unicode_escape'))(value))[0]
    elif (isinstance(value,str)):
        return value
    else:
        return decodeUnicode(str(value))

def threaded(func):
    def proxy(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return proxy

from Queue import Queue

class ThreadQueue(Queue):
    def __init__(self, maxsize, isDaemon=False):
        self.__stopevent = threading.Event()
        assert maxsize > 0, 'maxsize > 0 required for ThreadQueue class'
        Queue.__init__(self, maxsize)
        for i in xrange(maxsize):
            thread = Thread(target = self._worker)
            thread.setDaemon(isDaemon)
            thread.start()

    def _worker(self):
        while not self.__stopevent.isSet():
            if (not self.isRunning):
                break
            try:
                func, args, kwargs = self.get()
                func(*args, **kwargs)
            except Exception, details:
		if (logger):
		    logger.exception('(%s._worker).Error :: "%s".' % (self.__class__,str(details)))
		    logger.exception(traceback.format_exc())
                self.task_done()
                self.join()
                raise
            else:
                self.task_done()

    def addJob(self, func, *args, **kwargs):
        self.put((func, args, kwargs))

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.__stopevent.set()
        self.join()

    def isRunning():
	doc = "isRunning"
	def fget(self):
	    return not self.__stopevent.isSet()
	def fset(self, value):
	    if (not self.isRunning):
		self.__stopevent.set()
	return locals()
    isRunning = property(**isRunning())

def threadify(threadQ):
    assert threadQ.__class__ == ThreadQueue, 'threadify decorator requires a ThreadQueue object instance'
    def decorator(func):
        def proxy(*args, **kwargs):
            threadQ.put((func, args, kwargs))
            return threadQ
        return proxy
    return decorator

def parse_ip_address_and_port(ip_port,default_ip='0.0.0.0',default_port=55555):
    ip = default_ip
    port = default_port
    toks = ip_port.split(':')
    if (len(toks) > 1):
	ip = toks[0]
	port = int(toks[-1])
    return (ip,port)
	
__QQ__ = ThreadQueue(1)

class TCPIPBridge():
    def __init__(self, ipAddr, port, __eof__=None, callback=None):
        self.__ipAddr__ = ipAddr
        self.__port__ = port
        self.__callback__ = callback
	self.__eof__ = __eof__
	self.address = None
        
    def __repr__( self):
        return '%s.TCPIPBridge :: ipAddr=(%s), eof=(%s), port=(%s)' % (__name__, str(self.ipAddr),str(self.eof),str(self.port))
        
    def get_ipAddr(self):
        return self.__ipAddr__
    
    def set_ipAddr(self,value):
        self.__ipAddr__ = value
    
    def get_port(self):
        return self.__port__
    
    def set_port(self,value):
        self.__port__ = value
    
    def get_callback(self):
        return self.__callback__
    
    def set_callback(self,value):
        self.__callback__ = value
    
    def get_eof(self):
        return self.__eof__
    
    def set_eof(self,value):
        self.__eof__ = value
    
    ipAddr = property(get_ipAddr,set_ipAddr)
    port = property(get_port,set_port)
    callback = property(get_callback,set_callback)
    eof = property(get_eof,set_eof)
    
    def __handler__(self,data):
	if (callable(self.callback)):
	    return self.callback(data)
	return
    
    @threadify(__QQ__)
    def startup(self):
	# When ReverseProxy is used the asyncore.loop() handles this part of the process...
	mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
	if (logger):
	    logger.info('%s.startup() :: self.ipAddr=[%s], self.port=[%s]' % (self.__class__,self.ipAddr,self.port))
	mySocket.bind ( ( self.ipAddr, self.port) )
	mySocket.listen ( 1 )
	channel, details = mySocket.accept()
	if (logger):
	    logger.info('(%s) Opened a connection with "%s".' % (self.port,details))
	__data__ = ''
	__filename__ = None
	__fOut__ = None
	__chunk_count__ = 0
	__re1__ = re.compile("@@@filename=(?P<filename>.*)@@@", re.DOTALL | re.MULTILINE)
	__re2__ = re.compile("@@@address=(?P<address>.*)@@@", re.DOTALL | re.MULTILINE)
	while True:
	    try:
		data = channel.recv(8192)
		if (data) and (len(data) > 0):
		    for ch in data:
			if (not __filename__) and (ord(ch) == 0):
			    if (__data__) and (misc.isString(__data__)) and (len(__data__) > 0) and (callable(self.callback)):
				self.__handler__(__data__)
			    __data__ = ''
			else:
			    __data__ += ch
			    matches1 = __re1__.search(__data__)
			    matches2 = __re2__.search(__data__)
			    if (matches1):
				f = matches1.groupdict().get('filename',None)
				if (f):
				    __filename__ = f
				    dirname = os.path.dirname(__filename__)
				    if (callable(self.callback)):
					dirname2 = self.__handler__(dirname)
					if (misc.isIterable(dirname2) and (len(dirname2) > 0)):
					    dirname2 = dirname2[0]
					if (dirname != dirname2):
					    __filename__ = __filename__.replace(dirname,dirname2)
					    dirname = dirname2
				    if (not os.path.exists(dirname)):
					os.makedirs(dirname)
				    __fOut__ = open(__filename__,'wb')
				    __data__ = ''
			    elif (matches2):
				f = matches2.groupdict().get('address',None)
				if (f):
				    self.address = f
				    if (logger):
					logger.debug('Address is "%s".' % (self.address))
				    __data__ = ''
			    else:
				i = __data__.find(self.eof)
				if (__filename__) and (i > -1):
				    __data__ = [ch for ch in __data__]
				    del __data__[i:]
				    __data__ = ''.join(__data__)
				    __fOut__.write(__data__)
				    __fOut__.flush()
				    __fOut__.close()
				    if (callable(self.callback)):
					self.__handler__(__filename__)
				    if (_utils.is_valid_ip_and_port(self.address)):
					connect_to_ip,connect_to_port = parse_ip_address_and_port(self.address, default_ip='0.0.0.0', default_port=51555)
					__writer__ = SocketWriter(connect_to_ip, connect_to_port,retry=True)
					__writer__.send('@@@delete=%s@@@' % (os.path.basename(__filename__)))
					__writer__.close()
				    __filename__ = None
				    __fOut__ = None
				    __data__ = ''
		    if (__filename__):
			__chunk_count__ += 1
			if (logger):
			    logger.debug('DEBUG: writing (%s bytes) x (%s) --> "%s"' % (len(__data__),__chunk_count__,__fOut__.name))
			__fOut__.write(__data__)
			__data__ = ''
	    except socket.error:
		mySocket.close()
		mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
		if (logger):
		    logger.info('%s.reconnect() :: self.ipAddr=[%s], self.port=[%s]' % (self.__class__,self.ipAddr,self.port))
		mySocket.bind ( ( self.ipAddr, self.port) )
		mySocket.listen ( 1 )
		channel, details = mySocket.accept()
		if (logger):
		    logger.info('(%s) Reopened a connection with "%s".' % (self.port,details))
		__data__ = ''
		__filename__ = None
		__fOut__ = None
		__chunk_count__ = 0
	    except Exception, details:
		info_string = _utils.formattedException(details=details)
		if (logger):
		    logger.exception('EXCEPTION: %s\n%s' % (details,info_string))

class SocketWriter():
    def __init__(self,ipAddress,portNum,retry=False):
	self.ipAddress = ipAddress
	self.portNum = portNum
	self.retry = retry
	__is__ = False
	while (1):
	    try:
		self.__socket__ = socket.socket()
		self.__socket__.connect((self.ipAddress,self.portNum))
		__is__ = True
		print 'INFO: Connection established...'
		break
	    except socket.error:
		print >>sys.stderr, 'WARNING: Cannot connect to %s:%s at this time.' % (self.ipAddress,self.portNum)
		if (not retry):
		    break
		print >>sys.stderr, 'INFO: Retrying connetion in 10 seconds...'
		time.sleep(10)
	if (not __is__) and (not retry):
	    _utils.terminate('Cannot establish communications at this time.  Aborting due to lack of retry...')
	
    def send(self,someBytes):
	for ch in someBytes:
	    self.__socket__.send(ch)
	self.__socket__.send(chr(0))
	    
    def sendFile(self,fpath,__eof__='@@@EOF@@@'):
	def __send_file__(*args, **kwargs):
	    filename=kwargs.get('filename',None)
	    chunk=kwargs.get('chunk',None)
	    eof=kwargs.get('eof',None)
	    if (filename):
		self.__socket__.send('@@@filename=%s@@@' % (filename))
	    elif (chunk):
		self.__socket__.send(chunk)
	    elif (eof):
		self.__socket__.send(__eof__)
	if (os.path.exists(fpath) and os.path.isfile(fpath)):
	    from vyperlogix.misc  import _utils
	    _utils.copy_binary_files_by_chunks(fpath, None, callback=__send_file__)
	    
    def close(self):
	self.__socket__.close()

def getAsDateTimeStr(value, offset=0):
    """ return time as 2004-01-10T00:13:50.000Z """
    import time
    from types import StringType, UnicodeType, TupleType, LongType, FloatType
    strTypes = [StringType, UnicodeType]
    numTypes = (LongType, FloatType)
    if isinstance(value, (TupleType, time.struct_time)):
        return time.strftime('%Y-%m-%dT%H:%M:%S.000Z', value)
    if isinstance(value, numTypes):
        secs = time.gmtime(value+offset)
        return time.strftime('%Y-%m-%dT%H:%M:%S.000Z', secs)

    if isinstance(value, strTypes):
        try: 
            value = time.strptime(value, '%Y-%m-%dT%H:%M:%S.000Z')
            return time.strftime('%Y-%m-%dT%H:%M:%S.000Z', value)
        except: 
            print 'ERROR:getDateTimeTuple Could not parse %s'%value
            secs = time.gmtime(time.time()+offset)
            return time.strftime('%Y-%m-%dT%H:%M:%S.000Z', secs)
# END getAsDateTimeStr

def timeStamp():
    """ get standard timestamp """
    import time, datetime
    fromSecs = datetime.datetime.fromtimestamp(time.time())
    currentDay = time.mktime(fromSecs.timetuple())
    return getAsDateTimeStr(currentDay)

def dummyCallback(obj=None):
    pass

class ExceptionHandler:
    def __init__(self, logPath='.', callback=dummyCallback):
	import os, sys
        self.__logPath__ = os.path.abspath(logPath)
	self.__callback__ = callback
	sys.excepthook = self.__excepthook
	
    def get_logPath(self):
	return self.__logPath__
    
    def set_logPath(self,logpath):
	self.__logPath__ = logpath
	
    def get_callback(self):
	return self.__callback__
    
    def set_callback(self,callback):
	self.__callback__ = callback
	
    def __excepthook(self, excType, excValue, tracebackobj):
	"""
	Global function to catch unhandled exceptions.
	
	@param excType exception type
	@param excValue exception value
	@param tracebackobj traceback object
	"""
	import os, sys
	import traceback
	from StringIO import StringIO
	import time
	_computer_name = ''
	logFile = os.path.join(self.logPath, "%s.log" % sys.argv[0].split('.')[0])
	timeString = time.strftime("%Y-%m-%d, %H:%M:%S")
	
	separator = '='*80
	versionInfo = ("\nPlatform: %s (%s)\n%s\n") % (sys.platform, _computer_name, sys.version)
	tbinfofile = StringIO()
	traceback.print_tb(tracebackobj, None, tbinfofile)
	tbinfofile.seek(0)
	tbinfo = tbinfofile.read()
	errmsg = '%s: \n%s' % (str(excType), str(excValue))
	sections = [separator,timeString,errmsg,tbinfo,versionInfo,separator]
	msg = '\n'.join(sections)
	if (logger):
	    logger.exception(msg)
	try:
	    f = open(logFile, "a")
	    f.write(msg)
	    f.flush()
	    f.close()
	except IOError:
	    pass
	finally:
	    try:
		if (type(self.callback) == types.FunctionType):
		    val = self.callback('||'.join(sections))
	    except Exception, details:
		if (logger):
		    logger.exception('ERROR in firing callback for Error Handler due to "%s".' % str(details))

    logPath = property(get_logPath,set_logPath)
    callback = property(get_callback,set_callback)

def listify(maybe_list):
    """
    Ensure that input is a list, even if only a list of one item
    @maybeList: Item that shall join a list. If Item is a list, leave it alone
    """
    try:
	return list(maybe_list)
    except:
	return list(str(maybe_list))

    return maybe_list

def failUnlessEqual(first, second, msg=None):
    """Fail if the two objects are unequal as determined by the '=='
       operator.
    """
    if not first == second:
	raise AssertionError, (msg or '%r != %r' % (first, second))

def failIfEqual(first, second, msg=None):
    """Fail if the two objects are equal as determined by the '=='
       operator.
    """
    if first == second:
	raise AssertionError, (msg or '%r == %r' % (first, second))

def booleanize(data):
    return True if str(data).lower() in ['true','1','yes'] else False

def checkSaveResult(saveResult):
    idList = []
    try:
	saveResult = listify(saveResult)
	for saveResultItem in saveResult:
	    id = saveResultItem.get('id')
	    idList.append(str(id))
    except Exception, details:
	if (logger):
	    logger.exception('ERROR due to "%s".' % str(details))
    for saveResultItem in saveResult:
	if (saveResultItem.has_key('errors')):
	    for k,v in saveResultItem['errors'].iteritems():
		if (logger):
		    logger.info('%s=%s' % (k,v))

    return idList
    
def __processConnection__(data):
    try:
        _beginTime = time.time()
        _endTime = time.time()
        ret = simplejson.dumps({'beginTime':_beginTime,'endTime':_endTime,'elapsedTime':_endTime-_beginTime,'data':data})
    except ApiFault, details:
	if (logger):
	    logger.exception('ERROR due to "%s".' % (details))
        traceback.print_exc()
        ret = simplejson.dumps({'exception':details})
    if (logger):
	logger.info('='*80)
    return ret

def tcpipConnector(_cmd):

    value = '{}'
    try:
	if (len(_cmd) > 0):
	    if (logger):
		logger.debug('DEBUG.%s.1: _cmd=%s' % (misc.funcName(),_cmd))
	    __data__ = simplejson.loads(_cmd)
	    if (logger):
		logger.debug('DEBUG.%s.2: __data__=%s' % (misc.funcName(),__data__))
	    try:
		return __processConnection__(__data__)
	    except Exception, details:
		value = simplejson.dumps({'exception':details})
    except Exception, details:
	value = simplejson.dumps({'exception':details})
    return value

__Q2__ = ThreadQueue(1)

@threadify(__Q2__)
def startTCPIPBridge(ipAddr,port,callback=None,__eof__=None):
    b = TCPIPBridge(ipAddr,port,callback=callback,__eof__=__eof__)
    if (logger):
	logger.info('b=(%s)' % (str(b)))
    b.startup()

def myeval(statement, globals_=None, locals_=None): 
    try: 
        return eval(statement, globals_, locals_) 
    except SyntaxError: 
        if locals_ is None: 
            import inspect 
            locals_ = inspect.currentframe().f_back.f_locals 
        exec statement in globals_, locals_ 

if (__name__ == '__main__'):
    print 'Copyright 2014, Vyper Logix Corp, All Rights Reserved., Licensed under LGPL License Restricted to non-commercial educational use only.'
