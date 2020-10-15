import os, sys
import unittest
import StringIO

__data__ = []

__raw__ = '''abb cddpddef gh
'''

fIn = StringIO.StringIO(buf=__raw__)
for item in fIn:
    __data__.append(item.strip())

# Here's our "unit".
def IsCorrect(items):
    from q4 import analyze_chars
    pattern = analyze_chars(items)
    return pattern == 'abcdpdefgh'

# Here's our "unit tests".
class IsOddTests(unittest.TestCase):

    def testOne(self):
        self.failUnless(IsCorrect(__data__))

def main():
    unittest.main()

if __name__ == '__main__':
    main()