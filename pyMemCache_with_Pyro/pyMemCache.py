from vyperlogix.misc import _utils
from vyperlogix.misc import threadpool
from vyperlogix.hash import proxies

from vyperlogix.misc import ObjectTypeName

from vyperlogix.misc.GenPasswd import GenPasswd

from vyperlogix.analysis import ioTimeAnalysis

import sys
import time
import Queue

import uuid

_background_Q = threadpool.ThreadQueue(5,isDaemon=False)

#import Pyro
#Pyro.config.PYRO_NS_DEFAULTGROUP = ":pyro_objects"

@threadpool.threadify(_background_Q)
def server():
    import sys
    from Pyro.ext import remote
    
    print 'Providing local object as "memcache"...'
    remote.provide_local_object(proxies.HashedListsProxy(), 'memcache')
    
    print 'Waiting for requests.'
    sys.exit(remote.handle_requests())
    
if (__name__ == '__main__'):
    server()
    
    ioTimeAnalysis.init_AnalysisDataPoint('Test1')
    
    from Pyro.ext import remote
    
    try:
        time.sleep(20)
        try:
            print 'getting remote object "memcache"...'
            d_memcache = remote.get_remote_object('memcache')
            print ObjectTypeName.typeName(d_memcache)
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            print >>sys.stderr, info_string
        
        try:
            ioTimeAnalysis.begin_AnalysisDataPoint('Test1')
            for i in xrange(0,1000):
                d_memcache.set_item(uuid.uuid4(),GenPasswd(length=128))
            ioTimeAnalysis.end_AnalysisDataPoint('Test1')
            print 'd_memcache.get_size() is %d' % (d_memcache.get_size())
            n = 1
            for k in d_memcache.get_keys():
                print '%d :: %s --> %s' % (n,k,d_memcache.get_item(k))
                n += 1
            print ioTimeAnalysis.ioTimeAnalysis.ioTimeAnalysisReport()
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            print >>sys.stderr, info_string
    except Exception, details:
        info_string = _utils.formattedException(details=details)
        print >>sys.stderr, info_string
