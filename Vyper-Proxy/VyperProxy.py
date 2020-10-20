import os, sys
import time

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from vyperlogix.hash import lists

from vyperlogix.daemon.daemon import Log
from vyperlogix.daemon.daemon import EchoLog

from vyperlogix.process import Popen

from vyperlogix.zlib import zlibCompressor
from vyperlogix.gzip import gzipCompressor

from vyperlogix.misc.ReportTheList import reportTheList

from vyperlogix.process.killProcByPID import killProcByPID

from vyperlogix.win import WinProcesses
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

__copyright__ = """\
(c). Copyright 1990-2020, Vyper Logix Corp., 

                   All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

from vyperlogix.products import keys

#_template3 = '''START "VyperProxy:{{ port }}" /HIGH /B "{{ path }}\VyperProxyEngine.exe" {{ parms }}'''
#_template3a = '''{{ port }} --hosts "{{ hosts }}" --django "{{ djangos }}"'''

_template3 = keys._decode('53544152542022567970657250726F78793A7B7B20706F7274207D7D22202F48494748202F4220227B7B2070617468207D7D5C567970657250726F7879456E67696E652E65786522207B7B207061726D73207D7D')
_template3a = keys._decode('7B7B20706F7274207D7D202D2D686F73747320227B7B20686F737473207D7D22202D2D646A616E676F20227B7B20646A616E676F73207D7D22')

_basename_ = os.path.basename(sys.argv[0])
_root_ = os.path.dirname(sys.argv[0])
_log_path = os.path.join(_root_,'logs')

_confname_ = os.path.join(_root_,'%s.conf' % (_basename_.split('.')[0]))

def main(logger=sys.stderr):
    if (_isStart):
	_env = _utils.environ_copy()
	_hosts=[]
	commands = []
	for i in xrange(_django_port,_django_port+_django_num):
	    _hosts.append('127.0.0.1:%d' % (i))
	_djangos = '%s,%s,%s' % (_django.replace('\\','/'),_django_port,_django_num)
	for i in xrange(_port,_port+_num):
	    c = {'port':i,'hosts':','.join(_hosts),'djangos':_djangos}
	    s = _utils.expand_template(_template3a,c).strip()
	    c = {'port':i,'path':_path,'parms':s}
	    s = _utils.expand_template(_template3,c).strip()
	    commands.append(s)
	#print >>sys.stderr, 'commands=%s' % (commands)
	buffer = StringIO()
	shell = Popen.Shell(commands,env=_env,fOut=buffer,isExit=True,isWait=False,isVerbose=True)
	s = buffer.getvalue()
	print >>sys.stderr, 'VyperProxy is starting... Please remain patient, start-up can take about a minute.'
    elif (_isStop):
	if (os.path.exists(_path)):
	    print '_path=%s' % (_path)
	    _pidPath = os.path.join(_path,'pid')
	    if (os.path.exists(_pidPath)):
		print '_pidPath=%s' % (_pidPath)
		files = [os.path.join(_pidPath,f) for f in os.listdir(_pidPath)]
		print 'files=%s' % (files)
		aFileName = files[0]
		lines = _utils.read_lines_simple(aFileName,'r')
		pids = [_utils._int(line) for line in lines if (str(line).isdigit())]
		reportTheList(pids,'%s' % (aFileName))
		procTree = WinProcesses.ProcessTree()
		procTree.dump()
		print 'pids[0]=%d' % (pids[0])
		n = procTree.findForwards({'procId':pids[0]})
		n.dump()
		#for pid in pids:
		    #print 'killProcByPID :: pid=%s' % (pid)
		    #killProcByPID(pid,isVerbose=True)
	    else:
		print >>sys.stderr, 'ERROR 201: Cannot stop VyperProxy unless you stop the processes yourself manually.'
	else:
	    print >>sys.stderr, 'ERROR 101: Cannot stop VyperProxy unless you stop the processes yourself manually.'
	# +++ Code the tear-down sequence.
	# +++ Code the --license system
	# +++ Code the limits when no license is present. (When no license then shutdown if community edition is being used.)
	# +++ Encrypt the START templates.
	# +++ Code the useful help info while the process starts.
	# +++ Hide the stdout info we don't want people to see.
	pass

if (__name__ == '__main__'):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

    from vyperlogix.misc import Args
    from vyperlogix.misc import PrettyPrint

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--start':'start VyperProxy procs.',
	    '--stop':'stop VyperProxy procs.',
	    '--port=?':'first port number for VyperProxy.',
	    #'--num=?':'number of VyperProxy ports.',
	    #'--hosts=?':'comma delimited list of hosts.',
	    #'--script=?':'name of the script file.',
	    #'--path=?':'path to the VyperProxyEngine.',
	    '--django=?':'command line to the Django application (djangocerise or normal Django Command Line).',
	    #'--django_pythonpath=?':'PYTHONPATH for Django Applications..',
	    '--django_port=?':'first port number for Django Application.',
	    '--django_num=?':'number of Django ports.',
	    }
    _argsObj = Args.Args(args)

    _progName = _argsObj.programName

    _isHelp = False
    try:
	if _argsObj.booleans.has_key('isHelp'):
	    _isHelp = _argsObj.booleans['isHelp']
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
	_isHelp = False
	
    _isStart = False
    try:
	if _argsObj.booleans.has_key('isStart'):
	    _isStart = _argsObj.booleans['isStart']
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
	_isStart = False
	
    _isStop = False
    try:
	if _argsObj.booleans.has_key('isStop'):
	    _isStop = _argsObj.booleans['isStop']
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
	_isStop = False
	
    __port__ = 9000
    try:
	__port = _argsObj.arguments['port'] if _argsObj.arguments.has_key('port') else __port__
	__port__ = int(__port)
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
    _port = __port__
    
    if (_port < 1) or (_port > 65535):
	_port = __port__

    __num__ = 1
    try:
	__num = _argsObj.arguments['num'] if _argsObj.arguments.has_key('num') else __num__
	__num__ = int(__num)
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
    _num = __num__
    
    if (_num < 1) or (_num > 65535):
	_num = __num__
    
    __hosts__ = ''
    try:
	__hosts = _argsObj.arguments['hosts'] if _argsObj.arguments.has_key('hosts') else __hosts__
	__hosts__ = __hosts.split(',')
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
    _hosts = __hosts__
    
    __script__ = 'run-VyperProxy.cmd'
    try:
	__script = _argsObj.arguments['script'] if _argsObj.arguments.has_key('script') else __script__
	__script__ = __script
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
    _script = __script__
    
    if (not os.path.exists(_confname_)):
	t_root = _root_
	__path__ = os.path.dirname(_utils.searchForFileNamed('VyperProxyEngine.exe', t_root))
	while (not os.path.exists(os.path.join(__path__,'VyperProxyEngine.exe'))):
	    t_root = os.path.dirname(t_root)
	    __path__ = os.path.dirname(_utils.searchForFileNamed('VyperProxyEngine.exe', t_root))
	try:
	    __path = _argsObj.arguments['path'] if _argsObj.arguments.has_key('path') else __path__
	    __path__ = __path
	except Exception, details:
	    info_string = _utils.formattedException(details=details)
	    print >>sys.stderr, info_string
	_path = __path__
	
	fOut = open(_confname_,'w')
	try:
	    print >>fOut, '_path=%s' % (_path)
	finally:
	    fOut.flush()
	    fOut.close()
    else:
	d_conf = lists.HashedLists2()
	lines = lines = _utils.read_lines_simple(_confname_,'r')
	for line in lines:
	    toks = [t.strip() for t in line.split('=')]
	    if (len(toks) == 2):
		d_conf[toks[0]] = toks[-1]
	_path = d_conf['_path']
    
    __django__ = ''
    try:
	__django = _argsObj.arguments['django'] if _argsObj.arguments.has_key('django') else __django__
	__django__ = __django
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
    _django = __django__
    
    __django_pythonpath__ = ''
    try:
	__django_pythonpath = _argsObj.arguments['django_pythonpath'] if _argsObj.arguments.has_key('django_pythonpath') else __django_pythonpath__
	__django_pythonpath__ = __django_pythonpath
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
    _django_pythonpath = __django_pythonpath__
    
    __django_port__ = 8000
    try:
	__django_port = _argsObj.arguments['django_port'] if _argsObj.arguments.has_key('django_port') else __django_port__
	__django_port__ = int(__django_port)
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
    _django_port = __django_port__
    
    if (_django_port < 1) or (_django_port > 65535):
	_django_port = __django_port__

    __django_num__ = 1
    try:
	__django_num = _argsObj.arguments['django_num'] if _argsObj.arguments.has_key('django_num') else __django_num__
	__django_num__ = int(__django_num)
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
    _django_num = __django_num__
    
    if (_django_num < 1) or (_django_num > 65535):
	_django_num = __django_num__
    
    if (_isHelp):
	ppArgs()
    
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)

    if (len(_hosts) > 0):
	main(logger=sys.stderr)
    else:
	print >>_log, '%s :: Nothing to do.' % (misc.funcName())
