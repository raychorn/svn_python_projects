import os
import sys
from vyperlogix.misc import decodeUnicode
import pprint
from vyperlogix.money import floatValue
import traceback
from vyperlogix import oodb
import globalVars
from vyperlogix import _utils
from vyperlogix import misc
from vyperlogix.misc import _psyco
from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint
from vyperlogix.hash import lists
from vyperlogix.lists import ListWrapper
from vyperlogix.enum.Enum import *

import re
import logging
from vyperlogix.logging import standardLogging
#from vyperlogix.oodb import PickledHash
#from vyperlogix.oodb import PickledHash2
#from vyperlogix.oodb import PickleMethods

_available_sources = ['wellsfargo','paypal']
#_wellsfargo_input_path = ['Z:/#zDisk/#IRS/2005/WellsFargo','Z:/#zDisk/#IRS/2006/WellsFargo','Z:/#zDisk/#IRS/2007/WellsFargo']
_wellsfargo_input_path = ['Z:/#zDisk/#IRS/2009/WellsFargo/0285742623']
#_paypal_input_path = ['Z:/#zDisk/#IRS/2005/www.paypal.com/Download_01-01-2005_to_12-31-2005.csv','Z:/#zDisk/#IRS/2006/www.paypal.com/Download_01-01-2006_to_12-31-2006.csv','Z:/#zDisk/#IRS/2007/www.paypal.com/Download_01-01-2007_to_12-31-2007.csv']
_paypal_input_path = ['Z:/#zDisk/#IRS/2009/PayPal.com/Download_2009.csv']

_deposits_symbol = 'Deposits'
_withdrawls_symbol = 'Withdrawals'

isProblemWithMoneyAnalysis = False
isProblemWithChecksAnalysis = False

class ProcessingModel(Enum):
    deposits_withdrawals = 2**0
    just_withdrawals = 2**1
    just_deposits = 2**2

def accountStatementParser(content,token):
    d = []
    d.append(token)
    for l in content:
	if (l.find(token) > -1):
	    d.append(l)
	    d.append(content[len(d)-1])
	    break
    if (len(d) == 1):
	n = len(content)
	for i in xrange(0,len(content)):
	    l = ' '.join([content[j] for j in xrange(i,min(i+2,n))])
	    if (l.find(token) > -1):
		d.append(l)
		d.append(content[len(d)-1])
		break
    return d

def accountDataParser(content,token,isUnique=True):
    d = []
    d.append(token)
    for l in content:
	if (l.find(token) > -1):
	    d.append([t.split() for t in l.split(':')])
	    if (isUnique):
		break
    if (len(d) == 1):
	n = len(content)
	for i in xrange(0,len(content)):
	    l = ' '.join([content[j] for j in xrange(i,min(i+2,n))])
	    if (l.find(token) > -1):
		d.append(content[j+1])
		if (isUnique):
		    break
    return d

def accountDataBetweenParser(content,token1,token2):
    d = []
    d.append([token1,token2])
    isCollecting = False
    method = 1
    while ( (len(d) == 1) and (method <= 2) ):
	for l in content:
	    if (method == 1):
		if ( (not isCollecting) and (l.lower() == token1.lower()) ):
		    isCollecting = True
	    elif (method == 2):
		if ( (not isCollecting) and (l.lower().find(token1.lower()) > -1) ):
		    isCollecting = True
	    if (isCollecting):
		d.append([t.split() for t in l.split(':')])
		if (len(d[-1]) == 2):
		    dd = d[-1]
		    if ( (isTokenDateMMYY(dd[0][0])) and (isTokenDollarAmount(dd[1][-1])) ):
			for tok in d[-1][-1]:
			    d[-1][0].append(tok)
			del d[-1][-1]
	    isDoneCollecting = False
	    if (isCollecting):
		_token2 = list(token2) if not isinstance(token2,str) else [token2]
		for s in _token2:
		    if (l.find(s) > -1):
			isDoneCollecting = True
			break
	    if ( (isCollecting) and (isDoneCollecting) ):
		isCollecting = False
		break
	method += 1
    _d = []
    for i in xrange(len(d)-1,0,-1):
	dl = d[i]
	if ( (len(dl) == 1) and (dl[0][0] == token1) ):
	    _d.append(dl)
	    _d.reverse()
	    d = _d
	    break
	else:
	    _d.append(dl)
    return d

