import sys
import time
import random

import Queue

import threadpool

from static import staticmethod

__Q1__ = threadpool.ThreadQueue(10)
__Q2__ = threadpool.ThreadQueue(10)

__outputQ1__ = Queue.Queue(maxsize=100)

__Q3__ = threadpool.ThreadQueue(10)
__Q4__ = threadpool.ThreadQueue(10)

__outputQ2__ = Queue.Queue(maxsize=100)

class Sample1():
    __count__ = 0

    @threadpool.threadify(__Q2__)
    @staticmethod
    def dequeue(timeout=None):
        if (timeout is not None):
            data = __outputQ1__.get(timeout=timeout)
        else:
            data = __outputQ1__.get()
        while (data is not None) and (Sample1.__count__ > 0):
            print 'Sample1.DEQUEUE --> %s (#%s)' % (data,Sample1.__count__)
            Sample1.__count__ -= 1
            if (Sample1.__count__ > 0) and (timeout is not None):
                data = __outputQ1__.get(timeout=timeout)
            else:
                data = __outputQ1__.get()
        print 'Sample1.DEQUEUE DONE !!! data=%s, count=%s' % (data,Sample1.__count__)

    @threadpool.threadify(__Q1__)
    @staticmethod
    def worker(data,sleep=None):
        if (sleep):
            time.sleep(sleep)
        __outputQ1__.put_nowait(data)

    def __init__(self,count=10,serially=False):
        Sample1.__count__ = count
        Sample1.dequeue.__func__(15)
        
        if (serially):
            print 'Sample1.Workers execute serially...'
            for x in xrange(Sample1.__count__):
                Sample1.worker.__func__(x)
                
            print '\nSample1.Waiting for workers to finish...'
            print 'Sample1 __Q1__.join()...'
            __Q1__.join()
            
        Sample1.__count__ = count
        
        print 'Sample1.Workers execute out of order...'
        for x in xrange(Sample1.__count__):
            Sample1.worker.__func__(x,float(random.randint(1,10)))
        
        while (Sample1.__count__ > 0):
            print 'Sample1.WAIT FOR DEQUEUE #%s' % (Sample1.__count__)
            time.sleep(0.2)
        
        print 'Sample1.Q1 stopping...'
        __Q1__.isRunning = False
        print 'Sample1.Q2 stopping...'
        __Q2__.isRunning = False
        
        print '='*30
        
class Sample2():
    __count__ = 0

    @threadpool.threadify(__Q4__)
    def dequeue(timeout=None):
        Sample2.__dequeue__(timeout=timeout)

    @staticmethod
    def __dequeue__(timeout=None):
        if (timeout is not None):
            data = __outputQ2__.get(timeout=timeout)
        else:
            data = __outputQ2__.get()
        while (data is not None) and (Sample2.__count__ > 0):
            print 'Sample2.DEQUEUE --> %s (#%s)' % (data,Sample2.__count__)
            Sample2.__count__ -= 1
            if (Sample2.__count__ > 0) and (timeout is not None):
                data = __outputQ2__.get(timeout=timeout)
            else:
                data = __outputQ2__.get()
        print 'Sample2.DEQUEUE DONE !!! data=%s, count=%s' % (data,Sample2.__count__)

    @threadpool.threadify(__Q3__)
    def worker(data,sleep=None):
        Sample2.__worker__(data,sleep=sleep)

    @staticmethod
    def __worker__(data,sleep=None):
        if (sleep):
            time.sleep(sleep)
        __outputQ2__.put_nowait(data)

    def __init__(self,count=10,serially=False):
        Sample2.__count__ = count
        Sample2.dequeue.__func__(15)
        
        if (serially):
            print 'Sample2.Workers execute serially...'
            for x in xrange(Sample2.__count__):
                Sample2.worker.__func__(x)
                
            print '\nSample2.Waiting for workers to finish...'
            print 'Sample2 __Q3__.join()...'
            __Q3__.join()
            
        Sample2.__count__ = count
        
        print 'Sample2.Workers execute out of order...'
        for x in xrange(Sample2.__count__):
            Sample2.worker.__func__(x,float(random.randint(1,10)))
        
        while (Sample2.__count__ > 0):
            print 'Sample2.WAIT FOR DEQUEUE #%s' % (Sample2.__count__)
            time.sleep(0.2)
        
        print 'Sample2.Q3 stopping...'
        __Q3__.isRunning = False
        print 'Sample2.Q4 stopping...'
        __Q4__.isRunning = False
        
        print '='*30

__Q__ = threadpool.ThreadQueue(10)

@threadpool.threadify(__Q__)
def scheduler():
    for i in xrange(0,1):
        s = Sample1(count=10)

    for i in xrange(0,1):
        s = Sample2(count=10)

scheduler()

time.sleep(30)
while (1):
    print 'INFO: Waiting for all tasks to complete...'
    print 'INFO: __Q1__.%sempty()' % ('NOT_' if (not __Q1__.empty()) else '')
    print 'INFO: __Q2__.%sempty()' % ('NOT_' if (not __Q2__.empty()) else '')
    print 'INFO: __Q3__.%sempty()' % ('NOT_' if (not __Q3__.empty()) else '')
    print 'INFO: __Q4__.%sempty()' % ('NOT_' if (not __Q4__.empty()) else '')
    if (__Q1__.empty() and __Q2__.empty() and __Q3__.empty() and __Q4__.empty()):
        print 'INFO: __Q__.join()...'
        __Q__.join()
        print 'INFO: All tasks are complete.'

        import os
        import signal
        
        pid = os.getpid()
        print 'INFO: PID is %s' % (pid)
        
        print 'INFO: Terminating PID %s' % (pid)
        os.kill(pid,signal.SIGTERM)
    time.sleep(5)
