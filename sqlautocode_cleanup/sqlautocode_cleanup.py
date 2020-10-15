# Cleans-up for sqlautocode for Windows use.

import os, sys

from vyperlogix.misc import _utils

def main():
    _text = _utils.readFileFrom(_input,mode='r',noCRs=False)
    toks = _text.split('\r')
    _text = '\n'.join(toks)
    while (_text.find('\n\n') > -1):
	_text = _text.replace('\n\n','\n')

    _utils.writeFileFrom(_input,_text,mode='w')

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
	    '--input=?':'the input filename.',
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
	
    _input = ''
    try:
	if _argsObj.arguments.has_key('input'):
	    _input = _argsObj.arguments['input']
    except Exception, _details:
	info_string = _utils.formattedException(details=_details)
	print info_string
	_input = ''
	
    if (_isHelp):
	ppArgs()
    else:
	if (os.path.exists(_input)):
	    main()
	else:
	    print 'ERROR: Nothing to do, cannot use file --input=%s.' % (_input)
