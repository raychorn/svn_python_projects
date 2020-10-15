import os, sys
import ConfigParser

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.classes.SmartObject import SmartFuzzyObject

from vyperlogix.google import chromeUrl

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint


if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
	    '--fpath=?':'path to the shortcuts.',
	    }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = __args__.programName
	
	_isVerbose = __args__.get_var('isVerbose',bool,False)
	_isDebug = __args__.get_var('isDebug',bool,False)
	_isSkip = __args__.get_var('isSkip',bool,False)
	_isHelp = __args__.get_var('isHelp',bool,False)

	if (_isHelp):
	    ppArgs()
	    sys.exit()

	__fpath = __args__.get_var('fpath',misc.isString,None)
	
	if (os.path.exists(__fpath)):
	    items = chromeUrl.get_items_from_url_shortcuts(fpath=__fpath)
	    for k, v in items.iteritems():
		if (misc.isList(v)):
		    for item in v:
			print item
		else:
		    print v
	else:
	    print >> sys.stderr, 'WARNING: Cannot locate the directory "%s".' % (__fpath)