def isTokenDateMMYY(token):
    toks = token.split('/')
    return ( (len(toks) == 2) and (toks[0].isdigit()) and (toks[-1].isdigit()) )

def isTokenDollarAmount(token):
    toks = token.replace('$','').replace(',','').split('.')
    return ( (len(toks) == 2) and (toks[0].isdigit()) and (toks[-1].isdigit()) )

def depositsListAnalysis(content):
    d = []
    skip = []
    for i in xrange(0,len(content)-1):
	if (i in skip):
	    skip = skip[1:]
	    continue
	c = content[i]
	if (isTokenDateMMYY(c[0][0])):
	    d.append(c[0])
	    hasDollarAmount = False
	    while (not hasDollarAmount):
		if (isTokenDollarAmount(c[0][-1])):
		    hasDollarAmount = True
		else:
		    i += 1
		    skip.append(i)
		    c = content[i]
		    for cc in c[0]:
			d[-1].append(cc)
    return d

def depositsListReplacement(content,newList):
    for iBegin in xrange(1,len(content)-1):
	if (len(content[iBegin][0]) == 1):
	    break
    for iEnd in xrange(len(content)-1,iBegin,-1):
	if (len(content[iEnd][0]) == 1):
	    break
    cBegin = content[0:iBegin-1]
    cEnd = content[iEnd+1:]
    content = []
    for c in cBegin:
	content.append(c)
    for c in newList:
	content.append(c)
    for c in cEnd:
	content.append(c)
    return content

def withdrawlsListAnalysis(content):
    d = []
    skip = []
    for i in xrange(0,len(content)-1):
	if (i in skip):
	    skip = skip[1:]
	    continue
	c = content[i]
	if (isTokenDateMMYY(c[0][0])):
	    d.append(c[0])
	    hasDollarAmount = False
	    while (not hasDollarAmount):
		if (isTokenDollarAmount(c[0][-1])):
		    hasDollarAmount = True
		else:
		    i += 1
		    skip.append(i)
		    c = content[i]
		    for cc in c[0]:
			d[-1].append(cc)
    return d

def withdrawlsListReplacement(content,newList):
    for iBegin in xrange(1,len(content)-1):
	if (len(content[iBegin][0]) == 1):
	    break
    for iEnd in xrange(len(content)-1,iBegin,-1):
	if (len(content[iEnd][0]) == 1):
	    break
    content[iBegin:iEnd] = newList
    return content

def withdrawlsChecksAnalysis(content,token1):
    d = []
    isCollecting = False
    isNeedingValue = False
    for l in content:
	if (not isCollecting):
	    tag = l[0]
	    while (not isinstance(tag,str)):
		tag = tag[0]
	    if (tag.find(token1) > -1):
		isCollecting = True
		continue
	if (isCollecting):
	    tag = [t.replace('*','').replace(',','') for t in l[0]]
	    while ( (len(tag) > 2) and (tag[0].isdigit()) and (isTokenDateMMYY(tag[1])) and (isTokenDollarAmount(tag[2])) ):
		d.append(tag[0:3])
		del tag[:3]
		isNeedingValue = True
	    _tag = ' '.join(tag)
	    _tag = _tag.lower()
	    if ( (len(_tag) > 0) and (isNeedingValue) and ( (_tag.find('total checks') > -1) or (_tag.find('other withdrawals') > -1) or (isTokenDollarAmount(tag[-1])) ) ):
		if ( (isTokenDollarAmount(tag[-1])) or (_tag.find('other withdrawals') > -1) ):
		    d.append(l[0])
		    isCollecting = False
		    break
    return d

