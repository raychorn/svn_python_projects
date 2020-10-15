import os
import sys
import logging
import traceback
from vyperlogix import SequenceMatcher
import calendar
import types
from vyperlogix import PickledHash
from vyperlogix import Enum
from vyperlogix.aima import utils
from vyperlogix import hexConversions
from vyperlogix import CooperativeClass
import globalVars
from vyperlogix import AccumulatorHash
import copy

# To-Do:
#         (1). Find the name of the publisher in the ARP string from the tokens...  From Publishers list then Google ?
#         (1a). Sub-string searches on tokens OR concordance of publishers
#
# Flaws:
#          * Parentheticals need to be found using LR parser rather than tokenizer splitting on whitespace
#          * Synonyms need to be found using a Synonym matrix rather than an interative process that consumes too much time.
#              * Determine the length of the longest token and use this as a fixed value rather than using the length of each token.
#              * Compute the synonym matrix once based on the longest length of any token.
#              * Consumes a lot of RAM but may improve processing many fold.
#           * Make Synonym matrix into a huge dict where keys are the first number of chars from 2 or 3 thru the total chars in a token.
#              * Synonym search then becomes a process of doing dict look-ups which are very fast since synonym dict only must be
#                determined once rather than for each token.

class DebugLevels(Enum.Enum):
	no_debugging = 0
	warnings = 1
	initialization = 2
	filter = 4
	tokens = 8
	process = 16

def dummyCallback(data):
	pass

