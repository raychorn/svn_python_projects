#!/usr/bin/env python

# To-Do: 
#   Logging - log it all... Logging levels...
#   Error handling - log all errors... Queue errors and transmit back via xml from bridge...

import socket,asyncore
import types
import sys
import time
from threading import Thread
import threading
import traceback

__newConnection__ = 'newConnection'

__max_portNumber__ = (2**16)-1

_controller_ports = xrange(55555,55555+10)
_worker_ports = xrange(60000,60011)

_controller_portMap = {}

const_isProcessingCreation_symbol = 'isProcessingCreation'
const_isProcessingDeletion_symbol = 'isProcessingDeletion'
const_isProcessingUpdate_symbol = 'isProcessingUpdate'
const_tableName_symbol = 'tableName'
const_contents_symbol = 'contents'

def addto(instance):
    def decorator(f):
        import new
        f = new.instancemethod(f, instance, instance.__class__)
        setattr(instance, f.func_name, f)
        return f
    return decorator

def Property(function):
    import sys
    keys = 'fget', 'fset', 'fdel'
    func_locals = {'doc':function.__doc__}
    def probeFunc(frame, event, arg):
        if event == 'return':
            locals = frame.f_locals
            func_locals.update(dict((k,locals.get(k)) for k in keys))
            sys.settrace(None)
        return probeFunc
    sys.settrace(probeFunc)
    function()
    return property(**func_locals)

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

    def getIsRunning(self):
        return not self.__stopevent.isSet()
    
    def setIsRunning(self,isRunning):
        if (not isRunning):
            self.__stopevent.set()
        
    def _worker(self):
        while not self.__stopevent.isSet():
            if (not self.isRunning):
                break
            try:
                func, args, kwargs = self.get()
                func(*args, **kwargs)
            except Exception, details:
                print >>sys.stderr, '(%s._worker).Error :: "%s".' % (self.__class__,str(details))
		print >>sys.stderr, traceback.format_exc()
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

    isRunning = property(getIsRunning, setIsRunning)

_threadQ = ThreadQueue(1000)

def threadify(threadQ):
    assert threadQ.__class__ == ThreadQueue, 'threadify decorator requires a ThreadQueue object instance'
    def decorator(func):
        def proxy(*args, **kwargs):
            threadQ.put((func, args, kwargs))
            return threadQ
        return proxy
    return decorator

@threadify(_threadQ)
def portListener(obj, ipAddr, port, sShutdown, aCallbackFunc, isController=False):
    b = rubyPythonBridge(ipAddr, port, sShutdown, aCallbackFunc)
    b.isController = isController
    print 'b=(%s)' % (str(b))
    b.startup()
    if (obj):
	obj.deallocate_port(port)

@threadify(_threadQ)
def _portListener(ipAddr, port, sShutdown, aCallbackFunc, isController=False):
    b = rubyPythonBridge(ipAddr, port, sShutdown, aCallbackFunc)
    b.isController = isController
    print 'Bridge Spawned Worker as (%s)' % (str(b))
    b.startup()