def moneyValuesAnalysis(content,total_value):
    global isProblemWithMoneyAnalysis
    isProblemWithMoneyAnalysis = False
    transactions = []
    try:
	tag = content[0]
	while (not isinstance(tag,str)):
	    tag = tag[0]
	isAdding = (tag.lower().find(_deposits_symbol.lower()) > -1)
	isSubtracting = (tag.find(_withdrawls_symbol) > -1)
	if ( (not isAdding) and (not isSubtracting) ):
	    logging.warning('(moneyValuesAnalysis) :: Invalid Money Analysis Data.')
	    return
	_total = floatValue.floatAsDollars(0.0)
	num = 0
	for l in content:
	    toks = l
	    if (isinstance(toks[0],str)):
		if ( ( (isTokenDateMMYY(toks[0])) or ( (len(toks) == 3) and (isTokenDateMMYY(toks[1])) ) ) and (isTokenDollarAmount(toks[-1])) ):
		    val = floatValue.floatValue(toks[-1],floatValue.Options.asDollar)
		    if (isAdding):
			_total += val
			num += 1
		    else:
			_total -= val
			num += 1
		    transactions.append([toks[0],' '.join(toks[1:-1]),toks[-1]])
	if ( (_total != total_value) and (abs(_total) != abs(total_value)) ):
	    isProblemWithMoneyAnalysis = True
	    _msg = ''
	    msg += '(moneyValuesAnalysis) :: Invalid Money Analysis Data because the totals do not match.'
	    msg += '\t _total=(%s) [%s]' % (_total,str(_total.__class__))
	    msg += '\t total_value=(%s) [%s]' % (total_value,str(total_value.__class__))
	    msg += '\t num=(%s)' % (num)
	    logging.warning(msg)
	else:
	    logging.info('(moneyValuesAnalysis) :: Values match.')
    except Exception, details:
	_traceback = traceback.format_exc()
	logging.error('(moneyValuesAnalysis).ERROR :: Reason is "%s".\n%s' % (str(details),_traceback))
    return transactions

def valueOfChecks(content):
    global isProblemWithChecksAnalysis
    isProblemWithChecksAnalysis = False
    _total = floatValue.floatAsDollars(0.0)
    _totalValue = floatValue.floatAsDollars(0.0)
    if (isinstance(content,list)):
	for l in content:
	    toks = l
	    if (isinstance(toks[0],str)):
		if ( (len(toks) > 1) and (isTokenDateMMYY(toks[1])) and (isTokenDollarAmount(toks[-1])) ):
		    val = floatValue.floatValue(toks[-1],floatValue.Options.asDollar)
		    _total += val
		else:
		    val = floatValue.floatValue(toks[-1],floatValue.Options.asDollar)
		    _totalValue += val
	if (_total != _totalValue):
	    isProblemWithChecksAnalysis = True
	    msg = '(valueOfChecks) :: Invalid Checks Analysis Data because the totals do not match.'
	    msg += '\t _total=(%s) [%s]' % (_total,str(_total.__class__))
	    msg += '\t _totalValue=(%s) [%s]' % (_totalValue,str(_totalValue.__class__))
	    logging.warning(msg)
	else:
	    logging.info('(valueOfChecks) :: Check Values match.')
    return _total

def persistTransactions(filename,transactions):
    if (isinstance(filename,str)):
	if (isinstance(transactions,list)):
	    dbx = PickledHash.PickledHash(filename)
	    for t in transactions:
		if (isTokenDollarAmount(t[-1])):
		    t[1] = t[1].replace(',','')
		    t[-1] = '%10.2f' % floatValue.floatValue(t[2],floatValue.Options.asFloat)
		    t[-1] = t[-1].strip()
		dbx['%d' % len(dbx)] = t
	    dbx.close()
	else:
	    logging.warning('(persistTransactions) :: Invalid type for transactions which is of type "%s" but was supposed to be of type "list".' % (type(transactions)))
    else:
	logging.warning('(persistTransactions) :: Invalid type for filename which is of type "%s" but was supposed to be of type "str".' % (type(filename)))

