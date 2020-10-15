import os, sys
import random
from vyperlogix.decorators import ioTimeAnalysis

random.seed()

L1 = [n for n in xrange(1000000)]
L2 = [random.choice(L1) for n in xrange(100000)]

print 'L1=%s' % (len(L1))
print 'L2=%s' % (len(L2))

@ioTimeAnalysis.analyze('method1')
def method1(l1,l2):
    return [n for n in l1 if (n not in l2)]

@ioTimeAnalysis.analyze('method2')
def method2(l1,l2):
    return list(set(l1)-set(l2))

ioTimeAnalysis.ioTimeAnalysis.initIOTime('method1')
ioTimeAnalysis.ioTimeAnalysis.initIOTime('method2')

diff1 = method1(L1, L2)
diff2 = method2(L1, L2)

print 'diff1=%s' % (len(diff1))
print 'diff2=%s' % (len(diff2))

ioTimeAnalysis.ioTimeAnalysis.ioTimeAnalysisReport(fOut=sys.stdout)
