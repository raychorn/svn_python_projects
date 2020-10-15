import sys
import logging
import types

from vyperlogix.classes import CooperativeClass
from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc.ObjectTypeName import __typeName as ObjectTypeName__typeName

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
get = lambda source,key,default:source[key] if (source[key] is not None) else default

def isDict(foo):
    bool = False
    try:
        bool = (foo.iteritems != None)
    except:
        pass
    return bool

def can_asDict(foo):
    bool = False
    try:
        bool = (callable(foo.asDict))
    except:
        pass
    return bool

def copyAsDict(obj):
    if (isDict(obj)):
        d = HashedLists2()
        for k,v in obj.iteritems():
            d[k] = '' if (v is None) else str(v)
        return d
    return obj

def asDict(__dict__,insideOut=False,isCopy=False):
    cl = ObjectTypeName.typeClassName(__dict__)
    clName = cl.split('.')[-1]
    dObj = {} if (not isCopy) else eval('%s()' % (clName))
    for k,v in __dict__.iteritems():
        if (insideOut):
            if (isinstance(v,list)):
                for item in v:
                    if (not callable(item)) and (not isDict(item)):
                        dObj[item] = k
            else:
                if (not callable(v)) and (not isDict(v)):
                    dObj[v] = k
        else:
            if (not callable(v)):
                try:
                    if ((callable(v.asDict))):
                        v = v.asDict(isCopy=isCopy,insideOut=insideOut)
                except:
                    pass
                dObj[k] = v
            elif (misc.isList(v)):
                for _i_ in xrange(0,len(v)):
                    if ((callable(v[_i_].asDict))):
                        v[_i_] = v[_i_].asDict(isCopy=isCopy,insideOut=insideOut)
    return dObj

def asJSONSerializable(__dict__):
    def asJSON(vv):
        return misc._unpack_([asJSONSerializable(_vv) for _vv in vv]) if (misc.isList(vv)) else vv
    try:
        iterable = __dict__
        is_or_has_dict = False
        if (isDict(__dict__)):
            is_or_has_dict = True
            iterable = __dict__
        else:
            try:
                __dict__.__dict__
                is_or_has_dict = True
                iterable = __dict__.__dict__
            except:
                pass
        if (is_or_has_dict):
            dObj = {}
            for k,v in iterable.iteritems():
                if (not callable(v)):
                    try:
                        if (isDict(v)) or (isDict(v.__dict__)):
                            dObj[k] = asJSONSerializable(v)
                        else:
                            dObj[k] = asJSON(v)
                    except AttributeError:
                        dObj[k] = asJSON(v)
        elif (misc.isList(iterable)):
            dObj = []
            for v in iterable:
                if (not callable(v)):
                    try:
                        if (isDict(v)) or (isDict(v.__dict__)):
                            dObj.append(asJSONSerializable(v))
                        else:
                            dObj.append(asJSON(v))
                    except AttributeError:
                        dObj.append(asJSON(v))
        else:
            return iterable
    except:
        pass
    return dObj

def prettyPrint(item,prefix='',title='',tab_width=4,delay_end=False,asCSV=False,isHorizontal=False,csv_callback=None,fOut=sys.stdout):
    import types
    from vyperlogix.misc import ReportTheList

    _type_name = ObjectTypeName._typeName(item.__class__)
    ret = []
    try:
        if (isDict(item)):
            tab_width = 4 if (not str(tab_width).isdigit()) else tab_width
            if (asCSV):
                if (isHorizontal):
                    print >>fOut, '%s' % (misc.asCSV(item.keys()))
                    print >>fOut, '%s' % (misc.asCSV(item.values()))
                    print >>fOut, ''
                else:
                    isCallback = ( (csv_callback) and (callable(csv_callback)) )
                    i = 1
                    for kk,vv in item.iteritems():
                        l = [i,kk,vv]
                        if (isCallback):
                            try:
                                l = csv_callback(l)
                            except:
                                pass
                        print >>fOut, '%s' % (misc.asCSV(l))
                        i += 1
            else:
                l_keys = [len(kk) for kk,vv in item.iteritems()]
                if (len(l_keys) > 0):
                    max_len = misc.sort(l_keys)[-1]
                    print >>fOut, '%sBEGIN: %s (%d items)' % (prefix,title,len(item))
                    i = 1
                    for kk,vv in item.iteritems():
                        i_s_len = int(len(kk)/tab_width)
                        i_s_len = 1 if (i_s_len == 0) else i_s_len
                        i_spaces = (int(max_len/tab_width) - i_s_len) -1
                        if (isinstance(vv,tuple)):
                            vv = list(vv)
                        if (isinstance(vv,list)):
                            print >>fOut, '(%s' % ('-'*40)
                            ReportTheList.reportTheList(vv,title='%d :: (%s) %s' % (i,kk,title),fOut=fOut)
                            print >>fOut, ')%s' % ('-'*40)
                            print >>fOut, ''
                        elif (isDict(vv)):
                            print >>fOut, '{%s' % ('-'*40)
                            prettyPrint(vv,'\t\t',title='%d :: (%s) %s' % (i,kk,title),fOut=fOut)
                            print >>fOut, '}%s' % ('-'*40)
                            print >>fOut, ''
                        else:
                            try:
                                print >>fOut, '%s\t\t%d :: %s%s-->%s' % (prefix,i,kk,'\t'*i_spaces,vv)
                            except:
                                pass
                        i += 1
                    _end_msg = '%sEND! %s from %s' % (prefix,title,_type_name)
                    if (not delay_end):
                        print >>fOut, _end_msg
                        print >>fOut, ''
                    else:
                        ret.append(_end_msg)
                        ret.append('')
                else:
                    logging.warning('(%s) :: Unable to process the object passed to this function due to lack of data.' % (misc.funcName()))
        else:
            logging.warning('(%s) :: Unable to process the object passed to this function because it is of type "%s" and a dictionary object was expected.' % (misc.funcName(),_type_name))
    except Exception, details:
        info_string = misc.formattedException(details=details)
        print >>sys.stderr, info_string
    return ret

