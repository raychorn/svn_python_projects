import os, sys
import re
import glob

from vyperlogix.classes import SmartObject, CooperativeClass
from vyperlogix.lists import ListWrapper

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc import _utils

from vyperlogix.pyPdf.pyPdf import PdfFileReader, PdfFileWriter

import models

__db__ = None

__ftype__ = '*.pdf'

def report():
    ioBuf = _utils.stringIO()
    print >>ioBuf, '%s %s %s' % ('='*20,misc.funcName(),'='*20)
    report_sig = ioBuf.getvalue()
    print 'BEGIN: %s' % (report_sig)
    for aStatement in models.Statement:
	print '%s' % (aStatement.filename)
    print 'END!   %s' % (report_sig)

def remove_records_from_statement(target):
    items = [item for item in models.LineItem if item.statement == target]
    for anItem in items:
	pass

class BankStatementPDFParser(CooperativeClass.Cooperative):
    def __init__(self):
	self._Account_Statement_ = '_Account_Statement_'
	self._Account_Number_ = '_Account_Number_'
	self._Activity_summary_ = 'Activity_summary'
	self._Activity_detail_ = 'Activity_detail'
	self._Deposits_Or_Withdrawals_ = 'Deposits'
	self._Deposits_ = 'Deposits'
	self._Total_deposits_ = 'Total_deposits'
	self._Withdrawals_Or_Other_Withdrawals_ = 'Withdrawals Or Other Withdrawals'
	self._Total_Withdrawals_ = 'Total_Withdrawals'
	self._Balance_on_ = 'Balance_on'
	
	self.__symbols__ = SmartObject.SmartFuzzyObject({
	    self._Account_Statement_:re.compile(r"Account\s*Statement"),
	    self._Account_Number_:re.compile(r"Account\s*Number\s*:\s*(?P<account_number>.*)"),
	    self._Activity_summary_:re.compile(r"Activity\s*summary"),
	    self._Balance_on_:re.compile(r"Balance\s*on\s*(?P<date>(0[1-9]|1[012])[- /.][0-9]{2})\s*(?P<sign>[-])?\s*[$](?P<amount>[+-]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2})"),
	    self._Deposits_Or_Withdrawals_:r"(?P<type>Deposits|Withdrawals)\s*(?P<amount>(?P<sign>[$+-]*)?\s*[$]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2})",
	    self._Activity_detail_:re.compile(r"Activity\s*detail"),
	    self._Deposits_:re.compile(r"\A\s*Deposits\s*\Z"),
	    self._Withdrawals_Or_Other_Withdrawals_:re.compile(r"\A\s*(?P<type>Withdrawals|Other\s*[Ww]ithdrawals)\s*\Z"),
	    self._Total_deposits_:re.compile(r"Total\s*(?P<type>deposits)\s*(?P<amount>(?P<sign>[$+-])?\s*[$]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2})"),
	    self._Total_Withdrawals_:re.compile(r"Total.*(?P<type>withdrawals)\s*(?P<amount>(?P<sign>[$+-])?\s*[$]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2})")
	})
	self.__symbols__['Withdrawals'] = self.__symbols__['Deposits'];
	self._has_dollar_value_ = re.compile(r"(?P<amount>[+-]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2})")
	self._has_date_ = re.compile(r"\A(?P<date>(0[1-9]|1[012])[- /.][0-9]{2})\s*")
	self._Account_Statement_Date_Range_ = re.compile(r"(?P<fromMM>January|February|March|April|May|June|July|August|September|October|November|December)\s*(?P<fromDD>[1-9]|[12][0-9]|3[01])\s*,\s*(?P<fromYYYY>(19|20|21|22|23|24|25)[0-9]{2})\s*(through|-|to)\s*(?P<toMM>January|February|March|April|May|June|July|August|September|October|November|December)\s*(?P<toDD>[1-9]|[12][0-9]|3[01])\s*,\s*(?P<toYYYY>(19|20|21|22|23|24|25)[0-9]{2})")
	self._continued_ = re.compile(r"\A\s*Continued\s*on\s*next\s*page\s*\Z")
	self.has_Account_Statement_ = False
	self.has_Account_Number_Cnt = 0
	self.l_Account_Number_data = []
	self.has_Account_Summary_Cnt = 0
	self.l_Account_Summary_data = []
	self.l_Account_Deposit_data = []
	self.l_Account_Withdrawals_data = []
	self.isCollectingDeposts = False
	self.isCollectingWithdrawals = False
	self.isCollectingAccountSummary = False
	self.isCollectingDetails = False
	self.isSkippingItem = False
	
    def __hasDollarValue__(self,value):
	return (len(self._has_dollar_value_.findall(value)) > 0)

    def __hasDate__(self,value):
	return (len(self._has_date_.findall(value)) > 0)

    def __isContinued__(self,value):
	return (len(self._continued_.findall(value)) > 0)

    def parse(self,target,aList):
	iMax = len(aList)
	self.wasConsumed = False
	for i in xrange(0,iMax):
	    if (self.isSkippingItem):
		self.isSkippingItem = False
		self.wasConsumed = False
		continue
	    item = aList[i]
	    anItem = models.LineItem(statement = target,item = item)
	    for k in self.__symbols__.keys():
		aPattern = self.__symbols__[k]
		if (ObjectTypeName.typeClassName(aPattern) == '_sre.SRE_Pattern'):
		    matches = aPattern.findall(item)
		    if (len(matches) > 0):
			models.Element(_type = k, matches = [str(m).strip() for m in matches if (len(str(m)) > 0)], item = anItem)
			if (k == self._Account_Statement_):
			    if (not self.has_Account_Statement_):
				next_item = aList[i+1] if (i+1 < iMax) else None
				if (next_item):
				    next_pattern = self._Account_Statement_Date_Range_
				    next_matches = next_pattern.findall(next_item)
				    if (len(next_matches) > 0):
					self.has_Account_Statement_ = True
					models.Element(_type = '_Account_Statement_Date_Range_', matches = next_matches, item = anItem)
					self.isSkippingItem = True
					self.wasConsumed = True
					break
			elif (not self.isCollectingAccountSummary) and (not self.isCollectingWithdrawals) and (k == self._Account_Number_):
			    self.has_Account_Number_Cnt += 1
			    if (self.has_Account_Number_Cnt == 1):
				self.l_Account_Number_data.append(item)
				self.wasConsumed = True
				break
			    elif (self.has_Account_Number_Cnt == 2):
				models.Element(_type = k, matches = self.l_Account_Number_data, item = anItem)
				self.has_Account_Number_Cnt = 0
				self.l_Account_Number_data = []
				self.wasConsumed = True
				break
			elif (k == self._Activity_summary_):
			    self.has_Account_Summary_Cnt += 1
			    if (self.has_Account_Summary_Cnt == 1):
				self.isCollectingAccountSummary = True
				self.l_Account_Summary_data.append(item)
				self.wasConsumed = True
				break
			elif (k == self._Activity_detail_):
			    self.has_Account_Summary_Cnt += 1
			    if (self.has_Account_Summary_Cnt == 2):
				models.Element(_type = self._Activity_summary_, matches = self.l_Account_Summary_data, item = anItem)
				self.l_Account_Summary_data = []
				self.isCollectingAccountSummary = False
				self.isCollectingDetails = True
				self.wasConsumed = True
				break
			elif (k == self._Deposits_):
			    self.l_Account_Deposit_data = []
			    self.isCollectingDeposts = True
			    self.wasConsumed = True
			    break
			elif (k == self._Total_deposits_):
			    self.l_Account_Deposit_data.append(item)
			    models.Element(_type = k, matches = self.l_Account_Deposit_data, item = anItem)
			    self.l_Account_Deposit_data = []
			    self.isCollectingDeposts = False
			    self.wasConsumed = True
			    break
			elif (k == self._Withdrawals_Or_Other_Withdrawals_):
			    if (not self.isCollectingWithdrawals):
				self.isCollectingWithdrawals = True
				if (self.__hasDollarValue__(item)):
				    self.l_Account_Withdrawals_data.append(item)
			    self.wasConsumed = True
			    break
			elif (k == self._Total_Withdrawals_):
			    self.isCollectingWithdrawals = False
			    self.l_Account_Withdrawals_data.append(item)
			    models.Element(_type = k, matches = self.l_Account_Withdrawals_data, item = anItem)
			    self.l_Account_Withdrawals_data = []
			    break
			elif (k == self._Balance_on_):
			    self.l_Account_Summary_data.append(item)
			    self.wasConsumed = True
			    break
	    if (not self.wasConsumed):
		if (self.has_Account_Number_Cnt == 1): # Collect records until next occurence of the _Account_Number_
		    self.l_Account_Number_data.append(item)
		    continue
		if (self.isCollectingDeposts):
		    if (self.__hasDollarValue__(item)):
			self.l_Account_Deposit_data.append(item)
		    continue
		elif (self.isCollectingWithdrawals):
		    def isMatching(value,pattern):
			if (ObjectTypeName.typeClassName(pattern) == '_sre.SRE_Pattern'):
			    matches = pattern.findall(value)
			    return (len(matches) > 0)
			return False
		    if (self.__hasDate__(item)) and (self.__hasDollarValue__(item)):
			toks = ListWrapper.ListWrapper(item.split())
			_i_ = toks.findFirstMatching(self._has_date_,callback=isMatching)
			_j_ = toks.findFirstMatching(self._has_dollar_value_,callback=isMatching)
			memo = ' '.join(toks[_i_+1:_j_-1]) if (_i_ > -1) and (_i_ < _j_) else None
			next_item = aList[i+1] if (i+1 < iMax) else None
			if (next_item):
			    isC = self.__isContinued__(next_item)
			    if (not self.__hasDate__(next_item)) and (not self.__hasDollarValue__(next_item)) and (not isC):
				memo += ' ' + next_item
				item = '%s %s %s' % (toks[_i_],memo,toks[_j_])
				self.isSkippingItem = True
			    elif (isC):
				self.isSkippingItem = True
				self.wasConsumed = True
			self.l_Account_Withdrawals_data.append(item)
		    continue
		elif (self.isCollectingAccountSummary):
		    if (self.__hasDollarValue__(item)):
			self.l_Account_Summary_data.append(item)
		    continue
	    else:
		self.wasConsumed = False
	pass

