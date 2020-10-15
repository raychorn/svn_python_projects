import os, sys
import unittest
import StringIO

__data__ = []

__raw__ = '''1 2 3
4 5 6
7 8 9
'''

fIn = StringIO.StringIO(buf=__raw__)
for item in fIn:
    cols = [c for c in item.strip().split() if (len(c) > 0)]
    if (len(cols) > 0):
	__data__.append(cols)

# Here's our "unit".
def IsCorrect(items):
    from q5 import spiral_items
    __spiral__ = []
    for item in spiral_items(items):
	__spiral__.append(item)
    return __spiral__ == ['1', '2', '3', '6', '9', '8', '7', '4', '5']

# Here's our "unit tests".
class IsOddTests(unittest.TestCase):

    def testOne(self):
        self.failUnless(IsCorrect(__data__))

def main():
    unittest.main()

if __name__ == '__main__':
    main()