def _prettyPrint(item,prefix='',title='',tab_width=4,delay_end=False,fOut=sys.stdout):
    prettyPrint(item,prefix=prefix,title=title,tab_width=tab_width,delay_end=delay_end,fOut=fOut)

class UnicodeMixin(CooperativeClass.Cooperative):
    def encode(self,codec_name):
        '''encodes the contents of the object using the named codec'''
        if (isDict(self)):
            for k,v in self.iteritems():
                self[k] = v.encode(codec_name)
        elif (isinstance(self,list)):
            for i in xrange(len(self)):
                self[i] = self[i].encode(codec_name)
        elif (misc.isString(self)):
            self = self.encode(codec_name)
        else:
            self = str(self).encode(codec_name)

class HashedLists(UnicodeMixin, CooperativeClass.Cooperative):
    def __init__(self,fromDict={},caseless=False):
        self.__dict = {}
        self.__caseless__ = caseless
        self.__make_key__ = lambda key:str(key) if (not caseless) else str(key).lower()
        if (isinstance(fromDict,list)):
            self.fromListOfPairs(fromDict)
        else:
            try:
                if (fromDict.keys()) and (fromDict.values()):
                    self.fromDict(fromDict)
            except Exception, details:
                info_string = misc.formattedException(details=details)
                print >>sys.stderr, info_string

    def __repr__(self):
        return '(%s) storing %d keys.' % (ObjectTypeName__typeName(self),len(self.keys()))

    def prettyPrint(self,prefix='',title='',tab_width=4,delay_end=False,fOut=sys.stdout):
        _prettyPrint(self,prefix='',title='',tab_width=4,delay_end=delay_end,fOut=fOut)

    def fromDict(self, d):
        try:
            if (d.keys()) and (d.values()):
                for k,v in d.iteritems():
                    try:
                        if (v.keys()) and (v.values()):
                            cc = '%s()' % ObjectTypeName.typeName(self).split('.')[-1]
                            new_d = eval(cc)
                            new_d.fromDict(v)
                            self[k] = new_d
                    except:
                        if (isinstance(v,list)):
                            for item in v:
                                self[k] = item
                        else:
                            self[k] = v
        except:
            pass
        return self

    def fromListOfPairs(self,l_pairs):
        '''l_pairs is a list of pairs of values where the first value is the key and the next value is the value.'''
        for i in xrange(0,len(l_pairs),2):
            self[l_pairs[i]] = l_pairs[i+1]
        return self

    def asDict(self,insideOut=False,isCopy=False):
        return asDict(self,insideOut=insideOut,isCopy=isCopy)
    
    def asJSONSerializable(self,insideOut=False):
        return asJSONSerializable(self)

    def invert(self):
        return asDict(self,insideOut=True,isCopy=True)

    def insideOut(self):
        return asDict(self,insideOut=True,isCopy=True)

    #def invert(self):
        #return dict(zip(*zip(*self.items())[::-1]))
    
    def items(self):
        return ((k,v) for k,v in self.iteritems())

    def fileName():
        doc = "fileName"
        def fget(self):
            return ObjectTypeName.typeClassName(self)
        return locals()
    fileName = property(**fileName())

    def diff(self, other):
        d = {}
        for k,v in other.iteritems():
            key = self.__make_key__(k)
            if (self[key] != v):
                d[key] = v
        return d

    def __add__(self, other):
        for k,v in other.iteritems():
            self[self.__make_key__(k)] = v
        return self

    def __iadd__(self, other):
        self.__add__(other)
        return self

    def sortedKeys(self):
        return misc.sort(self.keys())

    def get(self,key, default):
        v = self.__dict[key] if (self.__dict.has_key(key)) else None
        if (v is not None):
            return v
        return default

    def __getitem__(self, key):
        _key = self.__make_key__(key)
        return self.__dict[_key] if (self.__dict.has_key(_key)) else None

    def __setitem__(self, key, value):
        _key = self.__make_key__(key)
        if (self.has_key(_key)) and (value == None):
            self.__delitem__(_key)
        elif (value != None):
            if (not self.__dict.has_key(_key)):
                self.__dict[_key] = []
            bucket = self.__dict[_key]
            bucket.append(value)
            self.__dict[_key] = bucket

    def __delitem__(self, key):
        _key = self.__make_key__(key)
        del self.__dict[_key]

    def pretty(self,delim=''):
        return ('{%s' % (delim))+(',%s' % (delim)).join(["'%s':%s%s%s" % (k,"'" if (not str(self[k]).isdigit()) else "",str(self[k]).replace("'",""),"'" if (not str(self[k]).isdigit()) else "") for k in self.keys()])+('%s}' % (delim))
    
    def __str__(self):
        return '(%s)%s' % (ObjectTypeName__typeName(self),self.pretty())

    def __len__(self):
        return len(self.keys())

    def length(self):
        n = 0
        for k,v in self.iteritems():
            n += len(v)
        return n

    def has_key(self, key):
        return self.__dict.has_key(self.__make_key__(key))

    def keys(self):
        return self.__dict.keys()

    def values(self):
        return self.__dict.values()

    def iteritems(self):
        return ((k,self.__getitem__(k)) for k in self.keys())

    def caseless():
        doc = "caseless flag, True if case is not used for keys otherwise False if case is used."
        def fget(self):
            return self.__caseless__
        def fset(self,isCaseless):
            self.__caseless__ = isCaseless if (isinstance(isCaseless,bool)) else False
        return locals()
    caseless = property(**caseless())

    def represent(self,level=0,output=False):
        s = []
        _indent = '\t'*level
        for k,v in self.iteritems():
            s.append('%s%s = ' % (_indent,k))
            if (isDict(v)):
                t = represent(v,level+1)
                s += t.split('\n')
            elif (isinstance(v,list)):
                for i in v:
                    if (isDict(i)):
                        t = represent(i,level+1)
                        s += t.split('\n')
                    else:
                        s[-1] = s[-1]+'"%s"' % (i)
            else:
                s[-1] = s[-1]+'"%s"' % (v)
        if (output):
            print '\n'.join(s)
        return '\n'.join(s)

