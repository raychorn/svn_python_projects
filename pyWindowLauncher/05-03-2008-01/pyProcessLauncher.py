import os, sys
import Args
import PrettyPrint
import subprocess
import _utils
import time

_isVerbose = False
_progPath = ''
_freq = -1

_details_symbol = 'details'

def main(progPath):
    if (not os.path.exists(_details_symbol)):
	os.mkdir(_details_symbol)
    fOut = open('%s_%s.txt' % (os.sep.join([_details_symbol,'.'.join(_utils.timeStamp().replace(':','').split('.')[0:-1])]),os.path.basename(progPath).replace('.','_')),'w')
    e = os.environ
    p = subprocess.Popen([progPath], env=e, stdout=fOut, shell=False)
    p.wait()
    fOut.flush()
    fOut.close()

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()
	
    args = {'--help':'displays this help text.','--verbose':'output more stuff.','--progpath=?':'path to program to launch.','--freq=?':'how often (seconds) should the progpath be executed.'}
    _argsObj = Args.Args(args)
    print >>sys.stderr, '_argsObj=(%s)' % str(_argsObj)

    if ( (len(sys.argv) == 1) or (sys.argv[-1] == args.keys()[0]) ):
	ppArgs()
    else:
	try:
	    _isVerbose = _argsObj.booleans['isVerbose'] if _argsObj.booleans.has_key('isVerbose') else False
	except:
	    _isVerbose = False
    
	try:
	    _freq = int(_argsObj.arguments['freq']) if _argsObj.arguments.has_key('freq') else False
	except:
	    _freq = -1
    
	try:
	    if _argsObj.arguments.has_key('progpath'):
		_progPath = os.path.abspath(_utils.expandEnvMacro(_argsObj.arguments['progpath']))
	    else:
		_progPath = ''
	except:
	    _progPath = ''

	if (os.path.exists(_progPath)):
	    if (_freq > -1):
		while (1):
		    main(_progPath)
		    time.sleep(_freq)
	    else:
		main(_progPath)
	else:
	    print 'ERROR :: Unable to launch this program using the arguments as listed below.'
	    ppArgs()
	    print str(sys.argv)