class rubyPythonBridge():
    def __init__(self, ipAddr, port, sShutdown, aCallbackFunc, portMap={}):
        self.__context1__ = {}
        self.__context2__ = {}
        self.__sShutdown__ = sShutdown
        self.__ipAddr__ = ipAddr
        self.__port__ = port
        self.__isController__ = True
        self.__callback__ = aCallbackFunc
        self.__portmap__ = portMap
        self.allocate_port(port)
        
    def __repr__( self):
        return '%s.rubyPythonBridge :: ipAddr=(%s), sShutdown=(%s), port=(%s), isController=(%s)' % (__name__, str(self.ipAddr),str(self.sShutdown),str(self.port),self.isController)
        
    def allocate_port(self,port):
	_port = '%d' % port
        if (port in _worker_ports):
	    if (not self.__portmap__.has_key(_port)):
		self.__portmap__[_port] = port
        elif (port in _controller_ports):
	    if (not _controller_portMap.has_key(_port)):
		_controller_portMap[_port] = port
    
    def deallocate_port(self,port):
	_port = '%d' % port
        if (port in _worker_ports):
	    if (self.__portmap__.has_key(_port)):
		del self.__portmap__[_port]
        elif (port in _controller_ports):
	    if (_controller_portMap.has_key(_port)):
		del _controller_portMap[_port]
    
    def get_context1(self):
        return self.__context1__
    
    def set_context1(self,value):
        self.__context1__ = value
        
    def get_context2(self):
        return self.__context2__
    
    def set_context2(self,value):
        self.__context2__ = value
    
    def get_sShutdown(self):
        return self.__sShutdown__
    
    def set_sShutdown(self,value):
        self.__sShutdown__ = value
    
    def get_ipAddr(self):
        return self.__ipAddr__
    
    def set_ipAddr(self,value):
        self.__ipAddr__ = value
    
    def get_port(self):
        return self.__port__
    
    def set_port(self,value):
        self.__port__ = value
    
    def get_portmap(self):
        return self.__portmap__
    
    def set_portmap(self,value):
        self.__portmap__ = value
    
    def get_callback(self):
        return self.__callback__
    
    def set_callback(self,value):
        self.__callback__ = value
    
    def get_isController(self):
        return self.__isController__
    
    def set_isController(self,value):
        self.__isController__ = value
    
    context1 = property(get_context1,set_context1)
    context2 = property(get_context2,set_context2)
    sShutdown = property(get_sShutdown,set_sShutdown)
    ipAddr = property(get_ipAddr,set_ipAddr)
    port = property(get_port,set_port)
    callback = property(get_callback,set_callback)
    portmap = property(get_portmap,set_portmap)
    isController = property(get_isController,set_isController)
    
    def getNextPort(self):
        ports = [int(n) for n in self.portmap.keys()]
        ports.sort()
        nMin = ports[0] if len(ports) > 0 else _worker_ports[0]
        while (self.portmap.has_key('%d'%nMin)):
            nMin += 1
            if (nMin > _worker_ports[-1]):
                return None
        n = nMin
        if (n <= _worker_ports[-1]):
            self.allocate_port(n)
            return n
        return None
    
    def getNextControllerPort(self):
        ports = [int(n) for n in _controller_portMap.keys()]
        ports.sort()
        nMin = ports[0] if len(ports) > 0 else _controller_ports[0]
        while (_controller_portMap.has_key('%d'%nMin)):
            nMin += 1
            if (nMin > _controller_ports[-1]):
                return None
        n = nMin
        if (n <= _controller_ports[-1]):
            self.allocate_port(n)
            return n
        return None
    
    def startup(self,proxy=None):
	if (not isinstance(proxy,ReverseProxy)):
	    # When ReverseProxy is used the asyncore.loop() handles this part of the process...
	    mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
	    print '%s.startup() :: self.ipAddr=[%s], self.port=[%s]' % (self.__class__,self.ipAddr,self.port)
	    mySocket.bind ( ( self.ipAddr, self.port) )
	    mySocket.listen ( 1 )
	    channel, details = mySocket.accept()
	    print '(%s) Opened a connection with "%s".' % (self.port,details)
	    while True:
		val = ''
		cmd = channel.recv(8192)
		_cmd = str(cmd)
		if (len(_cmd) > 0):
		    print '(%s) Received... (%s) [%s bytes]' % (self.port,_cmd,len(_cmd))
		    if (_cmd == self.sShutdown):
			print '(%s) Shutdown Received...' % (self.port)
			channel.close()
			self.deallocate_port(self.port)
			if (self.port in _controller_ports):
			    portListener(self,self.ipAddr,self.port,self.sShutdown,self.callback,True)
			return
		    elif (_cmd == __newConnection__):
			if (self.isController):
			    nextPort = self.getNextPort()
			    if (nextPort != None):
				val = '<port>%d</port>' % (nextPort)
				portListener(self,self.ipAddr,nextPort,self.sShutdown,self.callback,False)
			    else:
				val = '<port_error>-1</port_error>'
			else:
			    val = '<port_error>-2</port_error>'
		    else:
			try:
			    if (type(self.callback) == types.FunctionType):
				val = self.callback(_cmd, [self.ipAddr,self.port,self.sShutdown], self.context2)
			    else:
				val = '(ECHO)::(_cmd=[%s], self.context1=[%s], self.context2=[%s])' % (_cmd, self.context1, self.context2)
			except Exception, details:
			    val = str(details)
		    print '(%s) Sending... (%s bytes)' % (self.port,len(val))
		    if len(val) < 1000:
			print '%s' % val
		    channel.send(str(val))

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
	print >> sys.stderr, msg
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
		print >> sys.stderr, 'ERROR in firing callback for Error Handler due to "%s".' % str(details)

    logPath = property(get_logPath,set_logPath)
    callback = property(get_callback,set_callback)

