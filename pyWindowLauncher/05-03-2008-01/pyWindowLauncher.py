import os, sys
import win32gui
import Args
import PrettyPrint
import subprocess
import win32process

_isVerbose = False
_progPath = ''
_winName = ''

def callback(*args):
    pid = -1
    if (len(args) > 1):
	t = type(args[1]).__name__
	if (t == 'list'):
	    pid = args[1][0]
    hwnd = args[0]
    t = win32gui.GetWindowText(hwnd)
    _pid = []
    if (pid > 0):
	_pid = win32process.GetWindowThreadProcessId(hwnd)
    #if (pid in _pid):
    print 'callback :: args=[%s], t=[%s], pid=[%s], _pid=[%s]' % (str(args),t,pid,_pid)

def main(progPath,winName):
    fOut = open('stdout.txt','w')
    e = os.environ
    #e["PYTHONPATH"] = "c:\python25;"
    p = subprocess.Popen([progPath], env=e, stdout=fOut, shell=True) # {"PYTHONPATH": "c:\python25;"}
    print 'p.pid=[%s]' % p.pid
    win32gui.EnumWindows(callback,[p.pid])
    print 'p.poll()=[%s]' % p.poll()
    p.wait()
    print 'Done waiting...'
    fOut.flush()
    fOut.close()

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()
	
    args = {'--help':'displays this help text.','--verbose':'output more stuff.','--progpath=?':'path to program to launch.','--winname=?':'name of the window.'}
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
	    if _argsObj.arguments.has_key('progpath'):
		p = _argsObj.arguments['progpath']
		toks = p.split(os.sep)
		_toks = []
		for t in toks:
		    if (t.startswith('%') and t.endswith('%')):
			_t = t.replace('%','')
			if (os.environ.has_key(_t)):
			    t = os.environ[_t]
		    _toks.append(t)
		p = os.sep.join(_toks)
		_progPath = os.path.abspath(p)
	    else:
		_progPath = ''
	except:
	    _progPath = ''

	try:
	    _winName = _argsObj.arguments['winname'] if _argsObj.arguments.has_key('winname') else ''
	except:
	    _winName = ''

	if (os.path.exists(_progPath)) and (len(_winName) > 0):
	    main(_progPath,_winName)
	else:
	    print 'ERROR :: Unable to launch this program using the arguments as listed below.'
	    ppArgs()

