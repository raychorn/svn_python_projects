import os, sys
import unittest
import StringIO

__data__ = []

__raw__ = '''1,5,4,,3,2,5,,,,,,,0,8
4,2,5
'''

fIn = StringIO.StringIO(buf=__raw__)
for item in fIn:
    nodes = [c for c in item.strip().split(',')]
    __data__.append(nodes)

__tree__ = None

# Here's our "unit".
def IsCorrect(items):
    from q6 import build_tree, print_tree, walk_tree, display_node_left, display_node_right
    __tree__ = build_tree(items[0] if (len(items) > 0) else None)
    print_tree(__tree__)
    response = None
    if (len(items) > 1):
	target = items[1] if (len(items[1]) == 3) else None
	if (target):
	    for node in walk_tree(__tree__):
		item = [node.val,display_node_left(node),display_node_right(node)]
		if (target == item):
		    response = 'Yes'
		    break
	else:
	    print >>sys.stderr, 'WARNING(1): Cannot provide a response unless your data is consistent with the problem statement.  Please try again using properly formed data.'
    return response == 'Yes'

# Here's our "unit tests".
class IsOddTests(unittest.TestCase):

    def testOne(self):
        self.failUnless(IsCorrect(__data__))

def main():
    unittest.main()

if __name__ == '__main__':
    main()