class HashedLists2(HashedLists):
    def __getitem__(self, key):
        return super(HashedLists2, self).__getitem__(key)[0] if (super(HashedLists2, self).has_key(key)) else None

    def __setitem__(self, key, value):
        if (super(HashedLists2, self).has_key(key)):
            super(HashedLists2, self).__delitem__(key)
        super(HashedLists2, self).__setitem__(key,value)

class HashedUniqueLists(HashedLists):
    def __setitem__(self, key, value):
        super(HashedUniqueLists, self).__setitem__(key,value)
        items = self.__getitem__(key)
        if (items is not None):
            items = list(set(items))
            self.__delitem__(key)
            for item in items:
                super(HashedUniqueLists, self).__setitem__(key,item)

class HashedFuzzyLists(HashedLists):
    def __init__(self,d={},caseless=True):
        super(HashedFuzzyLists, self).__init__(fromDict=d,caseless=caseless)

    def __getitem__(self, key):
        lower = lambda value:value.lower() if (misc.isString(value)) else value
        _key = lower(key)
        for k in self.keys():
            if (lower(k) == _key):
                val = super(HashedFuzzyLists, self).__getitem__(k)
                return val
        return None

class HashedFuzzySmartLists(HashedFuzzyLists):
    def __init__(self,d={},caseless=True):
        super(HashedFuzzySmartLists, self).__init__(d=d,caseless=caseless)

class HashedFuzzyLists2(HashedLists2):
    def __init__(self,d={},caseless=True):
        super(HashedFuzzyLists2, self).__init__(fromDict=d,caseless=caseless)

    def __getitem__(self, key):
        _key = key.lower()
        for k in self.keys():
            if (k.lower() == _key):
                val = super(HashedFuzzyLists2, self).__getitem__(k)
                return val if (not isinstance(val,list)) else val[0]
        return None

class HashedOrderedList(HashedLists2):
    '''Takes a list of tuple items and makes an Ordered Dictionary from them.'''
    def __init__(self,fromTupleList=[]):
        self.__list = fromTupleList
        d = {}
        for item in self.__list:
            d[item[0]] = item[-1]
        super(HashedOrderedList, self).__init__(d)

    def keys(self):
        return [n[0] for n in self.__list]

    def values(self):
        return [n[-1] for n in self.__list]

    def length(self):
        return len(self.keys())
