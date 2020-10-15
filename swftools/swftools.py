import os,sys

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix.misc import _utils

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
	    '--recurse':'recurse into all folders.',
	    '--source=?':'path to the folder that contains all those files.',
	    '--cmd=?':'command to be executed for each folder.',
	    '--target=?':'file type target for this process.',
	    }
    _argsObj = Args.Args(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = _argsObj.programName
	_isVerbose = False
	try:
	    if _argsObj.booleans.has_key('isVerbose'):
		_isVerbose = _argsObj.booleans['isVerbose']
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print >>sys.stderr, info_string
	    _isVerbose = False
	    
	_isDebug = False
	try:
	    if _argsObj.booleans.has_key('isDebug'):
		_isDebug = _argsObj.booleans['isDebug']
	except:
	    pass
	
	_isRecurse = False
	try:
	    if _argsObj.booleans.has_key('isRecurse'):
		_isRecurse = _argsObj.booleans['isRecurse']
	except:
	    pass
	
	_isHelp = False
	try:
	    if _argsObj.booleans.has_key('isHelp'):
		_isHelp = _argsObj.booleans['isHelp']
	except:
	    pass
	
	if (_isHelp):
	    ppArgs()
	    sys.exit()
	    
	_source = ''
	try:
	    __source = _argsObj.arguments['source'] if _argsObj.arguments.has_key('source') else _source
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print >>sys.stderr, info_string
	_source = __source
	
	_cmd = ''
	try:
	    __cmd = _argsObj.arguments['cmd'] if _argsObj.arguments.has_key('cmd') else _cmd
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print >>sys.stderr, info_string
	_cmd = __cmd
	
	_target = ''
	try:
	    __target = _argsObj.arguments['target'] if _argsObj.arguments.has_key('target') else _target
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print >>sys.stderr, info_string
	_target = __target
	
	if (_isVerbose):
	    print >> sys.stderr, '_isDebug=', _isDebug
	    print >> sys.stderr, '_isRecurse=', _isRecurse
	    print >> sys.stderr, '_source=', _source
	    print >> sys.stderr, '_cmd=', _cmd
	    print >> sys.stderr, '_target=', _target
	    
	if (os.path.exists(_source)) and (os.path.exists(_cmd)):
	    for aDir,dirs,files in _utils.walk(_source):
		pass
	else:
	    print >> sys.stderr, 'WARNING: Double-check your options, there is something wrong with the --source=? or --cmd=?'
	