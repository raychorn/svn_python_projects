# Python Threads 1

import sys
import httplib

import time

from vyperlogix.misc import threadpool

_Q_ = threadpool.ThreadQueue(10, isDaemon=False)

pages = ['www.google.com', 'www.rubycentral.com', 'www.dice.com', 'www.python.org']

done = []

control = 'www.gmail.com'

def _fetch(url):
    conn = httplib.HTTPConnection(url)
    conn.request("GET", '')
    isError = False
    try:
        r1 = conn.getresponse()
    except:
        isError = True
    return url,r1.status,r1.reason,isError

@threadpool.threadify(_Q_)
def fetch(url):
    resp = _fetch(url)
    if (url == 'www.google.com'):
        print 'Hammer on %s' % (control)
        for i in xrange(0,1000):
            _fetch(control)
    done.append(url)
    print '%s --> r1.status is "%s" and r1.reason is "%s" and isError is "%s".' % (resp)
    if (len(done) == len(pages)):
        print 'Done !'
        sys.exit(1)

for p in pages:
    fetch(p)

