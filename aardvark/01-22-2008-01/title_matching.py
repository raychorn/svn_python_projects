import os
import time
import psyco
import sys
import pyodbc
import logging
from WinProcesses import *
from threadpool import *
from threading import BoundedSemaphore
import urllib
import httplib
from HTMLParser import HTMLParser
import traceback
from SequenceMatcher import *
from soundex import *
from ioTimeAnalysis import *
from deleteAllFilesUnder import *

# To-Do:
# 
# Add report of found links to the output from the google search.  Look for a usable pattern.

_isVerbose = False
_ignoreNoise = False
_useGoogle = False
_useTokenAnalysis = False
_useSequenceMatcher = True
_useSoundex = True

_pool = Pool(100)
_poolAnalysis = Pool(300)

_strategy = 0

_resultsFolderName = 'google'

_resultsFolderName_pubs = 'google/pubs'
_resultsFolderName_apps = 'google/apps'

_foundAllKey_symbol = 'found-all'
_foundAnyKey_symbol = 'found-any'

_foundSequence_symbol = 'found-sequence'

_tokens_symbol = 'tokens'

_vowels_list = ['a','e','i','o','u','y']

_analyzeTokens_hits = {}

_mssql_connection_string = 'DRIVER={SQL Server};SERVER=MURRE\DEV2005;DATABASE=title matching;CommandTimeout=0;UID=sa;PWD=peekab00'

SQL_STATEMENT_PUBLISHERS_CW = "SELECT * FROM excelcw_publishers WHERE (name IS NOT NULL) and (LEN(name) > 0)"
SQL_STATEMENT_PUBLISHERS_AARDVARK = "SELECT * FROM aardvark_publishers WHERE (name IS NOT NULL) and (LEN(name) > 0)"

_cwPubs = {}
_aardvarkPubs = {}

SQL_STATEMENT_APPS_CW = "SELECT * FROM excelcw_apps WHERE (name IS NOT NULL) and (LEN(name) > 0)"
SQL_STATEMENT_SOFTWARE_TITLES_AARDVARK = "SELECT * FROM aardvark_software_titles WHERE (name IS NOT NULL) and (LEN(name) > 0)"

_cwApps = {}
_aardvarkTitles = {}

_vague_terms = []

class MyHTMLParser(HTMLParser):

	def init(self):
		self._targetTag = ''
		self._targetAttr = ''
		self.tagCount = 0
		self.tagContents = []

	def targetTag(self,tag):
		self.init()
		self._targetTag = tag
		if (self._targetTag == 'a'):
			self._targetAttr = 'href'

	def isInterestInThisTag(self,tag,attrs=[]):
		bool = True
		try:
			if ( (len(self._targetTag) > 0) and (len(self._targetAttr) > 0) ):
				bool = ( (self._targetTag == tag) and (attrs[0][0] == self._targetAttr) and (str(attrs[0][1]).find('google.com') == -1) and (str(attrs[0][1]).startswith('http://') == True) )
		except:
			pass
		return bool

	def handle_starttag(self, tag, attrs):
		if (self.isInterestInThisTag(tag,attrs) == True):
			self.tagCount += 1
			self.tagContents.append(self.get_starttag_text())
			#print "Encountered the beginning of a '%s' tag [%s]" % (tag,attrs)

	def handle_endtag(self, tag):
		if (self.isInterestInThisTag(tag) == True):
			#print "Encountered the end of a '%s' tag" % tag
			pass

def exec_and_process_sql(_cnnStr,_sql,_callback):
	try:
		_aardvark_dbh = pyodbc.connect(_cnnStr)
		_cursor = _aardvark_dbh.cursor()
		rows = _cursor.execute(_sql)
		try:
			_callback(rows)
		except Exception, details:
			_info = '(exec_and_process_sql).1 :: Error "%s" _cnnStr=(%s), _sql=(%s).' % (str(details),_cnnStr,_sql)
			print _info
			logging.warning(_info)
			print '-'*60
			traceback.print_exc(file=sys.stdout)
			print '-'*60
		_aardvark_dbh.close()
	except Exception, details:
		_info = '(exec_and_process_sql).2 :: Error "%s" _cnnStr=(%s), _sql=(%s).' % (str(details),_cnnStr,_sql)
		print _info
		logging.warning(_info)
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60

def makeChoise(ifbool,arg1,arg2):
	# ifbool == True then arg1 else arg2
	val = arg1
	if (ifbool == False):
		val = arg2
	return val