def break_into_pages(aList):
    '''
    Process:
    
    Place all lines into a database, identify the unique ID for each line.  Process each line and remove from the database as each line is processed.
    Display visually to ensure proper processing using Adobe AIR.
    '''
    from vyperlogix.iterators import iterutils
    d1 = lists.HashedLists2()
    d2 = lists.HashedLists2()
    l_content = ListWrapper.ListWrapper(aList)
    pageRegX = re.compile(r"\APage\s\d\sof\s\d\Z")
    mm_dd_RegX = re.compile(r"\A[0-9]{2}/[0-9]{2}\Z")
    dollars_RegX = re.compile(r"^\$?(\d{1,3}(,\d{3})*|(\d+))(\.\d{2})?$")
    x = l_content.findAllMatching(pageRegX,returnIndexes=True)
    x.insert(0,0)
    x.append(len(l_content))
    n = len(x)
    for i in xrange(0,len(x)):
	aChunk = l_content[x[i]:x[i+1]] if ((i+1) < n) else l_content[x[i]:]
	l = len(aChunk)
	if (l > 0):
	    k = aChunk[0]
	    foo = pageRegX.match(k)
	    d1[k] = aChunk[1:] if (l > 1) and (foo) else aChunk
    keys = ListWrapper.ListWrapper(d1.keys())
    m_keys = keys.findAllMatching(pageRegX)
    for aKey in m_keys:
	d_model = lists.HashedFuzzyLists()
	proc_model = ProcessingModel.just_deposits
	l_blob = ListWrapper.ListWrapper(d1[aKey])
	for l in l_blob:
	    d_model[l] = l
	if (d_model['deposits']) and (d_model['withdrawals']):
	    proc_model = ProcessingModel.deposits_withdrawals
	elif (d_model['withdrawals']):
	    proc_model = ProcessingModel.just_withdrawals
	i_blob = l_blob.findAllMatching(mm_dd_RegX,returnIndexes=True)
	l_dates = l_blob[i_blob[0]:i_blob[-1]]
	l_temp = l_blob[i_blob[-1]+1+1:]
	l_trans = []
	del l_temp[0]
	del l_temp[0]
	for item in l_dates:
	    aChunk = l_temp[0]
	    if (len(aChunk) == 0):
		del l_temp[0]
		aChunk = l_temp[0]
	    l_trans.append(aChunk)
	    del l_temp[0]
	while (1):
	    if (dollars_RegX.match(l_temp[0])) or (len(l_temp) == 0):
		break
	    del l_temp[0]
	while (1):
	    if (dollars_RegX.match(l_temp[-1])) or (len(l_temp) == 0):
		break
	    del l_temp[-1]
	l_dollars = l_temp[0:-1]
	d_items = lists.HashedLists()
	if (proc_model == ProcessingModel.deposits_withdrawals):
	    d_items['deposits'] = lists.HashedLists()
	    d_deposits = d_items['deposits'][0]
	    d_items['withdrawals'] = lists.HashedLists()
	    d_withdrawals = d_items['withdrawals'][0]
	    while (1):
		if (not mm_dd_RegX.match(l_dates[0])) or (len(l_dates) == 0):
		    break
		try:
		    d_deposits[l_dates[0]] = {'trans':l_trans[0]+(l_trans[1] if (len(l_dates[1]) == 0) else ''),'$':floatValue.floatValue(l_dollars[0])}
		    while (1):
			if (len(l_trans[0]) > 0) or (len(l_trans) == 0):
			    del l_trans[0]
			    break
			del l_trans[0]
		    while (1):
			if (dollars_RegX.match(l_dollars[0])) or (len(l_dollars) == 0):
			    del l_dollars[0]
			    break
			del l_dollars[0]
		    while (1):
			if (mm_dd_RegX.match(l_dates[0])) or (len(l_dates) == 0):
			    del l_dates[0]
			    break
			del l_dates[0]
		except:
		    break
	    num_deposits = len(d_deposits)
	    total_deposits = floatValue.floatValue('0.00')
	    while (1):
		if (dollars_RegX.match(l_dollars[0])) or (len(l_dollars) == 0):
		    total_deposits = floatValue.floatValue(l_dollars[0])
		    del l_dollars[0]
		    break
		del l_dollars[0]
	    while (1):
		if (mm_dd_RegX.match(l_dates[0])) or (len(l_dates) == 0):
		    break
		del l_dates[0]
	    while (1):
		if (len(l_trans[0]) > 0) or (len(l_trans) == 0):
		    break
		del l_trans[0]
	    while (1):
		if (dollars_RegX.match(l_dollars[0])) or (len(l_dollars) == 0):
		    break
		del l_dollars[0]
	    pass
	elif (proc_model == ProcessingModel.just_withdrawals):
	    pass
	elif (proc_model == ProcessingModel.just_deposits):
	    pass
	pass
    pass

