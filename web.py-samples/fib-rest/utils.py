def fibonacci():
    a, b = 0, 1
    while 1:
        yield a
        a, b = b, a + b
        
def get_fibonacci_nums(num):
    num = int(num)
    if (num > 0):
        fib = fibonacci()
        items = ['%s'%(fib.next()) for n in xrange(num)]
    else:
        items = ['ERROR']
    return items

if (__name__ == '__main__'):
    num = 20
    fib = fibonacci()
    for n in xrange(num):
        print '%s'%(fib.next())
