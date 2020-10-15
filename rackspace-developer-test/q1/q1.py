import os, sys
import math

def slope (pts):
    x1, y1, x2, y2 = pts
    x2 = (x2 - x1)
    y2 = (y2 - y1)

    m = (y2/x2)
    return m

def intercept(pts):
    x1, y1, x2, y2 = pts
    m = slope(pts)
    b = y2 - (m*x2)
    return b 

def distance(pts):
    x1, y1, x2, y2 = pts
    return math.hypot(x2 - x1, y2 - y1)

def x_y_from_slope_distamce(m,b):
    x = int(b/m)
    return (float(x),float(m*x))

def compute_response(items):
    __x__,__y__ = None,None
    if (len(items) == 2):
	item1,item2 = items
	try:
	    points = (float(str(item1[0])), float(str(item1[1])), float(str(item2[0])), float(str(item2[1])))
	    signals = (float(str(item1[-1])), float(str(item2[-1])))
	    __slope__ = slope(points)
	    __intercept__ = intercept(points)
	    __distance__ = distance(points)
	    __signal__ = signals[0]+signals[-1]
	    __signals__ = (signals[0]/__signal__,signals[-1]/__signal__)
	    x1, y1, x2, y2 = points
	    min_x = min(x1,x2)
	    __x__,__y__ = x_y_from_slope_distamce(__slope__, __distance__*__signals__[0 if (min_x == x1) else -1])
	    #print 'slope=%s, __intercept__=%s, __distance__=%s, __signals__=%s' % (__slope__,__intercept__,__distance__,__signals__)
	    print '%s, %s' % (__x__,__y__)
	except:
	    print >>sys.stderr, 'ERROR: Seems like your data has some issues, might want to make sure your data is correct - most of the time this is caused by division by zero which should never happen but alas it seems to have this time.'
    return __x__,__y__

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
		item = item.strip()
		if (len(item) > 0):
		    toks = item.split()
		    if (len(toks) == 3):
			__data__.append(toks)
		    else:
			print >>sys.stderr, 'WARNING: Cannot accept this data item (%s) because it is not in the proper form; the proper form is (x,y,signal).' % (','.join(toks))
		    print ', '.join(toks)
	    fIn.close()
	    print '*'*3
	    print
	    
	    if (len(__data__) == 2):
		vector = (__data__[0],__data__[1])
		print '*'*3
		compute_response(vector)
		print '*'*3
	    else:
		print >>sys.stderr, 'WARNING: Cannot provide a response with more or less than two data items.  Please try again with exactly two data items, one per line.'
	else:
	    print >>sys.stderr, 'WARNING: Cannot proceed without an input file. Please use the -i or --input command line option to proceed.'
    else:
	print >>sys.stderr, 'WARNING: Cannot proceed without an input file. Please use the -i or --input command line option to proceed.'
	
	
    