def main_wellsfargo(fpath):
    if (not os.path.exists(globalVars.data_folder_symbol)):
	os.mkdir(globalVars.data_folder_symbol)
    pp = pprint.PrettyPrinter(indent=4)
    files = [f for f in os.listdir(fpath) if f.find('.txt') > -1]
    files.sort()
    print '(%s) :: files=(%s)' % (misc.funcName(),str(files))
    for f in files:
	content = [l.strip() for l in open(os.sep.join([fpath,f]), 'r').readlines()]
	#content = [l for l in content if len(l) > 0]
	d_content = break_into_pages(content)
	# 0xff ?
	print '(%s) :: f=(%s)' % (misc.funcName(),f)
	d_accountStatement = accountStatementParser(content,'Account Statement')
	statement_tag = d_accountStatement[-1]
	fileName = '.'.join(['_'.join(f.replace(',','').split()),'db'])
	print '(%s) :: fileName=(%s)' % (misc.funcName(),fileName)
	toks = fileName.split('.')
	deposits_fileName = os.sep.join([globalVars.data_folder_symbol,'.'.join([toks[0]+'_deposits',toks[-1]])])
	print '(%s) :: deposits_fileName=(%s)' % (misc.funcName(),deposits_fileName)
	withdrawls_fileName = os.sep.join([globalVars.data_folder_symbol,'.'.join([toks[0]+'_withdrawls',toks[-1]])])
	print '(%s) :: withdrawls_fileName=(%s)' % (misc.funcName(),withdrawls_fileName)
	d_accountNumber = accountDataParser(content,'Account Number:')
	d_balanceOn = accountDataParser(content,'Balance on', False)
	d_deposits = accountDataParser(content,'Deposits')
	d_deposits[1] = d_deposits[1][0]
	value_deposits = floatValue.floatValue(d_deposits[1][1],floatValue.Options.asDollar)
	d_withdrawls = accountDataParser(content,'Withdrawals')
	d_withdrawls[1] = d_withdrawls[1][0]
	if ( (not isTokenDollarAmount(d_withdrawls[1][1])) and (len(d_withdrawls[1]) > 2) ):
	    d_withdrawls[1][1] = ''.join(d_withdrawls[1][1:])
	    del d_withdrawls[1][-1]
	value_withdrawls = floatValue.floatValue(d_withdrawls[1][1],floatValue.Options.asDollar)
	d_depositsList = accountDataBetweenParser(content,'Deposits','Total deposits')
	d_depositsList[0] = d_depositsList[0][0]
	d_withdrawlsList = accountDataBetweenParser(content,'Total deposits',['Total withdrawals','Total other withdrawals'])
	print
	print '='*80
	print
	print '='*80
	print 'd_accountStatement:'
	pp.pprint(d_accountStatement)
	print '-'*80
	print 'd_accountNumber:'
	pp.pprint(d_accountNumber)
	print '-'*80
	print 'd_balanceOn:'
	pp.pprint(d_balanceOn)
	print '-'*80
	print 'd_deposits:'
	pp.pprint(d_deposits)
	print '-'*80
	print 'd_withdrawls:'
	pp.pprint(d_withdrawls)
	print '-'*80
	print 'd_depositsList: %6.2f' % value_deposits
	d_depositsList = depositsListReplacement(d_depositsList,depositsListAnalysis(d_depositsList))
	transactions_deposits = moneyValuesAnalysis(d_depositsList,value_deposits)
	if (isProblemWithMoneyAnalysis):
	    pp.pprint(transactions_deposits)
	persistTransactions(deposits_fileName,transactions_deposits)
	print '-'*80
	print 'd_withdrawlsList: %6.2f' % value_withdrawls
	# Gather checks from d_withdrawlsList - lines between 'Checks' and 'Total Checks'
	d_withdrawlsChecks = withdrawlsChecksAnalysis(d_withdrawlsList,'Checks')
	d_withdrawlsList = withdrawlsListReplacement(d_withdrawlsList,withdrawlsListAnalysis(d_withdrawlsList))
	val_chks = valueOfChecks(d_withdrawlsChecks)
	value_withdrawls += val_chks
	transactions_withdrawls = moneyValuesAnalysis(d_withdrawlsList,value_withdrawls)
	print 'len(transactions_withdrawls)=(%s)' % len(transactions_withdrawls)
	chks = d_withdrawlsChecks[0:-1]
	if (len(chks) > 0):
	    chks.reverse()
	    for chk in chks:
		transactions_withdrawls.insert(0,chk)
	if (isProblemWithMoneyAnalysis):
	    pp.pprint(d_withdrawlsChecks)
	    print '*'*80
	    pp.pprint(transactions_withdrawls)
	persistTransactions(withdrawls_fileName,transactions_withdrawls)
	
	print
	print '='*80
	print
	print '='*80

