import os,sys
import time

from vyperlogix.misc import _utils

CM404A_z = r'\\CM404A\z'

Unknownlaptop_z = r'\\Unknownlaptop\z'

def benchmark(top,t_limit):
    global t_begin, t_end, t_bytes
    t_bytes = 0
    t_begin = time.time()
    et = 0
    for root,dirs,files in _utils.walk(top):
        for f in files:
            _f = os.sep.join([root,f])
            try:
                s = _utils.readBinaryFileFrom(_f)
                print >>sys.stderr, _f
                t_bytes += len(s)
            except:
                pass
            t_end = time.time()
            et = t_end - t_begin
            if (et >= t_limit):
                print >>sys.stderr, '%s bytes in %s secs.' % (t_begin,et)
                return t_bytes,et
    return t_bytes,et

if (__name__ == '__main__'):
    b1,e1 = benchmark(Unknownlaptop_z,180)
    
    b2,e2 = benchmark(CM404A_z,180)
    
    print >>sys.stderr, '%s throughput is %s' % (Unknownlaptop_z,b1/e1)

    print >>sys.stderr, '%s throughput is %s' % (CM404A_z,b2/e2)
    