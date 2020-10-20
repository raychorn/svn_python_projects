import os, sys
import re
import logging

from vyperlogix.misc import _utils
from vyperlogix import misc
from vyperlogix.classes.CooperativeClass import Cooperative
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc.ObjectTypeName import __typeName as ObjectTypeName__typeName
from vyperlogix.hash import lists
from vyperlogix.misc.ReportTheList import reportTheList
from vyperlogix.lists.ListWrapper import ListWrapper

csv_file_types = ['.csv']

isCSVFile = lambda f:(os.path.splitext(f)[-1].lower() in csv_file_types)

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

def asCSV(aList):
    aList = aList if (isinstance(aList,list)) else [aList]
    v = ','.join([l if (l.find(',') == -1) else '"%s"' % (l.replace('"','')) for l in aList])
    return v

def __column_split_func__(value):
    '''Returns a simple split of a value into two parts based on the whitespace that exists, returns a list of N items.'''
    return value.split()

class CSV(Cooperative):
    def __init__(self,filename='',dict2_factory=lists.HashedLists2):
        self.__header__ = []
        self.__num_headers__ = len(self.__header__)
        self.__dict2_factory__ = dict2_factory
        self.__rows__ = []
        self.__rows_dicts__ = []
        self.__by_col__ = lists.HashedLists()
        self.__row_by_col__ = self.dict2_factory()
        self.__problem_rows__ = []
        self.__isValid__ = True
        self.__filename__ = ''
        self.codec = 'UTF-8'
        if (len(filename) > 0):
            if (isCSVFile(filename)):
                self.__filename__ = filename
                self.parse()
            else:
                raise ValueError('The filename "%s" must have the file type of one of the following: %s and it does not.' % (filename,csv_file_types))

    def __str__(self):
        return '(%s)(Storing %d rows, including the header.' % (ObjectTypeName__typeName(self.__class__),len(self))

    @classmethod
    def write_as_csv(self,fname,list_of_records=[],ordering=[]):
        """
        Writes a list of records (dict objects) to a .CSV filename.
        """
        info_string = ''
        info_strings = []
        if (misc.isList(list_of_records)):
            if (len(list_of_records) > 0):
                if (all([lists.isDict(r) for r in list_of_records])):
                    header = list_of_records[0].keys()
                    if (misc.isList(ordering)) and (len(ordering) > 0):
                        header = ordering
                    s_header = ','.join(header)
                    fOut = open(fname,'w')
                    try:
                        print >>fOut, s_header
                        for rec in list_of_records:
                            l_values = []
                            for h in header:
                                l_values.append(str(rec[h]) if (str(rec[h]).find(',') == -1) else '"%s"' % (rec[h]))
                            print >>fOut, ','.join(l_values)
                    except Exception, details:
                        info_string = _utils.formattedException(details=details)
                        info_strings.append(info_string)
                    finally:
                        fOut.flush()
                        fOut.close()
                else:
                    info_string = '%s :: Expected list_of_records to contains dictionary objects however some do not.' % (ObjectTypeName.objectSignature(self))
                    info_strings.append(info_string)
            else:
                info_string = '%s :: Expected list_of_records to contains dictionary objects however list is empty.' % (ObjectTypeName.objectSignature(self))
                info_strings.append(info_string)
        else:
            info_string = '%s :: Expected list_of_records to be of type list rather than type "%s".' % (ObjectTypeName.objectSignature(self),type(list_of_records))
            info_strings.append(info_string)
        return '\n'.join(info_strings)

    def __len__(self):
        return len(self.header) + len(self.rows)

    def split_column(self,colName,colName1,colName2,split_callback=__column_split_func__):
        '''Splits the contents of colName into colName1 and colName2.
        This function has not been tested and will not handle a split that results in more than two items per split.
        It is recommended the user split the data manually.
        '''
        split_callback = split_callback if (callable(split_callback)) else __column_split_func__
        num = self.column_number_for_name(colName)
        if (num > -1):
            recs = []
            # replace the col header for column at num and insert a new column then split the data...
            for k,v in self.__by_col__.iteritems():
                if (k.lower() == colName):
                    recs = [rec for rec in self.__by_col__[k]]
                    del self.__by_col__[k]
                    _recs = [split_callback(rec) for rec in recs]
                    self.__by_col__[colName1] = [_rec[0] for _rec in _recs]
                    self.__by_col__[colName2] = [_rec[-1] for _rec in _recs]
                    d = self.__row_by_col__[k]
                    new_d = lists.HashedLists()
                    for aKey,aValue in d.iteritems():
                        _aKey = split_callback(aKey)
                        new_d[_aKey[0]] = aValue
                        new_d[_aKey[-1]] = aValue
                    del self.__row_by_col__[k]
                    self.__row_by_col__[colName1] = new_d
                    self.__row_by_col__[colName2] = new_d
            self.header[num] = colName1
            pass
        pass

    def parse(self):
        fIn = open(self.filename,'r')
        try:
            lines = [l.strip() for l in fIn.readlines()]
        finally:
            fIn.close()

        self.__header__ = [h.strip() for h in lines[0].split(',') if (len(h) > 0)]
        self.__num_headers__ = len(self.header)
        for i in xrange(0,len(self.header)):
            self.__row_by_col__[self.header[i]] = lists.HashedLists()
        _re = re.compile('"[^"\r\n]*"|[^,\r\n]*', re.MULTILINE)
        for l in lines[1:]:
            recs = [match.group().replace('"','') for match in _re.finditer(l)]
            if (len(recs) != len(self.header)):
                i = 0
                n = len(recs)
                while (i < (n-1)):
                    can_remove = (len(recs[i]) > 0) and (len(recs[i+1]) == 0)
                    if (can_remove):
                        del recs[i+1]
                        n = len(recs)
                    i += 1
            len_header = len(self.header)
            len_recs = len(recs)
            _num_missing_cols = len_header - len_recs
            if (_num_missing_cols > 0):
                _msg = '(%s.%s) :: CSV parser warning "%s", number of fields do not match the first line, padding with "MISSING" data.' % (ObjectTypeName.typeName(self),misc.funcName(),l)
                logging.warning(_msg)
                for i in xrange(0,_num_missing_cols):
                    recs.append('MISSING')
                _num_missing_cols = len(self.header) - len(recs)
                self.__problem_rows__.append(recs)
            elif (_num_missing_cols == 0):
                self.__rows__.append(recs)
                for i in xrange(0,len(self.header)):
                    self.__by_col__[self.header[i]] = recs[i]
                    self.__row_by_col__[self.header[i]][recs[i]] = recs
            elif (_num_missing_cols < 0):
                self.__rows__.append(recs)

    def column_number_for_name(self,name_or_number):
        s = str(name_or_number)
        if (s.isdigit()):
            return int(s)
        try:
            return [str(name).lower() for name in self.header].index(str(name_or_number).lower())
        except:
            return -1

    def _rowByColumn(self,key,name_or_number):
        iCol = self.column_number_for_name(name_or_number)
        nCol = self.header[iCol]
        for r in self.rows:
            if (r[iCol] == key):
                rr = self.__row_by_col__[nCol][key]
                assert len(r) == len(rr), '%s Problem with #1.' % (ObjectTypeName.objectSignature(self))
                for i in xrange(0,len(rr)):
                    assert r[i] == rr[i], '%s Problem with #2.' % (ObjectTypeName.objectSignature(self))
                return r
        return None

    def associationsBy(self,name_or_number,callback=None):
        '''Returns a dict whose keys are composed by values from name_or_number and whose values are the row'''
        d = lists.HashedLists()
        iCol = self.column_number_for_name(name_or_number)
        for row in self.rows:
            key = row[iCol]
            if (callable(callback)):
                try:
                    key = callback(key)
                except:
                    pass
            d[key] = row
        return d

    def rowsAsRecords(self,dict2_factory=None):
        '''dict2_factory is optional and specifies a class to be used when making each record.'''
        is_dict2_factory_valid = (dict2_factory is not None) and (self.dict2_factory != dict2_factory)
        if (len(self.__rows_dicts__) == 0) or (is_dict2_factory_valid):
            if (is_dict2_factory_valid):
                self.dict2_factory = dict2_factory
            for row in self.rows:
                i = 0
                headers = [[h] for h in self.header]
                for r in row:
                    try:
                        headers[i].append(r)
                        headers[i] = tuple(headers[i])
                        i += 1
                    except IndexError:
                        pass
                d = self.dict2_factory(dict(headers))
                self.__rows_dicts__.append(d)
        return self.__rows_dicts__

    def rowByColumn(self,key,name_or_number):
        iCol = self.column_number_for_name(name_or_number)
        nCol = self.header[iCol]
        item = self.__row_by_col__[nCol][key]
        return item if (not isinstance(item,list)) and (not isinstance(item,tuple)) else item[0]

    def column(self,name_or_number):
        '''Retrieve a whole column of data by name or number, the name must be a valid column header or the sero-based number must reference a valid column header.'''
        s = str(name_or_number)
        guess = self.__by_col__[s]
        if (not guess) and (s.isdigit()):
            guess = self.__by_col__[self.header[int(s)]]
        if (guess):
            return guess
        _msg = '(%s.%s) :: Cannot return data for column "%s" because this number does not match the number of columns (%d) from row #1.' % (ObjectTypeName.typeName(self),misc.funcName(),name_or_number,self.num_headers)
        logging.warning(_msg)
        raise ValueError(_msg)

    def __codec_name__(self, codec):
        try:
            return codec.__name__.lower().replace('_encode','')
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            print >>sys.stderr, info_string
        return None

    def codec():
        doc = "codec"
        def fget(self):
            try:
                return self.__codec_name__(self.__codec__)
            except Exception, details:
                info_string = _utils.formattedException(details=details)
                print >>sys.stderr, info_string
            return None
        def fset(self, codec):
            if (not misc.isString(codec)):
                codec = self.__codec_name__(self.__codec__)
            if (misc.isString(codec)):
                import codecs
                try:
                    self.__codec__ = codecs.getencoder(codec)
                except Exception, details:
                    info_string = _utils.formattedException(details=details)
                    print >>sys.stderr, info_string
        return locals()
    codec = property(**codec())

    def dict2_factory():
        doc = "dict2_factory"
        def fget(self):
            return self.__dict2_factory__
        def fset(self, dict2_factory):
            self.__dict2_factory__ = dict2_factory
        return locals()
    dict2_factory = property(**dict2_factory())

    def isValid():
        doc = "True when the CSV is considered to be valid otherwise False."
        def fget(self):
            return self.__isValid__
        def fset(self, isValid):
            self.__isValid__ = isValid
        return locals()
    isValid = property(**isValid())

    def decodeUnicode(self, aString):
        from vyperlogix.misc import decodeUnicode
        try:
            aString = aString if (isinstance(aString,str)) else str(aString)
        except:
            pass
        _aString = decodeUnicode.decodeUnicode(aString)
        return decodeUnicode.ensureOnlyPrintableChars(_aString)

    def filename():
        doc = "The csv filename."
        def fget(self):
            return self.decodeUnicode(self.__filename__)
        def fset(self, filename):
            self.__filename__ = self.decodeUnicode(filename)
            if (os.path.exists(self.__filename__)):
                self.parse()
        return locals()
    filename = property(**filename())

    def rows():
        doc = "The csv rows."
        def fget(self):
            return self.__rows__
        return locals()
    rows = property(**rows())

    def header():
        doc = "The csv header, row #1."
        def fget(self):
            return self.__header__
        return locals()
    header = property(**header())

    def num_headers():
        doc = "The number of csv headers, from row #1."
        def fget(self):
            return self.__num_headers__
        return locals()
    num_headers = property(**num_headers())

    def problem_rows():
        doc = "The rows that would not parse due to missing data."
        def fget(self):
            return self.__problem_rows__
        return locals()
    problem_rows = property(**problem_rows())

