import os, sys

import win32api

print '__name__=%s' % (__name__)
if (__name__ == '__main__'):
    has_vyperlogix = [(f.find('vyperlogix') > -1) for f in sys.path]
    print 'DEBUG:  any(has_vyperlogix)=%s' % (any(has_vyperlogix))
    if (not any(has_vyperlogix)):
	__library__ = 'J:/@Vyper Logix Corp/@Projects/python-projects/@lib/12-13-2011-01/dist_2.7.0/vyperlogix_2_7_0.zip'
	_is_ = os.path.exists(__library__)
	print '1._is_=%s' % (_is_)
	if (_is_):
	    has_vyperlogix = [(f.find('vyperlogix') > -1) for f in sys.path]
	    print 'DEBUG:  any(has_vyperlogix)=%s' % (any(has_vyperlogix))
	    if (not any(has_vyperlogix)):
		sys.path.insert(0, __library__)

from vyperlogix.misc import threadpool

from vyperlogix.misc import _utils

__Q__ = threadpool.ThreadQueue(10)

import win32serviceutil
import win32service
import win32event
import win32evtlogutil

__programName__ = (sys.argv[0].split(os.sep)[-1].split('.'))[0]
__serviceToks__ = [n.capitalize() for n in __programName__.split('_')]
__serviceDescr__ = ' '.join(__serviceToks__)
__serviceName__ = ''.join(__serviceToks__)

__num__ = 12
__serviceName__ = '%s%d' % (__serviceName__,__num__)
__serviceDescr__ = '%s%d' % (__serviceDescr__,__num__)

print 'DEBUG:  __programName__=%s' % (__programName__)
print 'DEBUG:  __serviceName__=%s' % (__serviceName__)
print 'DEBUG:  __serviceDescr__="%s"' % (__serviceDescr__)

__count__ = 0

@threadpool.threadify(__Q__)
def processing(self):
    import servicemanager
    global __count__
    self.runflag=True
    while self.runflag:
	win32api.Sleep(10000)
	__count__ += 1
	win32evtlogutil.ReportEvent(self._svc_name_,
                                    servicemanager.EVENTLOG_INFORMATION_TYPE,
                                    0, # category
                                    servicemanager.EVENTLOG_INFORMATION_TYPE,
                                    (self._svc_name_, 'COUNT is %d' % (__count__)))

@threadpool.threadify(__Q__)
def launch_socket_server(self):
    import servicemanager
    import SocketServer2
    win32evtlogutil.ReportEvent(self._svc_name_,
                                servicemanager.EVENTLOG_INFORMATION_TYPE,
                                0, # category
                                servicemanager.EVENTLOG_INFORMATION_TYPE,
                                (self._svc_name_, 'Launching Sock Server.'))
    SocketServer2.server_startup()

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = __serviceName__
    _svc_display_name_ = __serviceDescr__
    _svc_deps_ = ["EventLog"]
    _svc_description_ = 'Handles Background Processing for the Windows Sleep Runner Process.'
    def __init__(self, args):
	win32serviceutil.ServiceFramework.__init__(self, args)
	self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
	self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
	win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
	import servicemanager
	# Write a 'started' event to the event log...
	win32evtlogutil.ReportEvent(self._svc_name_,
                                    servicemanager.PYS_SERVICE_STARTED,
                                    0, # category
                                    servicemanager.EVENTLOG_INFORMATION_TYPE,
                                    (self._svc_name_, ''))
	
	launch_socket_server(self)

	# wait for beeing stopped...
	win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

	# and write a 'stopped' event to the event log.
	win32evtlogutil.ReportEvent(self._svc_name_,
                                    servicemanager.PYS_SERVICE_STOPPED,
                                    0, # category
                                    servicemanager.EVENTLOG_INFORMATION_TYPE,
                                    (self._svc_name_, ''))

@threadpool.threadify(__Q__)
def __custom_handler__():
    print 'DEBUG:  Sleeping for 30 secs...'
    win32api.Sleep(30000)  # Service Manager has to get a response within 30 secs...
    print 'DEBUG:  Killing the process...'

    from vyperlogix.process import killProcByPID
    from vyperlogix.win.WinProcesses import Win32Processes
    
    from vyperlogix import misc
    from vyperlogix.misc import ObjectTypeName
    
    try:
	p = Win32Processes()
	pid = p.getProcessIdByName(__programName__)
	if (misc.isList(pid)) and (len(pid) > 0):
	    pid = pid[0]
	if (misc.isInteger(pid)):
	    print 'DEBUG:  pid="%s"' % (pid)
	    print 'BEGIN:'
	    killProcByPID.killProcByPID(pid,isVerbose=True)
	    print 'END !!!'
	else:
	    print 'DEBUG:  pid is not an Int because it is "%s" !!!' % (ObjectTypeName.typeClassName(pid))
    except Exception, ex:
	info_string = _utils.formattedException(details=ex)
	print info_string

print '__name__=%s' % (__name__)
if (__name__ == '__main__'):
    win32serviceutil.HandleCommandLine(MyService)
elif (__name__ == __programName__):
    __custom_handler__()
