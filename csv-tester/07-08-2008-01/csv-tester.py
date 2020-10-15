# csv tester

import re
import os, sys

import logging

from vyperlogix.misc import ioTimeAnalysis
from vyperlogix.misc import _utils

fname = "put-your-file-name-here.csv"

_re = re.compile('"[^"\r\n]*"|[^,\r\n]*', re.MULTILINE)

def useSplits(csv,lines):
    ioTimeAnalysis.ioBeginTime('PARSE-SPLITS')
    _guide = lines[0].split(',')
    csv.append(_guide)
    for l in lines[1:]:
        recs = l.split(',')
        if (len(_guide) == len(recs)):
            csv.append(recs)
        else:
            _msg = '(%s) :: Cannot parse "%s", number of fields do not match the first line.' % (_utils.funcName(),l)
            logging.warning(_msg)
            raise ValueError(_msg)
    ioTimeAnalysis.ioEndTime('PARSE-SPLITS')

def useRegex(csv,lines):
    ioTimeAnalysis.ioBeginTime('PARSE-REGEX')
    _guide = [match.group() for match in _re.finditer(lines[0])]
    csv.append(_guide)
    for l in lines[1:]:
        recs = [match.group() for match in _re.finditer(l)]
        if (len(_guide) == len(recs)):
            csv.append(recs)
        else:
            _msg = '(%s) :: Cannot parse "%s", number of fields do not match the first line.' % (_utils.funcName(),l)
            logging.warning(_msg)
            raise ValueError(_msg)
    ioTimeAnalysis.ioEndTime('PARSE-REGEX')

if (__name__ == '__main__'):
    if (os.path.exists(fname)):
        ioTimeAnalysis.initIOTime('READ')
        ioTimeAnalysis.initIOTime('PARSE-REGEX')
        ioTimeAnalysis.initIOTime('PARSE-SPLITS')
        
        ioTimeAnalysis.ioBeginTime('READ')
        fIn = open(fname,'r')
        lines = fIn.readlines()
        fIn.close()
        ioTimeAnalysis.ioEndTime('READ')
        
        csv1 = []
        csv2 = []
        
        for i in xrange(0,100):
            #print '%d' % (i)
            useSplits(csv1,lines)
            useRegex(csv2,lines)
            
        n_csv1 = len(csv1)
        n_csv2 = len(csv2)
        assert n_csv1 == n_csv2, 'Oops, something is wrong with one of the parsers; one says %d records and the other says %d records.' % (n_csv1,n_csv2)
            
        ioTimeAnalysis.ioTimeAnalysisReport(fOut=sys.stdout)
    else:
        logging.warning('Cannot open "%s".' % (fname))
    pass