def noiseFilter(s):
	noiseChars = [' Inc','& Co',' Co',' Ltd',' Inc. ',' Inc ']
	noiseChars2 = ['"',"'",',']
	specialBeginningNoise = ['DBA ']
	specialEndingNoise = ['Inc','Inc.']
	x = s
	for t in noiseChars:
		if (x.endswith(t)):
			x = x.replace(t.lower(),'').replace(t.upper(),'').replace(t.title(),'')
	for t in noiseChars2:
		x = x.replace(t,'')
	for t in specialBeginningNoise:
		if (x.startswith(t)):
			x = x.replace(t,'')
	for t in specialEndingNoise:
		if (x.endswith(t)):
			x = x.replace(t,'')
	return x.strip()

def filterOutNoise(d):
	for k in d.keys():
		datum = d[k]
		t = noiseFilter(k)
		d[t] = datum
		if (t != k):
			d.pop(k)

def makeResultsFolder(folderName):
	toks = folderName.split(os.sep)
	_folderName = ''
	for t in toks:
		_folderName += t
		if (os.path.exists(_folderName) == False):
			os.mkdir(_folderName)
		_folderName += os.sep

@threadpool(_pool)
def performGoogleSearch(searchString,folderName):
	global _useGoogle
	if (_useGoogle == False):
		return
	resultsFolderName = folderName
	resultsSuccessFolderName = 'success'
	resultsFailureFolderName = 'failure'
	failedSearch_symbol = 'did not match any documents'
	failedSearch2_symbol = 'No standard web pages containing all your search terms were found.'
	conn = httplib.HTTPConnection("www.google.com:80")
	term = "/search?q=%s&ie=utf-8&oe=utf-8&aq=t&rls=org.mozilla:en-US:official&client=firefox-a" % (urllib.quote(searchString))
	conn.request("GET", term)
	isError = False
	try:
		r1 = conn.getresponse()
	except:
		isError = True
	if ( (isError == False) and (r1.status == 200) and (r1.reason == 'OK') ):
		data1 = r1.read()
		myParser = MyHTMLParser()
		myParser.targetTag('a')
		myParser.feed(data1)
		fname = urllib.quote(searchString).replace('/','+')
		makeResultsFolder(resultsFolderName)
		_resultsSuccessFolderName = resultsFolderName+os.path.sep+resultsSuccessFolderName
		makeResultsFolder(_resultsSuccessFolderName)
		_resultsFailureFolderName = resultsFolderName+os.path.sep+resultsFailureFolderName
		makeResultsFolder(_resultsFailureFolderName)
		_reportFolderName = _resultsSuccessFolderName
		if ( (data1.find(failedSearch_symbol) == -1) and (data1.find(failedSearch2_symbol) == -1) and (myParser.tagCount > 0) ):
			pass
		else:
			_reportFolderName = _resultsFailureFolderName
			fHand = open('%s%s%s.htm' % (_reportFolderName,os.path.sep,fname),'w')
			fHand.writelines(data1)
			fHand.close()
		fHand = open('%s%s%s.txt' % (_reportFolderName,os.path.sep,fname),'w')
		fHand.writelines('(performGoogleSearch) :: searchString=(%s)\n' % (searchString))
		fHand.writelines('(performGoogleSearch) :: myParser.tagCount=(%s)\n' % (myParser.tagCount))
		for tc in myParser.tagContents:
			fHand.writelines('(performGoogleSearch) :: tc=(%s)\n' % (tc))
		fHand.close()

def tokenizeName(name):
	toks = [t.lower() for t in name.split(' ')]
	_toks = []
	for t in toks:
		_toks.append(t.split('/'))
	toks = _toks
	return toks

def processCWPublishers(rows):
	global _cwPubs
	global _ignoreNoise
	global _tokens_symbol
	global _useTokenAnalysis
	global _resultsFolderName_pubs
	if (str(rows.__class__).find('pyodbc.Cursor') > -1):
		r = rows.fetchone()
		try:
			while (r):
				if (_ignoreNoise):
					_name = noiseFilter(r.name)
				else:
					_name = r.name
				toks = []
				if (_useTokenAnalysis):
					toks = tokenizeName(_name)
				_cwPubs[_name] = {'id': r.id, _tokens_symbol: toks, 'name':r.name, 'name@':_name}
				performGoogleSearch(_name,_resultsFolderName_pubs)
				r = rows.fetchone()
		except Exception, details:
			_info = '(main.processCWPublishers).0 :: Error "%s".' % (str(details))
			print _info
			logging.warning(_info)
			print '-'*60
			traceback.print_exc(file=sys.stdout)
			print '-'*60