class DataNode(CooperativeClass.Cooperative):
	def __init__(self):
		self.__clsidSymbols = ['{','}']
		self.__parenthetical_symbols = ['(',')']
		self.__special_symbols = ['-','_','+',',','?']
		self.__dot_symbols = ['.']
		self.__vowel_symbols = ['a','e','i','o','u','y']
		self.__special_symbols = (','.join(self.parentheticalSymbols)+','+','.join(self.specialSymbols)).split(',')
		self.__month_name_symbols = (','.join([calendar.month_name[i] for i in xrange(1,len(calendar.month_name))])+','+','.join([str(calendar.month_name[i]).lower() for i in xrange(1,len(calendar.month_name))])+','+','.join([str(calendar.month_name[i]).upper() for i in xrange(1,len(calendar.month_name))])).split(',')
		self.__special_symbols_and_dot = (','.join(self.specialSymbols)+','+','.join(self.dotSymbols)).split(',')
		self.__isDebugging = DebugLevels.no_debugging
		self.__line_num = 0

	def get_line_num(self):
		return self.__line_num
	
	def next_line_num(self):
		self.__line_num += 1
		
	def reset_line_num(self):
		self.__line_num = 0
	
	def get_vowel_symbols(self):
		return self.__vowel_symbols
	
	def get_special_symbols_and_dot(self):
		return self.__special_symbols_and_dot
	
	def get_dot_symbols(self):
		return self.__dot_symbols
	
	def get_clsidSymbols(self):
		return self.__clsidSymbols
	
	def get_parenthetical_symbols(self):
		return self.__parenthetical_symbols

	def get_special_symbols(self):
		return self.__special_symbols

	def get_month_name_symbols(self):
		return self.__month_name_symbols

	def isDebuggingByLevel(self, debugLevel):
		return (self.__isDebugging & debugLevel) != 0
	
	def get_isDebugging(self):
		return self.__isDebugging != DebugLevels.no_debugging

	def maskedDebugLevelFor(self,debugLevel):
		mask = DebugLevels.no_debugging
		for e,v in DebugLevels:
			if (v & debugLevel):
				mask |= v
		return mask
	
	def set_isDebugging(self, debugLevel):
		self.__isDebugging = self.maskedDebugLevelFor(debugLevel)

	def getCLSIDVector(self,token):
		if (len(token) > 0):
			s = self.clsidSymbols
			return (token.find(s[0]),token.find(s[-1]))
		return (-1,-1)

	def isCLSIDToken(self,token):
		if (len(token) > 0):
			vector = self.getCLSIDVector(token)
			return (vector[0] > -1) and (vector[-1] > -1)
		return False

	def isCLSIDValue(self,token):
		vector = self.getCLSIDVector(token)
		if ( (vector[0] > -1) and (vector[-1] > -1) ):
			value = str(token[vector[0]+1:vector[-1]-1]).replace('-','')
			return hexConversions.isHexDigits(value)
		return False
	
	def isAnyCLSIDValue(self,tokens):
		return any([self.isCLSIDValue(t) for t in tokens])

	def isDigitsAndDots(self,token):
		tok = ''.join([t for t in token if t.isdigit()])
		_tok = ''.join([t for t in token if (not t.isdigit()) and (t in self.specialSymbolsAndDot)])
		return (len(token) - (len(tok)+len(_tok))) == 0

	def hasSpecialSymbols(self,token):
		if (len(token) > 0):
			tok = ''.join([t for t in token if t in self.specialSymbols])
			return (len(tok) > 0) and (len(tok) != len(token))
		return False

	def isPartialParenthetical(self,token):
		l = len(token)
		if (l > 0):
			if (l == 1):
				return ( (token == self.parentheticalSymbols[0]) and (token != self.parentheticalSymbols[-1]) ) or ( (token != self.parentheticalSymbols[0]) and (token == self.parentheticalSymbols[-1]) )
			return ( (token.find(self.parentheticalSymbols[0]) > -1) and (token.find(self.parentheticalSymbols[-1]) == -1) ) or ( (token.find(self.parentheticalSymbols[0]) == -1) and (token.find(self.parentheticalSymbols[-1]) > -1) )
		return False

	def isParenthetical(self,token):
		if ( (len(token) > 0) and (not self.isPartialParenthetical(token)) ):
			return (token[0] == self.parentheticalSymbols[0]) and (token[-1] == self.parentheticalSymbols[-1])
		return False

	def isParentheticalDigits(self,token):
		if (len(token) > 0):
			return (self.isParenthetical(token) or self.isPartialParenthetical(token)) and (str(token).replace(self.parentheticalSymbols[0],'').replace(self.parentheticalSymbols[-1],'').isdigit())
		return False

	def matchesAnyFrom(self,t,symbols):
		if (isinstance(symbols,list)):
			for s in symbols:
				if (t == s[:len(t)]):
					return True
		elif (self.isDebuggingByLevel(DebugLevels.warnings)):
			print >>sys.stderr, '(matchesAnyFrom) :: WARNING: symbols was supposed to be of type "list" but it is of type "%s".  Kindly make the required correction.' % (type(symbols))
		return False

	def isParentheticalDate(self,token):
		toks = [self.filterOut(t,self.parentheticalSymbols) for t in token.split()]
		isMonthName = False
		for t in toks:
			if ( (t in self.monthNameSymbols) or (self.matchesAnyFrom(t,self.monthNameSymbols)) ):
				isMonthName = True
				break
		return (self.isParenthetical(token) or self.isPartialParenthetical(token)) and isMonthName

	def filterOut(self,token,chars_or_func):
		if (isinstance(chars_or_func,list)):
			return ''.join([ch for ch in token if ch not in chars_or_func])
		elif ( (type(chars_or_func) == types.FunctionType) or (type(chars_or_func) == types.MethodType) ):
			return ''.join([ch for ch in token if not chars_or_func(ch)])
		elif (self.isDebuggingByLevel(DebugLevels.warnings)):
			print >>sys.stderr, '(filterOut) :: WARNING: chars_or_func was supposed to be of type "list" or type "function" but it is of type "%s".  Kindly make the required correction.' % (type(chars_or_func))
		return token

	def filter(self,token):
		i = 0
		val = ''
		if (self.isDebuggingByLevel(DebugLevels.filter)):
			print >>sys.stderr, '(filter).1 :: token=(%s)' % token
		for ch in token:
			if (ch.isalpha() or ch.isdigit() or (ch in self.specialSymbols) or (ch == ' ') or ( (ch == '.') and (str(token[i-1]).isalnum()) ) ):
				val += ch
			i += 1
		b1 = self.isDigitsAndDots(val)
		b2 = not val.isalnum()
		b3 = not self.hasSpecialSymbols(val)
		if ( (b1) or ( (b2) and (b3) ) ):
			_b1 = self.isParentheticalDigits(token)
			_b2 = self.isParentheticalDate(token)
			_b3 = len(''.join([x for x in token if not x in self.specialSymbols])) == 0
			_b4 = len(''.join([x for x in token if x in self.dotSymbols])) > 0
			if ( (b1) or (_b1) or (_b2) or (_b3) or (_b4) ):
				val = ' '
				if (self.isDebuggingByLevel(DebugLevels.filter)):
					print >>sys.stderr, '(filter).2 :: isDigitsAndDots ! val=(%s) [%s] [%s]' % (val,token[0],token[-1])
		if (self.isDebuggingByLevel(DebugLevels.filter)):
			print >>sys.stderr, '(filter).3 :: val=(%s)' % val
			print >>sys.stderr, ''
		return val
	
	def sampleProbabilitySpread(self,token):
		from nltk import WordTokenizer
		from nltk import FreqDist
		if (isinstance(token,str)):
			isAnyWhitespace = len(token.split()) > 1
			if ( (not isAnyWhitespace) and (token.isalnum()) ):
				phrase = ''.join([t if not t.isdigit() else ' ' for t in token])
				parser = WordTokenizer()
				fdist = FreqDist(word.lower() for word in parser.tokenize(phrase))
				samples = [fdist.freq(s) for s in fdist.samples()]
		return token

	def filterGibberishLevel1(self,token):
		from nltk import WordTokenizer
		if (isinstance(token,str)):
			isAnyWhitespace = len(token.split()) > 1
			if ( (not isAnyWhitespace) and (token.isalnum()) ):
				phrase = ''.join([t if not t.isdigit() else ' ' for t in token])
				parser = WordTokenizer()
				words = [word for word in parser.tokenize(phrase)]
				vowels_analysis = [len([ch for ch in word if ch in self.vowelSymbols]) for word in words]
				word_len_analysis = [len(word) for word in words]
				assert len(words) == len(vowels_analysis), 'Oops, vowels_analysis (%s) does not match number of words (%s).' % (len(vowels_analysis),len(words))
				assert len(words) == len(word_len_analysis), 'Oops, word_len_analysis (%s) does not match number of words (%s).' % (len(word_len_analysis),len(words))
				_words = []
				for i in xrange(len(words)):
					if ( (word_len_analysis[i] > 2) and (vowels_analysis[i] > 0) ):
						_words.append(words[i])
				token = ' '.join(_words).strip()
		return token

	def filterTokens(self,_toks):
		toks = [self.filter(t) for t in _toks]
		if (len(toks) == 1):
			sToks = toks.split() if isinstance(toks,str) else toks[0].split()
			if (len(sToks) > 1):
				toks = [' '.join([self.filter(t) for t in sToks]).strip()]
		toks = [self.filterGibberishLevel1(t) for t in toks]
		toks = [t.strip() for t in toks if len(t) > 0]
		return toks
	
	def handleObviousUnicodeTrash(self,_toks):
		return [''.join([ch for ch in t if ord(ch) < 128]) for t in _toks]
	
	def handlePartialParentheticals(self,_toks):
		return [self.filterOut(t,self.isPartialParenthetical) for t in _toks]
	
	def handleBlanks(self,_toks):
		return [t.strip() for t in _toks]
	
	clsidSymbols = property(get_clsidSymbols)
	parentheticalSymbols = property(get_parenthetical_symbols)
	specialSymbols = property(get_special_symbols)
	dotSymbols = property(get_dot_symbols)
	specialSymbolsAndDot = property(get_special_symbols_and_dot)
	isDebugging = property(get_isDebugging, set_isDebugging)
	monthNameSymbols = property(get_month_name_symbols)
	vowelSymbols = property(get_vowel_symbols)
	lineNum = property(get_line_num)
	
