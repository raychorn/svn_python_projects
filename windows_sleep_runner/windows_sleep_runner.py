import os, sys
import time

from vyperlogix import misc
from vyperlogix.process import Popen
from vyperlogix.misc import _utils

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix.process.shell import SmartShell

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
	    '--sleep=?':'a number of seconds.',
            '--command=?':'a command line.',
            '--sysout=?':'a filename or valid filespec for the OS.',
	    }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	__progName__ = os.path.splitext(__args__.programName)[0]

	_isVerbose = __args__.get_var('isVerbose',Args._bool_,False)
	if (_isVerbose):
	    print 'DEBUG: _isVerbose=%s' % (_isVerbose)
	_isDebug = __args__.get_var('isDebug',Args._bool_,False)
	if (_isVerbose):
	    print 'DEBUG: _isDebug=%s' % (_isDebug)
	_isHelp = __args__.get_var('isHelp',Args._bool_,False)
	if (_isVerbose):
	    print 'DEBUG: _isHelp=%s' % (_isHelp)

	if (_isHelp):
	    ppArgs()
	    sys.exit()

	__sleep__ = __args__.get_var('sleep',Args._int_,60*60*4) # 4 hours per run...
	if (_isVerbose):
	    print 'DEBUG: __sleep__=%s' % (__sleep__)
	try:
	    __sleep__ = eval(__sleep__)
	except TypeError:
	    __sleep__ = int(__sleep__)
	except Exception, ex:
	    info_string = _utils.formattedException(details=ex)
	    print >> sys.stderr, info_string

	__sysout__ = __args__.get_var('sysout',Args._str_,os.sep.join([os.path.abspath('.'),__progName__])+'.txt')
	fpath = os.path.dirname(__sysout__)
	if (len(fpath) == 0):
	    __sysout__ = os.sep.join([os.path.abspath('.'),__sysout__])
	if (_isVerbose):
	    print 'DEBUG: __sysout__=%s' % (__sysout__)
	    
	__cmd__ = __args__.get_var('command',Args._str_,'dir c:\\')
	if (_isVerbose):
	    print 'DEBUG: __cmd__=%s' % (__cmd__)
		
	if (misc.isString(__cmd__)):
	    while (1):
		__begin__ = -1
		__end__ = -1
		__elapsed__ = -1
		__sleep_interval__ = -1
		try:
		    parts = list(os.path.splitext(__sysout__))
		    parts.insert(len(parts)-1,_utils.timeStampForFileName())
		    parts[0] = '_'.join(parts[0:len(parts)-1])
		    del parts[1]
		    fOut = open(''.join(parts),'w',buffering=1)
		    print 'DEBUG: fOut.name=%s' % (fOut.name)
		except:
		    fOut = sys.stdout
		def __callback__(ss,data=None):
		    global __begin__
		    if (data) and (misc.isString(data)) and (len(data) > 0):
			print 'BEGIN:'
			print 'data=%s' % (data)
			print 'END !'
		    if (__begin__ == -1):
			__begin__ = time.time()
		def __onExit__(ss):
		    global __begin__, __end__, __elapsed__, __sleep_interval__
		    print 'BEGIN:'
		    if (__end__ == -1):
			__end__ = time.time()
			__elapsed__ = __end__ - __begin__
			__sleep_interval__ = (__sleep__ - __elapsed__) if (__sleep__ > __elapsed__) else 1
			print 'DEBUG: __elapsed__=%d' % (__elapsed__)
			print 'DEBUG: __sleep__=%d' % (__sleep__)
			print 'DEBUG: __sleep_interval__=%d' % (__sleep_interval__)
			if (__sleep_interval__ > 0):
			    print 'DEBUG: sleeping for %d seconds.' % (__sleep_interval__)
			    time.sleep(__sleep_interval__)
		    if (fOut not in [sys.stdout,sys.stderr]):
			fOut.flush()
			fOut.close()
		    print 'END !'
		ss = SmartShell(__cmd__,callback=__callback__,isDebugging=True,onExit=__onExit__,sysout=fOut)
		ss.execute()
	else:
	    print >>sys.stderr, 'WARNING: Cannot continue without a command line.'
