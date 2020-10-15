_colsep3 = chr(255)
_rowsep3 = '\n'

def readFile(fname):
	fHand = open(fname,'r')
	for l in fHand:
		print '%s\n' % l.split(_colsep3)
	fHand.close()

readFile('Bigtest.txt')
