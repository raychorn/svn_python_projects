import sys, os
import types
import logging
import glob
import string

from vyperlogix.misc import _utils
from vyperlogix import misc
from vyperlogix.classes.CooperativeClass import Cooperative
from vyperlogix.misc import ObjectTypeName

from vyperlogix.logging.standardLogging import LoggingLevels

__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

                   All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

class Log(Cooperative):
    """file like for writes with auto flush after each write
    to ensure that everything is logged, even during an
    unexpected exit."""
    def __init__(self, f):
        self.f = f
        logging.info('Init Log for "%s".' % (self.logFileName))
        
    def fileno(self):
        return self.f.fileno()
    
    def write(self, s):
        if (self.f):
            try:
		try:
		    self.f.flush()
		except:
		    pass
                self.f.write(s)
            except Exception, details:
                info_string = _utils.formattedException(details=details)
                logging.warning(info_string)
            
    def rotate(self):
	_fname = self.logFileName
        logging.info('Rotate Log for "%s".' % (_fname))
        ts = _utils.timeStamp()
        if (sys.platform == 'win32'):
            ts = ts.replace(':','-')
        _fh = open('%s_%s.log' % ('_'.join(_fname.split('_')[0:-1]),ts),'w')
        self.f.flush()
        self.f.seek(0)
        _fh.writelines('\n'.join(self.f.readlines()))
        _fh.close()
        self.f.truncate()
        
    def prune(self,pattern,_max):
        logging.info('Prune Log for "%s".' % (self.logFileName))
        files = misc.sort(glob.glob(pattern))
        numToDelete = len(files) - _max
        if (numToDelete > 0):
            for f in files[0:numToDelete]:
                try:
                    os.remove(f)
                    logging.info('(%s) :: Removed "%s".' % (misc.funcName(),f))
		except Exception, details:
		    info_string = _utils.formattedException(details=details)
		    logging.warning(info_string)
		
    def logFileName():
        doc = "The log's filename, if it exists."
        def fget(self):
	    _name = 'Log File is NOT Named.'
	    _className = ObjectTypeName.typeClassName(self.f)
	    if (_className not in ['StringIO.StringIO','cStringIO.StringO']):
		try:
		    _name = self.f.name
		except AttributeError, details:
		    info_string = _utils.formattedException(details=details)
		    logging.warning(info_string)
	    else:
		_name = _className
	    return _name
        return locals()
    logFileName = property(**logFileName())

    def close(self):
        logging.info('Closing Log for "%s".' % (self.logFileName))
	try:
	    self.f.close()
	except Exception, details:
	    info_string = _utils.formattedException(details=details)
	    logging.warning(info_string)

    def flush(self):
	try:
	    self.f.flush()
	except Exception, details:
	    info_string = _utils.formattedException(details=details)
	    logging.warning(info_string)

    def getLogger(self, name): # do nothing for now.  This method exists to suppress errors and warnings.
	pass
	    
    def name():
        doc = "name"
        def fget(self):
	    _name = 'Log File is NOT Named.'
	    try:
		_name = self.f.name
	    except AttributeError, details:
                info_string = _utils.formattedException(details=details)
                logging.warning(info_string)
	    return _name
        return locals()
    name = property(**name())

class EchoLog(Log):
    """file like for writes with auto flush after each write
    to ensure that everything is logged and echoed to sys.stdout,
    even during an unexpected exit."""
    def __init__(self, f, fOut=sys.stdout):
	self.fOut = fOut
	super(EchoLog, self).__init__(f)
        
    def write(self, s):
	_typeName = ObjectTypeName.typeClassName(self.fOut)
	if (_typeName.find('.EchoLog') == -1):
	    print >>self.fOut, s.strip()
	super(EchoLog, self).write(s)
    
class BackgroundLog(Log):
    """file like for writes that dump to sys.stdout in the background.
    """
    def __init__(self, threads=100, fOut=sys.stdout):
	from vyperlogix.misc import threadpool
	
	self._Q_ = threadpool.ThreadQueue(threads,isDaemon=False)

	@threadpool.threadify(self._Q_)
	def log_this(s,callback=None):
	    from vyperlogix.decorators.synchronized import synchronized
	    from threading import Lock
	    myLock = Lock()
	    
	    @synchronized(myLock)
	    def _log_this(s,callback):
		if (callable(callback)):
		    try:
			callback(s)
		    except:
			pass
		
	    _log_this(s,callback)
	    
	self.log_this = log_this
	    
	super(BackgroundLog, self).__init__(fOut)
        
    def logFileName():
        doc = "The log's filename, if it exists."
        def fget(self):
	    _name = 'Log File is NOT Named.'
	    try:
		_name = self.f.name
	    except AttributeError, details:
                info_string = _utils.formattedException(details=details)
                logging.warning(info_string)
	    return _name
        return locals()
    logFileName = property(**logFileName())

    def write(self, s):
	self.log_this(s,callback=super(BackgroundLog, self).write)
    
if hasattr(sys, 'frozen'): #support for py2exe
    _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])
elif string.lower(__file__[-4:]) in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)

def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        return sys.exc_traceback.tb_frame.f_back
    
if hasattr(sys, '_getframe'): currentframe = lambda: sys._getframe(3)

