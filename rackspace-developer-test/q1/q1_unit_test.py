import os, sys
import unittest
import StringIO

__data__ = []

__raw__ = '''
6.0 8.0 5.0
0.0 0.0 5.0
'''

fIn = StringIO.StringIO(buf=__raw__)
for item in fIn:
    item = item.strip()
    if (len(item) > 0):
	toks = item.split()
	if (len(toks) == 3):
	    __data__.append(toks)
	else:
	    print >>sys.stderr, 'WARNING: Cannot accept this data item (%s) because it is not in the proper form; the proper form is (x,y,signal).' % (','.join(toks))
	print ', '.join(toks)


# Here's our "unit".
def IsCorrect(vector):
    from q1 import compute_response
    x,y = compute_response(vector)
    return (x == 3.0) and (y == 4.0)

# Here's our "unit tests".
class IsOddTests(unittest.TestCase):

    def testOne(self):
        self.failUnless(IsCorrect((__data__[0],__data__[1])))

def main():
    unittest.main()

if __name__ == '__main__':
    main()