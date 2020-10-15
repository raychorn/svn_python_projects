import os, sys
import urlparse
import random
import time
import urllib

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix import oodb

import logging

from vyperlogix.daemon.daemon import Log
from vyperlogix.daemon.daemon import CustomLog
from vyperlogix.logging import standardLogging

_root_ = os.path.dirname(__file__)

def main(logging):
    pass

if (__name__ == '__main__'):
    from vyperlogix.misc import Args
    from vyperlogix.misc import PrettyPrint

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--cwd=?':'the path the program runs from, defaults to the path the program runs from.',
	    '--logging=?':'[logging.INFO,logging.WARNING,logging.ERROR,logging.DEBUG]',
	    '--console_logging=?':'[logging.INFO,logging.WARNING,logging.ERROR,logging.DEBUG]'}
    _argsObj = Args.Args(args)

    _progName = _argsObj.programName
    _isVerbose = True
    try:
	if _argsObj.booleans.has_key('isVerbose'):
	    _isVerbose = _argsObj.booleans['isVerbose']
    except Exception, e:
	info_string = _utils.formattedException(details=e)
	logging.warning(info_string)
	_isVerbose = False
	
    _isHelp = False
    try:
	if _argsObj.booleans.has_key('isHelp'):
	    _isHelp = _argsObj.booleans['isHelp']
    except:
	pass
    
    if (_isHelp):
	ppArgs()

    __cwd__ = os.path.dirname(sys.argv[0])
    try:
	__cwd = _argsObj.arguments['cwd'] if _argsObj.arguments.has_key('cwd') else __cwd__
	if (len(__cwd) == 0) or (not os.path.exists(__cwd)):
	    if (os.environ.has_key('cwd')):
		__cwd = os.environ['cwd']
	__cwd__ = __cwd
    except:
	pass
    _cwd = __cwd__
    
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

    name = _utils.getProgramName()
    fpath=_cwd
    _log_path = _utils.safely_mkdir_logs(fpath=fpath)
    _log_path = _utils.safely_mkdir(fpath=_log_path,dirname=_utils.timeStampLocalTimeForFileName(delimiters=('_'),format=_utils.formatDate_MMDDYYYY_dashes()))
    #_data_path = _utils.safely_mkdir(fpath=fpath,dirname='dbx')

    logFileName = os.sep.join([_log_path,'%s.log' % (name)])

    print '(%s) :: logFileName=%s' % (_utils.timeStampLocalTime(),logFileName)

    _stdOut = open(os.sep.join([_log_path,'stdout.txt']),'w')
    _stdErr = open(os.sep.join([_log_path,'stderr.txt']),'w')
    _stdLogging = open(logFileName,'w')

    if (not _utils.isBeingDebugged):
	sys.stdout = Log(_stdOut)
	sys.stderr = Log(_stdErr)
    _logLogging = CustomLog(_stdLogging)

    standardLogging.standardLogging(logFileName,_level=_logging,console_level=_console_logging,isVerbose=_isVerbose)

    _logLogging.logging = logging # echos the log back to the standard logging...
    logging = _logLogging # replace the default logging with our own custom logging...

    main(logging)
    