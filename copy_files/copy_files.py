# Copies files using multi-threads only during certain hours of the day.
# Program automatically stops at the desired time each day.

import os, sys

from vyperlogix.misc import _utils

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

def main():
    pass

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)
    
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--source=?':'the location of the files to be copied (source).',
	    '--dest=?':'the destination of the file copy and move process.',
	    '--hours=?':'effective hours of operation in a list [8-12,12-5].',
	    }
    _argsObj = Args.Args(args)

    _progName = _argsObj.programName
    _isVerbose = False
    try:
	if _argsObj.booleans.has_key('isVerbose'):
	    _isVerbose = _argsObj.booleans['isVerbose']
    except:
	exc_info = sys.exc_info()
	info_string = CaseWatcher.asMessage('\n'.join(traceback.format_exception(*exc_info)))
	print >>sys.stderr, info_string
	logging.warning(info_string)
	_isVerbose = False

    _isHelp = False
    try:
	if _argsObj.booleans.has_key('isHelp'):
	    _isHelp = _argsObj.booleans['isHelp']
    except:
	exc_info = sys.exc_info()
	info_string = CaseWatcher.asMessage('\n'.join(traceback.format_exception(*exc_info)))
	print >>sys.stderr, info_string
	logging.warning(info_string)
	_isHelp = False

    if (_isHelp):
	print '_argsObj=(%s)' % str(_argsObj)
	ppArgs()

    __source__ = 'x:\\'
    try:
	__source = _argsObj.arguments['source'] if _argsObj.arguments.has_key('source') else __source__
	if (len(__source) == 0) or (not os.path.exists(__source)):
	    print >>sys.stderr, 'ERROR: Cannot locate "%s" so cannot continue.' % (__source)
	    sys.exit(1)
	__source__ = __source
    except:
	pass
    _source = __source__
    
    __dest__ = 'z:\\'
    try:
	__dest = _argsObj.arguments['dest'] if _argsObj.arguments.has_key('dest') else __dest__
	if (len(__dest) == 0) or (not os.path.exists(__dest)):
	    print >>sys.stderr, 'ERROR: Cannot locate "%s" so cannot continue.' % (__dest)
	    sys.exit(1)
	__dest__ = __dest
    except:
	pass
    _dest = __dest__

    __hours__ = "{'Mo-Th':'21-5','Fr-Su':'0-0'}"
    try:
	__hours = _argsObj.arguments['hours'] if _argsObj.arguments.has_key('hours') else __hours__
	__hours__ = __hours
    except:
	pass
    _hours = __hours__

    v = _utils.getFloatVersionNumber()
    if (v >= 3.54):
	main()
    else:
	print >>sys.stderr, 'ERROR: Expected to run in Python 2.5.4 or later however cannot run in Python %s.' % (sys.version)
	sys.exit(1)
    