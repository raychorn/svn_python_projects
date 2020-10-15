import os, sys

import Queue

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.classes.SmartObject import SmartObject

__handler__ = SmartObject()
__handler__.baseFilename = 'http://127.0.0.1:9999/logger'
__handler__.baseFilePath = ''
__handler__.count = 0
__handler__.failure_count = 0
__handler__.queue = Queue.Queue(1000)

def initialize_crontab_if_necessary(__logger__,__handler__,schedulefpath):
    if (not os.path.exists(schedulefpath)):
        if (callable(__logger__)):
            __logger__(__handler__,'INFO: Creating default Crontab file: "%s".' % (schedulefpath))
        dname = os.path.dirname(schedulefpath)
        if (not os.path.exists(dname)):
            _utils._makeDirs(dname)
        fOut = open(schedulefpath,'w')
        content = '''
        # Minute   Hour   Day of Month       Month          Day of Week        Command    
        # (0-59)  (0-23)     (1-31)    (1-12 or Jan-Dec)  (0-6 or Sun-Sat)                
        '''
        print >>fOut, content
        if (callable(__logger__)):
            __logger__(__handler__,'INFO: Crontab Default Content: "%s".' % (content))
        fOut.flush()
        fOut.close()

from vyperlogix.misc import threadpool
_Q1_ = threadpool.ThreadQueue(1)
_Q2_ = threadpool.ThreadQueue(100)

@threadpool.threadify(_Q1_)
def __loggerHandler__():
    import requests
    
    while (1):
        handle,args,kwargs = __handler__.queue.get(True)
        
        msg = args[0]
    
        __isINFO__ = str(msg).find('INFO:') > -1
        __isWARNING__ = str(msg).find('WARNING:') > -1
        __isDEBUG__ = str(msg).find('DEBUG:') > -1
        __isERROR__ = str(msg).find('ERROR:') > -1
        __isCRITICAL__ = str(msg).find('CRITICAL:') > -1
        __isEXCEPTION__ = str(msg).find('EXCEPTION:') > -1
        
        __isINFO__ = (not __isINFO__) and (not __isWARNING__) and (not __isDEBUG__) and (not __isERROR__) and (not __isCRITICAL__) and (not __isEXCEPTION__)
        
        level = 'UNKNOWN-LEVEL'
        if (__isEXCEPTION__):
            level = 'EXCEPTION'
            msg += _utils.formattedException(details=exception)
        elif (__isINFO__):
            level = 'INFO'
        elif (__isWARNING__):
            level = 'WARNING'
        elif (__isDEBUG__):
            level = 'DEBUG'
        elif (__isERROR__):
            level = 'ERROR'
        elif (__isCRITICAL__):
            level = 'CRITCAL'

        def use_default_logger():
            if (__isEXCEPTION__):
                handle.logger.exception(msg)
            elif (__isINFO__):
                handle.logger.info(msg)
            elif (__isWARNING__):
                handle.logger.warning(msg)
            elif (__isDEBUG__):
                handle.logger.debug(msg)
            elif (__isERROR__):
                handle.logger.error(msg)
            elif (__isCRITICAL__):
                handle.logger.critical(msg)
        
        if (handle.failure_count == 0) and (misc.isStringValid(handle.baseFilename)):
            __header__ = {'Content-Type':'application/json',
                    'Accept':'application/json'}
            try:
                r = requests.post(handle.baseFilename,data=ujson.dumps({'product':'vCRON','message':msg,'level':level}),headers=__header__)
                result = r.content
                if (r.status_code == 200):
                    handle.count += 1
                else:
                    print >> sys.stderr, 'FAILED to log message.'
            except:
                handle.failure_count += 1
                use_default_logger()
                handle.count += 1
        else:
            use_default_logger()
            handle.count += 1

@threadpool.threadify(_Q2_)
def __logger__(handle,*args,**kwargs):
    item = (handle, args, kwargs)
    handle.queue.put_nowait(item)

