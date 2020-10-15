import os, sys

def analyze_routes(items):
    num_items = items[0]
    __items__ = items[1:]
    __cycles__ = []
    if (all([(int(t) >= -1) and (int(t) < num_items) for t in __items__])):
	for i in xrange(0,len(__items__)):
	    #print '--> %s' % (i)
	    __stack__ = []
	    n = __items__[i]
	    while (1):
		if (n in __stack__):
		    __cycles__.append(i)
		    break
		elif (n == -1):
		    return len(__cycles__)
		__stack__.append(n)
		n = __items__[n]
    else:
	print >>sys.stderr, 'WARNING: Cannot process puzzle containing invalid items.  Please try again using properly formed items.'
    return len(__cycles__)

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
		try:
		    __data__.append(int(item.strip()))
		except:
		    pass
	    fIn.close()
	    print '\n'.join([str(t) for t in __data__])
	    print '*'*3
	    print
	    
	    try:
		if (len(__data__[1:]) == int(__data__[0])):
		    print '*'*3
		    num_cycles = analyze_routes(__data__)
		    print num_cycles
		    print '*'*3
		else:
		    print >>sys.stderr, 'WARNING(1): Cannot provide a response unless your data is consistent with the problem statement.  Please try again using properly formed data.'
	    except:
		print >>sys.stderr, 'WARNING(2): Cannot provide a response unless your data is consistent with the problem statement.  Please try again using properly formed data.'
	else:
	    print >>sys.stderr, 'WARNING(3): Cannot proceed without an input file. Please use the -i or --input command line option to proceed.'
    else:
	print >>sys.stderr, 'WARNING(4): Cannot proceed without an input file. Please use the -i or --input command line option to proceed.'
	
	
    
