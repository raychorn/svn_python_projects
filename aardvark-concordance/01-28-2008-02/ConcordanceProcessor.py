import os
import sys
import logging
import traceback
from lib import SequenceMatcher
import calendar
import types
from lib import PickledHash
from lib import Enum
from lib.aima import utils

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

class Concordance():
	def __init__(self, fileName, callBack, debugLevel, dataBaseDictName=None, synonymsDictName=None, concordanceDictName=None):
		self.__dataBase = {} if (dataBaseDictName == None) or (len(dataBaseDictName) == 0) else PickledHash.PickledHash(dataBaseDictName)
		self.__synonyms = {} if (synonymsDictName == None) or (len(synonymsDictName) == 0)  else PickledHash.PickledHash(synonymsDictName)
		self.__concordance = {} if (concordanceDictName == None) or (len(concordanceDictName) == 0) else PickledHash.PickledHash(concordanceDictName)
		self.__isDebugging = DebugLevels.no_debugging
		self.__isDebugging = self.maskedDebugLevelFor(debugLevel)
		self.__callBack = callBack if type(callBack) == types.FunctionType else dummyCallback
		self.__parenthetical_symbols = ['(',')']
		self.__special_symbols = ['-','_','+',',']
		self.__month_name_symbols = (','.join([calendar.month_name[i] for i in xrange(1,len(calendar.month_name))])+','+','.join([str(calendar.month_name[i]).lower() for i in xrange(1,len(calendar.month_name))])+','+','.join([str(calendar.month_name[i]).upper() for i in xrange(1,len(calendar.month_name))])).split(',')
		self.__special_symbols = (','.join(self.parentheticalSymbols)+','+','.join(self.specialSymbols)).split(',')
		self.__filename = fileName if os.path.exists(fileName) else ''
		assert (len(self.__filename) > 0), 'Invalid fileName specified for %s object creation.  File name is "%s" however it seems to be the wrong path or the file does not exist.' % (str(self.__class__),self.__filename)
		self.__cacheSequenceMatcher = {}
		self.__allToks = []
		self.__allSynonyms = {}
		
		if (self.isDebuggingByLevel(DebugLevels.initialization)):
			print >>sys.stderr, 'dataBaseDictName=(%s), [%s]' % (dataBaseDictName,len(dataBaseDictName))
			print >>sys.stderr, 'type(self.dataBase)=(%s)' % type(self.dataBase)
		
		if (self.isDebuggingByLevel(DebugLevels.initialization)):
			print >>sys.stderr, 'synonymsDictName=(%s), [%s]' % (synonymsDictName,len(synonymsDictName))
			print >>sys.stderr, 'type(self.synonyms)=(%s)' % type(self.synonyms)

		if (self.isDebuggingByLevel(DebugLevels.initialization)):
			print >>sys.stderr, 'concordanceDictName=(%s), [%s]' % (concordanceDictName,len(concordanceDictName))
			print >>sys.stderr, 'type(self.concordance)=(%s)' % type(self.concordance)

		self.process()

	def get_allSynonyms(self):
		return self.__allSynonyms
	
	def get_allToks(self):
		return self.__allToks
	
	def get_cacheSequenceMatcher(self):
		return self.__cacheSequenceMatcher
	
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

	def get_filename(self):
		return self.__filename

	def get_dataBase(self):
		return self.__dataBase
	
	def get_synonyms(self):
		return self.__synonyms

	def get_concordance(self):
		return self.__concordance

	def get_parenthetical_symbols(self):
		return self.__parenthetical_symbols

	def get_special_symbols(self):
		return self.__special_symbols

	def get_month_name_symbols(self):
		return self.__month_name_symbols

	def get_special_symbols(self):
		return self.__special_symbols

	def readFromFile(self,fname):
		_list = []
		if (os.path.exists(fname)):
			fHand = open(fname, 'r')
			_list = [l.strip() for l in fHand.readlines()]
			fHand.close()
		return _list

	def isDigitsAndDots(self,token):
		return (''.join([t for t in token if t.isdigit()])).isdigit()

	def isParenthetical(self,token):
		if (len(token) > 0):
			return (token[0] in self.parentheticalSymbols) and (token[-1] in self.parentheticalSymbols)
		return False

	def isParentheticalDigits(self,token):
		if (len(token) > 0):
			return self.isParenthetical(token) and (str(token[1:-1]).isdigit())
		return False

	def hasSpecialSymbols(self,token):
		if (len(token) > 0):
			tok = ''.join([t for t in token if t in self.specialSymbols])
			return (len(tok) > 0) and (len(tok) != len(token))
		return False

	def filterOut(self,token,chars):
		if (isinstance(chars,list)):
			return ''.join([ch for ch in token if ch not in chars])
		elif (self.isDebuggingByLevel(DebugLevels.warnings)):
			print >>sys.stderr, '(filterOut) :: WARNING: chars was supposed to be of type "list" but it is of type "%s".  Kindly make the required correction.' % (type(chars))
		return token

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
		return self.isParenthetical(token) and isMonthName

	def filter(self,token):
		i = 0
		val = ''
		if (self.isDebuggingByLevel(DebugLevels.filter)):
			print >>sys.stderr, '(filter).1 :: token=(%s)' % token
		for ch in token:
			if (ch.isalpha() or ch.isdigit() or (ch in self.specialSymbols) or (ch == ' ') or ( (ch == '.') and (str(token[i-1]).isalnum()) ) ):
				val += ch
			i += 1
		if ( (self.isDigitsAndDots(val)) or ( (not val.isalnum()) and (not self.hasSpecialSymbols(val) ) ) ):
			if ( (self.isParentheticalDigits(token)) or (self.isParentheticalDate(token)) or ( (len(token) > 0) and (token[0] not in self.parentheticalSymbols) and (token[-1] not in self.parentheticalSymbols) ) ):
				val = ''
				if (self.isDebuggingByLevel(DebugLevels.filter)):
					print >>sys.stderr, '(filter).2 :: isDigitsAndDots ! val=(%s) [%s] [%s]' % (val,token[0],token[-1])
		if (self.isDebuggingByLevel(DebugLevels.filter)):
			print >>sys.stderr, '(filter).3 :: val=(%s)' % val
			print >>sys.stderr, ''
		return val

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
	
	def handleObviousUnicodeTrash(self,_toks):
		return [''.join([ch for ch in t if ord(ch) < 128]) for t in _toks]
	
	def handleDoubleQuotes(self,_toks):
		toks = [t.replace('"','') for t in _toks]
		toks = [t for t in toks if len(t) > 0]
		return toks
	
	def process(self,fname=None):
		if (self.isDebuggingByLevel(DebugLevels.process)):
			print >>sys.stderr, '(main) :: BEGIN:'
		if ( (isinstance(fname,str)) and (os.path.exists(fname)) ):
			self.__filename = fname
		_lines = self.makeUnique(self.readFromFile(self.filename))

		self.callback(len(_lines))
		
		i = 0
		for l in _lines:
			if (self.isDebuggingByLevel(DebugLevels.process)):
				print >>sys.stderr, '(main).1 :: l=(%s)' % l
			self.dataBase['%d' % i] = l.replace(',','')
			_toks = self.handleDoubleQuotes(l.split())
			_toks = self.handleParentheticals(_toks)
			_toks = self.handleObviousUnicodeTrash(_toks)
			if (self.isDebuggingByLevel(DebugLevels.tokens)):
				print >>sys.stderr, '(main).2 :: _toks=(%s)' % str(_toks)
			for _t in _toks:
				t = self.filter(_t)
				if (len(t) > 0):
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
	parentheticalSymbols = property(get_parenthetical_symbols)
	specialSymbols = property(get_special_symbols)
	monthNameSymbols = property(get_month_name_symbols)
	specialSymbols = property(get_special_symbols)
	filename = property(get_filename)
	isDebugging = property(get_isDebugging, set_isDebugging)
	cacheSequenceMatcher = property(get_cacheSequenceMatcher)
	allToks = property(get_allToks)
	allSynonyms = property(get_allSynonyms)