class DataProcessor(DataNode):
	def __init__(self, fileName, folder, callBack, debugLevel):
		super(DataProcessor, self).__init__()
		self.__filename = fileName if os.path.exists(fileName) else ''
		self.__folder = folder
		if (not os.path.exists(folder)):
			os.mkdir(folder)
		self.isDebugging = self.maskedDebugLevelFor(debugLevel)
		self.__callBack = callBack if type(callBack) == types.FunctionType else dummyCallback
		assert (len(self.__filename) > 0), 'Invalid fileName specified for %s object creation.  File name is "%s" however it seems to be the wrong path or the file does not exist.' % (str(self.__class__),self.__filename)
		self.__databases = []
		self.__reverse_databases = []
		self.__combined_databases = []
		self.__original_database = -1
		self.__original_reverse_database = -1
		self.__actual2original_database = -1
		self.process()

	def get_actual2original_database(self):
		return self.__actual2original_database
	
	def get_original_database(self):
		return self.__original_database
	
	def get_original_reverse_database(self):
		return self.__original_reverse_database
	
	def get_databases(self):
		return self.__databases
	
	def get_reverse_databases(self):
		return self.__reverse_databases
	
	def get_combined_databases(self):
		return self.__combined_databases
	
	def get_filename(self):
		return self.__filename
	
	def get_folder(self):
		return self.__folder

	def readFromFile(self,fname):
		_list = []
		if (os.path.exists(fname)):
			fHand = open(fname, 'r')
			_list = [l.strip() for l in fHand.readlines()]
			fHand.close()
		return _list

	def callback(self,data):
		self.__callBack(data)
	
	def isSplittingData(self,sep=''):
		fHand = open(self.filename, 'r')
		l = fHand.readline()
		toks = l.split(sep)
		isSplittingData = len(toks) > 1
		fHand.close()
		return isSplittingData
	
	def process(self,fname=None):
		if (self.isDebuggingByLevel(DebugLevels.process)):
			print >>sys.stderr, '(main) :: BEGIN:'
		if ( (isinstance(fname,str)) and (os.path.exists(fname)) ):
			self.__filename = fname
		
		data_split_symbol = '\t\t'
		
		isSplittingData = self.isSplittingData(data_split_symbol)
		
		databases = []
		reverse_databases = []
		combined_databases = []
		
		toks = []
		isFirstLine = True
		fHand = open(self.filename, 'r')
		self.reset_line_num()
		for line in fHand:
			if (isFirstLine):
				_toks = self.__filename.split('.')
				if (isSplittingData):
					toks = [t.replace('"','').strip() for t in line.split(data_split_symbol)]
					for t in toks:
						_t = [n for n in _toks]
						_t[0] += '_'+t
						_t[-1] = 'db'
						databases.append(PickledHash.PickledHash(os.sep.join([self.folder,'.'.join(_t)])))
						_t[0] += '_i'
						reverse_databases.append(PickledHash.PickledHash(os.sep.join([self.folder,'.'.join(_t)])))
					if (isSplittingData):
						_t = [n for n in _toks]
						_t[0] += '_'+'_'.join(toks)+'_c'
						_t[-1] = 'db'
						combined_databases.append(PickledHash.PickledHash(os.sep.join([self.folder,'.'.join(_t)])))
				else:
					_toks[-1] = 'db'
					databases.append(PickledHash.PickledHash(os.sep.join([self.folder,'.'.join(_toks)])))
					_toks[0] += '_i'
					reverse_databases.append(PickledHash.PickledHash(os.sep.join([self.folder,'.'.join(_toks)])))
				isFirstLine = False
				d_databases = {}
				for dbx in databases:
					d_databases[dbx.fileName] = 1
				d_reverse_databases = {}
				for rdbx in reverse_databases:
					d_reverse_databases[rdbx.fileName] = 1
				assert len(d_databases.keys()) == len(d_reverse_databases.keys()), 'Something went wrong with the creation of the various databases because the number of databases which is "%s" should be the same as the number of reversed databases which is "%s" and these numbers are not the same.' % (len(d_databases.keys()),len(d_reverse_databases.keys()))
				# create the databases for the original data, to keep track of how the token processing is going...
				_t = _toks = self.__filename.split('.')
				_t[0] += '_o'
				_t[-1] = 'db'
				self.__original_database = PickledHash.PickledHash(os.sep.join([self.folder,'.'.join(_t)]))
				_t = _toks = self.__filename.split('.')
				_t[0] += '_o_i'
				_t[-1] = 'db'
				self.__original_reverse_database = PickledHash.PickledHash(os.sep.join([self.folder,'.'.join(_t)]))
				# we need an actual to original for each of the original databases...
				_t = _toks = self.__filename.split('.')
				_t[0] += '_a_o'
				_t[-1] = 'db'
				self.__actual2original_database = PickledHash.PickledHash(os.sep.join([self.folder,'.'.join(_t)]))
			if (len(toks) == 0):
				# track the original data from each line of data
				_actual_line_nums = AccumulatorHash.HashedLists()
				_line_num = '%d' % self.lineNum
				_line = line.strip()
				if (not isSplittingData):
					toks = [_line]
				else:
					toks = [t.replace(',','').strip() for t in line.split(data_split_symbol)]
				toks = self.handleObviousUnicodeTrash(toks)
				if (self.isAnyCLSIDValue(toks)):
					#print 'CLSID Detected :: Skipping over (%s)' % toks
					self.next_line_num()
					continue
				if ( (len(toks) == len(databases)) and (len(toks) == len(reverse_databases)) ):
					toks = self.handlePartialParentheticals(toks)
					toks = self.filterTokens(toks)
					toks = self.handleBlanks(toks)
					if ( (len(toks) == 0) or ( (len(toks) == 1) and (len(toks[0]) == 0) ) ):
						self.next_line_num()
						continue
					i = 0
					for rdbx in reverse_databases:
						try:
							if (len(toks[i]) > 0):
								if (not rdbx.has_key(toks[i])):
									rdbx[toks[i]] = [self.lineNum]
									#print '(%s) :: (%s)=(%s)' % (rdbx.fileName,toks[i],[self.lineNum])
								else:
									bucket = rdbx[toks[i]]
									bucket.append(_line_num)
									rdbx[toks[i]] = bucket
									#print '(%s) :: (%s)=(%s)' % (rdbx.fileName,toks[i],bucket)
							i += 1 # next toks
						except:
							pass
					i = 0
					cKey = ''
					cValue = ''
					for dbx in databases:
						try:
							if (len(toks[i]) > 0):
								rdbx = reverse_databases[i]
								if (rdbx.has_key(toks[i])):
									line_nums = rdbx[toks[i]]
									dbx[line_nums[0]] = [toks[i],line_nums[1:]]
									for _n in line_nums:
										_actual_line_nums[_n] = toks[i]
									cKey += line_nums[0]
									cValue = '%d' % len(line_nums)
									#print '(%s) :: (%s)=(%s)' % (dbx.fileName,line_nums[0],toks[i])
								else:
									dbx[_line_num] = toks[i]
									_actual_line_nums[self.lineNum] = toks[i]
									cKey += _line_num
									cValue = '1'
									#print '(%s) :: (%s)=(%s)' % (dbx.fileName,self.lineNum,toks[i])
								if (i == 0):
									cKey += '.'
							i += 1 # next toks
						except:
							pass
					for cdbx in combined_databases:
						cdbx[cKey] = cValue
						#print '(%s) :: (%s)=(%s)' % (cdbx.fileName,cKey,cValue)
				else:
					print 'ERROR :: Invalid interpretation of tokens from input data source. Number of tokens MUST match number of databases.\ntoks=(%s)\nlen(databases)=%d\nlen(databases)=%d' % (str(toks),len(databases),len(reverse_databases))
				_akeys = _actual_line_nums.keys()
				if (len(_akeys) > 0):
					for k in _akeys:
						self.actual2OriginalDatabase[k] = _line_num
				self.originalDatabase[_line_num] = _line
				self.originalReverseDatabase[_line] = _line_num
				self.next_line_num()
			toks = [] # signal that the data has been consumed so go consume another one...
		fHand.close()
		
		self.__databases = databases
		self.__reverse_databases = reverse_databases
		self.__combined_databases = combined_databases

		for dbx in databases:
			dbx.close()
			
		for rdbx in reverse_databases:
			rdbx.close()
			
		for cdbx in combined_databases:
			cdbx.close()
			
		self.originalDatabase.close()
		self.originalReverseDatabase.close()
		
		self.actual2OriginalDatabase.close()
			
		if (self.isDebuggingByLevel(DebugLevels.process)):
			print >>sys.stderr, '(main) :: END !'

	filename = property(get_filename)
	databases = property(get_databases)
	reverseDatabases = property(get_reverse_databases)
	folder = property(get_folder)
	combinedDatabases = property(get_combined_databases)
	originalDatabase = property(get_original_database)
	originalReverseDatabase = property(get_original_reverse_database)
	actual2OriginalDatabase = property(get_actual2original_database)

