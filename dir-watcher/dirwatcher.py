import os
import sys
import time
import uuid
import Queue

import win32file
import win32con

import logging

from vyperlogix.daemon.daemon import Log
from vyperlogix.daemon.daemon import CustomLog
from vyperlogix.logging import standardLogging

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.enum import Enum

from vyperlogix.misc import threadpool

class Actions(Enum.Enum):
    UNKNOWN = -1
    Created = 1
    Deleted = 2
    Updated = 3
    Renamed_From = 4
    Renamed_To = 5

__Q1__ = threadpool.ThreadQueue(100)

__Q2__ = threadpool.ThreadQueue(1)

__Q3__ = threadpool.ThreadQueue(1)

__Q4__ = threadpool.ThreadQueue(100)

__Q5__ = threadpool.ThreadQueue(1)
__loggingQ__ = Queue.Queue(maxsize=100)

__Q6__ = threadpool.ThreadQueue(1)

__outputQ__ = Queue.Queue(1000)

__uuid_symbol__ = 'uuid'
__running_symbol__ = 'running'

__ignoring__ = ['$RECYCLE.BIN/','dont-touch-this-one/']

__allowing__ = lambda a,fn:(a != Actions.Deleted) and os.path.exists(fn) and os.path.isfile(fn) and (not any([(fn.replace(os.sep,'/').lower().find(f.replace(os.sep,'/').lower()) > -1) for f in __ignoring__]))

__running__ = True

__roots__ = {} # dirName-of-root-folder-->{__uuid_symbol__:str(uuid.uuid4()),__running_symbol__:True/False}

### BEGIN: LOGGING ###############################################################
__cwd__ = os.path.dirname(sys.argv[0])
name = _utils.getProgramName()
fpath = __cwd__
_log_path = _utils.safely_mkdir_logs(fpath=fpath)
_log_path = _utils.safely_mkdir(fpath=_log_path,dirname=_utils.timeStampLocalTimeForFileName(delimiters=('_','-'),format=_utils.formatSalesForceTimeStr()))

logFileName = os.sep.join([_log_path,'%s.log' % (name)])

print '(%s) :: logFileName=%s' % (_utils.timeStampLocalTime(),logFileName)

import atexit
@atexit.register
def __terminate__():
    import os
    from vyperlogix.process.killProcByPID import killProcByPID
    pid = os.getpid()
    killProcByPID(pid)

@threadpool.threadify(__Q1__)
def ProcessChange(action,fpath):
    fp = '/'.join([__watching__, fpath]).replace(os.sep,'/')
    queue_logging(logging.INFO,'%s.1 :: (%s) (%s) %s' % (misc.funcName(), action.name, 'D' if (os.path.isdir(fp)) else 'F' if (os.path.isfile(fp)) else 'U', fp))

@threadpool.threadify(__Q5__)
def dequeue_logging():
    data = __outputQ__.get()
    print >> sys.stdout, '%s :: %s' % (data.level,data.msg)
    while (1):
        msg = data.msg
        if (msg):
            level = data.level if (data.level) else logging.INFO
            if (level == logging.WARNING):
                logging.warning()
            elif (level == logging.INFO):
                logging.info(msg)
            elif (level == logging.DEBUG):
                logging.debug(msg)
            elif (level == logging.WARNING):
                logging.warning(msg)
            elif (level == logging.ERROR):
                logging.error(msg)
            elif (level == logging.CRITICAL):
                logging.critical(msg)
        data = __outputQ__.get()
        print >> sys.stdout, '%s :: %s' % (data.level,data.msg)

@threadpool.threadify(__Q6__)
def queue_logging(level,msg):
    _msg = '%s --> %s' % (_utils.timeStampLocalTime(),msg)
    __outputQ__.put_nowait(SmartObject({'msg':_msg,'level':level}))

if (__name__ == '__main__'):
    from optparse import OptionParser
    
    parser = OptionParser("usage: %prog [options]")
    parser.add_option('-w', '--watching', dest='watching', help="watching folder path")
    parser.add_option('-c', '--changes', dest='changes', help="changes (all)")
    parser.add_option('--ll', '--loglevel', dest='loglevel', help="loglevel (INFO)")
    parser.add_option('--cl', '--consoleloglevel', dest='consoleloglevel', help="consoleloglevel (INFO)")
    parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
    
    options, args = parser.parse_args()
    
    __watching__ = None
    __changes__ = None
    __hDir__ = None
    if (options.watching):
        __watching__ = options.watching if (os.path.exists(options.watching)) else None
        
        if (__watching__):
            FILE_LIST_DIRECTORY = 0x0001
            __hDir__ = win32file.CreateFile (
                __watching__,
                FILE_LIST_DIRECTORY,
                win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
                None,
                win32con.OPEN_EXISTING,
                win32con.FILE_FLAG_BACKUP_SEMANTICS,
                None
            )
    if (options.changes):
        __changes__ = win32con.FILE_NOTIFY_CHANGE_FILE_NAME
        __changes__ |= win32con.FILE_NOTIFY_CHANGE_DIR_NAME
        __changes__ |= win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES
        __changes__ |= win32con.FILE_NOTIFY_CHANGE_SIZE
        __changes__ |= win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
        __changes__ |= win32con.FILE_NOTIFY_CHANGE_SECURITY
        
    _logging = logging.INFO
    if (options.loglevel):
        pass
    
    _console_logging = logging.INFO
    if (options.consoleloglevel):
        pass
    
    _isVerbose = False
    if (options.verbose):
        _isVerbose = True
    
    standardLogging.standardLogging(logFileName,_level=_logging,console_level=_console_logging,isVerbose=_isVerbose)
    
    def report_changes(cflags):
        flags = []
        if (cflags & win32con.FILE_NOTIFY_CHANGE_FILE_NAME):
            flags.append('FILE_NOTIFY_CHANGE_FILE_NAME')
        if (cflags & win32con.FILE_NOTIFY_CHANGE_DIR_NAME):
            flags.append('FILE_NOTIFY_CHANGE_DIR_NAME')
        if (cflags & win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES):
            flags.append('FILE_NOTIFY_CHANGE_ATTRIBUTES')
        if (cflags & win32con.FILE_NOTIFY_CHANGE_SIZE):
            flags.append('FILE_NOTIFY_CHANGE_SIZE')
        if (cflags & win32con.FILE_NOTIFY_CHANGE_LAST_WRITE):
            flags.append('FILE_NOTIFY_CHANGE_LAST_WRITE')
        if (cflags & win32con.FILE_NOTIFY_CHANGE_SECURITY):
            flags.append('FILE_NOTIFY_CHANGE_SECURITY')
        queue_logging(logging.INFO, 'FLAGS: %s --> %s' % (format(cflags,'b'),flags))
    
    if (__hDir__ and __watching__ and __changes__):
        dequeue_logging()
        
        report_changes(__changes__)
    
        while (__running__):
            for action,aFile in win32file.ReadDirectoryChangesW(__hDir__,1024,True,__changes__,None,None):
                fpath = os.path.join(__watching__, aFile)
                action = Actions(action)
                ProcessChange(action,aFile)
    else:
        logging.warning('Nothing to do.')
        __terminate__()
