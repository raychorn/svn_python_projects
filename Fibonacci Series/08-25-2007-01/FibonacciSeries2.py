import time

def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
    
def fib_generator():
    a, b = 0, 1
    while 1:
        yield a
        a, b = b, a + b
        
if (__name__ == '__main__'):
    t0 = time.time()
    fib = fibonacci(100)
    t1 = time.time()
    
    print "%.3f seconds" % (t1-t0)

    print '='*40
    
    t0 = time.time()
    fib = fib_generator()
    for n in xrange(1,1000):
        print fib.next()
    t1 = time.time()
    
    print "%.3f seconds" % (t1-t0)
    