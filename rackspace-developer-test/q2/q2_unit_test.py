import os, sys
import unittest
import StringIO

__data__ = []

__raw__ = '''20
The quick brown fox jumps over the lazy dog.
'''

fIn = StringIO.StringIO(buf=__raw__)
for item in fIn:
    if (len(__data__) == 0):
	try:
	    width = int(item.strip())
	except:
	    width = -1
	__data__.append(width)
    elif (len(__data__) == 1):
	__data__.append(item.strip())

# Here's our "unit".
def IsCorrect(items):
    from q2 import justify_text
    response = justify_text(items)
    width = int(__data__[0])
    __values__ = [len(str(r).strip()) for r in response]
    __is__ = all([v <= width for v in __values__])
    print '%s' % (__is__)
    if (not __is__):
	print '%s' % (__values__)
    return __is__

# Here's our "unit tests".
class IsOddTests(unittest.TestCase):

    def testOne(self):
	items = (__data__[0],__data__[1])
        self.failUnless(IsCorrect(items))

def main():
    unittest.main()

if __name__ == '__main__':
    main()