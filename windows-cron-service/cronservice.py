import win32serviceutil
import win32service
import win32event
#import win32evtlogutil
import servicemanager
import re
import os, sys, signal
import tempfile
import time
import Queue

verbose = False
import imp
if (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")):
    import zipfile
    import pkg_resources

    import re
    __regex_libname__ = re.compile(r"(?P<libname>.*)_2_7\.zip", re.MULTILINE)

    my_file = pkg_resources.resource_stream('__main__',sys.executable)

    import tempfile
    __dirname__ = os.path.dirname(tempfile.NamedTemporaryFile().name)

    zip = zipfile.ZipFile(my_file)
    files = [z for z in zip.filelist if (__regex_libname__.match(z.filename))]
    for f in files:
        libname = f.filename
        data = zip.read(libname)
        fpath = os.sep.join([__dirname__,os.path.splitext(libname)[0]])
        __is__ = False
        if (not os.path.exists(fpath)):
            os.mkdir(fpath)
        else:
            fsize = os.path.getsize(fpath)
            if (fsize != f.file_size):
                __is__ = True
        fname = os.sep.join([fpath,libname])
        if (verbose):
            print 'INFO: fname is "%s".' % (fname)
            print 'INFO: __is__ is "%s".' % (__is__)
        if (not os.path.exists(fname)) or (__is__):
            file = open(fname, 'wb')
            file.write(data)
            file.flush()
            file.close()
            if (verbose):
                print 'INFO: fname(2) is "%s".' % (fname)
        __module__ = fname

        import zipextimporter
        zipextimporter.install()
        sys.path.insert(0, __module__)

import ujson
from vyperlogix import misc
from vyperlogix.win import folders
from vyperlogix.misc import _utils
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.crontab import scheduler
from vyperlogix.misc import ObjectTypeName

__json_fpath__ = None
__service_config__ = SmartObject()

__root_symbol__ = '%root%'

import webservice

def makedirs():
    __dirname__ = webservice.__dirname__
    return os.sep.join([__dirname__,vCRON_Service._svc_name_])

from utils import __handler__

import logging
from logging import handlers

def default_logger_init(handle):
    if (misc.isStringValid(handle.baseFilePath)):
        if (os.path.exists(handle.baseFilePath)):
            handle.LOG_FILENAME = os.sep.join([handle.baseFilePath,'cronservice.log'])

            handle.logger = logging.getLogger('cronservice')
            handle.handler = logging.FileHandler(handle.LOG_FILENAME)
            #handle.handler = handlers.TimedRotatingFileHandler(handle.LOG_FILENAME, when='d', interval=1, backupCount=30, encoding=None, delay=False, utc=False)
            #handle.handler = MyTimedRotatingFileHandler(handle.LOG_FILENAME, maxBytes=1000000, when='d', backupCount=30)
            #handle.handler = handlers.RotatingFileHandler(handle.LOG_FILENAME, maxBytes=1000000, backupCount=30, encoding=None, delay=False)
            handle.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            handle.handler.setFormatter(handle.formatter)
            handle.handler.setLevel(logging.INFO)
            handle.logger.addHandler(handle.handler) 
            print 'Logging to "%s".' % (handle.handler.baseFilename)
            
            handle.ch = logging.StreamHandler()
            handle.ch_format = logging.Formatter('%(asctime)s - %(message)s')
            handle.ch.setFormatter(handle.ch_format)
            handle.ch.setLevel(logging.INFO)
            handle.logger.addHandler(handle.ch)
            
            logging.getLogger().setLevel(logging.INFO)

from vyperlogix.misc import threadpool
_Q3_ = threadpool.ThreadQueue(1)

from utils import __logger__

def __SvcDoRun__(self):
    if (self is not None):
        __logger__(__handler__,'INFO: SvcDoRun !!!')
        __logger__(__handler__,'INFO: SERVICE_START_PENDING !!!')
    
    __fpath__ = makedirs()
    __logger__(__handler__,'INFO: __fpath__="%s".' % (__fpath__))
    __fname__ = os.sep.join([__fpath__,'%s.json'%(vCRON_Service._svc_name_)])
    __json__ = _utils.readFileFrom(__fname__,noCRs=True)
    __service_config__ = SmartObject(ujson.loads(__json__))
    __logger__(__handler__,'INFO: __fname__="%s".' % (__fname__))

    schedulefpath = __service_config__.schedulefpath

    __logger__(__handler__,'INFO: Crontab file: "%s".' % (schedulefpath))
    __logger__(__handler__,'INFO: os.path.exists("%s")="%s".' % (schedulefpath,os.path.exists(schedulefpath)))

    from utils import initialize_crontab_if_necessary
    initialize_crontab_if_necessary(__logger__, __handler__, schedulefpath)

    if (self is not None):
        __logger__(__handler__,'INFO: SERVICE_RUNNING !!!')
        servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, ''))
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
    
    if (os.path.exists(schedulefpath)):
        '''
        crontab jobs must specify the windows-service-restart command when performing restart operations.
        '''
        def logger_proxy(msg):
            __logger__(__handler__,msg)
        
        def __mainloop__(self):
            webservice.__start_webservice__(ip_port=__service_config__.webservice)
            __handler__.is_webservice_alive = False

	    from vCronMagicObject import vCronMagicProxy
	    __ws__ = vCronMagicProxy('http://%s' % (__service_config__.webservice))

            @threadpool.threadify(_Q3_)
            def __check_webservice_alive__():
                while (1):
                    so = __ws__.isalive()
		    if (so):
			print so.asPythonDict()
			if (str(so.status).upper() == 'SUCCESS'):
			    __handler__.is_webservice_alive = True
			    __logger__(__handler__,'(+++) is_webservice_alive=%s' % (__handler__.is_webservice_alive))
			    break
                    time.sleep(5)

            __check_webservice_alive__()
            self.timeout = __service_config__.resolution if (isinstance(__service_config__.resolution,float) or isinstance(__service_config__.resolution,int)) else 10
            if (self.timeout < 1000):
                self.timeout *= 1000
            isRunning = __service_config__.isRunning
            __logger__(__handler__,'(+++) isRunning=%s' % (isRunning))
            while (__service_config__.isRunning):
                __logger__(__handler__,'INFO: Crontab sleeping --> "%s ms".' % (self.timeout))
                if (ObjectTypeName.typeClassName(self) != 'vyperlogix.classes.SmartObject.SmartObject'):
                    rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
                    if rc == win32event.WAIT_OBJECT_0:
                        servicemanager.LogInfoMsg("SomeShortNameVersion - STOPPED!")  #For Event Log
                        break
                    else:
                        try:
                            __logger__(__handler__,'INFO: Crontab being processed --> "%s".' % (schedulefpath))
                            scheduler.crontab(__service_config__,jsonHandler=read_service_config,logging_callback=logger_proxy,threaded=False)
                        except Exception, ex:
                            __logger__(__handler__,'EXCEPTION: %s' % (_utils.formattedException(details=ex)))
			if (__handler__.is_webservice_alive):
			    __logger__(__handler__,'Webservice is alive !!!')
			    so = __ws__.has.config()
			    if (not so.data_has_config):
				__json__ = _utils.readFileFrom(__fname__,noCRs=True)
				so = __ws__.save.config(__json__)
			else:
			    __logger__(__handler__,'Webservice is NOT alive yet !!!')
                else:
                    msg = 'INFO: Crontab being processed --> "%s".' % (schedulefpath)
                    __logger__(__handler__,msg)
                    scheduler.crontab(__service_config__,jsonHandler=read_service_config,logging_callback=logger_proxy,threaded=True)
                    if (__handler__.is_webservice_alive):
                        __logger__(__handler__,'Webservice is alive !!!')
			so = __ws__.has.config()
			if (not so.data_has_config):
			    __json__ = _utils.readFileFrom(__fname__,noCRs=True)
			    so = __ws__.save.config(__json__)
                    else:
                        __logger__(__handler__,'Webservice is NOT alive yet !!!')
                    __logger__(__handler__,'Sleeping %s secs' % (self.timeout/1000))
                    time.sleep(self.timeout/1000)
                    
        if (self is None):
            from vyperlogix.misc import threadpool
            _Q_ = threadpool.ThreadQueue(1)
            
            @threadpool.threadify(_Q_)
            def __mainloop_threaded(self):
                __mainloop__(self)
            __mainloop_threaded(SmartObject())
        else:
            __mainloop__(self)
    elif (self is not None):
        __logger__(__handler__,'WARNING: SERVICE_NOT_RUNNING due to missing file "%s" !!!' % (schedulefpath))
        self.ReportServiceStatus(win32service.SERVICE_SPECIFIC_ERROR)
    
    return
        