def asXML(ret,ioTime=0.0):
    s = '%-10.2f' % ioTime
    xml = '<data iotime_seconds="%s">' % s.strip()
    try:
	if (isinstance(ret,list)):
	    for l in ret:
		xml += '<id value="%s"/>' % (l)
	else:
	    for k in ret.keys():
		v = ret[k]
		r = {}
		_xml = ''
		for vk in v.keys():
		    if (vk != k):
			_xml += '<%s>%s</%s>' % (vk,v[vk],vk)
		    r[v[vk]] = vk
		n = 'key'
		if (r.has_key(k)):
		    n = r[k]
		xml += '<item %s="%s">' % (n,k)
		xml += _xml
		xml += '</item>'
    except Exception, details:
        print 'ERROR due to "%s".' % details
	traceback.print_exc()
    xml += '</data>'
    return xml

def getSalesForceContext():
    from pyax.context import Context

    _ctx = Context()

    @addto(_ctx)
    def get__login_servers(self):
	try:
	    return self.__dict__['_Context__login_servers']
	except:
	    pass
	return []
    
    return _ctx

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
	print 'ERROR due to "%s".' % str(details)
    for saveResultItem in saveResult:
	if (saveResultItem.has_key('errors')):
	    for k,v in saveResultItem['errors'].iteritems():
		print '%s=%s' % (k,v)

    return idList
    
def createSalesForceObject(sfdc,className,contents):
    from pyax.sobject.classfactory import ClassFactory

    idList = []
    try:
	obj = ClassFactory(sfdc, className)
	saveResult = sfdc.create(obj, contents)
	idList = checkSaveResult(saveResult)
    except Exception, details:
	print 'ERROR due to "%s".' % str(details)
    return idList

def deleteSalesForceObject(sfdc,contents):
    deleted_ids = []
    try:
        delete_result = sfdc.delete(contents)
        deleted_ids = sfdc.resultToIdList(delete_result, success_status=True)
    except Exception, details:
	print 'ERROR due to "%s".' % str(details)
    return deleted_ids

def updateSalesForceObject(sfdc,className,contents):
    for item in contents:
	id = item[0]
	try:
	    obj = sfdc.retrieve(className, id)
	except:
	    obj = None
	if (obj):
	    for d_attr in item[1:]:
		for k,v in d_attr.iteritems():
		    obj[k] = v
	    try:
		obj.update()
	    except:
		pass
	    pass
	pass
    pass
    
