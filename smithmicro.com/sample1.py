import datetime
from mx import DateTime
from dbfpy import dbf

if (__name__ == '__main__'):
    db = dbf.Dbf("J:\\@SmithMicro.Com\\FCC Data\\am\\am.dbf")
    print '='*30
    for rec in db:
        print '-'*30
        print rec
        print '-'*30
        print 
    print '='*30
