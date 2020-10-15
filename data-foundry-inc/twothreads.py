'''
2) In a relevant language, create an array of 1000 numbers. 
Initialize all of the values in the array to zero. 
Create two threads that run concurrently and which increment 
each element of the array one time.

When both threads have finished running, all elements in the array should have the value of two. Verify this.
'''
import os, signal
from threadpool import ThreadQueue, threadify

__array_of_numbers__ = [n-n for n in xrange(0,1000)]

__Q__ = ThreadQueue(2)

@threadify(__Q__)
def threaded(threadid,numbers):
    for i in xrange(0,len(numbers)):
        #print 'Thread ID ',threadid,'item #',i,' was ',numbers[i],'becomes',
        numbers[i] += 1
        #print numbers[i]


if (__name__ == '__main__'):
    try:
        i = 0
        for item in __array_of_numbers__:
            print 'array[%s]=%s' % (i,item)
            assert item==0, 'Something went very wrong.'
            i += 1
            
        threaded(1,__array_of_numbers__) # this is the first thread.
        threaded(2,__array_of_numbers__) # this is the second thread.
    
        __Q__.join() # wait for all threads to complete.
    
        try:
            print 'Verifying all values are 2.'
            i = 0
            for item in __array_of_numbers__:
                print 'array[%s]=%s' % (i,item)
                assert item==2, 'Something went very wrong.'
                i += 1
            print 'Verified !!!'
        except:
            pass
    except:
        pass
    finally:
        pid = os.getpid()
        os.kill(pid,signal.SIGTERM)
    
    