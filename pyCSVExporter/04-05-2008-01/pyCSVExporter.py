import os
import sys

def readLines(fname):
	fin = open(fname,'r')
	lines = [l for l in fin]
	fin.close()
	return lines

def tokenize(l):
	return [t.strip() for t in l.split('\t')]

def main():
	lines = readLines('raw-data.txt')
	_lines = []
	for l in lines:
		_lines.append(['"%s"' % t.replace('"','\"').replace(',',';') for t in tokenize(l)])
	_lines = [[tt.replace('&copy; 1990-2007','&copy; 1990-2008').replace('&copy; 1990-2006','&copy; 1990-2008') for tt in t] for t in _lines]
	for l in _lines:
		print '%s' % ','.join(l)

if (__name__ == '__main__'):
	from vyperlogix import _psyco
	_psyco.importPsycoIfPossible()
	
	main()
	