def processSalesForce(args, context1, context2, isStaging=False):
    import sys,time
    from pyax.connection import Connection
    from pyax.exceptions import ApiFault

    if (len(args) == 3):
	_username, _password, soql = args
    elif (len(args) in [4,5]):
	if (len(args) == 4):
	    _username, _password, soql, isStaging = args
	elif (len(args) == 5):
	    _username, _password, _token, soql, isStaging = args
	isStaging = booleanize(isStaging)
    print '\n'
    print '='*80
    print '_username=[%s]' % _username
    print '_password=[%s]' % _password
    print '_token=[%s]' % _token
    print 'soql=[%s]' % soql
    print 'isStaging=[%s]' % isStaging
    print 'context1=[%s]' % context1
    print 'context2=[%s]' % context2
    try:
        _beginTime = time.time()
	_ctx = getSalesForceContext()
	if (isStaging):
	    _srvs = _ctx.get__login_servers()
	    if (_srvs.has_key('production')) and (_srvs.has_key('sandbox')):
		_ctx.login_endpoint = _ctx.login_endpoint.replace(_srvs['production'],_srvs['sandbox'])
	    _end = _ctx.login_endpoint
        sfdc = Connection.connect(_username, _password, token=_token, context=_ctx)
	print 'sfdc.endpoint=[%s]' % sfdc.endpoint
	if (isinstance(soql,dict)):
	    className = ''
	    if (soql.has_key(const_tableName_symbol)):
		className = soql[const_tableName_symbol]
	    isProcessingCreation = False
	    if (soql.has_key(const_isProcessingCreation_symbol)):
		isProcessingCreation = soql[const_isProcessingCreation_symbol]
	    isProcessingDeletion = False
	    if (soql.has_key(const_isProcessingDeletion_symbol)):
		isProcessingDeletion = soql[const_isProcessingDeletion_symbol]
	    isProcessingUpdate = False
	    if (soql.has_key(const_isProcessingUpdate_symbol)):
		isProcessingUpdate = soql[const_isProcessingUpdate_symbol]
	    contents = []
	    if (soql.has_key(const_contents_symbol)):
		contents = listify(soql[const_contents_symbol])
	    if (isProcessingCreation):
		val = createSalesForceObject(sfdc,className,contents)
	    if (isProcessingDeletion):
		val = deleteSalesForceObject(sfdc,contents)
	    if (isProcessingUpdate):
		val = updateSalesForceObject(sfdc,className,contents)
	else:
	    val = sfdc.query(soql)
        _endTime = time.time()
        ret = asXML(val,_endTime-_beginTime)
    except ApiFault, details:
        print 'ERROR due to "%s".' % (details)
        traceback.print_exc()
        ret = '<error>%s</error>' % details
    print '='*80
    print '\n'
    return ret

def getAttrFromNode(node,name):
    value = ''
    try:
	if (node.hasAttribute(name)):
	    value = decodeUnicode(node.getAttribute(name))
    except:
	pass
    return value

def getNodeText(node):
    from xml.dom import Node
    rc = ""
    if (node.nodeType == Node.TEXT_NODE):
	rc += node.data
    return decodeUnicode(str(rc))

def getAllNodeText(nodelist):
    rc = ""
    for node in nodelist:
	rc += getNodeText(node)
    return rc

def getAttrsFromNode(node):
    _attrs = {}
    try:
	attrs = node.attributes
	for attrName in attrs.keys():
	    _attrs[attrName] = attrs.get(attrName).nodeValue
    except:
	pass
    return _attrs

def xmlToDict(xml):
    from xml.dom.minidom import parse, parseString
    
    _dict = {}
    docs = [parseString(d) for d in xml.split('\x00')]
    for doc in docs:
	_data = doc.getElementsByTagName("data")
	for d in _data:
	    _dict['data'] = getAttrsFromNode(d)
	_items = doc.getElementsByTagName("item")
	for item in _items:
	    _item = {}
	    _attrs = getAttrsFromNode(item)
	    _key = ''
	    if (_attrs.has_key('Id')):
		_key = _attrs['Id']
	    if (len(_key) > 0):
		for child in item.childNodes:
		    _attrs = getAttrsFromNode(child)
		    _text = getNodeText(child)
		    if (len(_text) == 0):
			_text = getAllNodeText(child.childNodes)
		    _item['attributes'] = _attrs
		    _item[child.nodeName] = _text
		_dict[_key] = _item
	    pass
    return _dict