class CSV2(CSV):
    def parse(self):
        self.__header__ = None
        self.__rows_dicts__ = []

        import csv
        reader = csv.reader(open(self.filename, "rb"))
        for row in reader:
            if (self.__header__ is None):
                header = [r for r in row if (len(self.decodeUnicode(r).strip()) > 0)]
                self.__header__ = [self.decodeUnicode(h).strip() for h in header]
                self.__num_headers__ = len(self.header)
            else:
                _row = []
                header = self.header
                i = 0
                try:
                    for r in row:
                        _row.append(tuple([header[i],self.decodeUnicode(r)]))
                        i += 1
                except:
                    pass
                finally:
                    d = self.dict2_factory(dict(_row))
                    self.__rows_dicts__.append(d)

    def rowsAsRecords(self):
        return self.__rows_dicts__

class InvalidMethod(Exception):
    def __init__(self, message, Errors=None):
        Exception.__init__(self, message)
        self.Errors = Errors

class CSVgenerator(CSV):

    def rowsAsRecords(self):
        raise InvalidMethod('This method has been deprecated for this class.  Kindly use the parse method instead.')

    def __rowAsRecords__(self,row,dict2_factory=dict):
        '''dict2_factory is optional and specifies a class to be used when making each record.'''
        records = {}
        is_dict2_factory_valid = (dict2_factory is not None) and (self.dict2_factory != dict2_factory)
        if (len(self.__rows_dicts__) == 0) or (is_dict2_factory_valid):
            if (is_dict2_factory_valid):
                self.dict2_factory = dict2_factory
            if (row):
                i = 0
                headers = [[h] for h in self.header]
                for r in row:
                    try:
                        headers[i].append(r)
                        headers[i] = tuple(headers[i])
                        i += 1
                    except IndexError:
                        pass
                records = self.dict2_factory(dict(headers))
        return records

    def parse(self,dict2_factory=dict):
        '''dict2_factory is optional and specifies a class to be used when making each record.'''
        self.__header__ = None
        self.fIn = open(self.filename,'r')
        _re = re.compile('"[^"\r\n]*"|[^,\r\n]*', re.MULTILINE)
        for l in self.fIn:
            l = str(l).strip()
            if (self.__header__ is None):
                self.__header__ = [h.strip() for h in l.split(',') if (len(h) > 0)]
                self.__num_headers__ = len(self.header)
                for i in xrange(0,len(self.header)):
                    self.__row_by_col__[self.header[i]] = lists.HashedLists()
            recs = [match.group().replace('"','') for match in _re.finditer(l)]
            if (len(recs) != len(self.header)):
                i = 0
                n = len(recs)
                while (i < (n-1)):
                    can_remove = (len(recs[i]) > 0) and (len(recs[i+1]) == 0)
                    if (can_remove):
                        del recs[i+1]
                        n = len(recs)
                    i += 1
            len_header = len(self.header)
            len_recs = len(recs)
            _num_missing_cols = len_header - len_recs
            if (_num_missing_cols > 0):
                _msg = '(%s.%s) :: CSV parser warning "%s", number of fields do not match the first line, padding with "MISSING" data.' % (ObjectTypeName.typeName(self),misc.funcName(),l)
                logging.warning(_msg)
                for i in xrange(0,_num_missing_cols):
                    recs.append('MISSING')
                _num_missing_cols = len(self.header) - len(recs)
                self.__problem_rows__.append(recs)
            elif (_num_missing_cols == 0):
                for i in xrange(0,len(self.header)):
                    self.__by_col__[self.header[i]] = recs[i]
                    self.__row_by_col__[self.header[i]][recs[i]] = recs
                yield recs if (dict2_factory) else self.__rowAsRecords__(recs,dict2_factory=dict2_factory)
            elif (_num_missing_cols < 0):
                yield recs if (dict2_factory) else self.__rowAsRecords__(recs,dict2_factory=dict2_factory)
        self.fIn.close()
        
    def close(self):
        self.fIn.close()


