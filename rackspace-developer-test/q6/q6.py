import os, sys

class Node(object):
    def __init__(self,val,nodeLeft=None,nodeRight=None):
	self.val = val
	self.nodeLeft = nodeLeft
	self.nodeRight = nodeRight
	
def build_tree(nodes):
    __tree__ = None
    __stack__ = []
    n = None
    if (nodes and (len(nodes) > 0)):
	for item in nodes:
	    aNode = Node(item)
	    __stack__.append(aNode)
	    if (__tree__ is None):
		__tree__ = aNode
	    elif (n is None) and (len(__stack__) > 0):
		n = __stack__[0]
		del __stack__[0]
	    if (n):
		if (n.nodeLeft is None):
		    n.nodeLeft = aNode
		elif (n.nodeRight is None):
		    n.nodeRight = aNode
		if (n.nodeLeft and n.nodeRight):
		    n = None
    return __tree__

display_node_left = lambda node:node.nodeLeft.val if (node.nodeLeft and node.nodeLeft.val) else ''
display_node_right = lambda node:node.nodeRight.val if (node.nodeRight and node.nodeRight.val) else ''

def walk_tree(tree):
    __stack__ = []
    if (tree):
	while (1):
	    aNode = tree
	    if (aNode):
		yield aNode
		if (aNode.nodeLeft):
		    __stack__.append(aNode.nodeLeft)
		if (aNode.nodeRight):
		    __stack__.append(aNode.nodeRight)
	    if (len(__stack__) > 0):
		tree = __stack__[0]
		del __stack__[0]
	    else:
		break

def print_tree(tree):
    __stack__ = []
    if (tree):
	while (1):
	    aNode = tree
	    if (aNode):
		if (aNode.val): #  and display_node_left(aNode) and display_node_right(aNode)
		    print '%s --> (%s,%s)' % (aNode.val,display_node_left(aNode),display_node_right(aNode))
		if (aNode.nodeLeft):
		    __stack__.append(aNode.nodeLeft)
		if (aNode.nodeRight):
		    __stack__.append(aNode.nodeRight)
	    if (len(__stack__) > 0):
		tree = __stack__[0]
		del __stack__[0]
	    else:
		break

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
		nodes = [c for c in item.strip().split(',')]
		__data__.append(nodes)
	    fIn.close()
	    print '\n'.join([','.join(t) for t in __data__])
	    print '*'*3
	    print
	    
	    try:
		print '*'*3
		__tree__ = build_tree(__data__[0] if (len(__data__) > 0) else None)
		print_tree(__tree__)
		print '*'*3
		if (len(__data__) > 1):
		    target = __data__[1] if (len(__data__[1]) == 3) else None
		    if (target):
			for node in walk_tree(__tree__):
			    item = [node.val,display_node_left(node),display_node_right(node)]
			    if (target == item):
				print 'Yes'
				break
		    else:
			print >>sys.stderr, 'WARNING(1): Cannot provide a response unless your data is consistent with the problem statement.  Please try again using properly formed data.'
		print
		print '*'*3
	    except:
		print >>sys.stderr, 'WARNING(2): Cannot provide a response unless your data is consistent with the problem statement.  Please try again using properly formed data.'
	else:
	    print >>sys.stderr, 'WARNING(3): Cannot proceed without an input file. Please use the -i or --input command line option to proceed.'
    else:
	print >>sys.stderr, 'WARNING(4): Cannot proceed without an input file. Please use the -i or --input command line option to proceed.'
	
	
    
