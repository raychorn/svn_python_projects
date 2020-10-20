__copyright__ = """\
(c). Copyright 1990-2014, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
import os, sys
import re

#sys.path.insert(0,'Z:\python projects\@lib')

from vyperlogix.misc import _utils
from vyperlogix.misc.FormatWithCommas import FormatWithCommas

from vyperlogix.decorators import ioTimeAnalysis

from vyperlogix.misc import threadpool

__Q__ = threadpool.ThreadQueue(100)

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

__default__ = r"J:\@Vyper Logix Corp\@Projects\python-projects"

@ioTimeAnalysis.analyze('main')
def main(top,file_endswith='.py',isthreaded=False):
    loc = 0
    __reFilter = '[._]svn'
    rejecting_re=re.compile(__reFilter)

    def count_lines_for_file(fname,isthreaded=False):
	_loc = 0
	if (os.path.exists(fname)):
	    lines = _utils.readFileFrom(fname).split('\n')
	    _loc = len(lines)
	    print '%s has %d lines of code [%s].' % (fname,_loc,'single' if (not isthreaded) else 'threaded')
	return _loc

    @threadpool.threadify(__Q__)
    def count_lines_for_file_threaded(fname,isthreaded=False):
	return count_lines_for_file(fname,isthreaded=isthreaded)

    def count_lines_for_files(files,isthreaded=False):
	_loc = 0
	__loc__ = 0
	_files = [_f for _f in files if (_f.endswith(file_endswith) if (isinstance(file_endswith,str)) else any([_f.endswith(ending) for ending in file_endswith]) if (isinstance(file_endswith,list)) else False)]
	for f in _files:
	    fname = os.sep.join([root,f])
	    __loc__ += count_lines_for_file(fname,isthreaded=isthreaded) if (not isthreaded) else count_lines_for_file_threaded(fname,isthreaded=isthreaded)
	return _loc
    
    if (os.path.isdir(top)):
	for root, dirs, files in _utils.walk(top, topdown=True, rejecting_re=rejecting_re):
	    _files = [_f for _f in files if (_f.endswith(file_endswith) if (isinstance(file_endswith,str)) else any([_f.endswith(ending) for ending in file_endswith]) if (isinstance(file_endswith,list)) else False)]
	    loc += count_lines_for_files(_files,isthreaded=isthreaded)
    print 'lines of code is "%s" [%s].' % (FormatWithCommas('%d',loc),'single' if (not isthreaded) else 'threaded')
    return loc

@ioTimeAnalysis.analyze('report_loc')
def report_loc(dirs,isthreaded=False):
    _total_lines_of_code = 0
    reportIO = StringIO()
    for dirname in dirs:
	_loc = main(dirname,file_endswith=['.rb','.py'],isthreaded=isthreaded)
	_total_lines_of_code += _loc
	print >>reportIO, 'lines of code in "%s" is "%s".' % (dirname,FormatWithCommas('%d',_loc))
    print >>reportIO, 'total lines of code is "%s".' % (FormatWithCommas('%d',_total_lines_of_code))
    reportIO.flush()
    print reportIO.getvalue()
    
@ioTimeAnalysis.analyze('run_timed')
def run_timed(args,isthreaded=False):
    dirp2 = __default__ if (len(args) == 0) else args[0] if (len(args) > 0) else args
    if (os.path.exists(dirp2)):
	dirs = [os.path.join(dirp2,f) for f in os.listdir(dirp2)]
	report_loc(dirs,isthreaded=isthreaded)
    else:
	print >> sys.stderr, 'WARNING: Cannot locate the directory you wish to act upon with this utility. Please try again.'

if (__name__ == '__main__'):
    from vyperlogix.misc import _utils
    
    ioTimeAnalysis.ioTimeAnalysis.initIOTime('main')
    ioTimeAnalysis.ioTimeAnalysis.initIOTime('report_loc')
    ioTimeAnalysis.ioTimeAnalysis.initIOTime('run_timed')
    
    #lines = [l for l in _utils.readFileFrom('report.txt').split('\n') if (len(l.strip()) > 0)]
    #lines = [int(''.join([ch for ch in l if (ch.isdigit())])) for l in lines]
    #n = 0
    #for l in lines:
	#n += l
    #pass
    
    #dir1 = r'Z:\@myMagma\!!python-trunk'
    #dir2 = r'Z:\@myMagma\python-local-new-trunk'
    #dir3 = r'Z:\@myMagma\python-local-new-trunk-ruby-daemon'
    #dir4 = r'Z:\@myMagma\python-local-projects'
    #dir5 = r'Z:\@myMagma\python-local-trunk'
    #dirs = [dir1,dir2,dir3,dir4,dir5]
    #report_loc(dirs)

    #dirp1 = r'Z:\python projects'
    #main(dirp1)

    #dirr1 = r'Z:\@myMagma\molten-trunk\molten3'
    #dirr2 = r'Z:\@myMagma\molten-trunk\molten4'
    #dirr3 = r'Z:\@myMagma\molten-trunk\molten5'
    #dirr4 = r'Z:\@myMagma\molten-trunk\molten_python'
    #dirr5 = r'Z:\@myMagma\molten-trunk\ruby-python-bridge'
    #dirs = [dirr1,dirr2,dirr3,dirr4,dirr5]
    #report_loc(dirs)

    #dirp2 = r"Z:\python projects\@lib\vyperlogix"
    #main(dirp2)

    from optparse import OptionParser
    
    parser = OptionParser("usage: %prog path [options]")
    parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
    parser.add_option('-s', '--single', dest='single_threaded', help="single threaded", action="store_true")
    parser.add_option('-t', '--threaded', dest='multi_threaded', help="multi threaded", action="store_true")
    
    options, args = parser.parse_args()
    
    _isVerbose = False
    if (options.verbose):
	_isVerbose = True

    _isSingleThreaded = True
    if (options.single_threaded):
	_isSingleThreaded = True

    _isThreaded = False
    if (options.multi_threaded):
	_isThreaded = True
	_isSingleThreaded = False

    if (_isSingleThreaded):
	run_timed(args)
    elif (_isThreaded):
	run_timed(args,isthreaded=_isThreaded)
    else:
	print >> sys.stderr, 'WARNING: Cannot execute this utility without a valid choice as to the threading model.'
	_utils.terminate('Abend.')

    ioTimeAnalysis.ioTimeAnalysis.ioTimeAnalysisReport()
    _utils.terminate('Program Complete.')
    