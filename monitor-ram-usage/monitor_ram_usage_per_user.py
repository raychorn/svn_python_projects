# Monitor RAM Usage on Linux boxes using ps aux command.

# Total RAM consumed, Average RAM consume, Data Points for Each Mongrel.

import os, sys

from vyperlogix import misc
from vyperlogix.misc  import _utils
from vyperlogix.misc import ReportTheList
from vyperlogix.lists import ListWrapper

from vyperlogix.hash import lists

from vyperlogix.daemon.daemon import Log

StringIO = _utils.stringIO

_rss_total = 0

def main():
    if (sys.platform != 'win32'):
        from vyperlogix.process import Popen
        
        print 'BEGIN: %s' % (_utils.timeStampApache())
        
        buf = StringIO()
        shell = Popen.Shell(['cat /etc/passwd |cut -d: -f1'],isExit=True,isWait=True,isVerbose=True,fOut=buf)
        users = ListWrapper.ListWrapper([l.strip() for l in buf.getvalue().split('\n') if (len(l.strip()) > 0)])
	
	d = lists.HashedLists()
	
	def accumulate(n):
	    global _rss_total
	    _rss_total += n
	
	funcs = {'RSS':lambda n:accumulate(n)}
	
	_headers = []
	for aUser in users:
	    buf = StringIO()
	    shell = Popen.Shell(['ps -u %s -o pid,rss,command' % (aUser)],isExit=True,isWait=True,isVerbose=True,fOut=buf)
	    data = ListWrapper.ListWrapper([l.strip() for l in buf.getvalue().split('\n') if (len(l.strip()) > 0)])
	    if (len(data) > 1):
		#ReportTheList.reportTheList(data,'data for %s' % (aUser))
		_headers = data[0].split()
		for item in data[1:]:
		    _toks = item.split()
		    _d = lists.HashedLists2()
		    n = len(_headers)
		    for i in xrange(0,n):
			aHeader = _headers[i]
			_d[aHeader] = _toks[i] if (i < n-1) else ' '.join(_toks[i:])
			if (str(_d[aHeader]).isdigit()):
			    _d[aHeader] = int(_d[aHeader])
			if (funcs.has_key(aHeader)) and (callable(funcs[aHeader])):
			    funcs[aHeader](_d[aHeader])
		    #_d.prettyPrint(title='Data for %s' % (aUser))
		    d[aUser] = _d
		    #print '+'*40
		#print '-'*40
	    
	print '(+++) _rss_total = %s' % (_rss_total)
	d.prettyPrint(title='Users')
	    
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
	_dataPath = os.path.dirname(sys.argv[0])
	main()
 