def salesForceConnector(_cmd, _context1={}, _context2={}):
    from xml.dom.minidom import parse, parseString

    value = ''
    try:
	if (len(_cmd) > 0):
	    _username = ''
	    _password = ''
	    _token = ''
	    _staging = '0'
	    _soql = ''
	    _isProcessingSOQL = False
	    _tableName = ''
	    _contents = {}
	    contents = []
	    _isProcessingCreation = False
	    _isProcessingDeletion = False
	    _isProcessingUpdate = False
	    docs = [parseString(d) for d in _cmd.split('\x00')]
	    for doc in docs:
		_bridges = doc.getElementsByTagName("bridge")
		for b in _bridges:
		    _username = getAttrFromNode(b,'username')
		    _password = getAttrFromNode(b,'password')
		    _token = getAttrFromNode(b,'token')
		    _staging = booleanize(getAttrFromNode(b,'staging'))
		    _soqls = b.getElementsByTagName("soql")
		    if (len(_soqls) > 0):
			_isProcessingSOQL = True
			for s in _soqls:
			    _soql = getAllNodeText(s.childNodes)
		    _new_objs = b.getElementsByTagName("create")
		    if (len(_new_objs) > 0):
			_isProcessingCreation = True
			for o in _new_objs:
			    _tableName = getAttrFromNode(o,'table')
			    for c in o.childNodes:
				_name = getAttrFromNode(c,'name')
				_value = getAttrFromNode(c,'value')
				_contents[_name] = _value
			    contents.append(_contents)
			    pass
		    _new_objs = b.getElementsByTagName("delete")
		    if (len(_new_objs) > 0):
			_isProcessingDeletion = True
			for o in _new_objs:
			    contents = []
			    _tableName = getAttrFromNode(o,'table')
			    for c in o.childNodes:
				_id = getAttrFromNode(c,'id')
				contents.append(_id)
			    pass
		    _new_objs = b.getElementsByTagName("update")
		    if (len(_new_objs) > 0):
			_isProcessingUpdate = True
			for o in _new_objs:
			    contents = []
			    item = []
			    _tableName = getAttrFromNode(o,'table')
			    for c in o.childNodes:
				_id = getAttrFromNode(c,'id')
				item.append(_id)
				for cc in c.childNodes:
				    cc_attrs = getAttrsFromNode(cc)
				    cc_d = {}
				    if (cc_attrs.has_key('name')) and (cc_attrs.has_key('value')):
					cc_d[cc_attrs['name']] = cc_attrs['value']
				    item.append(cc_d)
				contents.append(item)
				item = []
				pass
			    pass
	    try:
		if (_isProcessingCreation):
		    _soql = {const_isProcessingCreation_symbol : _isProcessingCreation, const_tableName_symbol : _tableName, const_contents_symbol : contents}
		if (_isProcessingDeletion):
		    _soql = {const_isProcessingDeletion_symbol : _isProcessingDeletion, const_tableName_symbol : _tableName, const_contents_symbol : contents}
		if (_isProcessingUpdate):
		    _soql = {const_isProcessingUpdate_symbol : _isProcessingUpdate, const_tableName_symbol : _tableName, const_contents_symbol : contents}
		return processSalesForce([_username,_password,_token,_soql,_staging], _context1, _context2)
	    except Exception, details:
		value = 'ERROR %s' % details
	pass
    except:
	pass
    if (len(value) == 0):
	try:
	    return processSalesForce(_cmd.split('||'), _context1, _context2)
	except Exception, details:
	    value = 'ERROR %s' % details
    return value

def spawnListenersForAllButBasePort(obj):
    for port in [p for p in _controller_ports][1:]:
        portListener(obj,obj.ipAddr,port,obj.sShutdown,obj.callback,True)

def startPythonController(ipAddr,shutdown,callback,proxy=None):
    global _controller_ports, _worker_ports
    if (isinstance(proxy,ReverseProxy)):
	_controller_ports = proxy._controller_ports
	_worker_ports = proxy._worker_ports
    port = _controller_ports[0]
    portMap = {}
    if (not isinstance(proxy,ReverseProxy)):
	b = rubyPythonBridge(ipAddr,port,shutdown,callback,portMap)
	spawnListenersForAllButBasePort(b)
	print 'b=(%s)' % (str(b))
	b.startup(proxy)
	portMap = b.portmap
    else:
	pass
    _port = '%d'%port
    if (portMap.has_key(_port)):
	del portMap[_port]
    print 'Python Controller is waiting for _threadQ.'
    _threadQ.join()
    print 'Python Controller has ended.'