class XLS(CSV):
    def parse(self):
        try:
            import xlrd
            book = xlrd.open_workbook(self.filename)
            sheet = book.sheets()[0]

            self.__header__ = [h.strip() for h in sheet.row_values(0,0)]
            self.__num_headers__ = len(self.header)
            for i in xrange(0,self.__num_headers__):
                self.__row_by_col__[self.header[i]] = lists.HashedLists()
            for rowNum in xrange(1,sheet._dimnrows):
                try:
                    recs = sheet.row_values(rowNum,0)
                    self.__rows__.append(recs)
                    for i in xrange(0,self.__num_headers__):
                        self.__by_col__[self.header[i]] = recs[i]
                        self.__row_by_col__[self.header[i]][recs[i]] = recs
                except:
                    pass
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            print >>sys.stderr, info_string

class XLS2(XLS):
    def decode_and_strip(self,aString):
        if (isinstance(aString,unicode)):
            fr_encoding = self.reader.__book__.encoding
            try:
                #s = aString.decode(fr_encoding)
                s = aString.encode(fr_encoding)
                s = s.encode(self.codec, "xmlcharrefreplace").strip()
                return s
            except UnicodeEncodeError, details:
                #_details = str(details)
                #toks = ListWrapper(_details.split("'"))
                #i = toks.findFirstContaining('\\x')
                #if (i > -1):
                    #pass
                info_string = _utils.formattedException(details=details)
                print >>sys.stderr, info_string
        else:
            s = str(aString).strip()
        return s.encode(self.codec)

    def parse(self):
        try:
            from vyperlogix.xlrd import excelReader

            decode_and_strip = lambda aString:self.decode_and_strip(aString)

            self.__header__ = None
            self.__rows_dicts__ = []

            self.__reader__ = reader = excelReader.readexcel(self.filename)
            self.__sheets__ = sheets = reader.worksheets()
            for sheet in sheets:
                for row in reader.getiter(sheet):
                    if (self.__header__ is None):
                        self.__header__ = [decode_and_strip(h) for h in row if (len(decode_and_strip(h)) > 0)]
                        self.__num_headers__ = len(self.header)
                    else:
                        header = self.header
                        _row = {}
                        for k,v in row.iteritems():
                            if (v is None):
                                row[k] = ''
                            try:
                                _k = decode_and_strip(k)
                            except UnicodeEncodeError, details:
                                info_string = _utils.formattedException(details=details)
                                print >>sys.stderr, info_string
                            try:
                                _v = decode_and_strip(v)
                            except UnicodeEncodeError, details:
                                info_string = _utils.formattedException(details=details)
                                print >>sys.stderr, info_string
                            _row[_k] = _v
                        d = self.dict2_factory(_row)
                        self.__rows_dicts__.append(d)
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            print >>sys.stderr, info_string

    def rowsAsRecords(self):
        return self.__rows_dicts__

    def reader():
        doc = "XLS reader."
        def fget(self):
            return self.__reader__
        return locals()
    reader = property(**reader())

    def sheets():
        doc = "XLS sheets as in worksheets."
        def fget(self):
            return self.__sheets__
        return locals()
    sheets = property(**sheets())