def post_process_paypal(fpath):
    def normalizedDate(d):
	toks = d.split('/')
	del toks[1]
	toks[0] = '%02d' % int(toks[0])
	toks[-1] = '%04d' % int(toks[-1])
	return '/'.join(toks)

    toks = [t for t in fpath.split('/') if (t.isdigit())]
    try:
	_yyyy = int(toks[0])
    except:
	_yyyy = -1
    if (_yyyy > -1):
	p = os.path.abspath('data\\paypal\\%d' % _yyyy)
	try:
	    d_map_dates = lists.HashedLists2()
	    d_map_name = lists.HashedLists2()
	    files = [os.sep.join([p,f]) for f in os.listdir(p)]
	    for f in files:
		dbx = PickledHash(f,PickleMethods.useSafeSerializer)
		if (d_map_dates[f] == None):
		    d_map_dates[f] = f.replace('.dbx','-details_dates.dbx')
		ff_dates = d_map_dates[f]
		if (d_map_name[f] == None):
		    d_map_name[f] = f.replace('.dbx','-details_name.dbx')
		ff_name = d_map_name[f]
		dbx_details_date = PickledHash2(ff_dates,PickleMethods.useSafeSerializer)
		dbx_details_name = PickledHash2(ff_name,PickleMethods.useSafeSerializer)
		_keys = dbx.normalizedSortedKeys()
		for k,v in dbx.iteritems():
		    print '(%s) :: %s=(%s) %s' % (f,k,type(v),v)
		    norm_k = normalizedDate(k)
		    print '\t(dbx_details_date) :: %s=%s' % (norm_k,v)
		    dbx_details_date[norm_k] = v
		    print '\t(dbx_details_date) :: (%d) (%s) %s=%s' % (len(dbx_details_date[norm_k]),type(dbx_details_date[norm_k]),norm_k,v)
		    name_k = v['Name'] if not isinstance(v,str) else v
		    print 'name_k=[%s]' % name_k
		    print '\t(dbx_details_name) :: %s=%s' % (norm_k,v)
		    dbx_details_name[name_k] = v
		dbx.close()
		dbx_details_name.sync()
		dbx_details_name.close()
		dbx_details_date.sync()
		dbx_details_date.close()
		print '='*80
		print ''
		pass
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print >>sys.stderr, info_string
    else:
	print >>sys.stderr, 'Unable to process due to a problem with the determination of the year from "%s", one of these tokens "%s" must be a number.' % (fpath,toks)
    pass

