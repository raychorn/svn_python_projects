import re

def isSimpleWildcard(str):
	return (str.find('*') > -1)

def containsWildcard(str):
	return (isSimpleWildcard(str))

def regularExpressionFromWildCard(rexStr):
	rStr = ''
	openCh = ''
	for ch in rexStr:
		if (ch == '*'):
			if (openCh == '('):
				openCh = ''
				rStr += ')'
			rStr += '.*'
		elif (ch == '.'):
			if (openCh == '('):
				openCh = ''
				rStr += ')'
			rStr += '\\.'
		else:
			if (len(openCh) == 0):
				openCh = '('
				rStr += openCh
			rStr += ch
	if (openCh == '('):
		openCh = ''
		rStr += ')'
	rxo = re.compile(rStr)
	return rxo
	
