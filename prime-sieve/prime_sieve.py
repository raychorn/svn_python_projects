# time a number of progressively imrove prime number functions
# a decorator timing function is used
# declare the @decorator just above the function to invoke print_timing()
# tested with Python25    HAB      03feb2007

import time

def print_timing(func):
    """set up a decorator function for timing"""
    def wrapper(*arg):
        t1 = time.clock()
        res = func(*arg)
        t2 = time.clock()
        print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        return res
    return wrapper


@print_timing
def get_primes1(r=10):
    """
    unimproved original version
    """
    primes = []
    for i in range(2, r+1):
        prime = 1
        for divisor in range(2, i):
            if i % divisor == 0:
                prime = 0
                break
        if prime:
            primes.append(i)
    return primes

@print_timing
def get_primes2(r=10):
    """
    improved version, loop only over odd numbers starting with 3
    also limit the divisor range
    """
    primes = [2]
    # now ranges return odd numbers only ...
    for i in range(3, r+1, 2):
        prime = 1
        for divisor in range(3, i//2, 2):
            if i % divisor == 0:
                prime = 0
                break
        if prime:
            primes.append(i)
    return primes

@print_timing
def get_primes3(r=10):
    """
    improved version, loop only over odd numbers starting with 3
    and limit devisor range even more
    """
    primes = [2]
    # now ranges return odd numbers only ...
    for i in range(3, r+1, 2):
        prime = 1
        for divisor in range(3, i//7+3, 2):
            if i % divisor == 0:
                prime = 0
                break
        if prime:
            primes.append(i)
    return primes

@print_timing
def get_primes4(r=10):
    """
    improved version, loop only over odd numbers starting with 3
    and limit devisor range even more and using xrange()
    """
    primes = [2]
    # now ranges return odd numbers only ...
    for i in xrange(3, r+1, 2):
        prime = 1
        for divisor in xrange(3, i//7+3, 2):
            if i % divisor == 0:
                prime = 0
                break
        if prime:
            primes.append(i)
    return primes

@print_timing
def get_primes5(r=10):
    """
    improved version, loop only over odd numbers starting with 3
    and limit devisor range further with **0.5 and using xrange()
    """
    primes = [2]
    # now ranges return odd numbers only ...
    for i in xrange(3, r+1, 2):
        prime = 1
        for divisor in xrange(3, int(i ** 0.5)+1, 2):
            if i % divisor == 0:
                prime = 0
                break
        if prime:
            primes.append(i)
    return primes

@print_timing
def get_primes7(n):
    """
    standard optimized sieve algorithm to get a list of prime numbers
    --- this is the function to compare your functions against! ---
    """
    if n < 2:  return []
    if n == 2: return [2]
    # do only odd numbers starting at 3
    s = range(3, n+1, 2)
    # n**0.5 simpler than math.sqr(n)
    mroot = n ** 0.5
    half = len(s)
    i = 0
    m = 3
    while m <= mroot:
        if s[i]:
            j = (m*m-3)//2  # int div
            s[j] = 0
            while j < half:
                s[j] = 0
                j += m
        i = i+1
        m = 2*i+3
    return [2]+[x for x in s if x]

r = 9000
p1 = get_primes1(r)           
p2 = get_primes2(r)
p3 = get_primes3(r)
p4 = get_primes4(r)
p5 = get_primes5(r)
p7 = get_primes7(r)

# print the first 15 primes in the returned prime list for testing
print p1[:15]
print p2[:15]
print p3[:15]
print p4[:15]
print p5[:15]
print p7[:15]
print
# print the last 5 primes in the returned prime list for testing
print p1[-5:]
print p2[-5:]
print p3[-5:]
print p4[-5:]
print p5[-5:]
print p7[-5:]

"""
timing results for r=9000
get_primes1 took 2365.512 ms
get_primes2 took 467.231 ms
get_primes3 took 148.986 ms
get_primes4 took 104.222 ms
get_primes5 took 25.376 ms
get_primes7 took 2.483 ms
"""