def processCWApps(rows):
	global _cwApps
	global _ignoreNoise
	global _tokens_symbol
	global _useTokenAnalysis
	global _resultsFolderName_apps
	if (str(rows.__class__).find('pyodbc.Cursor') > -1):
		r = rows.fetchone()
		try:
			while (r):
				if (_ignoreNoise):
					_name = noiseFilter(r.name)
				else:
					_name = r.name
				toks = []
				if (_useTokenAnalysis):
					toks = tokenizeName(_name)
				_cwApps[_name] = {'id': r.id, _tokens_symbol: toks, 'name':r.name, 'name@':_name}
				performGoogleSearch(_name,_resultsFolderName_apps)
				r = rows.fetchone()
		except Exception, details:
			_info = '(main.processCWApps).0 :: Error "%s".' % (str(details))
			print _info
			logging.warning(_info)
			print '-'*60
			traceback.print_exc(file=sys.stdout)
			print '-'*60

def processAardvarkPublishers(rows):
	global _ignoreNoise
	global _aardvarkPubs
	global _tokens_symbol
	global _useTokenAnalysis
	if (str(rows.__class__).find('pyodbc.Cursor') > -1):
		r = rows.fetchone()
		try:
			while (r):
				if (_ignoreNoise):
					_name = noiseFilter(r.name)
				else:
					_name = r.name
				toks = []
				if (_useTokenAnalysis):
					toks = tokenizeName(_name)
				_aardvarkPubs[_name] = {'id': r.id, _tokens_symbol: toks, 'name':r.name, 'name@':_name}
				r = rows.fetchone()
		except Exception, details:
			_info = '(main.processAardvarkPublishers).0 :: Error "%s".' % (str(details))
			print _info
			logging.warning(_info)
			print '-'*60
			traceback.print_exc(file=sys.stdout)
			print '-'*60

def processAardvarkTitles(rows):
	global _ignoreNoise
	global _aardvarkTitles
	global _tokens_symbol
	global _tokens_symbol
	if (str(rows.__class__).find('pyodbc.Cursor') > -1):
		r = rows.fetchone()
		try:
			while (r):
				if (_ignoreNoise):
					_name = noiseFilter(r.name)
				else:
					_name = r.name
				toks = []
				if (_useTokenAnalysis):
					toks = tokenizeName(_name)
				_aardvarkTitles[_name] = {'id': r.id, _tokens_symbol: toks, 'name':r.name, 'name@':_name}
				r = rows.fetchone()
		except Exception, details:
			_info = '(main.processAardvarkTitles).0 :: Error "%s".' % (str(details))
			print _info
			logging.warning(_info)
			print '-'*60
			traceback.print_exc(file=sys.stdout)
			print '-'*60

def markAnalysisInto(l,reason,name,d):
	try:
		for d in l:
			d[reason] = [name,'id=%s' % d['id'],'name=%s' % d['name']]
	except:
		pass

#Do not make the threaded...
def tokenAnalysis(k,t,target,toks,d):
	global _foundAllKey_symbol
	global _foundAnyKey_symbol
	global _analyzeTokens_hits
	try:
		_t = t[0]
		dh = []
		for kk in target.keys():
			if ( (kk.find(_t.upper()) > -1) or (kk.find(_t.lower()) > -1) or (kk.find(_t.title()) > -1) ):
				dh.append(target[kk])
		_analyzeTokens_hits[k] = dh
		if (len(_analyzeTokens_hits[k]) == len(toks)):
			markAnalysisInto(_analyzeTokens_hits[k],_foundAllKey_symbol,k,d)
		elif (len(_analyzeTokens_hits[k]) > 0):
			markAnalysisInto(_analyzeTokens_hits[k],_foundAnyKey_symbol,k,d)
	except:
		pass
# +++
def sequenceAnalysis(k,tk,target,d,dict1,dict2):
	global _foundSequence_symbol
	global _useSoundex
	s = computeRatios(k,tk)
	if (str(dict1.__class__).find("'dict'") > -1):
		_ratio = s.ratio()
		if (dict1.has_key(_ratio) == False):
			dict1[_ratio] = []
		lst = dict1[_ratio]
		lst.append([k,tk])
		dict1[_ratio] = lst
	_txt = ''
	if (_useSoundex):
		n = max(len(k),len(tk))
		_k = soundex(k,n)
		_tk = soundex(tk,n)
		_s = computeRatios(_k,_tk)
		_txt = '[%s]' % _s.ratio()
		if (str(dict2.__class__).find("'dict'") > -1):
			_ratio = _s.ratio()
			if (dict2.has_key(_ratio) == False):
				dict2[_ratio] = []
			lst = dict2[_ratio]
			lst.append([k,tk])
			dict2[_ratio] = lst
	print '(sequenceAnalysis) :: k=(%s), tk=(%s) [%s] %s\n' % (k,tk,s.ratio(),_txt)