def myeval(statement, globals_=None, locals_=None): 
    try: 
        return eval(statement, globals_, locals_) 
    except SyntaxError: 
        if locals_ is None: 
            import inspect 
            locals_ = inspect.currentframe().f_back.f_locals 
        exec statement in globals_, locals_ 

class ReverseProxy(asyncore.dispatcher):
    def __init__(self, ip, port, remoteip, remoteport, sShutdown='xxxShutdownxxx', backlog=5):
	global _controller_ports, _worker_ports
        asyncore.dispatcher.__init__(self)
        self.remoteip = remoteip
        self.remoteport = remoteport
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip,port))
	num_ports = len(self.remoteport) if (isinstance(self.remoteport,xrange)) else 1
	self.backlog = num_ports
        self.listen(self.backlog)
	self._controller_ports = _controller_ports = xrange(55555,55555+num_ports-1)
	self._worker_ports = _worker_ports = xrange(60000,60000+num_ports-1)
	self.__next_port__ = self._worker_ports[0]
	self.__shutdown__ = sShutdown
        print '--- Bridge Ready for Connections --- '
	
    def handle_connections(self):
        print '--- Bridge Waiting for Connections --- '
	asyncore.loop()

    def handle_accept(self):
        conn, addr = self.accept()
        print '--- Connect --- '
	_p = p = self.nextPort
	p += 1
	if (p not in self._worker_ports):
	    p = self._worker_ports[0]
	self.nextPort = p
	# Spawn a Bridge thread now and connect it to the caller...
	_portListener(self.remoteip,_p,self.shutdown,salesForceConnector,False)
        sender(receiver(conn,self.shutdown),self.remoteip,_p)

    @Property
    def nextPort():
	def fget(self):
	    return self.__next_port__
	def fset(self,port):
	    self.__next_port__ = port
    
    @Property
    def shutdown():
	def fget(self):
	    return self.__shutdown__
	def fset(self,sShutdown):
	    self.__shutdown__ = sShutdown
    
class receiver(asyncore.dispatcher):
    def __init__(self,conn,shutdown):
        asyncore.dispatcher.__init__(self,conn)
        self.from_remote_buffer = ''
        self.to_remote_buffer = ''
        self.sender = None
	self.shutdown = shutdown

    def handle_connect(self):
        print '(%s.handle_connect)' % (self.__class__)
        pass

    def handle_read(self):
        read = self.recv(4096)
        print '(%s.handle_read) %04i --> [%s]' % (self.__class__,len(read),read)
        self.from_remote_buffer += read

    def writable(self):
        return (len(self.to_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.to_remote_buffer)
        print '(%s.handle_write) %04i <--' % (self.__class__,sent)
        self.to_remote_buffer = self.to_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        print '(%s.handle_close)' % (self.__class__)
        if (self.sender):
	    print '(%s.handle_close) self.sender=[%s]' % (self.__class__,self.sender)
	    self.sender.send(self.shutdown)
            self.sender.close()

class sender(asyncore.dispatcher):
    def __init__(self, receiver, remoteaddr, remoteport):
        asyncore.dispatcher.__init__(self)
        self.receiver=receiver
        receiver.sender=self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((remoteaddr, remoteport))

    def handle_connect(self):
        print '(%s.handle_connect)' % (self.__class__)
        pass

    def handle_read(self):
        read = self.recv(4096)
        print '(%s.handle_read) %04i -->' % (self.__class__,len(read))
        self.receiver.to_remote_buffer += read

    def writable(self):
        return (len(self.receiver.from_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.receiver.from_remote_buffer)
        print '(%s.handle_write) %04i <--' % (self.__class__,sent)
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[sent:]

    def handle_close(self):
        print '(%s.handle_close)' % (self.__class__)
        self.close()
        self.receiver.close()

if (__name__ == '__main__'):
    print 'Copyright 2007-2008, Hierarchical Applications Limited, Inc., All Rights Reserved., Licensed under LGPL License Restricted to non-commercial educational use only.'