class CustomLog(Log):
    """Use in-place of logging, provides INFO, WARNING, DEBUG and ERROR logging to a single log-file."""
    def __init__(self, f):
	self.__logging__ = None
	super(CustomLog, self).__init__(f)
    
    def logging():
        doc = "Echo to this logging instance also."
        def fget(self):
	    return self.__logging__
        def fset(self, log):
	    self.__logging__ = log
        return locals()
    logging = property(**logging())

    def findCaller(self):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe().f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            rv = (filename, f.f_lineno, co.co_name)
            break
        return rv

    def log_as(self, _levelName, s):
	if (self.__logging__ is not None):
	    try:
		if (_levelName == 'INFO'):
		    self.__logging__.info(s)
		if (_levelName == 'WARNING'):
		    self.__logging__.warning(s)
		if (_levelName == 'DEBUG'):
		    self.__logging__.debug(s)
		if (_levelName == 'ERROR'):
		    self.__logging__.error(s)
	    except:
		pass
	fn, lno, func = self.findCaller()
	super(CustomLog, self).write('%s :: %s :: %s\n' % (_levelName,'%s %s' % (fn, lno),s))
    
    def info(self, s):
	self.log_as('INFO', s)
    
    def warning(self, s):
	self.log_as('WARNING', s)
    
    def warn(self, s):
	self.log_as('WARNING', s)
    
    def debug(self, s):
	self.log_as('DEBUG', s)
    
    def error(self, s):
	self.log_as('ERROR', s)
	
def dummy():
    pass

class Daemon:
    def __init__(self,name='pydaemon',func=dummy,dirName=''):
        self.__LOGFILE__ = '/var/log/%s.log' % name
        self.__PIDFILE__ = '/var/run/%s.pid' % name
        self.__USERPROG__ = func if callable(func) else dummy
        self.__DIRNAME__ = dirName if (os.path.exists(dirName)) else ''

        # do the UNIX double-fork magic, see Stevens' "Advanced
        # Programming in the UNIX Environment" for details (ISBN 0201563177)
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
            sys.exit(1)
        
        # decouple from parent environment
        os.chdir("/")   #don't prevent unmounting....
        os.setsid()
        os.umask(0)
        
        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent, print eventual PID before
                print "Daemon PID %d" % pid
                try:
                    fh = open(self.PIDFILE,'w')
                except:
                    exc_info = sys.exc_info()
                    info_string = '\n'.join(traceback.format_exception(*exc_info))
                    print >>sys.stderr, info_string
                    print >>sys.stderr, 'Cannot continue...'
                    sys.exit(0)
                fh.write("%d"%pid)
                fh.flush()
                fh.close()
                sys.exit(0)
        except OSError, e:
            print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
            sys.exit(1)
        
        # start the daemon main loop
        #change to data directory if needed
        if (os.path.exists(self.DIRNAME)):
            os.chdir(self.DIRNAME)
        #redirect outputs to a logfile
        try:
            fh = open(self.LOGFILE,'a+')
        except:
            exc_info = sys.exc_info()
            info_string = '\n'.join(traceback.format_exception(*exc_info))
            print >>sys.stderr, info_string
            print >>sys.stderr, 'Cannot continue...'
            sys.exit(0)
        sys.stdout = sys.stderr = Log(fh)
        #ensure the that the daemon runs a normal user
        os.setegid(103)     #set group first "pydaemon"
        os.seteuid(103)     #set user "pydaemon"
        #start the user program here:
        try:
            self.USERPROG()
        except:
            exc_info = sys.exc_info()
            info_string = '\n'.join(traceback.format_exception(*exc_info))
            print >>sys.stderr, info_string
    
    def get_LOGFILE(self):
        return self.__LOGFILE__
    
    def set_LOGFILE(self,fname):
        self.__LOGFILE__ = fname
    
    def get_PIDFILE(self):
        return self.__PIDFILE__
    
    def set_PIDFILE(self,fname):
        self.__PIDFILE__ = fname
    
    def get_USERPROG(self):
        return self.__USERPROG__
    
    def get_DIRNAME(self):
        return self.__DIRNAME__

    LOGFILE = property(get_LOGFILE,set_LOGFILE)
    PIDFILE = property(get_PIDFILE,set_PIDFILE)
    USERPROG = property(get_USERPROG)
    DIRNAME = property(get_DIRNAME)

def redirectStdErrOutWrapper(func=dummy,args=[],top=os.path.abspath('.')):
    info_string = ''
    if (callable(func)):
	_stderr = sys.stderr
	_stdout = sys.stdout
	fStderr = open(os.sep.join([top,'stderr.txt']),'w')
	fStdout = open(os.sep.join([top,'stdout.txt']),'w')
	sys.stdout = daemon.Log(fStdout)
	sys.stderr = daemon.Log(fStderr)
	try:
	    ret = func(args)
	except:
            exc_info = sys.exc_info()
            info_string = '\n'.join(traceback.format_exception(*exc_info))
	finally:
	    sys.stderr.close()
	    sys.stderr = _stderr
	    sys.stdout.close()
	    sys.stdout = _stdout
	print >>sys.stderr, info_string
    else:
	print >>sys.stderr, '%s :: Cannot process this function due to an error in the parameters, are you sure you are awake ?' % (misc.funcName())
    return ret
