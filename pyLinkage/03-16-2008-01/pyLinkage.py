from vyperlogix import CooperativeClass
import OneWayNode
import OneWayLinkage
import random
from vyperlogix import ioTimeAnalysis
from vyperlogix import _utils
import sys

if (_utils.getVersionNumber() <= 251):
    print 'You seem to be using the wrong version of Python !\nMaybe now would be a good time to upgrade.'
    sys.exit(0)

def dumpNodes(n):
    print n
    if (n.next):
	dumpNodes(n.next)

# a singly-linked linked list is just a series of nodes linked one to another

n = OneWayLinkage.OneWayLinkage('one')
n.append('two')
n.append('three')

print 'Dumping One-Way Linked List using the new method.'
n.dumpNodes()

print
print '='*30
print

n = OneWayNode.OneWayNode('one')
n.next = OneWayNode.OneWayNode('two')
n.next.next = OneWayNode.OneWayNode('three')

# one-way linked list automatically walks the list when the first node is printed...
print 'Dumping One-Way Linked List using the old method.'
dumpNodes(n)

print
print '='*30
print

# insert a value between 'one' and 'two'
x = OneWayNode.OneWayNode('one.1')
x.next = n.next
n.next = x

print 'Dumping One-Way Linked List using the old method with one node inserted.'
dumpNodes(n)

# delete the value 'one.1'
n.next = x.next
x = None

print
print '='*30
print

print 'Dumping One-Way Linked List using the old method with one node deleted.'
dumpNodes(n)

# this begins the sorted linked list

def insertSortedBefore(n,ptr):
    global h
    global p
    if (h == n):
	h = ptr
	h.next = n
    else:
	ptr.next = n
	if (p.next == n):
	    p.next = ptr

def insertSortedAfter(n,ptr):
    n.next = ptr

def walkNodes(n,ptr):
    global p
    if (n):
	if (ptr.data >= n.data):
	    if (n.next):
		p = n
		walkNodes(n.next,ptr)
	    else:
		insertSortedAfter(n,ptr)
	else:
	    insertSortedBefore(n,ptr)

n = OneWayNode.OneWayNode(5)
h = n
p = h
walkNodes(h,OneWayNode.OneWayNode(1))

print
print '='*30
print

print 'Dumping One-Way Linked List using the old method (Sorted List).'
dumpNodes(h)

walkNodes(h,OneWayNode.OneWayNode(6))

print
print '='*30
print

print 'Dumping One-Way Linked List using the old method (Sorted List).'
dumpNodes(h)

walkNodes(h,OneWayNode.OneWayNode(0))

print
print '='*30
print

print 'Dumping One-Way Linked List using the old method (Sorted List).'
dumpNodes(h)

walkNodes(h,OneWayNode.OneWayNode(2))

print
print '='*30
print

print 'Dumping One-Way Linked List using the old method (Sorted List).'
dumpNodes(h)

walkNodes(h,OneWayNode.OneWayNode(7))

print
print '='*30
print

print 'Dumping One-Way Linked List using the old method (Sorted List).'
dumpNodes(h)

walkNodes(h,OneWayNode.OneWayNode(3))

print
print '='*30
print

print 'Dumping One-Way Linked List using the old method (Sorted List).'
dumpNodes(h)

print
print '='*30
print

# this begins the circular linked list

n = OneWayNode.OneWayNode('one')
n.next = OneWayNode.OneWayNode('two')
n.next.next = OneWayNode.OneWayNode('three')
n.next.next.next = n

_nodes = []
def dumpCircularNodes(nodes,n):
    print n
    if (n.next) and (n.next not in nodes):
	nodes.append(n)
	dumpCircularNodes(nodes,n.next)

print 'Dumping Circular Linked List using the old method.'
dumpCircularNodes(_nodes,n)

print 'Stress Test for the Sorted One-Way Linked List.'

numNodes = 900

foo = [n for n in xrange(numNodes+1)]
random.shuffle(foo)
#print foo

ioTimeAnalysis.initIOTime('One-Way Linked List')
ioTimeAnalysis.ioBeginTime('One-Way Linked List')

n = OneWayNode.OneWayNode(-1)
h = n
p = h
for num in foo:
    walkNodes(h,OneWayNode.OneWayNode(num))
ioTimeAnalysis.ioEndTime('One-Way Linked List')
    
print 'Dumping One-Way Linked List using the old method (Sorted List Stress List).'
dumpNodes(h)

_et1 = ioTimeAnalysis.ioTimeAnalysis()
print '_et1=(%s)' % _et1

foo = [n for n in xrange(numNodes+1)]
random.shuffle(foo)
#print foo

ioTimeAnalysis._ioTime = {}
ioTimeAnalysis.initIOTime('Python List')
ioTimeAnalysis.ioBeginTime('Python List')
foo.sort()
ioTimeAnalysis.ioEndTime('Python List')

print 'Dumping Python List.'
#print foo

_et2 = ioTimeAnalysis.ioTimeAnalysis()
print '_et2=(%s)' % _et2

_isSlower = (_et1 < _et2)

print '_isSlower=(%s)' % _isSlower

factor = 0.0
try:
    if (_isSlower):
	factor = _et2 / _et1
    else:
	factor = _et1 / _et2
except:
    pass

if (factor == 0.0):
    print 'Linked List is infinitely %s then Python native List and Sorting methods.' % ('faster' if _isSlower else 'slower')
else:
    print 'factor=(%s)' % factor
    print 'Linked List is %6.0f times %s then Python native List and Sorting methods.' % (factor, 'faster' if _isSlower else 'slower')