class DataReporter(CooperativeClass.Cooperative):
	def __init__(self):
		d = AccumulatorHash.HashedLists()
		files = [f for f in globalVars.dataFiles() if f.endswith('.db') and f.find('_i') == -1 and f.find('_c') == -1 and f.find('_a_o') == -1 and f.find('_o') == -1]
		#print 'files=(%s)' % files
		for f in files:
			_key = ''
			for ch in f:
				_key += ch
				d[_key] = f
		_d = copy.deepcopy(d)
		_method = 0
		while (_method < 2):
			for k,v in d.iteritems():
				if (_method == 0):
					if ( (len(v) <= 1) or (len(v) == len(files)) ):
						del d[k]
				elif (_method == 1):
					if ( (len(v) <= 1) or (len(v) != len(files)) ):
						del d[k]
			if (len(d.keys()) == 0):
				_method += 1
				d = copy.deepcopy(_d)
			else:
				break
		if (_method == 0):
			_min = 9999
			for k in d.keys():
				_min = min(_min,len(k))
			_min_files = [k for k in d.keys() if len(k) == _min]
			_max_files = []
			for kg in _min_files:
				_max = -1
				for k in d.keys():
					if ( (k.startswith(kg)) and (not k.endswith('_')) ):
						_max = max(_max,len(k))
				_max_files.append([k for k in d.keys() if k.startswith(kg) and len(k) == _max])
			_groups = []
			for _f in _max_files:
				_groups.append([f for f in files if f.startswith(_f[0] if isinstance(_f,list) else _f)])
			for g in _groups:
				_o = [f for f in g if f.find('_o') > -1]
				_r = [f for f in g if f not in _o]
				self.performPostProcessAnalysis(_o,_r)
		else:
			_o = [f for f in globalVars.dataFiles() if f.endswith('_o.db') and f.find('_a_o') == -1]
			_r = [f for f in files]
			self.performPostProcessAnalysis(_o,_r)

	def performPostProcessAnalysis(self,_originals,_regulars):
		p = os.sep.join([globalVars.pathName(),'analysis'])
		if (not os.path.exists(p)):
			os.mkdir(p)
		fHand = open(os.sep.join([p,'@performPostProcessAnalysis_%s.txt' % _originals[0].replace('_o','')]),'w')
		print >>fHand, 'BEGIN: performPostProcessAnalysis.'
		print >>fHand, '_originals=(%s)' % _originals
		print >>fHand, '_regulars=(%s)' % _regulars
		o_databases = [PickledHash.PickledHash(os.sep.join([globalVars.pathName(),f])) for f in _originals]
		r_databases = [PickledHash.PickledHash(os.sep.join([globalVars.pathName(),f])) for f in _regulars]
		o_keys = []
		for o_dbx in o_databases:
			for k in o_dbx.keys():
				o_keys.append(k)
			print >>fHand, 'ORIGINAL :: %s' % o_dbx
		o_set = set(o_keys)
		o_numKeys = len(o_set)
		r_keys = []
		r_numKeys = 0
		for dbx in r_databases:
			print >>fHand, 'REGULAR :: %s' % dbx
			for k,v in dbx.iteritems():
				r_numKeys += 1
				r_keys.append(k)
				for _v in v:
					r_keys.append(_v)
		r_set = set(r_keys)
		diff_set = o_set.difference(r_set)
		# To-Do: Account for the repeated elements that were filtered-out from the original data-set via the reversed-database look-ups.
		print >>fHand, 'Cannot locate %s original keys in the regular database(s).' % len(diff_set)
		print >>fHand, 'There are %d keys in the original database and %d keys in the regular database(s) for a difference of %d or %4.2f%%.' % (o_numKeys,r_numKeys,o_numKeys-r_numKeys,(float(o_numKeys-r_numKeys)/float(o_numKeys))*100.0)
		print >>fHand, '='*80
		if (0):
			i = 0
			max_per_line = 15
			_content = ''
			for k in diff_set:
				if ((i % max_per_line) == 0):
					print >>fHand, '%s' % _content
					_content = '%-10s' % k
				else:
					_content += '%-10s' % k
				i += 1
			print >>fHand, '='*80
		if (1):
			for k in diff_set:
				for o_dbx in o_databases:
					if (o_dbx.has_key(k)):
						print >>fHand, '(%s)->(%s)' % (k,o_dbx[k])
			print >>fHand, '='*80
		print >>fHand, 'END! performPostProcessAnalysis.'
		fHand.close()
		for o_dbx in o_databases:
			o_dbx.close()
		for dbx in r_databases:
			dbx.close()
		#assert o_numKeys == r_numKeys, 'Oops, Number of keys do NOT match ! o_numKeys=(%d), r_numKeys=(%d)' % (o_numKeys,r_numKeys)

