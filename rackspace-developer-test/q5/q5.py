import os, sys

def flatten_matrix(matrix):
    n = len(matrix)
    m = len(matrix[0])
    for nn in xrange(0,n):
	for mm in xrange(0,m):
	    yield matrix[nn][mm]
	    
def corner(turns):
    while (1):
	for i in xrange(0,len(turns)):
	    yield i

def spiral_items(matrix):
    n = len(matrix)
    m = len(matrix[0])
    turns = [(0,1),(1,0),(0,-1),(-1,0)]
    tcg = corner(turns)
    tc = tcg.next()
    for nn in xrange(0,n):
	for mm in xrange(0,m):
	    matrix[nn][mm] = '%s' % (matrix[nn][mm])
    nn = mm = 0
    nz = n-1
    mz = m-1
    __is__ = lambda cell:(str(cell[0]).isdigit() and str(cell[-1]).isdigit())
    while (1):
	if (not __is__(matrix[nn][mm])):
	    tc = tcg.next()
	    _nn_ = nn + 1
	    _mm_ = mm + turns[tc][-1]
	    nn,mm = (_nn_,_mm_)
	    continue
	yield matrix[nn][mm]
	matrix[nn][mm] = '(%s)' % (matrix[nn][mm])
	if (not any([(__is__(t)) for t in flatten_matrix(matrix)])):
	    break
	_nn_ = nn + turns[tc][0]
	_mm_ = mm + turns[tc][-1]
	if (_nn_ > nz) or (_mm_ > mz) or (_nn_ < 0) or (_mm_ < 0):
	    tc = tcg.next()
	    _nn_ = nn + turns[tc][0]
	    _mm_ = mm + turns[tc][-1]
	nn,mm = (_nn_,_mm_)

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
		cols = [c for c in item.strip().split() if (len(c) > 0)]
		if (len(cols) > 0):
		    __data__.append(cols)
	    fIn.close()
	    print '\n'.join([str(t) for t in __data__])
	    print '*'*3
	    print
	    
	    try:
		print '*'*3
		for item in spiral_items(__data__):
		    print '%s ' % item,
		print
		print '*'*3
	    except:
		print >>sys.stderr, 'WARNING(2): Cannot provide a response unless your data is consistent with the problem statement.  Please try again using properly formed data.'
	else:
	    print >>sys.stderr, 'WARNING(3): Cannot proceed without an input file. Please use the -i or --input command line option to proceed.'
    else:
	print >>sys.stderr, 'WARNING(4): Cannot proceed without an input file. Please use the -i or --input command line option to proceed.'
	
	
    
