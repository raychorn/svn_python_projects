import os
import sys
import logging
import traceback
import SequenceMatcher
import calendar

class Concordance():
	def __init__(self, fileName):
		self.__dataBase = {}
		self.__synonyms = {}
		self.__concordance = {}
		self.__parenthetical_symbols = ['(',')']
		self.__special_symbols = ['-','_','+']
		self.__month_name_symbols = (','.join([calendar.month_name[i] for i in xrange(1,len(calendar.month_name))])+','+','.join([str(calendar.month_name[i]).lower() for i in xrange(1,len(calendar.month_name))])+','+','.join([str(calendar.month_name[i]).upper() for i in xrange(1,len(calendar.month_name))])).split(',')
		self.__special_symbols = (','.join(self.parentheticalSymbols)+','+','.join(self.specialSymbols)).split(',')
		self.__filename = fileName if os.path.exists(fileName) else ''
		assert (len(self.__filename) > 0), 'Invalid fileName specified for %s object creation.' % str(self.__class__)
		self.process()

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

	def readFromFile(self):
		fHand = open(self.filename, 'r')
		_list = [l.strip() for l in fHand.readlines()]
		fHand.close()
		return _list

	def isDigitsAndDots(self,token):
		return (''.join([t for t in token if t.isdigit()])).isdigit()

	def isParenthetical(self,token):
		return (token[0] in self.parentheticalSymbols) and (token[-1] in self.parentheticalSymbols)

	def isParentheticalDigits(self,token):
		return self.isParenthetical(token) and (str(token[1:-1]).isdigit())

	def hasSpecialSymbols(self,token):
		tok = ''.join([t for t in token if t in self.specialSymbols])
		return (len(tok) > 0) and (len(tok) != len(token))

	def filterOut(self,token,chars):
		if (isinstance(chars,list)):
			return ''.join([ch for ch in token if ch not in chars])
		else:
			print '(filterOut) :: WARNING: chars was supposed to be of type "list" but it is of type "%s".  Kindly make the required correction.' % (type(chars))
		return token

	def matchesAnyFrom(self,t,symbols):
		if (isinstance(symbols,list)):
			for s in symbols:
				if (t == s[:len(t)]):
					return True
		else:
			print '(matchesAnyFrom) :: WARNING: symbols was supposed to be of type "list" but it is of type "%s".  Kindly make the required correction.' % (type(symbols))
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
		print '(filter).1 :: token=(%s)' % token
		for ch in token:
			if (ch.isalpha() or ch.isdigit() or (ch in self.specialSymbols) or (ch == ' ') or ( (ch == '.') and (str(token[i-1]).isalnum()) ) ):
				val += ch
			i += 1
		if ( (self.isDigitsAndDots(val)) or ( (not val.isalnum()) and (not self.hasSpecialSymbols(val) ) ) ):
			if ( (self.isParentheticalDigits(token)) or (self.isParentheticalDate(token)) or ( (len(token) > 0) and (token[0] not in self.parentheticalSymbols) and (token[-1] not in self.parentheticalSymbols) ) ):
				val = ''
				print '(filter).2 :: isDigitsAndDots ! val=(%s) [%s] [%s]' % (val,token[0],token[-1])
		print '(filter).3 :: val=(%s)' % val
		print
		return val

	def synonymSearch(self,token,concordance):
		if (isinstance(concordance,dict)):
			keys = concordance.keys()
			for k in keys:
				bSlice = 3 if self.isParenthetical(token) else 2
				for slice in xrange(bSlice,len(token)):
					_k = k[:slice] if len(k) >= slice else k
					if (token[:slice] == _k):
						if (not self.synonyms.has_key(token)):
							bucket = []
						else:
							bucket = self.synonyms[token]
						_k_in_bucket = False
						for b in bucket:
							if (k == b[0]):
								_k_in_bucket = True
								break
						if ( (not _k_in_bucket) and (token != k) ):
							_ratio = SequenceMatcher.computeAllRatios(k,token)
							bucket.append((k,_ratio))
							self.synonyms[token] = bucket
			print
		else:
			print '(synonymSearch) :: Invalid concordance was supposed to be of type dict but is of type "%s".' % type(concordance)

	def process(self,fname=None):
		print '(main) :: BEGIN:'
		if ( (isinstance(fname,str)) and (os.path.exists(fname)) ):
			self.__filename = fname
		_lines = self.readFromFile()
		i = 0
		for l in _lines:
			print '(main) :: l=(%s)' % l
			self.dataBase[i] = l
			_toks = l.split()
			for j in xrange(len(_toks)-1):
				if ( (_toks[j][0] in self.parentheticalSymbols) and (_toks[j+1][-1] in self.parentheticalSymbols) ):
					_toks[j] = ' '.join([_toks[j],_toks[j+1]])
					del _toks[j+1]
			for _t in _toks:
				t = self.filter(_t)
				if (len(t) > 0):
					if (not self.concordance.has_key(t)):
						bucket = []
					else:
						bucket = self.concordance[t]
					if (i not in bucket):
						bucket.append(i)
						self.concordance[t] = bucket
						self.synonymSearch(t,self.concordance)
			i += 1
			print
		self.dataBase['_count'] = len(_lines)
		
		print '(main) :: END !'

	dataBase = property(get_dataBase)
	synonyms = property(get_synonyms)
	concordance = property(get_concordance)
	parentheticalSymbols = property(get_parenthetical_symbols)
	specialSymbols = property(get_special_symbols)
	monthNameSymbols = property(get_month_name_symbols)
	specialSymbols = property(get_special_symbols)
	filename = property(get_filename)