def main_paypal(fpath):
    _data_folder_name = os.path.abspath(os.sep.join([globalVars.data_folder_symbol,'paypal']))
    if (not os.path.exists(_data_folder_name)):
	os.makedirs(_data_folder_name)
    pp = pprint.PrettyPrinter(indent=4)
    _funcName = misc.funcName()
    try:
	files = ['/'.join([fpath,f]) for f in os.listdir(fpath) if f.find('.csv') > -1]
    except:
	dirName = os.path.dirname(fpath)
	files = ['/'.join([dirName,f]) for f in os.listdir(dirName) if f.find('.csv') > -1]
    files.sort()
    logging.info('(%s) :: files=(%s)' % (_funcName,str(files)))
    for f in files:
	data_d = lists.HashedLists()
	content = [l.strip() for l in open(f, 'r').readlines()]
	content = [[col.group().replace('"','').strip() for col in re.finditer('(?m)"[^"\r\n]*"|[^,\r\n]*', l) if (len(col.group()) > 0)] for l in content]
	logging.info('(%s) :: f=(%s)' % (_funcName,f))
	for c in content[1:]:
	    d = {}
	    cc = [cd for cd in content[0]]
	    for i in xrange(0,len(c)):
		if (len(cc[i]) > 0) and (len(c[i]) > 0):
		    d[cc[i]] = c[i]
		pass
	    dp = []
	    _date = ''
	    if (d.has_key('Date')):
		_date = d['Date']
		dp.append(_date.split('/')[-1])
	    #if (d.has_key('Type')):
		#dp.append(d['Type'])
	    dpath = os.sep.join([_data_folder_name,os.sep.join(dp)])
	    try:
		if (not os.path.exists(dpath)):
		    os.makedirs(dpath)
	    except:
		pass
	    if (d.has_key('Balance Impact')):
		dp.append(d['Balance Impact'])
	    if (len(dp) > 1):
		dpath = '.'.join([os.sep.join([_data_folder_name,os.sep.join(dp)]),'dbx'])
		if (len(_date) > 0):
		    dbx = oodb.PickledHash(dpath,oodb.PickleMethods.useSafeSerializer)
		    dbx[_date] = d
		    logging.info('STORE key="%s", value="%s" into "%s".' % (_date,d,dpath))
		    dbx.sync()
		    dbx.close()
	    else:
		logging.warning('Unable to classify this transaction, "%s"' % d)
	    pass
    pass

def main(fpath):
    if (fpath.lower().find('wellsfargo') > -1):
	main_wellsfargo(fpath)
    elif (fpath.lower().find('www.paypal.com') > -1):
	main_paypal(fpath)
	post_process_paypal(fpath)
    pass

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()
      
    args = {'--help':'displays this help text.',
	    '--verbose':'output more stuff.',
	    '--source=?':'%s' % _available_sources,
	    '--logging=?':'[logging.INFO,logging.WARNING,logging.ERROR,logging.DEBUG]'}
    _argsObj = Args.Args(args)
    print >>sys.stderr, '_argsObj=(%s)' % str(_argsObj)
  
    try:
	_isHelp = _argsObj.booleans['isHelp'] if _argsObj.booleans.has_key('isHelp') else False
    except:
	_isHelp = False
  
    try:
	_isVerbose = _argsObj.booleans['isVerbose'] if _argsObj.booleans.has_key('isVerbose') else False
    except:
	_isVerbose = False
  
    try:
	_source = _argsObj.arguments['source'] if _argsObj.arguments.has_key('source') else _available_sources[-1]
	k = [s for s in args.keys() if s.find('--source') > -1]
	possible_sources = []
	if (len(k) > 0):
	    try:
		possible_sources = eval(args[k[0]])
		possible_sources = possible_sources[0] if (misc.isList(possible_sources[0])) else possible_sources
	    except:
		pass
	_source = _source if _source in possible_sources else _available_sources[-1]
	pass
    except:
	_source = _available_sources[-1]
  
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
    
    logging.info('_version=[%s], _source=[%s]' % (_version,_source))
    
    if (_version >= 2.51):
	if (_isHelp):
	    ppArgs()
	else:
	    _psyco.importPsycoIfPossible(main)

	    _input_path = _wellsfargo_input_path if (_source in [s for s in _available_sources if s == 'wellsfargo']) else _paypal_input_path
	    logging.info('_input_path=[%s]' % _input_path)
	    if (isinstance(_input_path,str)):
		main(_input_path)
	    elif (isinstance(_input_path,list)):
		for f in _input_path:
		    main(f)
	    else:
		logging.warning('Invalid _input_path of type "%s".' % str(_input_path.__class__))
    else:
	print >> sys.stderr, 'You seem to be using the wrong version of Python, try using 2.5.1 rather than "%s".' % sys.version.split()[0]

