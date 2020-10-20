"""
A simple class to represent a Quicken (QIF) file, and a parser to
load a QIF file into a sequence of those classes.

It's enough to be useful for writing conversions.
"""

import os
import sys
from vyperlogix import misc
from vyperlogix.classes import CooperativeClass
from vyperlogix.gds import julian
from vyperlogix.oodb import *
from vyperlogix.money import floatValue

const_money_symbol = 'money'
 
__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

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

class QifItem(CooperativeClass.Cooperative):
    def __init__(self,s=None):
        self.__date = None
        self.__julianDate = None
        self.__mm = None
        self.__dd = None
        self.__yyyy = None
        self.__amount = None
        self.cleared = None
        self.num = None
        self.payee = None
        self.memo = None
        self.checkNumber = None
        self.address = None
        self.category = None
        self.categoryInSplit = None
        self.memoInSplit = None
        self.amountOfSplit = None
        if (misc.isString(s)):
            toks = s.split('::')
            cname = fullClassName(self)
            if (toks[0] == cname):
                _cname = terseClassName(cname)
                _parms = [p.split('=') for p in toks[-1].split('|')]
                for p in _parms:
                    if (p[0].startswith('__')):
                        p[0] = '_%s%s' % (_cname,p[0])
                    v = p[-1]
                    if (p[0] == 'amount'):
                        v = floatValue.floatValue(p[-1],floatValue.Options.asDollar)
                    self.__dict__[p[0]] = v
                pass
            else:
                print 'ERROR :: Invalid object spec "%s".  The expected class name is "%s" however this class name was not detected in the object spec that was passed into this function.' % (s,cname)
            pass
        self.order = self.__dict__.keys()
        
    def show(self):
        pass
    
    def __repr__(self):
        _className = fullClassName(self)
        __className = terseClassName(_className)
        _fields = self.__dict__.keys()
        _fields.sort()
        tmpstring = '|'.join( ['%s=%s' % (field.replace('_%s' % __className,''),str(self.__dict__[field]).replace('|',' ')) for field in _fields if field != 'order' and self.__dict__[field]])
        tmpstring = tmpstring.replace('None', '')
        return '%s::%s' % (_className,tmpstring)
    
    def pretty(self):
        _className = fullClassName(self)
        __className = terseClassName(_className)
        _fields = self.__dict__.keys()
        _fields.sort()
        tmpstring = '\n\t'.join( ['%s=%s' % (field.replace('_%s' % __className,''),str(self.__dict__[field]).replace('|',' ')) for field in _fields if field != 'order' and self.__dict__[field]])
        tmpstring = tmpstring.replace('None', '')
        return '%s::%s\n' % (_className,tmpstring)
    
    def parseDate(self,dt):
        if (misc.isString(dt)):
            toks = dt.split('/')
            if (len(toks) == 1):
                toks = dt.split('-')
            if (len(toks) == 2):
                _toks = toks[-1].split("'")
                del toks[-1]
                for t in _toks:
                    toks.append(t)
            dt = toks
        return dt
    
    def set_amount(self,value):
        self.__amount = floatValue.floatValue(str(value),floatValue.Options.asDollar)
    
    def get_amount(self):
        val = '%10.2f' % self.__amount
        return val.strip()
    
    def get_date(self):
        return self.parseDate(self.__date)
    
    def get_mm(self):
        return self.__mm
    
    def get_dd(self):
        return self.__dd
    
    def get_yyyy(self):
        return self.__yyyy
    
    def set_yyyy(self,yyyy):
        self.__yyyy = yyyy
    
    def set_date(self,dt):
        if (misc.isList(dt)):
            dt = '/'.join([str(n) for n in dt])
        self.__date = [int(n) if misc.isString(n) else n for n in self.parseDate(dt)]
        self.__mm,self.__dd,self.__yyyy = self.__date
        self.__julianDate = julian.Julian(self.__mm,self.__dd,self.__yyyy)
        
    def get_julianDate(self):
        return self.__julianDate if self.__julianDate else 0.0

    def dataString(self):
        """
        Returns the data of this QIF without a header row
        """
        tmpstring = ','.join( [str(self.__dict__[field]) for field in self.order] )
        tmpstring = tmpstring.replace('None', '')
        return tmpstring
    
    date = property(get_date,set_date)
    julianDate = property(get_julianDate)
    mm = property(get_mm)
    dd = property(get_dd)
    yyyy = property(get_yyyy,set_yyyy)
    amount = property(get_amount, set_amount)

