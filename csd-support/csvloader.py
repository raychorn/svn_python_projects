__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

                   All Rights Reserved.

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

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.parsers.CSV import CSV

from vyperlogix.enum.Enum import Enum

class Tables(Enum):
    nothing = 0
    Tblinterpreters = 2^1
    Tbllanguages = 2^2
    Tblinterplang = 2^3
    tblScheduleAssignments = 2^4
    tblSchedStatus = 2^5
    tblPersonalSched = 2^6
    tblServicesFor = 2^7

def process_records(fnameIn,fnameOut,choice=Tables.nothing):
    from vyperlogix.parsers.CSV import CSV
    print 'Reading %s...' % (fnameIn)
    reader = CSV(filename=fnameIn)
    records = reader.rowsAsRecords()
    ioBuf = _utils.stringIO()
    n = 1
    m = len(records)
    print 'Writing %s records...' % (m)
    for aRec in records:
        items = []
        for k,v in aRec.iteritems():
            if (v is None):
                continue
            v = str(v)
            if (len(v) == 0):
                continue
            if (choice == Tables.Tblinterpreters):
                if (k in ['interpreterid']):
                    continue
            if (choice == Tables.Tbllanguages):
                if (k in ['id']):
                    continue
            quote = "'" if (v.find("'") == -1) else '"'
            items.append(":%s => %s%s%s" % (k,quote,_utils.ascii_only(str(v)),quote))
        if (choice == Tables.Tblinterpreters):
            print >> ioBuf, "interp = Tblinterpreters.new(%s)" % (','.join(items))
            print >> ioBuf, 'interp.save'
            print >> ioBuf, ''
        elif (choice == Tables.Tbllanguages):
            print >> ioBuf, "lang = Tbllanguages.new(%s)" % (','.join(items))
            print >> ioBuf, 'lang.save'
            print >> ioBuf, ''
        elif (choice == Tables.Tblinterplang):
            print >> ioBuf, "assoc = Tblinterplang.new(%s)" % (','.join(items))
            print >> ioBuf, 'assoc.save'
            print >> ioBuf, ''
        elif (choice == Tables.tblScheduleAssignments):
            print >> ioBuf, "assign = Tblscheduleassignments.new(%s)" % (','.join(items))
            print >> ioBuf, 'assign.save'
            print >> ioBuf, ''
        elif (choice == Tables.tblSchedStatus):
            print >> ioBuf, "status = Tblschedstatus.new(%s)" % (','.join(items))
            print >> ioBuf, 'status.save'
            print >> ioBuf, ''
        elif (choice == Tables.tblPersonalSched):
            print >> ioBuf, "sched = Tblpersonalsched.new(%s)" % (','.join(items))
            print >> ioBuf, 'sched.save'
            print >> ioBuf, ''
        elif (choice == Tables.tblServicesFor):
            print >> ioBuf, "serv = Tblservicesfor.new(%s)" % (','.join(items))
            print >> ioBuf, 'serv.save'
            print >> ioBuf, ''
        
        print 'Writing record #%s of %s...' % (n,m)
        n += 1
    print >> ioBuf, 'puts "DB DATA IMPORT SUCCESSFUL for %s"' % (choice.name)
    _utils.writeFileFrom(fnameOut,ioBuf.getvalue())
    print 'Done !!!'

if (__name__ == '__main__'):
    fnameIn = r'J:\@Vyper Logix Corp\@Projects\python-projects\csd-support\tblInterpreters.csv'
    fnameOut = r'J:\@Vyper Logix Corp\@Projects\python-projects\csd-support\seeds-tblInterpreters.rb'
    process_records(fnameIn,fnameOut,Tables.Tblinterpreters)

    fnameIn = r'J:\@Vyper Logix Corp\@Projects\python-projects\csd-support\tblLanguages.csv'
    fnameOut = r'J:\@Vyper Logix Corp\@Projects\python-projects\csd-support\seeds-tblLanguages.rb'
    process_records(fnameIn,fnameOut,Tables.Tbllanguages)

    fnameIn = r'J:\@Vyper Logix Corp\@Projects\python-projects\csd-support\tblInterpLang.csv'
    fnameOut = r'J:\@Vyper Logix Corp\@Projects\python-projects\csd-support\seeds-tblInterpLang.rb'
    process_records(fnameIn,fnameOut,Tables.Tblinterplang)

    fnameIn = r'J:\@Vyper Logix Corp\@Projects\python-projects\csd-support\tblScheduleAssignments.csv'
    fnameOut = r'J:\@Vyper Logix Corp\@Projects\python-projects\csd-support\seeds-tblScheduleAssignments.rb'
    process_records(fnameIn,fnameOut,Tables.tblScheduleAssignments)
    
    fnameIn = r'J:\@Vyper Logix Corp\@Projects\python-projects\csd-support\tblSchedStatus.csv'
    fnameOut = r'J:\@Vyper Logix Corp\@Projects\python-projects\csd-support\seeds-tblSchedStatus.rb'
    process_records(fnameIn,fnameOut,Tables.tblSchedStatus)
    
    fnameIn = r'J:\@Vyper Logix Corp\@Projects\python-projects\csd-support\tblPersonalSched.csv'
    fnameOut = r'J:\@Vyper Logix Corp\@Projects\python-projects\csd-support\seeds-tblPersonalSched.rb'
    process_records(fnameIn,fnameOut,Tables.tblPersonalSched)

    fnameIn = r'J:\@Vyper Logix Corp\@Projects\python-projects\csd-support\tblServicesFor.csv'
    fnameOut = r'J:\@Vyper Logix Corp\@Projects\python-projects\csd-support\seeds-tblServicesFor.rb'
    process_records(fnameIn,fnameOut,Tables.tblServicesFor)
