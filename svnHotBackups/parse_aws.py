import  os, sys

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from  vyperlogix import misc

from  vyperlogix.aws import parse

__path__ = ''  #--source="./sample-aws-ls.txt"

__data__ = []

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
	    '--source=?':'path to the source.',
	    }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = __args__.programName
	
	_isVerbose = __args__.get_var('isVerbose',misc.isBooleanString,False)
	_isDebug = __args__.get_var('isDebug',misc.isBooleanString,False)
	_isHelp = __args__.get_var('isHelp',misc.isBooleanString,False)

	print 'DEBUG: _isVerbose=%s' % (_isVerbose)
	print 'DEBUG: _isDebug=%s' % (_isDebug)
	print 'DEBUG: _isHelp=%s' % (_isHelp)

	if (_isHelp):
	    ppArgs()
	    sys.exit()

	_source_path = __args__.get_var('source',parse.is_valid_file,__path__)
	__path__ = _source_path

	print 'DEBUG: __path__=%s' % (__path__)

	__is_found__ = False
	__data__ =  parse.parseAws(__path__)
	for  item in  __data__:
	    try:
		if item.key.find('repo1-14793.tar.gz') >  -1:
		    __is_found__ = True
		    break
	    except:
		pass
	print '__is_found__=%s' % (__is_found__)
	print __data__
	