import os, sys, traceback

from vyperlogix.ssh import sshUtils

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix.misc import _utils
from vyperlogix.misc import _psyco

def do_sftp(server,source,dest,username,password,isRemove=False):
    isError = False
    try:
	sshUtils.sftp_to_host(server,username,password,source,dest,isSilent=not _isVerbose)
    except:
	isError = True
	exc_info = sys.exc_info()
	info_string = _utils.asMessage('\n'.join(traceback.format_exception(*exc_info)))
	print >>sys.stderr, info_string
    finally:
	if (not isError) and (isRemove):
	    os.remove(source)

def main(server,source,dest,username,password):
    if (os.path.exists(source)):
	do_sftp(server,source,dest,username,password)
    elif (any([ch in source for ch in ['*']])):
	_pattern = os.path.basename(source).replace('*','')
	_root_ = os.path.dirname(source)
	_files = [f for f in os.listdir(_root_) if (f.find(_pattern) > -1)]
	if (not _isDeletes):
	    # determine which files need to be copied based on whether or not they exist on the target server...
	    cx = sshUtils.SSHConnection(hostname=server,username=username,password=password)
	    try:
		_files = [f for f in _files if ( (cx.isdir(dest)) and (not cx.exists(cx.sep.join([dest,f]))) ) or _utils.fileSize(os.sep.join([_root_,f])) != cx.fileSize(cx.sep.join([dest,f]))]
	    finally:
		cx.close()
	for f in _files:
	    _f = os.sep.join([_root_,f])
	    do_sftp(server,_f,dest,username,password,isRemove=_isDeletes)
    else:
	print >>sys.stderr, '(%s) :: Source of "%s" does not apparently exist.' % (_utils.funcName(),source)

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('Computer Name: %s' % (_utils.getComputerName().lower()),pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--computer=?':'name the computer this command should run on.',
	    '--computer':'get the name the computer this command should run on.',
	    '--server=?':'name the server (tide2 or river).',
	    '--source=?':'name the source file path.',
	    '--dest=?':'name the dest file path.',
	    '--sudo':'use sudo on the server.',
	    '--username=?':'username for SFTP.',
	    '--password=?':'password for SFTP.',
	    '--deletes':'copies and removes source files upon completion.',
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
	    info_string = _utils.asMessage('\n'.join(traceback.format_exception(*exc_info)))
	    print >>sys.stderr, info_string
	    _isVerbose = False
	    
	_isDeletes = False
	try:
	    if _argsObj.booleans.has_key('isDeletes'):
		_isDeletes = _argsObj.booleans['isDeletes']
	except:
	    exc_info = sys.exc_info()
	    info_string = _utils.asMessage('\n'.join(traceback.format_exception(*exc_info)))
	    print >>sys.stderr, info_string
	    _isDeletes = False

	if (_isVerbose):
	    print '_argsObj=(%s)' % str(_argsObj)
	    
	_isHelp = False
	try:
	    if _argsObj.booleans.has_key('isHelp'):
		_isHelp = _argsObj.booleans['isHelp']
	except:
	    pass
	
	if (_isHelp):
	    ppArgs()
	
	_username = ''
	try:
	    __username = _argsObj.arguments['username'] if _argsObj.arguments.has_key('username') else _username
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print >>sys.stderr, info_string
	_username = __username
	
	_password = ''
	try:
	    __password = _argsObj.arguments['password'] if _argsObj.arguments.has_key('password') else _password
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print >>sys.stderr, info_string
	_password = __password
	
	_isSudo = False
	try:
	    if _argsObj.booleans.has_key('isSudo'):
		_isSudo = _argsObj.booleans['isSudo']
	except:
	    pass
	
	_server = ''
	try:
	    if _argsObj.arguments.has_key('server'):
		__server = _argsObj.arguments['server']
		if (len(__server) > 0):
		    _server = __server
	except:
	    exc_info = sys.exc_info()
	    info_string = _utils.asMessage('\n'.join(traceback.format_exception(*exc_info)))
	    print >>sys.stderr, info_string
	    
	_computer = _utils.getComputerName().lower()
	try:
	    if _argsObj.arguments.has_key('computer'):
		__computer = _argsObj.arguments['computer']
		if (len(__computer) > 0):
		    _computer = __computer
	except:
	    exc_info = sys.exc_info()
	    info_string = _utils.asMessage('\n'.join(traceback.format_exception(*exc_info)))
	    print >>sys.stderr, info_string

	_isComputer = False
	try:
	    if _argsObj.booleans.has_key('isComputer'):
		_isComputer = _argsObj.booleans['isComputer']
	except:
	    pass
	
	if (_isComputer):
	    print >>sys.stderr, 'Your com;puter name is "%s".' % (_computer)
	
	_source = ''
	try:
	    if _argsObj.arguments.has_key('source'):
		__source = _argsObj.arguments['source']
		if (len(__source) > 0):
		    _source = __source
	except:
	    exc_info = sys.exc_info()
	    info_string = _utils.asMessage('\n'.join(traceback.format_exception(*exc_info)))
	    print >>sys.stderr, info_string

   	_dest = ''
	try:
	    if _argsObj.arguments.has_key('dest'):
		__dest = _argsObj.arguments['dest']
		if (len(__dest) > 0):
		    _dest = __dest
	except:
	    exc_info = sys.exc_info()
	    info_string = _utils.asMessage('\n'.join(traceback.format_exception(*exc_info)))
	    print >>sys.stderr, info_string
 
	s_computer = _computer.lower()
	s_ComputerName = _utils.getComputerName().lower()
	if (s_computer == s_ComputerName):
	    _psyco.importPsycoIfPossible(main)
	    main(_server,_source,_dest,_username,_password)
	    sys.exit()
	else:
	    print >>sys.stderr, 'Nothing to do because "%s" is not "%s".' % (s_computer,s_ComputerName)
	    
	