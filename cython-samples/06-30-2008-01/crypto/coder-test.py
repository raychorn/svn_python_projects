# test coder

from vyperlogix.misc import ioTimeAnalysis

from vyperlogix.crypto import coder as _coder

import coder

def speedTest1(s_in):
    for i in xrange(100000):
        x = _coder.encode(s_in)

def speedTest2(s_in):
    for i in xrange(100000):
        x = coder.encode(s_in)

def main():
    ioTimeAnalysis.initIOTime('speedTest1')
    ioTimeAnalysis.initIOTime('speedTest2')
    
    print 'speedTest1'
    ioTimeAnalysis.ioBeginTime('speedTest1')
    speedTest1(_plain)
    ioTimeAnalysis.ioEndTime('speedTest1')
    
    print 'speedTest2'
    ioTimeAnalysis.ioBeginTime('speedTest2')
    speedTest2(_plain)
    ioTimeAnalysis.ioEndTime('speedTest2')

    print 'Done !'
    
    print ioTimeAnalysis.ioTimeAnalysisReport()

if (__name__ == '__main__'):
    _plain = ''.join([chr(n) for n in xrange(ord('a'),ord('z')+1)])
    print '_plain=%s' % (_plain)
    
    x = _coder.encode(_plain)
    print 'x=%s' % (x)
    
    xx = coder.encode(_plain)
    
    assert x == xx, 'Oops something went wrong with the Cython coder because its output does not match that from Python.'
    
    print 'xx=%s' % (xx)
    
    main()
    