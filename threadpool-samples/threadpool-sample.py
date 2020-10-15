import sys
import time
import random

import Queue

from vyperlogix.misc import threadpool

__Q1__ = threadpool.ThreadQueue(10)

__Q2__ = threadpool.ThreadQueue(10)

__outputQ__ = Queue.Queue(maxsize=100)

__count__ = 0

@threadpool.threadify(__Q2__)
def dequeue(timeout=None):
    global __count__
    if (timeout is not None):
        data = __outputQ__.get(timeout=timeout)
    else:
        data = __outputQ__.get()
    while (data is not None) and (__count__ > 0):
        print 'DEQUEUE --> %s (#%s)' % (data,__count__)
        __count__ -= 1
        if (__count__ > 0) and (timeout is not None):
            data = __outputQ__.get(timeout=timeout)
        else:
            data = __outputQ__.get()
    print 'DEQUEUE DONE !!! data=%s, count=%s' % (data,__count__)

@threadpool.threadify(__Q1__)
def worker(data,sleep=None):
    if (sleep):
        time.sleep(sleep)
    __outputQ__.put_nowait(data)

__count__ = 10
dequeue(15)

print 'Workers execute serially...'
for x in xrange(__count__):
    worker(x)
    
print '\n1.Wait for workers to finish...'
__Q1__.join()

__count__ = 10

print 'Workers execute out of order...'
for x in xrange(__count__):
    worker(x,float(random.randint(1,10)))

while (__count__ > 0):
    print 'WAIT FOR DEQUEUE #%s' % (__count__)
    time.sleep(0.2)

print 'Q1 stopping...'
__Q1__.isRunning = False
print 'Q2 stopping...'
__Q2__.isRunning = False

import os
pid = os.getpid()
print 'PID is %s' % (pid)

from vyperlogix.process import killProcByPID
killProcByPID.killProcByPID(pid)
