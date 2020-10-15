import os, sys
import traceback
import logging

from vyperlogix.pyPdf.getPDFContent import getPDFContent
from vyperlogix.misc import _utils
from vyperlogix import oodb
from vyperlogix.logging import standardLogging
from vyperlogix.hash import lists

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

_years = [2005,2006,2007]

_input_path = 'Z:/#zDisk/#IRS/%04d/WellsFargo'

_tokens_list = []
_tokens_list.append('Account Statement')
_tokens_list.append('[Date]')
_tokens_list.append(['Account Number:','[Account_Number]'])
_tokens_list.append(['Deposits','[Deposits]'])
_tokens_list.append(['Withdrawals','[Withdrawals]'])
_tokens_list.append(['Balance on','[Balance_on]'])
_tokens_list.append('Activity detail')
_tokens_list.append('Deposits')
_tokens_list.append(['Total deposits','[Total_deposits]'])
_tokens_list.append('Withdrawals')
_tokens_list.append('Other withdrawals')
_tokens_list.append(['Total other withdrawals','[Total_other_withdrawals]'])

_tokens_list_i = 0

dbx_name = lambda root, name:os.sep.join([root,'.'.join([name.replace('.dbx',''),'dbx'])])
    
def mainPDF(y,top):
    root = os.path.dirname(os.path.abspath(sys.argv[0]))
    _data_root = _utils.safely_mkdir(fpath=root,dirname='dbx')
    y = '%04d'%y
    _data_root = _utils.safely_mkdir(fpath=_data_root,dirname=y)
    pdf_files = [f for f in os.listdir(top) if f.find('.pdf') > -1]
    pdf_files.sort()
    dbx_files = [f for f in os.listdir(_data_root) if f.find('.dbx') > -1]
    dbx_files.sort()
    s_pdf = set([n.split('.')[0] for n in pdf_files])
    s_dbx = set([n.replace('_pdf','').split('.')[0] for n in dbx_files])
    s = s_pdf - s_dbx
    _phase = 1
    if (len(s) == 0):
	_phase = 2
    print '(%s) :: _phase=(%s)' % (_utils.funcName(),_phase)
    if (_phase == 1):
	files = [f for f in os.listdir(_data_root)]
	for f in files:
	    _utils.safely_remove(dbx_name(_data_root,f))
    elif (_phase == 2):
	pass
    if (_isVerbose):
	print '(%s) :: pdf_files=(%s)' % (_utils.funcName(),str(pdf_files))
    phase_files = lists.HashedLists2({'1':pdf_files,'2':dbx_files})
    for f in phase_files['%d'%_phase][0:]:
	if (_phase == 1):
	    dbName = dbx_name(_data_root,f.replace('.','_'))
	elif (_phase == 2):
	    dbName = dbx_name(_data_root,f)
	dbx = oodb.PickledFastCompressedHash2(dbName)
	try:
	    if (_phase == 1):
		content = getPDFContent(os.sep.join([top,f]))
		if (_isVerbose):
		    print '(%s) :: f (%s)' % (_utils.funcName(),f)
		for pgNum,pg in content.iteritems():
		    if (_isVerbose):
			print '(%s) :: page (%s)' % (_utils.funcName(),pgNum)
		    s_key = '%02d'%pgNum
		    i_line = 1
		    for l in pg:
			dbx[s_key] = i_line
			dbx['%s.%02d'%(s_key,i_line)] = l
			if (_isVerbose):
			    print '\t(%s)' % l
			i_line += 1
		    if (_isVerbose):
			print '-'*80
	    elif (_phase == 2):
		print '(%s) :: f (%s)' % (_utils.funcName(),f)
		for k,v in dbx.iteritems():
		    print '%s=%s' % (k,v)
		pass
	    if (_isVerbose):
		print
		print '='*80
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print >>sys.stderr, '(%s) Error due to "%s".' % (_utils.funcName(),info_string)
	finally:
	    if (_phase == 1):
		dbx.sync()
	    dbx.close()

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible([mainPDF])

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()
      
    args = {'--help':'displays this help text.',
	    '--verbose':'output more stuff.',
	    '--logging=?':'[logging.INFO,logging.WARNING,logging.ERROR,logging.DEBUG]'}
    _argsObj = Args.Args(args)
    print >>sys.stderr, '_argsObj=(%s)' % str(_argsObj)
  
    _isHelp = False
    try:
	_isHelp = _argsObj.booleans['isHelp'] if _argsObj.booleans.has_key('isHelp') else False
    except:
	_isHelp = False
  
    _isVerbose = False
    try:
	_isVerbose = _argsObj.booleans['isVerbose'] if _argsObj.booleans.has_key('isVerbose') else False
    except:
	_isVerbose = False
  
    _logging = logging.WARNING
    try:
	_logging = eval(_argsObj.arguments['logging']) if _argsObj.arguments.has_key('logging') else logging.INFO
    except:
	_logging = logging.INFO
  
    name = _utils.getProgramName()
    logFileName = os.sep.join([os.path.abspath('.'),'%s.log' % (name)])
    print >>sys.stderr, 'name=[%s]' % name
    print >>sys.stderr, 'logFileName=[%s] %s (%s)' % (logFileName,standardLogging.explainLogging(_logging),_logging)
    standardLogging.standardLogging(logFileName,_level=_logging,isVerbose=_isVerbose)

    _version = _utils.getFloatVersionNumber()
    
    logging.info('_version=[%s]' % (_version))
    
    if (_version >= 2.51):
	if (_isHelp):
	    ppArgs()
	else:
	    for y in _years:
		mainPDF(y,_input_path % y)
    else:
	print >> sys.stderr, 'You seem to be using the wrong version of Python, try using 2.5.1 rather than "%s".' % sys.version.split()[0]

