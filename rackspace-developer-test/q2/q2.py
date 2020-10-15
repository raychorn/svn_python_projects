import os, sys

def justify_phrase(phrase,width):
    __is__ = True
    while (__is__):
	phrase = phrase.strip()
	__words__ = phrase.split()
	num_spaces = width - len(phrase)
	if (num_spaces > 0) and (len(__words__) > 1):
	    for i in xrange(1 if ( (len(__words__) > 1) and (num_spaces > (len(__words__)/2) ) ) else 2,len(__words__)):
		if (len(' '.join(__words__)+' ') <= width):
		    __words__.insert(i, '_')
		    num_spaces -= 1
		    if (num_spaces == 0):
			break
	phrase = ' '.join(__words__)
	if (len(phrase) > width):
	    phrase = phrase.replace('_','')
	print '%s' % (len(phrase))
	__is__ = False
	break
    return phrase

def justify_text(items):
    response = []
    if (len(items) == 2):
	width,text = items
	words = text.split()
	phrase = ''
	phrases = []
	while (len(words) > 0):
	    word = words[0]
	    if (len(phrase.strip() + word) >= width):
		phrase = justify_phrase(phrase, width)
		phrases.append(phrase.strip())
		phrase = ''
	    phrase += word + ' '
	    del words[0]
	if (len(phrase.strip()) > 0):
	    phrases.append(phrase.strip())
	    
	response = [p.replace('_',' ') for p in phrases]
	print '\n'.join(response)
    return response

if (__name__ == '__main__'):
    from optparse import OptionParser
    
    if (len(sys.argv) == 1):
	sys.argv.insert(len(sys.argv), '-h')
    
    parser = OptionParser("usage: %prog [options]")
    parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
    parser.add_option("-i", "--input", action="store", type="string", help="Fully qualified filesystem path for data.", dest="ipath")
    
    options, args = parser.parse_args()
    
    _isVerbose = False
    if (options.verbose):
	_isVerbose = True
	
    __ipath__ = None
    if (options.ipath):
	f = os.path.abspath(options.ipath)
	if (os.path.exists(f) and os.path.isfile(f)):
	    __ipath__ = f
	
	    __data__ = []
	    
	    print '*'*3
	    fIn = open(__ipath__, 'r')
	    for item in fIn:
		if (len(__data__) == 0):
		    try:
			width = int(item.strip())
		    except:
			width = -1
		    __data__.append(width)
		elif (len(__data__) == 1):
		    __data__.append(item.strip())
	    fIn.close()
	    print '\n'.join([str(t) for t in __data__])
	    print '*'*3
	    print
	    
	    if (len(__data__) == 2):
		items = (__data__[0],__data__[1])
		print '*'*3
		justify_text(items)
		print '*'*3
	    else:
		print >>sys.stderr, 'WARNING: Cannot provide a response with more or less than two data items.  Please try again with exactly two data items, one per line.'
	else:
	    print >>sys.stderr, 'WARNING: Cannot proceed without an input file. Please use the -i or --input command line option to proceed.'
    else:
	print >>sys.stderr, 'WARNING: Cannot proceed without an input file. Please use the -i or --input command line option to proceed.'
