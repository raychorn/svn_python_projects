# regexBenchmarks.py
from ioTimeAnalysis import *
from _utils import *
import re

_numIters = 10000
_datum = []
_dataRegex = []
_dataTokens1 = []
_dataTokens2 = []

def useRegex(num):
    for d in _datum:
        if (num == 1):
            _dataRegex.append(re.findall("(19|20[0-9]{2})[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])(T)([0-9]{2})[:]([0-9]{2})[:]([0-9]{2})[.]([0-9]{3})(Z)", d))

def flattenList(input):
    _toks = []
    for t in input:
        for _t in t:
            _toks.append(_t)
    return _toks

def useTokenSplitter(num):
    for d in _datum:
        if (num == 1):
            toks = d.split('Z')
            toks[-1] = 'Z'
            toks = [t.split('T') for t in toks]
            toks[0].insert(1,'T')
            toks = flattenList(toks)
            toks = [t.split('-') for t in toks]
            toks = flattenList(toks)
            toks = [t.split(':') for t in toks]
            toks = flattenList(toks)
            toks = [t.split('.') for t in toks]
            toks = flattenList(toks)
            _dataTokens1.append(toks)
        elif (2):
            toks = [_d if _d.isalnum() else '' for _d in d]
            _tokens = []
            _token = ''
            for t in toks:
                if (len(t) > 0):
                    if (t.isdigit()):
                        _token += t
                    else:
                        _tokens.append(_token)
                        _tokens.append(t)
                        _token = ''
                else:
                    _tokens.append(_token)
                    _token = ''
            _dataTokens2.append(_tokens)

def initialization():
    initIOTime('initialization')
    ioBeginTime('initialization')
    for i in xrange(_numIters):
        _datum.append(timeStamp())
    ioEndTime('initialization')

def doRegex():
    initIOTime('Regex-1')
    ioBeginTime('Regex-1')
    useRegex(1)
    ioEndTime('Regex-1')

def doTokenSplitter(num):
    initIOTime('TokenSplitter-%s' % num)
    ioBeginTime('TokenSplitter-%s' % num)
    useTokenSplitter(num)
    ioEndTime('TokenSplitter-%s' % num)

def main():
    doRegex()
    doTokenSplitter(1)
    doTokenSplitter(2)
    print ioTimeAnalysisReport()
    print '_datum::'
    print '\n'.join(_datum[0:10])
    print '='*30
    print
    print '_dataRegex::'
    for d in _dataRegex[0:10]:
        print d
    print '='*30
    print
    print '_dataTokens1::'
    for d in _dataTokens1[0:10]:
        print d
    print '='*30
    print
    print '_dataTokens2::'
    for d in _dataTokens2[0:10]:
        print d
    print '='*30
    print

if (__name__ == '__main__'):
    import _psyco
    _psyco.importPsycoIfPossible()
    initialization()
    main()
    pass
