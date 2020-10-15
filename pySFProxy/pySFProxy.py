import os, sys
import socket,asyncore
import logging
from vyperlogix.misc import _utils
from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint
from vyperlogix.logging import standardLogging
from vyperlogix.misc import ObjectTypeName
import traceback

_isBeingDebugged = (os.environ.has_key('WINGDB_ACTIVE')) # When debugger is being used we do not use threads...

_isVerbose = False

class ReverseProxy(asyncore.dispatcher):
    def __init__(self, ip, port, remoteip,remoteport,backlog=5):
        asyncore.dispatcher.__init__(self)
        self.remoteip=remoteip
        self.remoteport=remoteport
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip,port))
        self.listen(backlog)

    def handle_accept(self):
        conn, addr = self.accept()
	logging.info('--- Connect --- ')
        sender(receiver(conn),self.remoteip,self.remoteport)

class receiver(asyncore.dispatcher):
    def __init__(self,conn):
        asyncore.dispatcher.__init__(self,conn)
        self.from_remote_buffer=''
        self.to_remote_buffer=''
        self.sender=None

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(4096)
	logging.info('(%s.%s) %04i --> [%s]' % (ObjectTypeName.typeName(self),_utils.funcName(),len(read),read))
        self.from_remote_buffer += read

    def writable(self):
        return (len(self.to_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.to_remote_buffer)
	logging.info('(%s.%s) %04i <--' % (ObjectTypeName.typeName(self),_utils.funcName(),sent))
        self.to_remote_buffer = self.to_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()

class sender(asyncore.dispatcher):
    def __init__(self, receiver, remoteaddr,remoteport):
        asyncore.dispatcher.__init__(self)
        self.receiver=receiver
        receiver.sender=self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((remoteaddr, remoteport))

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(4096)
	logging.info('(%s.%s) %04i -->' % (ObjectTypeName.typeName(self),_utils.funcName(),len(read)))
        self.receiver.to_remote_buffer += read

    def writable(self):
        return (len(self.receiver.from_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.receiver.from_remote_buffer)
	logging.info('(%s.%s) %04i <--' % (ObjectTypeName.typeName(self),_utils.funcName(),sent))
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        self.receiver.close()

def ip_port_split(ip):
    toks = ip.split(':')
    _ip = toks[0]
    _port = 80 if (len(toks) == 1) else 80 if (not str(toks[-1]).isdigit()) else int(toks[-1])
    return (_ip,_port)

def exception_callback(sections):
    _msg = 'EXCEPTION Causing Abend.\n%s' % '\n'.join(sections)
    print >>sys.stdout, _msg
    print >>sys.stderr, _msg
    logging.error(_msg)
    sys.exit(0)

from vyperlogix.decorators import onexit
@onexit.onexit
def _onExit():
    import os, sys
    _msg = 'SHUTDOWN !'
    print >>sys.stdout, _msg
    print >>sys.stderr, _msg
    _msg = 'END! ReverseProxy !'
    print >>sys.stdout, _msg
    print >>sys.stderr, _msg

if __name__=='__main__':
    def ppArgs():
        pArgs = [(k,args[k]) for k in args.keys()]
        pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
        pPretty.pprint()

    args = {'--verbose':'output more stuff.',
            '--cwd=?':'the path the program runs from, defaults to the path the program runs from.',
            '--local-ip=?':'the ip address for the local interface, defaults to 127.0.0.1:80, may use the form of ip:port.',
            '--local-port=?':'the local port, defaults to 80',
            '--remote-ip=?':'the ip address for the remote interface, does not default, must be supplied, may use the form of ip:port.',
            '--remote-port=?':'the remote port, defaults to 80',
            '--logging=?':'[logging.INFO,logging.WARNING,logging.ERROR,logging.DEBUG]',
            '--console_logging=?':'[logging.INFO,logging.WARNING,logging.ERROR,logging.DEBUG]'}
    _argsObj = Args.Args(args)
    if (_isVerbose):
        print '_argsObj=(%s)' % str(_argsObj)

    print '_isBeingDebugged=%s' % _isBeingDebugged
    print 'sys.version=[%s]' % sys.version
    v = _utils.getFloatVersionNumber()
    if (v >= 2.51):
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
		logging.warning('(%s) :: %s' % (_utils.funcName(),info_string))
		_isVerbose = False
    
	    __cwd = os.path.dirname(sys.argv[0])
	    try:
		__cwd = _argsObj.arguments['cwd'] if _argsObj.arguments.has_key('cwd') else __cwd
		if (len(__cwd) == 0) or (not os.path.exists(__cwd)):
		    if (os.environ.has_key('cwd')):
			__cwd = os.environ['cwd']
	    except:
		pass
	    _cwd = __cwd
	    
	    _local_ip, _local_port = ip_port_split('127.0.0.1:80')
	    try:
		__local_ip = _argsObj.arguments['local-ip'] if _argsObj.arguments.has_key('local-ip') else '127.0.0.1:80'
		_local_ip, _local_port = ip_port_split(__local_ip)
	    except:
		exc_info = sys.exc_info()
		info_string = '\n'.join(traceback.format_exception(*exc_info))
		logging.warning('(%s) :: %s' % (_utils.funcName(),info_string))
		_local_ip, _local_port = ip_port_split('127.0.0.1:80')
	    
	    try:
		__local_port = _argsObj.arguments['local-port'] if _argsObj.arguments.has_key('local-port') else _local_port
		_local_ip, _local_port = ip_port_split('%s:%s' % (_local_ip,__local_port))
	    except:
		exc_info = sys.exc_info()
		info_string = '\n'.join(traceback.format_exception(*exc_info))
		logging.warning('(%s) :: %s' % (_utils.funcName(),info_string))
		_local_ip, _local_port = ip_port_split('%s:80' % (_local_ip))
	    
	    _remote_ip, _remote_port = ip_port_split('cs1.salesforce.com:80')
	    try:
		__remote_ip = _argsObj.arguments['remote-ip'] if _argsObj.arguments.has_key('remote-ip') else ''
		_remote_ip, _remote_port = ip_port_split(__remote_ip)
	    except:
		exc_info = sys.exc_info()
		info_string = '\n'.join(traceback.format_exception(*exc_info))
		logging.warning('(%s) :: %s' % (_utils.funcName(),info_string))
		_remote_ip, _remote_port = ip_port_split('cs1.salesforce.com:80')
	    
	    try:
		__remote_port = _argsObj.arguments['remote-port'] if _argsObj.arguments.has_key('remote-port') else _remote_port
		_remote_ip, _remote_port = ip_port_split('%s:%s' % (_remote_ip,__remote_port))
	    except:
		exc_info = sys.exc_info()
		info_string = '\n'.join(traceback.format_exception(*exc_info))
		logging.warning('(%s) :: %s' % (_utils.funcName(),info_string))
		_remote_ip, _remote_port = ip_port_split('%s:80' % (_remote_ip))
	    
	    _logging = logging.WARNING
	    try:
		_logging = eval(_argsObj.arguments['logging']) if _argsObj.arguments.has_key('logging') else False
	    except:
		_logging = logging.WARNING
		
	    _console_logging = logging.WARNING
	    try:
		_console_logging = eval(_argsObj.arguments['console_logging']) if _argsObj.arguments.has_key('console_logging') else False
	    except:
		_console_logging = logging.WARNING
    
	    if (not _isBeingDebugged):
		from vyperlogix.handlers.ExceptionHandler import *
		excp = ExceptionHandler()
		excp.callback = exception_callback
	    
	    if (len(_cwd) > 0) and (os.path.exists(_cwd)):
		name = _utils.getProgramName()
		_log_path = _utils.safely_mkdir_logs(_cwd)
		logFileName = os.sep.join([_log_path,'%s.log' % (name)])
		
		standardLogging.standardLogging(logFileName,_level=_logging,console_level=_console_logging,isVerbose=_isVerbose)
		
		logging.warning('Logging to "%s" using level of "%s:.' % (logFileName,standardLogging.explainLogging(_logging)))
	    
		logging.info('BEGIN: ReverseProxy !')
		logging.info('_local_ip = %s, _local_port = %s' % (_local_ip,_local_port))
		logging.info('_remote_ip = %s, _remote_port = %s' % (_remote_ip,_remote_port))
		ReverseProxy(_local_ip,_local_port,_remote_ip,_remote_port)
		asyncore.loop()
	    else:
		logging.error('Cannot figure-out where to put the log files. Sorry !')
    else:
	logging.error('You are using the wrong version of Python, you should be using 2.51 or later but you seem to be using "%s".' % sys.version)