class vCRON_Service(win32serviceutil.ServiceFramework):
    _svc_name_ = webservice.__svc_name__
    _svc_display_name_ = "vCRON"
    _svc_description_ = "Vyper Logix CRON for Windows"
    _svc_deps_ = ["EventLog"]
    
    def __init__(self, args):
        __logger__(__handler__,'INFO: __init__ --> args=%s' % (args))
        win32serviceutil.ServiceFramework.__init__(self, args)
        __logger__(__handler__,'INFO: __init__ --> self.ssh=%s' % (self.ssh))
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcDoRun(self):
        return __SvcDoRun__(self)
        
    def SvcStop(self):
        __logger__(__handler__,'INFO: SERVICE_STOP_PENDING !!!')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        __service_config__.isRunning = False
        win32event.SetEvent(self.hWaitStop)
        servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STOPPED,
                (self._svc_name_, ''))
        self.ReportServiceStatus(win32service.SERVICE_STOPPED) 
        __logger__(__handler__,'INFO: SERVICE_STOPPED !!!')
        pid = os.getpid()
        os.kill(pid,signal.SIGTERM)

def read_service_config(jsonFpath):
    __config__ = SmartObject()
    s = _utils.readFileFrom(jsonFpath)
    try:
        d = ujson.loads(s)
    except:
        __logger__(__handler__,'ERROR: Cannot load the json from "%s" due to a syntax error of some kind.' % (jsonFpath))
        d = {}
    __re__ = re.compile(r"%(?P<value>\w*)%", re.MULTILINE)
    __config__ = SmartObject(d)
    for k,v in __config__.iteritems():
        if (misc.isStringValid(v)):
            __m__ = __re__.match(v)
            if (__m__):
                __d__ = SmartObject(__m__.groupdict())
                __sym__ = __d__.value
                __vector__ = folders.__vectors__[__sym__]
                if (callable(__vector__)):
                    _v_ = v.replace('%'+__sym__+'%',__vector__())
                    __config__[k] = _v_
    for k,v in __config__.iteritems():
        if (misc.isStringValid(v)) and (v.find(__root_symbol__) > -1):
            r = __config__[__root_symbol__.replace('%','')]
            if (misc.isStringValid(r)):
                _v_ = v.replace(__root_symbol__,r)
                __config__[k] = _v_
    return __config__

