import os, sys
import unittest
import StringIO

__data__ = []

__raw__ = '''7
2
3
4
5
6
-1
0

'''

fIn = StringIO.StringIO(buf=__raw__)
for item in fIn:
    try:
	__data__.append(int(item.strip()))
    except:
	pass

# Here's our "unit".
def IsCorrect(items):
    from q3 import analyze_routes
    num_cycles = analyze_routes(__data__)
    return num_cycles == 1

# Here's our "unit tests".
class IsOddTests(unittest.TestCase):

    def testOne(self):
	items = (__data__[0],__data__[1])
        self.failUnless(IsCorrect(items))

def main():
    unittest.main()

if __name__ == '__main__':
    main()