class QifReader(CooperativeClass.Cooperative):
    def __init__(self,fname=None,dateSpec=None):
        self.__items = []
        self.fileName = fname if (misc.isString(fname)) and (os.path.exists(fname)) else 'Z:/#zDisk/#IRS/Microsoft Money (1996-2007).qif'
        self.dateSpec = dateSpec
        if (self.dateSpec):
            if (misc.isList(self.dateSpec)):
                if (len(self.dateSpec) >= 1):
                    if (misc.isString(self.dateSpec[0])):
                        self.dateSpec[0] = self.dateSpecToFloat(self.dateSpec[0])
                if (len(self.dateSpec) > 1):
                    if (misc.isString(self.dateSpec[-1])):
                        self.dateSpec[-1] = self.dateSpecToFloat(self.dateSpec[-1])
            elif (misc.isString(self.dateSpec)):
                self.dateSpec = [self.dateSpecToFloat(self.dateSpec)]
            else:
                self.dateSpec = [self.dateSpec]

    def __repr__(self):
        return '(%s) from "%s".' % str(self.__class__,self.fileName)
    
    def get_items(self):
        if (len(self.__items) == 0):
            if (os.path.exists(self.fileName)):
                fHand = open(self.fileName,'r')
                self.__items = self.parseQif(fHand)
                fHand.close()
            else:
                self.__items = self.parseQif(self.fileName)
        return self.__items
    
    def get_filepath(self):
        return os.path.dirname(self.fileName)
    
    def getDatabaseFileNameFor(self,yyyy):
        toks = self.fileName.split('.')
        if (misc.isString(yyyy)):
            toks[0] += '_%s' % yyyy
        else:
            toks[0] += '_%d' % yyyy
        toks[-1] = 'db'
        fname = '.'.join(toks)
        dname = os.sep.join([self.filepath,const_money_symbol])
        bname = os.path.basename(fname)
        fname = os.sep.join([dname,bname])
        if (not os.path.exists(dname)):
            os.mkdir(dname)
        return fname
    
    def get_databases(self):
        toks = self.fileName.split('.')
        fname = toks[0]+'_'
        dname = os.sep.join([self.filepath,const_money_symbol])
        if (not os.path.exists(dname)):
            os.mkdir(dname)
        return [f for f in os.listdir(dname) if (f.find(fname) > -1) and f.endswith('.db')]
    
    def parseDate(self,dt):
        toks = dt.split('/')
        if (len(toks) == 1):
            toks = dt.split('-')
        if (len(toks) == 2):
            _toks = toks[-1].split("'")
            del toks[-1]
            for t in _toks:
                toks.append(t)
        return toks
    
    def dateSpecToFloat(self,date_or_toks):
        _date = 0.0
        toks = date_or_toks
        if (misc.isString(date_or_toks)):
            toks = self.parseDate(date_or_toks)
        if (len(toks) == 3):
            _date = julian.Julian(int(toks[0]),int(toks[1]),int(toks[2]))
        return _date

    def parseQif(self,infile):
        """
        Parse a qif file and return a list of entries.
        infile should be open file-like object (supporting readline() ).
        """
    
        inItem = False
        
        items = []
        curItem = QifItem()
        curRecord = []
        line = infile.readline()
        while line != '':
            curRecord.append(line)
            if line[0] == '\n': # blank line
                pass
            elif line[0] == '^': # end of item
                # save the item
                if (isWithinDateSpec):
                    items.append(curItem)
                curItem = QifItem()
                curRecord = []
            elif line[0] == 'D':
                isWithinDateSpec = True
                curItem.date = line[1:-1]
                mm,dd,yyyy = curItem.date
                if ( (mm == 2) and (dd == 23) and (yyyy == 2005) ):
                    pass
                if (self.dateSpec):
                    if (len(self.dateSpec) == 1):
                        isWithinDateSpec = curItem.julianDate >= self.dateSpec[0]
                    else:
                        isWithinDateSpec = (curItem.julianDate >= self.dateSpec[0]) and (curItem.julianDate <= self.dateSpec[-1])
            elif line[0] == 'T':
                curItem.amount = line[1:-1]
            elif line[0] == 'C':
                curItem.cleared = line[1:-1]
            elif line[0] == 'P':
                curItem.payee = line[1:-1]
            elif line[0] == 'M':
                curItem.memo = line[1:-1]
            elif line[0] == 'A':
                curItem.address = line[1:-1]
            elif line[0] == 'L':
                curItem.category = line[1:-1]
            elif line[0] == 'N':
                curItem.checkNumber = int(line[1:-1].strip())
                if (curItem.checkNumber == 5254):
                    pass
            elif line[0] == 'S':
                try:
                    curItem.categoryInSplit.append(";" + line[1:-1])
                except AttributeError:
                    curItem.categoryInSplit = line[1:-1]
            elif line[0] == 'E':
                try:
                    curItem.memoInSplit.append(";" + line[1:-1])
                except AttributeError:
                    curItem.memoInSplit = line[1:-1]
            elif line[0] == '$':
                try:
                    curItem.amountInSplit.append(";" + line[1:-1])
                except AttributeError:
                    curItem.amountInSplit = line[1:-1]
            else:
                # don't recognise this line; make it a memo as a series of memo items
                bucket = line.split()
                if (len(bucket) == 1):
                    bucket = bucket[0]
                if ( (bucket != None) and(bucket[0] == 'N') and (bucket[1:].isdigit()) ):
                    curItem.checkNumber = int(bucket[1:])
                    if (curItem.checkNumber == 5254):
                        pass
                else:
                    if ( (curItem.memo) and (misc.isString(curItem.memo)) ):
                        curItem.memo = [curItem.memo,bucket]
                    elif (misc.isList(curItem.memo)):
                        curItem.memo.apend(bucket)
                    else:
                        curItem.memo = bucket
    
            line = infile.readline()
        return items
    
    items = property(get_items)
    filepath = property(get_filepath)
    databases = property(get_databases)
    
if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

    import _psyco
    _psyco.importPsycoIfPossible()
    # read from stdin and write CSV to stdout
    fname = 'Z:/#zDisk/#IRS/Microsoft Money (1996-2007).qif'
    qif = QifReader(fname,['1/1/2006','12/31/2006'])
    _items = qif.items[0:1000]
    print repr(_items[0])
    for item in _items[1:]:
        print item.dataString()

