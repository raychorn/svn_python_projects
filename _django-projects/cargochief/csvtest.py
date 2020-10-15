from vyperlogix.misc import _utils
from vyperlogix.parsers.CSV import CSV

def process_records(fnameIn,fnameOut):
    from vyperlogix.parsers.CSV import CSV
    print 'Reading %s...' % (fnameIn)
    reader = CSV(filename=fnameIn)
    records = reader.rowsAsRecords()
    ioBuf = _utils.stringIO()
    print >> ioBuf, '<root>'
    n = 1
    m = len(records)
    print 'Writing %s records...' % (m)
    for aRec in records:
        print >> ioBuf, '<node>'
        for k,v in aRec.iteritems():
            print >> ioBuf, '<%s>%s</%s>' % (k,v,k)
        print >> ioBuf, '</node>'
        print 'Writing record #%s of %s...' % (n,m)
        n += 1
    print >> ioBuf, '</root>'
    _utils.writeFileFrom(fnameOut,ioBuf.getvalue())
    print 'Done !!!'

if (__name__ == '__main__'):
    fnameIn = r'J:\@Cargo Chief\trunk\trunk\db\data\cities.csv'
    fnameOut = r'J:\@Cargo Chief\trunk\trunk\db\data\cities.xml'
    process_records(fnameIn,fnameOut)

