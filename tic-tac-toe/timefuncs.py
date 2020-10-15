import time
import random

if (__name__ == '__main__'):
    random.seed(time.time())
    t = time.localtime()
    l = list(t)
    p = 0
    while (1):
        l[3] -= int(random.gammavariate(1.1, 10.0))
        t1 = time.mktime(t)
        t2 = time.mktime(tuple(l))
        d = int(max(t1,t2) - min(t1,t2))
        try:
            choices = [i for i in xrange(-d,d)]
            random.shuffle(choices)
            p = random.choice(choices)
            break
        except:
            pass
    o = '+' if (p > 0) else '-'
    print t1
    print t2
    print '%s%s' % (o,d)
    
    t = time.localtime()
    midnite = list(tuple(t))[0:3]
    filler = [0 for i in xrange(0,t.n_fields-3)]
    midnite = time.mktime(midnite+filler)
    
    c = int(time.time()-midnite)
    print c
    if (o == '+') and (c == d):
        print 'ERROR time!!!'
    else:
        print 'NOMINAL !!!'
    
