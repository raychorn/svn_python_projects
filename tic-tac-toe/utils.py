'''
(c). Copyright 2014-2018, Ray C Horn, All RIghts Reserved.
'''
import os, sys
import signal

def get_function_name():
    import traceback
    return traceback.extract_stack(None, 2)[0][2]

def callersName():
    """ get name of caller of a function """
    import sys
    return sys._getframe(2).f_code.co_name

def __formattedException__(details='',_callersName=None,depth=None,delims='\n'):
    _callersName = _callersName if (_callersName is not None) else callersName()
    import sys, traceback
    exc_info = sys.exc_info()
    stack = traceback.format_exception(*exc_info)
    stack = stack if ( (depth is None) or (not isInteger(depth)) ) else stack[0:depth]
    try:
        info_string = delims.join(stack)
    except:
        info_string = '\n'.join(stack)
    return '(' + _callersName + ') :: "' + str(details) + '". ' + info_string

def formattedException(details='',depth=None,delims='\n'):
    return __formattedException__(details=details,_callersName=callersName(),depth=depth,delims=delims)

def killProcByPID(pid):
    try:
        os.kill(pid, signal.SIGILL)
    except Exception, details:
        print >>sys.stderr, formattedException(details)

def terminate(pid=None):
    killProcByPID(os.getpid() if (pid is None) else pid)

def convertMillis(millis):
    ms_per_sec = 1000
    seconds=(millis/ms_per_sec)%60
    ms_per_min = 1000*60
    minutes=(millis/ms_per_min)%60
    ms_per_hour = (1000*60*60)
    hours=(millis/ms_per_hour)%24
    ms = millis - ((hours*ms_per_hour)+(minutes*ms_per_min)+(seconds*ms_per_sec))
    return ms, seconds, minutes, hours

def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer

__kwargs__ = {}

@parametrized
def timeit(method, *args, **kwargs):
    import time
    global __kwargs__
    __kwargs__ = kwargs
    def timed(*args, **kwargs):
        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()
        if ('log_time' in __kwargs__) and ('callback' in __kwargs__):
            name = __kwargs__.get('log_name', method.__name__.upper())
            log_time = __kwargs__.get('log_time', {})
            if (log_time is None):
                log_time = {}
            log_time[name] = int((te - ts) * 1000)
            __kwargs__['log_time'] = log_time
            
            ms = (te - ts) * 1000
            __ms__, __ss__, __mm__, __hh__ = convertMillis(int(ms))
            msg = '%r  %2.2f ms or %02d:%02d:%02d.%d' % (method.__name__, ms, __hh__, __mm__, __ss__, __ms__)

            callback = __kwargs__.get('callback', None)
            if (isinstance(callback, dict)):
                callback = callback.get(callback.keys()[0], None)
            if (callable(callback)):
                try:
                    callback(msg)
                except Exception as details:
                    print('%s :: %s' % (method.__name__, formattedException(details=details, depth=2)))
        else:
            print(msg)
        return result
    return timed

