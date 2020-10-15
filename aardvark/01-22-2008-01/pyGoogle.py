import os
import sys
from vyperlogix import threadpool
from vyperlogix import _psyco
from vyperlogix import _utils
from vyperlogix import google
from vyperlogix import AccumulatorHash

_pool = threadpool.Pool(100)

_results = []

_phrase = 'Once upon a time there was a little man who failed to grow taller'

@threadpool.threadpool(_pool)
def googleSearch(keyword):
    _results.append(google.performGoogleSearch(keyword))

def href(value):
    _symbol = 'href='
    i = value.find(_symbol)
    if (i > -1):
        l = (i+len(_symbol))
        value = value[l:]
        if (value[0] == '"'):
            value = value[1:]
            j = value.find('"')
            if (j > -1):
                value = value[0:j-1]
            j = value.find('?')
            if (j > -1):
                value = value[0:j-1]
            value = value.replace('http://','')
            toks = value.split('/')
            value = toks[0]
    return value

def main():
    urls = []
    toks = _phrase.split()
    for t in toks:
        googleSearch(t)
    _pool.join() # wait for all the work to be done...
    # collect all of the lists of href tags from each parser objects
    for r in _results:
        urls.append([href(t) for t in r['parser'][0].tagContents])
    # resolve frequency of common urls from each href tag
    analysis = AccumulatorHash.HashedLists()
    for u in urls:
        for x in u:
            analysis[x] = x
    # quantify frequency analysis
    analysis2 = AccumulatorHash.HashedLists()
    for k,v in analysis.iteritems():
        analysis2[k] = len(v)
    # reverse the quanitification
    analysis3 = AccumulatorHash.HashedLists()
    for k,v in analysis2.iteritems():
        analysis3['%d' % v[0]] = k
    # retrieve the quantification
    keys = [int(n) for n in analysis3.keys()]
    # order the quantification least to most
    keys.sort()
    keys.reverse()
    keys = [str(k) for k in keys]
    urls = [analysis3[k] for k in keys if len(analysis3[k]) == 1]
    print 'These words %s appear most often in the following urls.' % str(toks)
    print 'BEGIN:'
    for u in urls:
        print u
    print 'END !'
    print 'Now imagine you wanted to find URLs or web addresses that contained intersections of certain words or tokens.'
    print 'You would be hard-pressed to perform this type of analysis using Google alone.'
    print 'Now you can more easily perform this type of analysis with no muss and no fuss all without having to wait for Google to provide you with an API for this purpose.'

if (_utils.getVersionNumber() >= 251):
    _psyco.importPsycoIfPossible()
    main()
else:
    print 'Try using Python Version 2.5.1 or later rather than verison "%s".' % sys.version_info
