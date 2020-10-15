#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:et
# (c) 2007 under terms of LGPL v 2.1
# by Vsevolod S. Balashov <vsevolod@balashov.name> 
import sys
import time
from threading import Thread
import threading

def threaded(func):
    def proxy(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return proxy

from Queue import Queue

class Pool(Queue):
    def __init__(self, maxsize, isDaemon=False):
        self.__stopevent = threading.Event()
        assert maxsize > 0, 'maxsize > 0 required for Pool class'
        Queue.__init__(self, maxsize)
        for i in xrange(maxsize):
            thread = Thread(target = self._worker)
            thread.setDaemon(isDaemon)
            thread.start()

    def getIsRunning(self):
        return not self.__stopevent.isSet()
    
    def setIsRunning(self,isRunning):
        if (not isRunning):
            self.__stopevent.set()
        
    def _worker(self):
        while not self.__stopevent.isSet():
            if (not self.isRunning):
                break
            try:
                func, args, kwargs = self.get()
                func(*args, **kwargs)
            except Exception, details:
                print >>sys.stderr, '(_worker).Error :: "%s".' % str(details)
                self.task_done()
                self.join()
                raise
            else:
                self.task_done()

    def addJob(self, func, *args, **kwargs):
        self.put((func, args, kwargs))

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.__stopevent.set()
        self.join()

    isRunning = property(getIsRunning, setIsRunning)

def threadpool(pool):
    assert pool.__class__ == Pool, 'threadpool decorator require a Pool object'
    def decorator(func):
        def proxy(*args, **kwargs):
            pool.put((func, args, kwargs))
            return pool
        return proxy
    return decorator

