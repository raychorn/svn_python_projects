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

__Q__ = threadpool.ThreadQueue(1)

__Q1__ = threadpool.ThreadQueue(100)

__Q5__ = threadpool.ThreadQueue(1)

__Q6__ = threadpool.ThreadQueue(1)

__ignoring__ = ['$RECYCLE.BIN/','dont-touch-this-one/']

__allowing__ = lambda a,fn:(a != Actions.Deleted) and os.path.exists(fn) and os.path.isfile(fn) and (not any([(fn.replace(os.sep,'/').lower().find(f.replace(os.sep,'/').lower()) > -1) for f in __ignoring__]))

def __terminate__():
    _utils.terminate()

class DirectoryWatcher():
    def __init__(self,fpath):
        self.__watching__ = fpath if (os.path.exists(fpath)) else None
        self.__hDir__ = None
        self.__running__ = False
        self.__callback__ = None
        self.__outputQ__ = Queue.Queue(1000)

        self.__changes__ = win32con.FILE_NOTIFY_CHANGE_FILE_NAME
        self.__changes__ |= win32con.FILE_NOTIFY_CHANGE_DIR_NAME
        self.__changes__ |= win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES
        self.__changes__ |= win32con.FILE_NOTIFY_CHANGE_SIZE
        self.__changes__ |= win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
        self.__changes__ |= win32con.FILE_NOTIFY_CHANGE_SECURITY
        return
    
    @threadpool.threadify(__Q1__)
    def ProcessChange(self,action,fpath):
        fp = '/'.join([self.__watching__, fpath]).replace(os.sep,'/')
        if (callable(self.__callback__)):
            try:
                self.__callback__(self,action,fpath)
            except Exception, ex:
                self.queue_logging(logging.ERROR,'%s.1 :: %s' % (misc.funcName(),_utils.formattedException(details=ex)))
        self.queue_logging(logging.INFO,'%s.1 :: (%s) (%s) %s' % (misc.funcName(), action.name, 'D' if (os.path.isdir(fp)) else 'F' if (os.path.isfile(fp)) else 'U', fp))

    @threadpool.threadify(__Q6__)
    def queue_logging(self,level,msg):
        _msg = '%s --> %s' % (_utils.timeStampLocalTime(),msg)
        self.__outputQ__.put_nowait(SmartObject({'msg':_msg,'level':level}))
        
    @threadpool.threadify(__Q5__)
    def dequeue_logging(self):
        data = self.__outputQ__.get()
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
            data = self.__outputQ__.get()
            print >> sys.stdout, '%s :: %s' % (data.level,data.msg)

    @threadpool.threadify(__Q__)
    def execute(self,callback=None,changeFlags=None):
        if (not self.__running__):
            if (changeFlags):
                self.__changes__ = changeFlags
                
            if (callable(callback)):
                self.__callback__ = callback
            
            self.__running__ = True

            name = _utils.getProgramName()
            fpath = os.path.dirname(sys.argv[0])
            _log_path = _utils.safely_mkdir_logs(fpath=fpath)
            _log_path = _utils.safely_mkdir(fpath=_log_path,dirname=_utils.timeStampLocalTimeForFileName(delimiters=('_','-'),format=_utils.formatSalesForceTimeStr()))
            
            logFileName = os.sep.join([_log_path,'%s.log' % (name)])
            
            print '(%s) :: logFileName=%s' % (_utils.timeStampLocalTime(),logFileName)
    
            _logging = logging.INFO
            _console_logging = logging.INFO
    
            standardLogging.standardLogging(logFileName,_level=_logging,console_level=_console_logging,isVerbose=True)
    
            self.dequeue_logging()
    
            self.report_changes(self.__changes__)
    
            if (os.path.exists(self.__watching__)):
                FILE_LIST_DIRECTORY = 0x0001
                self.__hDir__ = win32file.CreateFile (
                    self.__watching__,
                    FILE_LIST_DIRECTORY,
                    win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
                    None,
                    win32con.OPEN_EXISTING,
                    win32con.FILE_FLAG_BACKUP_SEMANTICS,
                    None
                )

                while (self.__running__):
                    for action,aFile in win32file.ReadDirectoryChangesW(self.__hDir__,1024,True,self.__changes__,None,None):
                        fpath = os.path.join(self.__watching__, aFile)
                        action = Actions(action)
                        self.ProcessChange(action,aFile)
            else:
                print >>sys.stderr, 'ERROR: Nothing to do unless you watch a directory.'
    

    def report_changes(self,cflags):
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
        self.queue_logging(logging.INFO, 'FLAGS: %s --> %s' % (format(cflags,'b'),flags))

