import os, sys

from vyperlogix.hash import lists
from vyperlogix.misc  import _utils
from vyperlogix.process import Popen
from vyperlogix.lists import ListWrapper
from vyperlogix.misc import ReportTheList

from vyperlogix.misc import ObjectTypeName

StringIO = _utils.stringIO

_pid_folder = '/var/run/django'

def _main(ip,port1,port2):
    print '_pid_folder is "%s".' % (_pid_folder)
    
    ports = xrange(port1,port2+1)
    
    buf = StringIO()
    cmd = 'ps -ef | grep %s:' % (ip)
    shell = Popen.Shell([cmd],isExit=True,isWait=True,isVerbose=True,fOut=buf)
    _lines = [l for l in buf.getvalue().split('\n') if (len(l.strip()) > 0)]
    _lines = [ListWrapper.ListWrapper(l.split()) for l in _lines]
    d_lines = lists.HashedLists2(dict([(l[l.findFirstContaining('127.0.0.1:')],l[1]) for l in _lines if (l.findFirstContaining('127.0.0.1:') > -1) and (l.findFirstContaining('webserver.pyc') > -1)]))
    
    _d_lines = lists.HashedLists2(d_lines.insideOut())
    
    l_files = [os.path.join(_pid_folder,f) for f in os.listdir(_pid_folder)]
    
    d_files = lists.HashedLists2()
    for f in l_files:
        pid = int(_utils.readFileFrom(f))
        d_files[pid] = f
    
    #for l in _lines:
        #print '(**) %s' % (str(l))
    
    lists.prettyPrint(d_lines,title='d_lines')
    
    lists.prettyPrint(_d_lines,title='_d_lines')
    
    pids = []
    for p in ports:
	_ip_port = '%s:%s' % (ip,p)
	if (d_lines.has_key(_ip_port)):
	    pids.append(d_lines[_ip_port])
    
    cmds = []
    for k,v in _d_lines.iteritems():
	if (k in pids):
	    cmds.append('kill -9 %s' % (k))
	    _k = int(k)
	    if (d_files.has_key(_k)):
		_f = d_files[_k]
		print 'Removing "%s".' % (_f)
		os.remove(_f)
    
    print 'BEGIN: %s' % (cmds)
    shell = Popen.Shell(cmds,isExit=True,isWait=True,isVerbose=True,fOut=sys.stdout)
    print 'END!  %s' % (cmds)

def main(kill_spec):
    print 'kill_spec is "%s".' % (kill_spec)
    toks = kill_spec.split(':')
    toks2 = toks[-1].split('-')
    port1 = port2 = int(toks2[0])
    if (len(toks2) > 1):
	port2 = int(toks2[-1])
    ip = toks[0]
    _main(ip,port1,port2)

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
	    '--kill=?':'127.0.0.1:9000-9002.',
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
	
    _kill_spec = None
    try:
	if _argsObj.arguments.has_key('kill'):
	    _kill_spec = _argsObj.arguments['kill']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_kill_spec = None
	
    if (_isHelp):
	ppArgs()
    else:
	main(_kill_spec)
    