def analyzeTokensFromTo(source,target,reason):
	global _analyzeTokens_hits
	global _tokens_symbol
	try:
		if ( (str(source.__class__).find("'dict'") > -1) and (str(target.__class__).find("'dict'") > -1) ):
			dict1 = []
			dict2 = []
			for k in source.keys():
				d = source[k]
				toks = d[_tokens_symbol]
				_analyzeTokens_hits = {}
				for t in toks:
					tokenAnalysis(k,t,target,toks,d,dict1,dict2)
				print '\n\n'
	except Exception, details:
		print '(analyzeTokensFromTo.%s) :: Error (%s)' % (reason,str(details))
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60

def analyzeSequencesFromTo(source,target,reason):
	try:
		if ( (str(source.__class__).find("'dict'") > -1) and (str(target.__class__).find("'dict'") > -1) ):
			for k in source.keys():
				d = source[k]
				for tk in target.keys():
					sequenceAnalysis(k,tk,target,d)
	except Exception, details:
		print '(analyzeTokensFromTo.%s) :: Error (%s)' % (reason,str(details))
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60

def reportDict(d,title):
	if (str(d.__class__).find("'dict'") > -1):
		print '(reportDict) :: len(%s)=(%s)\n' % (title,len(d))
		keysList = d.keys()
		keysList.sort()
		for k in keysList:
			print '%s=(%s)\n' % (k,d[k])
		print '%s\n\n' % ('='*50)

def hasDigits(term):
	for ch in term:
		if (ch.isdigit()):
			return True
	return False

def hasNonAlphaNumeric(term):
	for ch in term:
		if (ch.isalnum() == False):
			return True
	return False

def isVowel(ch):
	global _vowels_list
	return (ch.lower() in _vowels_list)

def hasVowels(term):
	global _vowels_list
	for ch in term:
		if (isVowel(ch)):
			return True
	return False

def numSyllables(term):
	cv_rule = (isVowel(term[0]) == False)
	vc_rule = (not cv_rule)
	pattern_to_match = ''
	if (cv_rule):
		pattern_to_match = 'cv'
	else:
		pattern_to_match = 'vc'
	count = 0
	pattern = ''
	for ch in term:
		if (isVowel(ch)):
			pattern += 'v'
		else:
			pattern += 'c'
		#print '(numSyllables).1 :: ch=(%s), pattern=(%s), pattern_to_match=(%s), count=(%s)' % (ch,pattern,pattern_to_match,count)
		if (pattern.find(pattern_to_match) > -1):
			count += 1
			pattern = ''
	#print '(numSyllables).2 :: count=(%s)\n' % (count)
	return count

def isTermVague(term):
	#(any chars digits)
	#(any chars non-alpha-numeric)
	#(any words that don't have vowels)
	#(any terms startswith 'ai')
	#(any terms with one syllable)
	# also... terms that are used more often proprtional to their length <-- also vague.
	rule1 = hasDigits(term)
	rule2 = hasNonAlphaNumeric(term)
	rule3 = (hasVowels(term) == False)
	rule4 = term.lower().startswith('ai')
	numSyl = numSyllables(term)
	rule5 = (numSyl == 1)
	bool = ( (rule1) or (rule2) or (rule3) or (rule4) or (rule5) )
	#print '(isTermVague) :: term=(%s), rule1=(%s), rule2=(%s), rule3=(%s), rule4=(%s), rule5=(%s) (%s) --> [%s]\n' % (term,rule1,rule2,rule3,rule4,rule5,numSyl,bool)
	return bool

