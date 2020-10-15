import os, sys

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

def profile(fpath):
    '''
    Usage:

    @profile(fpath)
    def method(item):
        print item
    '''
    def decorator(func):
        def wrapper(*args, **kwargs):
            import cProfile, pprint, StringIO
            prof = cProfile.Profile()
            retval = prof.runcall(func, *args, **kwargs)
            fOut = StringIO.StringIO()
            pprint.pprint(prof.getstats(),fOut)
            n = '%s-%s'%(func.__module__,func.__name__)
            fname = '%s.profile' % (n.replace('.','_'))
            fp = os.sep.join([fpath,fname])
            if (not os.path.exists(fpath)):
                os.makedirs(fpath)
            from util import writes
            writes.to_file(fp, fOut.getvalue())
            fOut = StringIO.StringIO()
            print >>fOut, '@echo off'
            print >>fOut, ''
            print >>fOut, 'python -m pstats "%s"' % (fname)
            fname2 = 'pstat_%s.cmd' % (n.replace('.','_'))
            fp2 = os.sep.join([fpath,fname2])
            writes.to_file(fp2, fOut.getvalue())
            return retval
        return wrapper        
    return decorator
