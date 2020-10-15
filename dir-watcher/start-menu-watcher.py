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

__testing__ = True

__uuid_symbol__ = 'uuid'
__running_symbol__ = 'running'

if (not __testing__):
    __watching__ = "C:/ProgramData/Microsoft/Windows/Start Menu"
    __target__ = 'J:/#rackspace/Windows/Start Menu'
    __shred_source__ = True
else:
    __watching__ = 'C:/@1'
    __target__ = 'C:/@2'
    __shred_source__ = True

__ignoring__ = ['$RECYCLE.BIN/','dont-touch-this-one/']

__allowing__ = lambda a,fn:(a != Actions.Deleted) and os.path.exists(fn) and os.path.isfile(fn) and (not any([(fn.replace(os.sep,'/').lower().find(f.replace(os.sep,'/').lower()) > -1) for f in __ignoring__]))

__running__ = True

__roots__ = {} # dirName-of-root-folder-->{__uuid_symbol__:str(uuid.uuid4()),__running_symbol__:True/False}

### BEGIN: LOGGING ###############################################################
name = _utils.getProgramName()
fpath = os.getcwd()
_log_path = _utils.safely_mkdir_logs(fpath=fpath)
_log_path = _utils.safely_mkdir(fpath=_log_path,dirname=_utils.timeStampLocalTimeForFileName(delimiters=('_','-'),format=_utils.formatSalesForceTimeStr()))

logFileName = os.sep.join([_log_path,'%s_%s.log' % (name,_source)])

print '(%s) :: logFileName=%s' % (_utils.timeStampLocalTime(),logFileName)

_stdOut = open(os.sep.join([_log_path,'stdout.txt']),'a')
_stdErr = open(os.sep.join([_log_path,'stderr.txt']),'a')
_stdLogging = open(logFileName,'a')

if (not _utils.isBeingDebugged):
    sys.stdout = Log(_stdOut)
    sys.stderr = Log(_stdErr)
_logLogging = CustomLog(_stdLogging)

standardLogging.standardLogging(logFileName,_level=_logging,console_level=_console_logging,isVerbose=_isVerbose)

_logLogging.logging = logging # echos the log back to the standard logging...
logging = _logLogging # replace the default logging with our own custom logging...
### END! LOGGING #################################################################

import atexit
@atexit.register
def goodbye():
    import os
    from vyperlogix.process.killProcByPID import killProcByPID
    print 'INFO: Saying goodbye() !!!'
    pid = os.getpid()
    killProcByPID(pid)

@threadpool.threadify(__Q1__)
def ProcessChange(action,fpath):
    global __count__
    print '%s.1 :: %s\n(%s)' % (misc.funcName(),'%s\n\t%s' % (__watching__, fpath), action.name)
    oldFn = os.path.join(__watching__, fpath)
    newFn = os.path.join(__target__, fpath)
    _utils.makeDirs(newFn)
    _newFn = os.path.join(os.path.dirname(newFn) if (os.path.isfile(newFn)) else newFn,'info.txt')
    _utils.copy_binary_files_by_chunks(oldFn,newFn)
    if (__shred_source__):
        os.remove(oldF)
    print '%s.2 :: %s' % (misc.funcName(),'%s\n\t%s' % (__target__, _newFn.replace(__target__,'')))
    __count__ += 1
    print '%s.3 :: __count__=%s' % (misc.funcName(),__count__)

FILE_LIST_DIRECTORY = 0x0001
hDir = win32file.CreateFile (
    __watching__,
    FILE_LIST_DIRECTORY,
    win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
    None,
    win32con.OPEN_EXISTING,
    win32con.FILE_FLAG_BACKUP_SEMANTICS,
    None
)

__changes__ = win32con.FILE_NOTIFY_CHANGE_FILE_NAME
__changes__ |= win32con.FILE_NOTIFY_CHANGE_DIR_NAME
__changes__ |= win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES
__changes__ |= win32con.FILE_NOTIFY_CHANGE_SIZE
__changes__ |= win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
__changes__ |= win32con.FILE_NOTIFY_CHANGE_SECURITY

__count__ = 0

@threadpool.threadify(__Q2__)
def watcher():
    global __running__
    while (__running__):
        print '%s.1 :: %s ???' % (misc.funcName(),__count__)
        if (__count__ > 5):
            print '%s.2 :: %s !!!' % (misc.funcName(),__count__)
            __running__ = False
            print '%s.2 :: About to exit... !!!' % (misc.funcName())
            __Q1__.isRunning = False
            __Q2__.isRunning = False
            goodbye()
        time.sleep(1)
watcher()

__is_root_valid_in_roots__ = lambda v:(misc.isDict(v)) and (v.has_key(__uuid_symbol__)) and (v.has_key(__running_symbol__))
__is_root_valid_and_running__ = lambda v:__is_root_valid_in_roots__(v) and (v[__running_symbol__])

@threadpool.threadify(__Q4__)
def root_worker(fpath,bucket):
    _is_ = __is_root_valid_and_running__(bucket)
    print '%s.1 :: __is_root_valid_and_running__=%s ???' % (misc.funcName(),_is_)
    if (_is_):
        print '%s.2 :: __running__=%s ???' % (misc.funcName(),__running__)
        while (__running__ and _is_):
            print '%s.3 :: __running__=%s ???' % (misc.funcName(),__running__)
            count,numBytes = _utils.folderSize(fpath)
            if (count == 0):
                _utils.removeAllFilesUnder(fpath)
            if (not os.path.exists(fpath)):
                bucket[__running_symbol__] = False
            time.sleep(1)
            _is_ = __is_root_valid_and_running__(bucket)

@threadpool.threadify(__Q3__)
def root_watcher():
    print '%s.1 :: __running__=%s ???' % (misc.funcName(),__running__)
    while (__running__):
        print '%s.2 :: __running__=%s ???' % (misc.funcName(),__running__)
        if (len(__roots__) > 0):
            for k,v in __roots__.iteritems(): # dirName-of-root-folder-->{__uuid_symbol__:str(uuid.uuid4()),__running_symbol__:True/False}
                if (not __is_root_valid_in_roots__(v)):
                    __roots__[k] = {__uuid_symbol__:str(uuid.uuid4()),__running_symbol__:True}
                    root_worker(k,__roots__[k])
            pass
        time.sleep(1)
root_watcher()

@threadpool.threadify(__Q5__)
def dequeue_logging():
    data = __outputQ__.get()
    while (1):
        msg = data.get('msg',None)
        if (msg):
            level = data.get('level',logging.WARNING)
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
dequeue_logging()

@threadpool.threadify(__Q6__)
def queue_logging(level,msg):
    _msg = '%s --> %s' % (_utils.timeStampLocalTime(),msg)
    __outputQ__.put_nowait(data)

while (__running__):
    for action,aFile in win32file.ReadDirectoryChangesW(hDir,1024,True,__changes__,None,None):
        fpath = os.path.join(__watching__, aFile)
        action = Actions(action)
        if (__allowing__(action,fpath)):
            ProcessChange(action,aFile)