def reportFoundFromDict(d,title,reason,tokensFileName=''):
	global _tokens_symbol
	global _resultsFolderName
	if (str(d.__class__).find("'dict'") > -1):
		fname = '%s%sreportFoundFromDict_%s_%s.txt' % (_resultsFolderName,os.sep,title,reason)
		fname2 = '%s%s@reportFoundFromDict_%s_%s.txt' % (_resultsFolderName,os.sep,title,reason)
		rep_fhand = open(fname,'w')
		rep_fhand2 = open(fname2,'w')
		fhands = [rep_fhand,rep_fhand2]
		found = []
		keysList = d.keys()
		keysList.sort()
		for k in keysList:
			try:
				if (d.has_key(k)):
					dd = d[k]
					if (reason in dd):
						found.append(dd)
			except Exception, details:
				print '(reportFoundFromDict.%s.%s) :: Error (%s)\n' % (title,reason,str(details))
				print '-'*60
				traceback.print_exc(file=sys.stdout)
				print '-'*60
		for fh in fhands:
			print >> fh, '(reportFoundFromDict.%s.%s) :: len()=(%s)\n' % (title,reason,len(found))
		if (len(tokensFileName) > 0):
			toks = tokensFileName.split('.')
			toks[0] += '-vague'
			vagueFileName = '.'.join(toks)
			fHand = open(tokensFileName,'w')
			fHandv = open(vagueFileName,'w')
		for f in found:
			print >> rep_fhand, '\t\t%s\n' % (str(f))
			if (f.has_key(reason)):
				lst = f[reason]
				print >> rep_fhand2, '%s\n' % (str(lst))
				#print >> rep_fhand2, '(+++)\t%s\n' % (str(f))
			if ( (len(tokensFileName) > 0) and (f.has_key(_tokens_symbol)) ):
				toks = f[_tokens_symbol]
				for t in toks[0]:
					_fhand = fHand
					if (isTermVague(t)):
						_fhand = fHandv
					_fhand.writelines('%s\n' % t)
		for fh in fhands:
			print >> fh, '%s\n\n' % ('='*50)
		if (len(tokensFileName) > 0):
			fHand.close()
			fHandv.close()
		for fh in fhands:
			fh.close()

