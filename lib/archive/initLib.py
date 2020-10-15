import os
import sys

#print str(sys.argv)

# Note: This module exists to write the __init__.py whenever the contents
#   changes.  Do not try to use this code directly within the __init__.py file
#   or the packaged EXE will fail to find the files it needs to find.  Some
#   additional work could be done to automate all this but for now time is
#   needed elsewhere.

d = {}
files = [f.split('.')[0] for f in os.listdir('..')]
for f in files:
	d[f] = f
del d['']
del d['__init__']
files = d.keys()
print 'files=(%s)' % str(files)
fHand = open('../__init__.py', 'w')
fHand.writelines('\n'.join(['__all__ = %s' % str(files)]))
fHand.flush()
fHand.close()

