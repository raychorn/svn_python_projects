def __formattedException__(details='',_callersName=None):
    _callersName = _callersName if (_callersName is not None) else callersName()
    import sys, traceback
    exc_info = sys.exc_info()
    info_string = '\n'.join(traceback.format_exception(*exc_info))
    return '(' + _callersName + ') :: "' + str(details) + '". ' + info_string

def formattedException(details=''):
    return __formattedException__(details=details,_callersName=misc.callersName())

