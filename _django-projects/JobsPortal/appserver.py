import os, sys

from vyperlogix import misc
from vyperlogix.misc  import _utils
from vyperlogix.misc import ReportTheList
from vyperlogix.lists import ListWrapper

from vyperlogix.hash import lists

from vyperlogix.daemon.daemon import Log

from vyperlogix.process import Popen

StringIO = _utils.stringIO

_scan_for_procs = 'ps -ef | grep manage2.py'

_kill_proc = 'kill -9 %s'

_start_proc = None #'/usr/local/cargochief/cargochief/run2.sh'

def handle_execute_command(cmd):
    try:
	buf = StringIO()
	shell = Popen.Shell([cmd],isExit=True,isWait=True,isVerbose=True,fOut=buf)
	print >> sys.stdout, buf.getvalue()
    except Exception, ex:
	info_str = _utils.formattedException(ex)
	print >> sys.stderr, info_str

def handle_restart(item,procid):
    if (_isVerbose):
	print 'item --> %s' % (item)
    if (_kill_proc):
	cmdBuf = StringIO()	    
	print >> cmdBuf, _kill_proc % (procid)
	handle_execute_command(cmdBuf.getvalue())
    if (_isVerbose):
	print 'cmd --> %s' % (cmdBuf.getvalue())
    if (_start_proc):
	cmdBuf2 = StringIO()	    
	print >> cmdBuf2, _start_proc
	if (_isVerbose):
	    print 'cmd2 --> %s' % (cmdBuf2.getvalue())

def main():
    if (sys.platform != 'win32'):
        print '_isVerbose=%s\n\n' % (_isVerbose)
        print 'BEGIN: %s' % (_utils.timeStampApache())
        
        buf = StringIO()
        shell = Popen.Shell([_scan_for_procs],isExit=True,isWait=True,isVerbose=True,fOut=buf)
	#print 'BEGIN: #1 %s' % ('*'*50)
	#print buf.getvalue()
	#print 'END!   #1 %s' % ('*'*50)
	#print '\n'
	#print 'BEGIN: #2 %s' % ('*'*50)
	#print buf.getvalue().split('\n')
	#print 'END!   #2 %s' % ('*'*50)
	lines2 = ListWrapper.ListWrapper([l for l in buf.getvalue().split('\n') if (len(l.strip()) > 0) and (l.find('python manage2.py') > -1)])
	if (_isVerbose):
	    ReportTheList.reportTheList(lines2,'2.',fOut=sys.stdout)
        
	_lines = [ListWrapper.ListWrapper(l.split()) for l in lines2]
	if (_isVerbose):
	    ReportTheList.reportTheList(_lines,'4.',fOut=sys.stdout)
	    
	d1 = lists.HashedLists()
	d2 = lists.HashedLists()
	
	for item in _lines:
	    d1[int(item[1])] = item
	    d2[int(item[2])] = item

	print 'BEGIN: #d1 %s' % ('*'*50)
	for k,v in d1.iteritems():
	    print '%s=%s' % (k,v)
	print 'END!   #d1 %s' % ('*'*50)

	print '\n\n'
	
	print 'BEGIN: #d2 %s' % ('*'*50)
	for k,v in d2.iteritems():
	    print '%s=%s' % (k,v)
	print 'END!   #d2 %s' % ('*'*50)

	print '\n\n'
	
	sorted_keys_d1 = misc.sortCopy(d1.keys())
	sorted_keys_d2 = misc.sortCopy(d2.keys())
	
	sorted_keys = []
	for item in sorted_keys_d1:
	    sorted_keys.append(item)
	for item in sorted_keys_d2:
	    sorted_keys.append(item)
	sorted_keys = misc.sortCopy(sorted_keys)

	print 'BEGIN: #sorted_keys %s' % ('*'*50)
	for k in sorted_keys:
	    print '%s' % (k)
	print 'END!   #sorted_keys %s' % ('*'*50)

	print '\n\n'
	
	if (sorted_keys) and (len(sorted_keys) > 0):
	    try:
		print 'BEGIN: #Terminate Processes %s %s' % (sorted_keys,'*'*50)

		for proc_id in sorted_keys:
		    print 'proc_id --> %s' % (proc_id)
		    item1 = d1[proc_id]
		    item2 = d2[proc_id]
		    if (item1):
			handle_restart(item1,proc_id)
		    elif (item2):
			handle_restart(item2,proc_id)

		print 'END!   #Terminate Process %s' % ('*'*50)
	
		print '\n\n'
	    except Exception, ex:
		info_str = _utils.formattedException(ex)
		print >> sys.stderr, info_str
	else: # start the server because it does not appear to be running at this time...
	    if (_start_proc):
		try:
		    buf = StringIO()
		    shell = Popen.Shell([_start_proc],isExit=True,isWait=True,isVerbose=True,fOut=buf)
		    print >> sys.stdout, buf.getvalue()
		except Exception, ex:
		    info_str = _utils.formattedException(ex)
		    print >> sys.stderr, info_str
	
        print 'END: %s' % (_utils.timeStampApache())
        print '='*80
            

if (__name__ == '__main__'):
    # from vyperlogix.misc import _psyco
    # _psyco.importPsycoIfPossible(func=main)
    
    from vyperlogix.misc import Args
    from vyperlogix.misc import PrettyPrint

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    }
    __args__ = Args.SmartArgs(args)

    _progName = __args__.programName
    
    _isVerbose = True #__args__.get_var('isVerbose',Args._bool_,False)
    
    if (_isVerbose):
	print '__args__=(%s)' % str(__args__)
	
    _isHelp = __args__.get_var('isHelp',Args._bool_,False)
	
    if (_isHelp):
	ppArgs()
    else:
	_stderr = sys.stderr
	_stdout = sys.stdout
	try:
	    pass
	finally:
	    sys.stderr = _stderr
	    sys.stdout = _stdout
	    main()
 