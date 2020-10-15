import time

def fib(n):
    a, b = 0, 1
    while b < n:
        print b
        a, b = b, a+b

t0 = time.time()
fib(10000000000000000) #0000000000000000
t1 = time.time()

print "%.3f seconds" % (t1-t0)