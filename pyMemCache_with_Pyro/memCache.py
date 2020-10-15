from vyperlogix.misc import _utils
from vyperlogix.hash import proxies

from vyperlogix.misc import ObjectTypeName

from vyperlogix.misc.GenPasswd import GenPasswd

from vyperlogix.analysis import ioTimeAnalysis

import sys
import time

import uuid

if (__name__ == '__main__'):
    is_memcachable = True
    try:
        import memcache
    except ImportError:
        is_memcachable = False
        
    if (is_memcachable):
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        is_memcachable = all([s.connect() for s in mc.servers])
    
    if (is_memcachable):
        ioTimeAnalysis.init_AnalysisDataPoint('Test1')
        
        try:
            d = {}
            ioTimeAnalysis.begin_AnalysisDataPoint('Test1')
            for i in xrange(0,5000):
                k = str(uuid.uuid4())
                d[k] = GenPasswd(length=128)
                mc.set(k,d[k])
            ioTimeAnalysis.end_AnalysisDataPoint('Test1')
            print 'stats is %s' % (mc.stats)
            n = 1
            for k in d.keys():
                print '%d :: %s --> %s' % (n,k,mc.get(k))
                n += 1
            print ioTimeAnalysis.ioTimeAnalysis.ioTimeAnalysisReport()
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            print >>sys.stderr, info_string
    else:
        print 'ERROR cannot run the test.'