def main(strategy):
	global _cwPubs
	global _aardvarkPubs
	global _cwApps
	global _aardvarkTitles
	global _resultsFolderName
	global _pool
	global _ignoreNoise
	global _foundAllKey_symbol
	global _foundAnyKey_symbol
	global SQL_STATEMENT_PUBLISHERS_CW
	global SQL_STATEMENT_PUBLISHERS_AARDVARK
	global SQL_STATEMENT_APPS_CW
	global SQL_STATEMENT_SOFTWARE_TITLES_AARDVARK
	global _useTokenAnalysis
	global _useSequenceMatcher

	ioBeginTime('main')
	
	ioBeginTime('main.deleteAllFilesUnder')
	deleteAllFilesUnder(_resultsFolderName)
	ioEndTime('main.deleteAllFilesUnder')

	ioBeginTime('main.deleteAllFilesUnder._pool.join')
	_pool.join()
	ioEndTime('main.deleteAllFilesUnder._pool.join')

	_ignoreNoise = True

	ioBeginTime('main.exec_and_process_sql.publishers')
	exec_and_process_sql(_mssql_connection_string,SQL_STATEMENT_PUBLISHERS_CW,processCWPublishers)
	exec_and_process_sql(_mssql_connection_string,SQL_STATEMENT_PUBLISHERS_AARDVARK,processAardvarkPublishers)
	ioEndTime('main.exec_and_process_sql.publishers')

	_ignoreNoise = False

	ioBeginTime('main.exec_and_process_sql.titles')
	exec_and_process_sql(_mssql_connection_string,SQL_STATEMENT_APPS_CW,processCWApps)
	exec_and_process_sql(_mssql_connection_string,SQL_STATEMENT_SOFTWARE_TITLES_AARDVARK,processAardvarkTitles)
	ioEndTime('main.exec_and_process_sql.titles')

	if (_useTokenAnalysis):
		ioBeginTime('main.analyzeTokensFromTo._cwPubs->_aardvarkPubs')
		analyzeTokensFromTo(_cwPubs,_aardvarkPubs,'_cwPubs->_aardvarkPubs')
		ioEndTime('main.analyzeTokensFromTo._cwPubs->_aardvarkPubs')
		
		ioBeginTime('main.analyzeTokensFromTo._cwApps->_aardvarkTitles')
		analyzeTokensFromTo(_cwApps,_aardvarkTitles,'_cwApps->_aardvarkTitles')
		ioEndTime('main.analyzeTokensFromTo._cwApps->_aardvarkTitles')
		
	if (_useSequenceMatcher):
		ioBeginTime('main.analyzeSequencesFromTo._cwPubs->_aardvarkPubs')
		analyzeSequencesFromTo(_cwPubs,_aardvarkPubs,'_cwPubs->_aardvarkPubs')
		ioEndTime('main.analyzeSequencesFromTo._cwPubs->_aardvarkPubs')
		
		ioBeginTime('main.analyzeSequencesFromTo._cwApps->_aardvarkTitles')
		analyzeSequencesFromTo(_cwApps,_aardvarkTitles,'_cwApps->_aardvarkTitles')
		ioEndTime('main.analyzeSequencesFromTo._cwApps->_aardvarkTitles')

	ioBeginTime('main.reportDict.Pubs')
	reportDict(_cwPubs,'_cwPubs')
	reportDict(_aardvarkPubs,'_aardvarkPubs')
	ioEndTime('main.reportDict.Pubs')
	
	ioBeginTime('main.reportDict.Apps')
	reportDict(_cwApps,'_cwApps')
	reportDict(_aardvarkTitles,'_aardvarkTitles')
	ioEndTime('main.reportDict.Apps')
	
	ioBeginTime('main.reportDict.Pubs')
	reportFoundFromDict(_cwPubs,'_cwPubs Found',_foundAllKey_symbol,'%s%s_cwPubs-%s.txt' % (_resultsFolderName,os.path.sep,_foundAllKey_symbol))
	reportFoundFromDict(_cwPubs,'_cwPubs Found',_foundAnyKey_symbol,'%s%s_cwPubs-%s.txt' % (_resultsFolderName,os.path.sep,_foundAnyKey_symbol))
	reportFoundFromDict(_aardvarkPubs,'_aardvarkPubs Found',_foundAllKey_symbol,'%s%s_aardvarkPubs-%s.txt' % (_resultsFolderName,os.path.sep,_foundAllKey_symbol))
	reportFoundFromDict(_aardvarkPubs,'_aardvarkPubs Found',_foundAnyKey_symbol,'%s%s_aardvarkPubs-%s.txt' % (_resultsFolderName,os.path.sep,_foundAnyKey_symbol))
	ioEndTime('main.reportDict.Pubs')

	ioBeginTime('main.reportDict.Apps')
	reportFoundFromDict(_cwApps,'_cwApps Found',_foundAllKey_symbol,'%s%s_cwApps-%s.txt' % (_resultsFolderName,os.path.sep,_foundAllKey_symbol))
	reportFoundFromDict(_cwApps,'_cwApps Found',_foundAnyKey_symbol,'%s%s_cwApps-%s.txt' % (_resultsFolderName,os.path.sep,_foundAnyKey_symbol))
	reportFoundFromDict(_aardvarkTitles,'_aardvarkTitles Found',_foundAllKey_symbol,'%s%s_aardvarkTitles-%s.txt' % (_resultsFolderName,os.path.sep,_foundAllKey_symbol))
	reportFoundFromDict(_aardvarkTitles,'_aardvarkTitles Found',_foundAnyKey_symbol,'%s%s_aardvarkTitles-%s.txt' % (_resultsFolderName,os.path.sep,_foundAnyKey_symbol))
	ioEndTime('main.reportDict.Apps')

	ioBeginTime('main._pool.join')
	_pool.join()
	ioEndTime('main._pool.join')

	ioEndTime('main')

	ioAnalysis = ioTimeAnalysis()
	print "\n\nTime spent doing I/O :: (%s)" % (str(ioAnalysis))

if ( (len(sys.argv) == 1) or (sys.argv[1] == '--help') ):
	print '--help                      ... displays this help text.'
	print '--verbose                   ... output more stuff.'
	print '--google                    ... perform google searches.'
	print '--tokens                    ... perform token analysis.'
	print '--sequence                  ... perform sequence analysis.'
	print '--soundex                   ... perform soundex analysis.'
	print '--match=num                 ... specify the strategy number.'
else:
	for i in xrange(len(sys.argv)):
		bool = (sys.argv[i].find('--match=') > -1)
		if (bool): 
			toks = sys.argv[i].split('=')
			_strategy = toks[1]
		elif (sys.argv[i].find('--verbose') > -1):
			_isVerbose = True
		elif (sys.argv[i].find('--google') > -1):
			_useGoogle = True
		elif (sys.argv[i].find('--tokens') > -1):
			_useTokenAnalysis = True
		elif (sys.argv[i].find('--sequence') > -1):
			_useSequenceMatcher = True
		elif (sys.argv[i].find('--soundex') > -1):
			_useSoundex = True
	if (sys.argv[i].find('--match=') > -1):
		psyco.bind(main)
		main(_strategy)