def main(_iterator):
    global __db__
    parser = BankStatementPDFParser()
    __db__ = models.pod.Db(file = db_fpath, dynamic_index = True)
    try:
	for fname in _iterator:
	    if (os.path.exists(fname)):
		statements = [s for s in models.Statement if s.filename == fname]
		statement = models.Statement(filename=fname) if (len(statements) == 0) else statements[0]
		print 'Statement is %s' % (statement.filename)
		input1 = PdfFileReader(file(fname, "rb"))
		print "title = %s" % (input1.getDocumentInfo().title)
		numPages = input1.getNumPages()
		print "%s has %s pages." % (fname,numPages)
		print '='*40
		remove_records_from_statement(statement)
		for pageNo in xrange(0,numPages):
		    pg = input1.getPage(pageNo)
		    t = pg.extractText()
		    parser.parse(statement,t)
		    print '\n'.join(t)
		    print '-'*40
		print '='*40
	    else:
		print >>sys.stderr, 'Nothing to do !'
    except Exception, e:
	info_string = _utils.formattedException(details=e)
	print >>sys.stderr, info_string
    finally:
	__db__.commit()
	report()

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=[main,report])
    
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
	    '--clear':'clear the database.',
	    '--input=?':'name the input file or a glob spec.',
	    }
    _argsObj = Args.Args(args)

    _progName = _argsObj.programName
    db_fpath = '%s.sqlite3' % (_progName)
    _isVerbose = False
    try:
	if _argsObj.booleans.has_key('isVerbose'):
	    _isVerbose = _argsObj.booleans['isVerbose']
    except:
	exc_info = sys.exc_info()
	info_string = '\n'.join(traceback.format_exception(*exc_info))
	print info_string
	_isVerbose = False
	
    _isDebug = False
    try:
	if _argsObj.booleans.has_key('isDebug'):
	    _isDebug = _argsObj.booleans['isDebug']
    except:
	pass
    
    _isClear = False
    try:
	if _argsObj.booleans.has_key('isClear'):
	    _isClear = _argsObj.booleans['isClear']
    except:
	pass
    
    _isHelp = False
    try:
	if _argsObj.booleans.has_key('isHelp'):
	    _isHelp = _argsObj.booleans['isHelp']
    except:
	pass
    
    if (_isClear):
	import glob
	print 'Clear DB !'
	for f in glob.glob('%s*' % (db_fpath)):
	    try:
		print 'os.unlink(%s)' % (f)
		os.unlink(f)
	    except WindowsError, e:
		pass
	
    if (_isHelp):
	ppArgs()
	sys.exit()
    
    _input = __ftype__
    try:
	__input = _argsObj.arguments['input'] if _argsObj.arguments.has_key('input') else _input
    except:
	exc_info = sys.exc_info()
	info_string = '\n'.join(traceback.format_exception(*exc_info))
	print info_string
    _input = __input

    if (_input in ['.','*.*']) or (_input.find('*.') > -1):
	_input = __ftype__
    try:
	iterator = glob.iglob(_input)
	aFile = iterator.next()
	if (os.path.exists(aFile)) and (os.path.isdir(aFile)):
	    spec = os.sep.join(_input.split(os.sep)+[__ftype__])
	    iterator = glob.iglob(spec)
	else:
	    iterator = glob.iglob(_input)
    except:
	pass
    main(iterator)


