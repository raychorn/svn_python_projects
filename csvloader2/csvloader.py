__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

                   All Rights Reserved.

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

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.parsers.CSV import CSV

from vyperlogix.enum.Enum import Enum

class Tables(Enum):
    nothing = 0

def process_records(fnameIn,choice=Tables.nothing):
    from vyperlogix.parsers.CSV import CSVgenerator
    print 'Reading %s...' % (fnameIn)
    reader = CSVgenerator(filename=fnameIn)
    ioBuf = _utils.stringIO()
    n = 1
    print 'Writing records...'
    for aRec in reader.parse():
        items = []
        for k,v in aRec.iteritems():
            if (v is None):
                continue
            v = str(v)
            if (len(v) == 0):
                continue
            items.append(":%s => %s%s%s" % (k,quote,_utils.ascii_only(str(v)),quote))
        
        print 'Writing record #%s...' % (n)
        n += 1
    print 'Done !!!'

if (__name__ == '__main__'):
    fnameIn = r'J:\#rackspace-cloud-sites\blog.raychorn.com\714455_wordpressdb.csv'
    process_records(fnameIn)
