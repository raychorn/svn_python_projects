import os
import sys

class Args:
	def __init__(self,args):
		self.args = args
		self.dArgs = {}
		self.arguments = {}
		self.booleans = {}
		self.programName = sys.argv[0].split(os.sep)[-1]
		self._programName = (self.programName.split('.'))[0]
		for a in self.args.keys():
			toks = a.split('=')
			if ( (len(toks) == 2) or (a.endswith('=')) ):
				self.arguments[toks[0].lower()] = ''
				self.dArgs[toks[0].lower()] = toks[-1]
			else:
				self.arguments['is'+toks[0].replace('--','').title()] = ''
		for i in xrange(len(sys.argv)):
			if (i > 0):
				toks = sys.argv[i].split('=')
				if ( (len(toks) == 2) or (sys.argv[i].endswith('=')) ):
					argName = self.stripBeginningNonAlphaNumericsFrom(toks[0]).lower()
				else:
					argName = 'is'+self.upperCaseLikeTitle(toks[0].replace('--',''))
					self.booleans[argName] = True
				self.arguments[argName] = toks[-1]
				
	def upperCaseLikeTitle(self,s):
		if (len(s) < 2):
			return s[0].upper()
		return s[0].upper()+s[1:]
	
	def stripBeginningNonAlphaNumericsFrom(self,s):
		while ( (len(s) > 0) and (not s[0].isalpha()) and (not s[0].isdigit()) ):
			s = s[1:]
		return s

	def __repr__(self):
		return 'Args for "%s"\n\t%s\n\t%s' % (self.programName,str(self.arguments),str(self.booleans))
