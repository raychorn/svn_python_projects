# Monitor RAM Usage on Linux boxes using ps aux command.

# Total RAM consumed, Average RAM consume, Data Points for Each Mongrel.

import os, sys

import sqlalchemy_models

from vyperlogix import misc
from vyperlogix.misc  import _utils
from vyperlogix.misc import ReportTheList
from vyperlogix.lists import ListWrapper

from vyperlogix.hash import lists

from vyperlogix.daemon.daemon import Log

from maglib.salesforce.cred import credentials
from maglib.salesforce.auth import CredentialTypes
from maglib.salesforce.auth import magma_molten_passphrase

_use_staging = False

__sf_account__ = credentials(magma_molten_passphrase,CredentialTypes.Magma_RHORN_Production)

from vyperlogix.wx.pyax.SalesForceLoginModel import SalesForceLoginModel
sf_login_model = SalesForceLoginModel(username=__sf_account__['username'],password=__sf_account__['password'])

StringIO = _utils.stringIO

_start_proc = '/usr/local/bin/mongrel_rails cluster::start -C /etc/mongrel_cluster/molten.yml --clean --only %d'

def main():
    if (sys.platform != 'win32'):
        from vyperlogix.process import Popen
        
        print 'BEGIN: %s' % (_utils.timeStampApache())
        
        buf = StringIO()
        shell = Popen.Shell(['ps --headers aux'],isExit=True,isWait=True,isVerbose=True,fOut=buf)
        lines = ListWrapper.ListWrapper([l for l in buf.getvalue().split('\n') if (len(l.strip()) > 0) and ( (l.find('/mongrel_rails') > -1) or ( (l.startswith('USER')) and (l.find('%CPU') > -1) and (l.find('%MEM') > -1)) )])
	_f = lines.findAllContaining('%CPU',returnIndexes=True)
	if (_isVerbose):
	    print '_f=%s' % (str(_f))
	if (len(_f) > 1):
	    for i in misc.reverseCopy(_f[1:]):
		del lines[i]
	if (_isVerbose):
	    ReportTheList.reportTheList(lines,'ps aux',fOut=sys.stdout)
        
        _lines = [ListWrapper.ListWrapper(l.split()) for l in lines]
	if (_isVerbose):
	    ReportTheList.reportTheList(_lines,'ps aux',fOut=sys.stdout)
        
	# BEGIN: Record the data in the database...
	_logPath = os.path.join(_dataPath,'data')
	_utils._makeDirs(_logPath)
	fname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
	fLog = open(os.path.join(_logPath,'%s_%s.log' % (fname,_utils.timeStampForFileName())),'a')
	logger = Log(fLog)
	_stdout = sys.stdout
	sys.stdout = logger
	try:
	    ReportTheList.reportTheList(_lines,'data',fOut=sys.stdout)
	finally:
	    sys.stdout = _stdout
	# END!   Record the data in the database...
	
        d = lists.HashedLists2()
        for _l in _lines:
            i = _l.findFirstContaining('-p')
            if (i > -1):
                n = int(_l[i+1])
		if (_isVerbose):
		    print _l[i:i+2],n
                d[n] = _l
		if (_isVerbose):
		    print '-'*40
	if (_isVerbose):
	    print '='*40
        
        keys = misc.sortCopy(d.keys())
        
	if (_isVerbose):
	    ReportTheList.reportTheList(d.keys(),'Present Mongrels',fOut=sys.stdout)

        d_expected = lists.HashedLists2(dict([(n,n) for n in xrange(8100,8160)]))
        for n in d.keys():
            del d_expected[n]

        commands = []
        for n in d_expected.keys():
            aCommand = _start_proc % int(n)
            commands.append(aCommand)

        if (len(commands) > 0):
            ReportTheList.reportTheList(d_expected.keys(),'Missing Mongrels',fOut=sys.stdout)
            ReportTheList.reportTheList(commands,'Commands',fOut=sys.stdout)
            
            _logPath = os.path.join(_dataPath,'log')
            _utils._makeDirs(_logPath)
            fname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
            fLog = open(os.path.join(_logPath,'%s_%s.log' % (fname,_utils.timeStampForFileName())),'a')
            logger = Log(fLog)
            _stdout = sys.stdout
            sys.stdout = logger
            
            try:
                buf = StringIO()
                shell = Popen.Shell(commands,isExit=True,isWait=True,isVerbose=True,fOut=buf)
                lines = [l for l in buf.getvalue().split('\n')]
                ReportTheList.reportTheList(lines,'Restart Dead Mongrels',fOut=sys.stdout)
            finally:
                sys.stdout = _stdout
                
        print 'END: %s' % (_utils.timeStampApache())
        print '='*80
            

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)
    
    from vyperlogix.misc import Args
    from vyperlogix.misc import PrettyPrint

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    }
    _argsObj = Args.Args(args)

    _progName = _argsObj.programName
    _isVerbose = False
    try:
	if _argsObj.booleans.has_key('isVerbose'):
	    _isVerbose = _argsObj.booleans['isVerbose']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_isVerbose = False
    
    if (_isVerbose):
	print '_argsObj=(%s)' % str(_argsObj)
	
    _isHelp = False
    try:
	if _argsObj.booleans.has_key('isHelp'):
	    _isHelp = _argsObj.booleans['isHelp']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_isHelp = False
	
    if (_isHelp):
	ppArgs()
    else:
	_stderr = sys.stderr
	_stdout = sys.stdout
	try:
	    if (_use_staging):
		sf_login_model.isStaging = True
		sf_login_model.perform_login(end_point=sf_login_model.get_endpoint(sf_login_model.sfServers['sandbox']))
	    else:
		sf_login_model.isStaging = False
		sf_login_model.perform_login(end_point=sf_login_model.get_endpoint(sf_login_model.sfServers['production']))
	finally:
	    sys.stderr = _stderr
	    sys.stdout = _stdout
	if (sf_login_model.isLoggedIn):
	    _dataPath = os.path.dirname(sys.argv[0])
	    main()
	else:
	    print >>logger, sf_login_model.lastError
	    print >>logger, str(sf_login_model)
 