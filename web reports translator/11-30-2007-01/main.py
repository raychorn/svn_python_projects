import os
import sys
import psyco
from xml.dom.minidom import parseString, Text, Element, CDATASection

_isVerbose = False

_input_fileName = "Z:\\@myFiles\\#BigFix Inc\\Zack's Web Reports\\contentReports\\MSpatches-flex.beswrpt"

_programName = ''

def walkDOMNodes(dom,num=0):
	try:
		prefix = '\t'*num
		print '%s(%s) (%s).' % (prefix,str(dom.__class__),str(dom))
		if (_isVerbose):
			if (isinstance(dom,Text)):
				print 'BEGIN_TEXT:\n'
				print '"%s"' % (str(dom.data))
				print 'END_TEXT!\n\n'
			elif (isinstance(dom,Element)):
				print 'BEGIN_ELEMENT:\n'
				print '"%s"' % (str(dom.tagName))
				print 'END_ELEMENT!\n\n'
			elif (isinstance(dom,CDATASection)):
				print 'BEGIN_CDATA:\n'
				print '"%s"' % (str(dom.data))
				print 'END_CDATA!\n\n'
		for node in dom.childNodes:
			walkDOMNodes(node,num+1)
	except Exception, details:
		print '(walkDOMNodes).1 :: ERROR due to "%s".' % str(details)

def main(fname):
	print '(main) :: fname=(%s)' % fname
	if (os.path.exists(fname)):
		try:
			fHand = open(fname,'r')
			data = fHand.read()
			fHand.close()
		except Exception, details:
			print '(main) :: ERROR :: This file "%s" cannot be parsed because "%s".' % (fname,str(details))
		try:
			doc = parseString(data)
			print '(main) :: doc=(%s)' % str(doc)
			if (doc):
				print '(main) :: Proof of concept is minimally functional thus proving that a Web Reports HTML file can indeed be parsed.\n'
				print '(main) :: All that remains is the task of walking the nodes, pulling out elements and converting them into a representation that can be easily understood by Flex3.\n'
				walkDOMNodes(doc)
		except Exception, details:
			print '(main).2 :: ERROR :: This file "%s" cannot be parsed because "%s".' % (fname,str(details))
	else:
		print '(main).1 :: ERROR due to invalid file name of "%s".  Reason: This file is missing or cannot be opened.' % fname

if ( (len(sys.argv) > 1) and (sys.argv[1] == '--help') ):
	print '--help                  ... displays this help text.'
	print '--verbose               ... output more stuff.'
	print '--input=file_name       ... completely uninstall this app.'
else:
	toks = sys.argv[0].split(os.sep)
	_programName = toks[-1]
	for i in xrange(len(sys.argv)):
		bool = (sys.argv[i].find('--input=') > -1)
		if (bool): 
			toks = sys.argv[i].split('=')
			if (sys.argv[i].find('--input=') > -1):
				_input_fileName = toks[1]
		elif (sys.argv[i].find('--verbose') > -1):
			_isVerbose = True
psyco.full()
main(_input_fileName)
