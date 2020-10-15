import os,sys

from vyperlogix.misc import ioTimeAnalysis

max_size_of_file = 1024*1024

def create_the_file(name):
    _mode = 'w+'
    fOut = open(name,mode=_mode,buffering=1)
    num = 1
    while (1):
        #fOut.seek(0,2)
        print >> fOut, '%d' % num
        num += 1
        statinfo = os.stat(name)        
        print '%s of %s' % (statinfo.st_size,max_size_of_file)
        if (statinfo.st_size > max_size_of_file):
            break
        _mode = 'a+' if (_mode == 'w+') else _mode
    fOut.flush()
    fOut.close()
    
def reverse_the_file(name,has_lines=True):
    fOut = open(name,mode='rb',buffering=1)

if (__name__ == '__main__'):
    print 'BEGIN:'
    __creation_symbol__ = 'Creation'
    ioTimeAnalysis.initIOTime(__creation_symbol__)
    ioTimeAnalysis.ioBeginTime(__creation_symbol__)
    fname = os.path.abspath('./10-gb-file-reversal.dat')
    if (not os.path.exists(fname)):
        print 'Creating the file... "%s"' % (fname)
        create_the_file(fname)
    ioTimeAnalysis.ioEndTime(__creation_symbol__)
    
    ioTimeAnalysis.ioTimeAnalysisReport()
        
    # reverse the file here...
    print 'END !!!'