class Concordance(DataNode):
	def __init__(self, fileName, callBack, debugLevel):
		super(Concordance, self).__init__()
		self.__filename = fileName if os.path.exists(fileName) else ''
		self.__dataBase = {} if len(self.__filename) > 0 else PickledHash.PickledHash(self.__filename)
		toks = self.__filename.split('.')
		toks[0] += '_synonyms'
		self.__synonyms = {} if len(toks) > 1 else PickledHash.PickledHash('.'.join(toks))
		toks = self.__filename.split('.')
		toks[0] += '_concordance'
		self.__concordance = {} if len(toks) > 1 else PickledHash.PickledHash('.'.join(toks))
		self.isDebugging = self.maskedDebugLevelFor(debugLevel)
		self.__callBack = callBack if type(callBack) == types.FunctionType else dummyCallback
		assert (len(self.__filename) > 0), 'Invalid fileName specified for %s object creation.  File name is "%s" however it seems to be the wrong path or the file does not exist.' % (str(self.__class__),self.__filename)
		self.__cacheSequenceMatcher = {}
		self.__allToks = []
		self.__allSynonyms = {}
		
		if (self.isDebuggingByLevel(DebugLevels.initialization)):
			print >>sys.stderr, 'type(self.dataBase)=(%s)' % type(self.dataBase)
		
		if (self.isDebuggingByLevel(DebugLevels.initialization)):
			print >>sys.stderr, 'type(self.synonyms)=(%s)' % type(self.synonyms)

		if (self.isDebuggingByLevel(DebugLevels.initialization)):
			print >>sys.stderr, 'type(self.concordance)=(%s)' % type(self.concordance)

		self.process()

	def get_allSynonyms(self):
		return self.__allSynonyms
	
	def get_allToks(self):
		return self.__allToks
	
	def get_cacheSequenceMatcher(self):
		return self.__cacheSequenceMatcher
	
	def get_filename(self):
		return self.__filename

	def get_dataBase(self):
		return self.__dataBase
	
	def get_synonyms(self):
		return self.__synonyms

	def get_concordance(self):
		return self.__concordance

	def quickRatioUsing(self,token1,token2):
		_ratio = -1
		_token12 = ''.join([token1,token2])
		_token21 = ''.join([token2,token1])
		if (self.cacheSequenceMatcher.has_key(_token12)):
			_ratio = self.cacheSequenceMatcher[_token12]
		elif (self.cacheSequenceMatcher.has_key(_token21)):
			_ratio = self.cacheSequenceMatcher[_token21]
		else:
			self.cacheSequenceMatcher[_token21] = self.cacheSequenceMatcher[_token12] = _ratio = SequenceMatcher.computeRatio(token1,token2)
		return _ratio
	
	def makeSynonyms(self):
		for token in self.allToks:
			bSlice = 3 if self.isParenthetical(token) else 2
			_sliceMax = xrange(bSlice,len(token))
			for slice in _sliceMax:
				tSlice = token[:slice]
				if (not self.allSynonyms.has_key(tSlice)):
					self.allSynonyms[tSlice] = {}
				self.allSynonyms[tSlice][token] = 1
		for k,v in self.allSynonyms.iteritems():
			v = v.keys()
			if (len(v) > 1):
				for item in v:
					items = [s for s in v if s != item]
					if (len(items) > 1):
						self.synonyms[item] = [(x,self.quickRatioUsing(item,x)) for x in items]

	def makeUnique(self,_items):
		_items = utils.unique(_items)
		_items.sort()
		return _items
	
	def callback(self,data):
		self.__callBack(data)
	
	def handleParentheticals(self,_toks):
		_skip = []
		isScanning = True
		while (isScanning):
			for j in xrange(len(_toks)-1):
				try:
					if (_toks[j][0] == self.parentheticalSymbols[0]):
						if (_toks[j][-1] == self.parentheticalSymbols[-1]):
							continue
						_skip.append(j)
						j += 1
						while (j < len(_toks)):
							_skip.append(j)
							if (_toks[j][-1] == self.parentheticalSymbols[-1]):
								break
							j += 1
				except:
					pass
				if (len(_skip) > 1):
					break
			if (len(_skip) > 1):
				b = _skip[0]
				e = _skip[-1]
				_toks[b] = ' '.join(_toks[b:e+1])
				# Ensure we have a paid of (..) rather than just the "(" without the ")".
				if (_toks[b][-1] != self.parentheticalSymbols[-1]):
					_toks[b] += self.parentheticalSymbols[-1]
				# Remove whitespace bounding tokens between (..) and the tokens we wish to keep that are not whitespace.
				toks = _toks[b].split()
				if (len(toks) > 1):
					if (toks[0] == self.parentheticalSymbols[0]):
						toks[1] = toks[0]+toks[1]
						del toks[0]
					if (toks[-1] == self.parentheticalSymbols[-1]):
						toks[len(toks)-2] = toks[len(toks)-2]+toks[-1]
						del toks[-1]
					_toks[b] = ' '.join(toks)
				_skip = _skip[1:]
				isScanning = (len(_skip) > 0)
				try:
					for t in _skip:
						del _toks[t]
				except:
					pass
				_skip = []
			else:
				isScanning = False
		return _toks
	
	def handleDoubleQuotes(self,_toks):
		toks = [t.replace('"','') for t in _toks]
		toks = [t for t in toks if len(t) > 0]
		return toks
	
	def process(self,fname=None):
		if (self.isDebuggingByLevel(DebugLevels.process)):
			print >>sys.stderr, '(main) :: BEGIN:'
		if ( (isinstance(fname,str)) and (os.path.exists(fname)) ):
			self.__filename = fname
		_lines = [v for k,v in self.dataBase.iteritems()]

		self.callback(len(_lines))
		
		i = 0
		for l in _lines:
			if (self.isDebuggingByLevel(DebugLevels.process)):
				print >>sys.stderr, '(main).1 :: l=(%s)' % l
			_toks = self.handleDoubleQuotes(l.split())
			_toks = self.handleParentheticals(_toks)
			_toks = self.handleObviousUnicodeTrash(_toks)
			_toks = self.filterTokens(_toks)
			if (self.isDebuggingByLevel(DebugLevels.tokens)):
				print >>sys.stderr, '(main).2 :: _toks=(%s)' % str(_toks)
			for t in _toks:
				self.allToks.append(t)
				if (self.isDebuggingByLevel(DebugLevels.tokens)):
					print >>sys.stderr, '(main).3 :: t=(%s)' % t
				if (not self.concordance.has_key(t)):
					bucket = []
				else:
					bucket = list(self.concordance[t])
				if (self.isDebuggingByLevel(DebugLevels.tokens)):
					print >>sys.stderr, '(main).4 :: [%s] bucket=(%s) [%s]' % (i,str(bucket),(i not in bucket))
				if (i not in bucket):
					bucket.append(i)
					if (self.isDebuggingByLevel(DebugLevels.tokens)):
						print >>sys.stderr, '(main).5 :: bucket=(%s)' % (str(bucket))
					self.concordance[t] = bucket
					if (self.isDebuggingByLevel(DebugLevels.tokens)):
						print >>sys.stderr, '\n'
			i += 1
			self.callback(i)
			if (self.isDebuggingByLevel(DebugLevels.process)):
				print >>sys.stderr, ''
				
		self.makeSynonyms()

		if (isinstance(self.dataBase,PickledHash.PickledHash)):
			self.dataBase.close()
		if (isinstance(self.synonyms,PickledHash.PickledHash)):
			self.synonyms.close()
		if (isinstance(self.concordance,PickledHash.PickledHash)):
			self.concordance.close()

		if (self.isDebuggingByLevel(DebugLevels.process)):
			print >>sys.stderr, '(main) :: END !'

	dataBase = property(get_dataBase)
	synonyms = property(get_synonyms)
	concordance = property(get_concordance)
	filename = property(get_filename)
	cacheSequenceMatcher = property(get_cacheSequenceMatcher)
	allToks = property(get_allToks)
	allSynonyms = property(get_allSynonyms)

