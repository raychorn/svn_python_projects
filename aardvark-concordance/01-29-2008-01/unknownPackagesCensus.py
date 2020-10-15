import psyco
import os
import sys
import globalVars

_open_curly_brace_symbol = '{'
_close_curly_brace_symbol = '}'

def main():
	fHand = open(globalVars._unknown_packages_filename,'r')
	total_count = 0
	clsid_count = 0
	for l in fHand.readlines():
		total_count += 1
		if ((l.find(_open_curly_brace_symbol) > -1) and ((l.find(_close_curly_brace_symbol) > -1))):
			clsid_count += 1
	fHand.close()
	
	print '(main) :: total_count=(%s), clsid_count=(%s), percentage_clsid=(%2.2f%%)' % (total_count,clsid_count,(float(clsid_count)/float(total_count))*100.0)

if (__name__ == '__main__'):
	main()
	