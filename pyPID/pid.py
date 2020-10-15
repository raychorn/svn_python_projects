# Monitor RAM Usage on Linux boxes using ps aux command.

# Total RAM consumed, Average RAM consume, Data Points for Each Mongrel.

import os, sys

from vyperlogix import misc
from vyperlogix.misc  import _utils
from vyperlogix.misc import ReportTheList
from vyperlogix.lists import ListWrapper

from vyperlogix.classes.SmartObject import SmartFuzzyObject

from vyperlogix.hash import lists

from vyperlogix.daemon.daemon import Log

StringIO = _utils.stringIO

special_cases = ['php-cgi']

template_php_cgi = '''
check process {{ process-name }} with pidfile {{ pid_file }}
  if cpu > 60% for 2 cycles then alert
  if cpu > 80% for 5 cycles then alert
  if totalmem > 200.0 MB for 5 cycles then alert
  group php
'''

template_php_cgi_stop = '''
kill -9 {{ process-pid }}
'''

def main():
    if (sys.platform != 'win32'):
	from vyperlogix.process import Popen

	if (len(_pname) > 0) or (len(_cmd) > 0):
	    if (_isVerbose):
		print 'BEGIN: %s' % (_utils.timeStampApache())
	    
	    buf = StringIO()
	    _command = 'ps -ef'
	    if (_isVerbose):
		print 'INFO: %s' % (_command)
	    shell = Popen.Shell([_command],shell='bash',isExit=True,isWait=True,isVerbose=True,fOut=buf)
	    lines = ListWrapper.ListWrapper([l.split() for l in buf.getvalue().split('\n') if (len(l.strip()) > 0)])
	    cols = lines[0]
	    if (_isVerbose):
		print 'INFO: %s' % (str(cols))
		ReportTheList.reportTheList(lines,'ps',fOut=sys.stdout)
	    
	    if (_isVerbose):
		print 'INFO: %s' % (__file__)

	    _pid = -1
	    for item in lines[1:]:
		d = lists.HashedLists2()
		i = 0
		for aCol in cols[0:-1]:
		    d[aCol] = item[i]
		    i += 1
		d[cols[-1]] = ' '.join(item[i:])
		if (_isVerbose):
		    d.prettyPrint(title='ps')
		    print '-'*40
		so = SmartFuzzyObject(d)
		if (_isVerbose):
		    print 'so.cmd is "%s", _cmd is "%s", _pname is "%s".' % (so.cmd,_cmd,_pname)
		if ( ( (len(_cmd) > 0) and (so.cmd.find(_cmd) > -1) ) or ( (len(_pname) > 0) and (so.cmd.find(_pname) > -1) ) ) and (so.cmd.find(__file__) == -1):
		    _pid = so.pid
		    if (_isVerbose):
			print 'INFO: (%s) %s' % (_pid,d)
		    break
	    if (_isVerbose):
		print '='*40
		
	    if (_pid > -1):
		fOut = open(_pidfile,'w')
		try:
		    print >>fOut, _pid
		finally:
		    fOut.flush()
		    fOut.close()
		    if (_isVerbose):
			print 'pid of %s written to %s' % (_pid,_pidfile)
	    else:
		print 'WARNING: Cannot write the pidfile to %s because the pid that was found is %s.' % (_pidfile,_pid)
	    
	    if (_isVerbose):
		print 'END: %s' % (_utils.timeStampApache())
		print '='*80
	else:
	    if (len(_pname) == 0):
		print 'WARNING: No named process via the --pname=? option.\nNothing to do!'
	    if (len(_cmd) == 0):
		print 'WARNING: No named process via the --cmd=? option.\nNothing to do!'

	for special_case in special_cases:
	    d0 = lists.HashedLists()
	    d = lists.HashedLists()
	    
	    buf = StringIO()
	    shell = Popen.Shell(['ps axco pid,command | grep %s' % (special_case)],isExit=True,isWait=True,isVerbose=True,fOut=buf)
	    lines = ListWrapper.ListWrapper([l.split() for l in buf.getvalue().split('\n') if (len(l.strip()) > 0)])
	    if (_isVerbose):
		ReportTheList.reportTheList(lines,special_case,fOut=sys.stdout)

	    for item in lines:
		d0[item[0]] = item[-1]
		d[item[-1]] = item[0]
	    if (_isVerbose):
		d.prettyPrint(title=special_case)

	    pathName = '/etc/monit/%s*.monitrc' % (special_case)
	    try:
		dname = os.path.dirname(pathName)
		files_monitrc = [os.path.join(dname,f) for f in os.listdir(pathName)]
	    except:
		files_monitrc = []
	    if (_isVerbose):
		ReportTheList.reportTheList(files_monitrc,pathName,fOut=sys.stdout)

	    _pids = []
	    pathName = '/var/run/%s*.pid' % (special_case)
	    try:
		dname = os.path.dirname(pathName)
		files_pid = [os.path.join(dname,f) for f in os.listdir(pathName)]
		for fn in files_pid:
		    _pids.append(_utils.readFileFrom(fn))
	    except:
		files_pid = []
	    if (_isVerbose):
		ReportTheList.reportTheList(files_pid,pathName,fOut=sys.stdout)

	    if (len(files_pid) != len(d)):
		if (_isVerbose):
		    print 'INFO: Number of procs named %s does not match the number (%s) of pid files.' % (d.keys(),len(files_pid))
		# create the pid files...
		
	    for f in files_pid:
		if (_isVerbose):
		    print 'INFO: Removing %s.' % (f)
		os.remove(f)
	    # remove all the existing files_monitrc files...
	    for f in files_monitrc:
		if (_isVerbose):
		    print 'INFO: Removing %s.' % (f)
		os.remove(f)
	    if (_isPhpcgi):
		# create all the files for files_monitrc using the latest files_pid...
		num = 1
		for f in d0.keys():
		    pname = '%s%s' % (special_case,num)
		    vname = '/var/run/%s.pid' % (pname)
		    fname = '/etc/monit/%s.monitrc' % (pname)
		    s = template_php_cgi.replace('{{ process-name }}',pname).replace('{{ pid_file }}',vname)
		    if (_isVerbose):
			print 'INFO: Writing %s.' % (fname)
		    _utils.writeFileFrom(fname,s)
		    _utils.writeFileFrom(vname,f)
		    num = num + 1
	    if (_isPhpcgiStop):
		if (len(_name) > 0):
		    fOut = open(_name,'w')
		    try:
			for f in d0.keys():
			    s = template_php_cgi_stop.replace('{{ process-pid }}',f)
			    print >>fOut, '%s' % (s.strip())
		    finally:
			fOut.flush()
			fOut.close()
		else:
		    print 'WARNING: No named file via the --name=? option.\nNothing to do!'

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
	    '--pname=?':'name the process.',
	    '--cmd=?':'name the command (can include any part of the command).',
	    '--pidfile=?':'name the pid file name (usually /var/run/something.pid).',
	    '--phpcgi':'make PID files for all the php-cgi procs.',
	    '--phpcgi=?':'make a shell script to stop all the phpcgi procs when the value to the right of the "=" is stop.',
	    '--name=?':'name the script file.',
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
	
    _isPhpcgi = False
    try:
	if _argsObj.booleans.has_key('isPhpcgi'):
	    _isPhpcgi = _argsObj.booleans['isPhpcgi']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_isPhpcgi = False

    _isPhpcgiStop = False
    try:
	if _argsObj.arguments.has_key('phpcgi'):
	    _isPhpcgiStop = _argsObj.arguments['phpcgi'] == 'stop'
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_isPhpcgiStop = False

    _name = ''
    try:
	if _argsObj.arguments.has_key('name'):
	    _name = _argsObj.arguments['name']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string

    _pname = ''
    try:
	if _argsObj.arguments.has_key('pname'):
	    _pname = _argsObj.arguments['pname']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_pname = ''
	
    _cmd = ''
    try:
	if _argsObj.arguments.has_key('cmd'):
	    _cmd = _argsObj.arguments['cmd']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_cmd = ''
	
    _pidfile = ''
    try:
	if _argsObj.arguments.has_key('pidfile'):
	    _pidfile = _argsObj.arguments['pidfile']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_pidfile = ''
	
    if (len(_pidfile) == 0):
	_pidfile = '/var/run/%s.pid' % (_pname)

    if (_isHelp):
	ppArgs()
    else:
	_dataPath = os.path.dirname(sys.argv[0])
	main()
 