def HandleCommandLine():
    '''
    --json path_to_json_file
    '''
    from optparse import OptionParser
    
    parser = OptionParser("usage: %prog [options]")
    parser.add_option("-j", "--json",action="store", type="string", dest="json_fpath")
    parser.add_option("-l", "--log",action="store", type="string", dest="log_url")
    parser.add_option("-w", "--webservice",action="store", type="string", dest="webservice")
    
    options, args = parser.parse_args()

    print 'DEBUG: options.json_fpath=%s' % (options.json_fpath)
    __argv__ = ListWrapper(sys.argv)
    __ip_port__ = options.webservice if (options.webservice and _utils.is_valid_ip_and_port(options.webservice)) else webservice.__default_webservice__
        
    from utils import __loggerHandler__
    __loggerHandler__()
    
    if (options.json_fpath):
        o = parser.get_option('-j')
        for s in o._long_opts+o._short_opts:
            i = __argv__.findFirstMatching(s)
            print 'DEBUG: (json_fpath) i=%s' % (i)
            if (i > -1):
                del sys.argv[i]
                del sys.argv[i]
        if (_utils.isBeingDebugged):
            cwd = os.path.dirname(sys.argv[0])
            __json_fpath__ = options.json_fpath.replace('./',cwd+'/')
        else:
            __json_fpath__ = os.path.abspath(options.json_fpath)
        __service_config__ = read_service_config(__json_fpath__)
        if (__service_config__.logger):
            __handler__.baseFilename = __service_config__.logger
            __handler__.baseFilePath = __json_fpath__ if (os.path.isdir(__json_fpath__)) else os.path.dirname(__json_fpath__)
            default_logger_init(__handler__)
            __logger__(__handler__,'INFO: Logger URL from "%s": "%s".' % (__json_fpath__,__handler__.baseFilename))
        __service_config__.schedulefpath = os.sep.join([os.path.dirname(__json_fpath__),__service_config__.crontab])
        __service_config__.jsonFpath = __json_fpath__
        __service_config__.webservice = __ip_port__
        __fpath__ = makedirs()
        __logger__(__handler__,'INFO: __fpath__="%s".' % (__fpath__))
        if (not os.path.exists(__fpath__)):
            os.mkdir(__fpath__)
        __fname__ = os.sep.join([__fpath__,'%s.json'%(vCRON_Service._svc_name_)])
        __service_config__.fname = __fname__
        __service_config__.isRunning = True
	__server_crt__ = os.sep.join([__fpath__,'server.crt'])
	if (os.path.exists(__server_crt__)):
	    __service_config__.server_crt = __server_crt__
	__server_key_insecure__ = os.sep.join([__fpath__,'server.key.insecure'])
	if (os.path.exists(__server_key_insecure__)):
	    __service_config__.server_key_insecure = __server_key_insecure__
	__favicon_ico__ = os.sep.join([__fpath__,'favicon.ico'])
	if (os.path.exists(__favicon_ico__)):
	    __service_config__.favicon_ico = __favicon_ico__
	__crossdomain_xml__ = os.sep.join([__fpath__,'crossdomain.xml'])
	if (os.path.exists(__crossdomain_xml__)):
	    __service_config__.crossdomain_xml = __crossdomain_xml__
        _utils.writeFileFrom(__fname__,ujson.dumps(__service_config__.asPythonDict()))
        __logger__(__handler__,'INFO: __fname__="%s".' % (__fname__))
    if (options.log_url):
        o = parser.get_option('-l')
        for s in o._long_opts+o._short_opts:
            i = __argv__.findFirstMatching(s)
            print 'DEBUG: (log_url) i=%s' % (i)
            if (i > -1):
                del sys.argv[i]
                del sys.argv[i]
        __handler__.baseFilename = options.log_url
        __logger__(__handler__,'INFO: Logger URL: "%s".' % (__handler__.baseFilename))
    if (not options.json_fpath):
        print >> sys.stderr, 'ERROR: Cannot continue without the "service_config.json" file that has to be specified using the appropriate command line option(s).'
        pid = os.getpid()
        os.kill(pid,signal.SIGTERM)
    elif (_utils.isBeingDebugged):
            __SvcDoRun__(None)
            while (1):
                print 'Sleeping...'
                time.sleep(5)
        

    print 'Logging to "%s".' % (__handler__.baseFilename)
    __logger__(__handler__,'Testing...')
    if (any([arg in ['install','remove','restart','start','stop'] for arg in sys.argv])):
        win32serviceutil.HandleCommandLine(vCRON_Service)

    pid = os.getpid()
    os.kill(pid,signal.SIGTERM)

if (__name__ == '__main__'):
    HandleCommandLine()
    
    
