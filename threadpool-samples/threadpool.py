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

class ThreadQueue(Queue):
    def __init__(self, maxsize, isDaemon=False):
        self.__stopevent = threading.Event()
        assert maxsize > 0, 'maxsize > 0 required for ThreadQueue class'
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
		import traceback
                print >>sys.stderr, '(%s._worker).Error :: "%s".' % (self.__class__,str(details))
		print >>sys.stderr, traceback.format_exc()
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
        self.__shutdown__()

    def __shutdown__(self):
        self.__stopevent.set()
        self.join()

    isRunning = property(getIsRunning, setIsRunning)

def threadify(threadQ):
    assert threadQ.__class__ in [ThreadQueue], 'threadify decorator requires a ThreadQueue or Queue object instance, use Queue when threading is not required.'
    def decorator(func):
        def proxy(*args, **kwargs):
            threadQ.put((func, args, kwargs))
            return threadQ
        return proxy
    return decorator
