from vyperlogix.misc import ioTimeAnalysis

from code import str_replace
from code import str_replace2
try:
    from code import str_replace2a
except ImportError:
    str_replace2a = None

import os, sys
import re

s = '/'.join(['%d'%n for n in xrange(1000)])

_new_sep = os.sep
_replacement = r"\1\%s" % _new_sep

regex = re.compile('(?i)((?:"[^"]*")|[^/]+)*/')

def splitter(x):
    return _new_sep.join(x.split('/'))

def replacer(x):
    return x.replace('/',_new_sep)

def regexer(x):
    return re.sub('(?i)((?:"[^"]*")|[^/]+)*/', _replacement, x)

def regexer2(x):
    return regex.sub(_replacement, x)

def str_replacer(x):
    return str_replace.str_replace(x,'/',_new_sep)

def str_replacer2(x):
    return str_replace2.str_replace2(x,'/',_new_sep)

def str_replacer2a(x):
    try:
        value = str_replace2a.str_replace2(x,'/',_new_sep)
    except:
        value = str(x).replace('/',_new_sep)
    return value

def main():
    ioTimeAnalysis.ioBeginTime(_splitter_tag)
    for n in xrange(1,100):
        z = splitter(s)
        pass
    ioTimeAnalysis.ioEndTime(_splitter_tag)
    
    ioTimeAnalysis.ioBeginTime(_replacer_tag)
    for n in xrange(1,100):
        z = replacer(s)
        pass
    ioTimeAnalysis.ioEndTime(_replacer_tag)
    
    ioTimeAnalysis.ioBeginTime(_regexer_tag)
    for n in xrange(1,100):
        z = regexer(s)
        pass
    ioTimeAnalysis.ioEndTime(_regexer_tag)

    ioTimeAnalysis.ioBeginTime(_regexer2_tag)
    for n in xrange(1,100):
        z = regexer2(s)
        pass
    ioTimeAnalysis.ioEndTime(_regexer2_tag)
    
    ioTimeAnalysis.ioBeginTime(_str_replacer_tag)
    for n in xrange(1,100):
        z = str_replacer(s)
        pass
    ioTimeAnalysis.ioEndTime(_str_replacer_tag)
    
    ioTimeAnalysis.ioBeginTime(_str_replacer2_tag)
    for n in xrange(1,100):
        z = str_replacer2(s)
        pass
    ioTimeAnalysis.ioEndTime(_str_replacer2_tag)
    
    ioTimeAnalysis.ioBeginTime(_str_replacer2a_tag)
    for n in xrange(1,100):
        z = str_replacer2a(s)
        pass
    ioTimeAnalysis.ioEndTime(_str_replacer2a_tag)
    
def __main__():
    global _splitter_tag, _replacer_tag, _regexer_tag, _regexer2_tag, _str_replacer_tag, _str_replacer2_tag, _str_replacer2a_tag
    
    _splitter_tag = 'splitter'
    _replacer_tag = 'replacer'
    _regexer_tag = 'regexer'
    _regexer2_tag = 'regexer2'
    _str_replacer_tag = 'str_replacer'
    _str_replacer2_tag = 'str_replacer2'
    _str_replacer2a_tag = 'str_replacer2a'

    ioTimeAnalysis.initIOTime(_splitter_tag)
    ioTimeAnalysis.initIOTime(_replacer_tag)
    ioTimeAnalysis.initIOTime(_regexer_tag)
    ioTimeAnalysis.initIOTime(_regexer2_tag)
    ioTimeAnalysis.initIOTime(_str_replacer_tag)
    ioTimeAnalysis.initIOTime(_str_replacer2_tag)
    ioTimeAnalysis.initIOTime(_str_replacer2a_tag)

    main()
    
    ioTimeAnalysis.ioTimeAnalysisReport(fOut=sys.stdout)

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible()
    
    __main__()