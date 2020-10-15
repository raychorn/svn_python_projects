import os, sys

def analyze_chars(items):
    __pattern__ = ''
    items = items[0] if (len(items) > 0) else None
    if (items):
	items = [str(ch) for ch in items]
	for ch in items:
	    if (len(__pattern__) == 0):
		__pattern__ += ch
	    elif (len(str(ch).strip()) == 0):
		continue
	    elif (__pattern__[-1] == ch):
		continue
	    else:
		__pattern__ += ch
    return __pattern__

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
		__data__.append(item.strip())
	    fIn.close()
	    print '\n'.join([str(t) for t in __data__])
	    print '*'*3
	    print
	    
	    try:
		print '*'*3
		pattern = analyze_chars(__data__)
		print pattern
		print '*'*3
	    except:
		print >>sys.stderr, 'WARNING(2): Cannot provide a response unless your data is consistent with the problem statement.  Please try again using properly formed data.'
	else:
	    print >>sys.stderr, 'WARNING(3): Cannot proceed without an input file. Please use the -i or --input command line option to proceed.'
    else:
	print >>sys.stderr, 'WARNING(4): Cannot proceed without an input file. Please use the -i or --input command line option to proceed.'
	
	
    
