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

import os
import sys
import uuid
__has_bsddb = False
try:
    import bsddb
    __has_bsddb = True
except ImportError:
    pass
try:
    import shelve
except ImportError:
    pass
try:
    import marshal
except ImportError:
    pass
try:
    import pylzma
except ImportError:
    pass
import types
import struct
import re

from struct import pack, unpack
import zlib

from vyperlogix.hash.lists import HashedLists
from vyperlogix.hash.lists import HashedLists2
try:
    from pyax.datatype.apexdatetime import ApexDatetime
except ImportError:
    from datetime import datetime as ApexDatetime
import traceback
from vyperlogix.enum.Enum import *
from vyperlogix.classes import CooperativeClass
from vyperlogix.misc import _utils
from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc.ObjectTypeName import __typeName as ObjectTypeName__typeName
from vyperlogix.hash import lists

from vyperlogix import cerealizer

try:
    from cPickle import Pickler, Unpickler
except ImportError:
    from pickle import Pickler, Unpickler

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

dbx_name = lambda name,data_path:os.sep.join([data_path,'.'.join([os.path.basename(name.split('.')[0]),'dbx'])])

def crypt(key,data,iv='\00\00\00\00\00\00\00\00',n=32):
    """
        Encrypt/decrypt variable length string using XTEA cypher as
        key generator (OFB mode)
        * key = 128 bit (16 char) 
        * iv = 64 bit (8 char)
        * data = string (any length)

        >>> import os
        >>> key = os.urandom(16)
        >>> iv = os.urandom(8)
        >>> data = os.urandom(10000)
        >>> z = crypt(key,data,iv)
        >>> crypt(key,z,iv) == data
        True

    """
    def keygen(key,iv,n):
        while True:
            iv = xtea_encrypt(key,iv,n)
            for k in iv:
                yield ord(k)
    xor = [ chr(x^y) for (x,y) in zip(map(ord,data),keygen(key,iv,n)) ]
    return "".join(xor)

def xtea_encrypt(key,block,n=32,endian="!"):
    """
        Encrypt 64 bit data block using XTEA block cypher
        * key = 128 bit (16 char) 
        * block = 64 bit (8 char)
        * n = rounds (default 32)
        * endian = byte order (see 'struct' doc - default big/network) 

        >>> z = xtea_encrypt('0123456789012345','ABCDEFGH')
        >>> z.encode('hex')
        'b67c01662ff6964a'

        Only need to change byte order if sending/receiving from 
        alternative endian implementation 

        >>> z = xtea_encrypt('0123456789012345','ABCDEFGH',endian="<")
        >>> z.encode('hex')
        'ea0c3d7c1c22557f'

    """
    v0,v1 = struct.unpack(endian+"2L",block)
    k = struct.unpack(endian+"4L",key)
    sum,delta,mask = 0L,0x9e3779b9L,0xffffffffL
    for round in range(n):
        v0 = (v0 + (((v1<<4 ^ v1>>5) + v1) ^ (sum + k[sum & 3]))) & mask
        sum = (sum + delta) & mask
        v1 = (v1 + (((v0<<4 ^ v0>>5) + v0) ^ (sum + k[sum>>11 & 3]))) & mask
    return struct.pack(endian+"2L",v0,v1)

def xtea_decrypt(key,block,n=32,endian="!"):
    """
        Decrypt 64 bit data block using XTEA block cypher
        * key = 128 bit (16 char) 
        * block = 64 bit (8 char)
        * n = rounds (default 32)
        * endian = byte order (see 'struct' doc - default big/network) 

        >>> z = 'b67c01662ff6964a'.decode('hex')
        >>> xtea_decrypt('0123456789012345',z)
        'ABCDEFGH'

        Only need to change byte order if sending/receiving from 
        alternative endian implementation 

        >>> z = 'ea0c3d7c1c22557f'.decode('hex')
        >>> xtea_decrypt('0123456789012345',z,endian="<")
        'ABCDEFGH'

    """
    v0,v1 = struct.unpack(endian+"2L",block)
    k = struct.unpack(endian+"4L",key)
    delta,mask = 0x9e3779b9L,0xffffffffL
    sum = (delta * n) & mask
    for round in range(n):
        v1 = (v1 - (((v0<<4 ^ v0>>5) + v0) ^ (sum + k[sum>>11 & 3]))) & mask
        sum = (sum - delta) & mask
        v0 = (v0 - (((v1<<4 ^ v1>>5) + v1) ^ (sum + k[sum & 3]))) & mask
    return struct.pack(endian+"2L",v0,v1)

const_class_symbol = '__class__'

def unique(items):
    d = {}
    for item in items:
        d[item] = 1
    return d.keys()

def fileSize(fname):
    statinfo = os.stat(fname)
    return statinfo.st_size

def fullClassName(obj):
    return str(type(obj)).split("'")[1]

def terseClassName(sClassName):
    if (misc.isString(sClassName)):
        return sClassName.split('.')[-1]
    return ''

def obj2Dict(obj):
    d = {}
    d[const_class_symbol] = fullClassName(obj)
    spam = '_%s' % terseClassName(d[const_class_symbol])
    try:
        for k,v in obj.__dict__.iteritems():
            d[k.replace(spam,'')] = v
    except:
        o = [n for n in obj]
        o.insert(0,type(obj))
        return obj2Dict(o)
    return d

def dict2Obj(value):
    obj = value
    if (isinstance(value,dict)):
        if (value.has_key(const_class_symbol)):
            cname = value[const_class_symbol]
            try:
                toks = cname.split('.')
                s = 'from %s import %s\nobj=%s()' % (toks[0],'.'.join(toks[1:-1]),'.'.join(toks[1:]))
                exec(s)
            except:
                obj = None
            if (obj):
                for k in [n for n in value.keys() if n != const_class_symbol]:
                    if not n.startswith('__'):
                        _k = '_%s' % toks[-1]
                    else:
                        _k = '%s' % (k)
                    try:
                        isQuoted = misc.isString(value[k])
                        _quote = '"' if isQuoted else ''
                        s = 'obj.%s=%s%s%s' % (_k.replace('__',''),_quote,value[k],_quote)
                        exec(s)
                    except AttributeError:
                        pass
    return obj

def isAnyAlphaNumeric(token):
    for t in token:
        if (t.isalnum()):
            return True
    return False

def isAllNonAlphaNumeric(token):
    for t in token:
        if (t.isalnum()):
            return False
    return True

# change a hexadecimal string to decimal number and reverse
# check two different representations of the hexadecimal string
# negative values and zero are accepted

from vyperlogix.misc.hex import strToHex, hexToStr

from types import (
    IntType, TupleType, StringType,
    FloatType, LongType, ListType,
    DictType, NoneType, BooleanType, UnicodeType
)

class EncodeError(Exception): pass
class DecodeError(Exception): pass

class CompressionOption(Enum):
    no_compression = 0
    compression = 1

HEADER = "SRW3"

protocol = {
    TupleType          :"T",
    ListType           :"L",
    DictType           :"D",
    lists.HashedLists2 :"D",
    LongType           :"B",
    IntType            :"I",
    FloatType          :"F",
    StringType         :"S",
    ApexDatetime       :"a",
    NoneType           :"N",
    BooleanType        :"b",
    UnicodeType        :"U"
}

encoder = {}
class register_encoder_for_type(object):
    """Registers an encoder function, for a type, in the global encoder dictionary."""
    def __init__(self, t):
        self.type = t
    def __call__(self, func):
        encoder[self.type] = func
        return func

#contains dictionary of decoding functions, where the dictionary key is the type prefix used.
decoder = {}
class register_decoder_for_type(object):
    """Registers a decoder function, for a prefix, in the global decoder dictionary."""
    def __init__(self, t):
        self.prefix = protocol[t]
    def __call__(self, func):
        decoder[self.prefix] = func
        return func

## <encoding functions> ##
@register_encoder_for_type(DictType)
@register_encoder_for_type(lists.HashedLists2)
def enc_dict_type(obj):
    data = "".join([encoder[type(i)](i) for i in obj.items()])
    return "%s%s%s" % (protocol[type(obj)], pack("!L", len(data)), data)

@register_encoder_for_type(TupleType)
@register_encoder_for_type(ListType)
def enc_list_type(obj):
    data = "".join([encoder[type(i)](i) for i in obj])
    return "%s%s%s" % (protocol[type(obj)], pack("!L", len(data)), data)

@register_encoder_for_type(IntType)
def enc_int_type(obj):
    return "%s%s" % (protocol[IntType], pack("!i", obj))

@register_encoder_for_type(FloatType)
def enc_float_type(obj):
    return "%s%s" % (protocol[FloatType], pack("!d", obj))

@register_encoder_for_type(LongType)
def enc_long_type(obj):
    obj = hex(obj)[2:-1]
    return "%s%s%s" % (protocol[LongType], pack("!L", len(obj)), obj)

@register_encoder_for_type(UnicodeType)
def enc_unicode_type(obj):
    obj = obj.encode('utf-8')
    return "%s%s%s" % (protocol[UnicodeType], pack("!L", len(obj)), obj)

@register_encoder_for_type(StringType)
def enc_string_type(obj):
    return "%s%s%s" % (protocol[StringType], pack("!L", len(obj)), obj)

@register_encoder_for_type(ApexDatetime)
def enc_apex_datetime_type(obj):
    obj = str(obj)
    return "%s%s%s" % (protocol[ApexDatetime], pack("!L", len(obj)), obj)

@register_encoder_for_type(NoneType)
def enc_none_type(obj):
    return protocol[NoneType]

@register_encoder_for_type(BooleanType)
def enc_bool_type(obj):
    return protocol[BooleanType] + str(int(obj))

def dumps(obj, compress=CompressionOption.no_compression, phase=1):
    """Encode simple Python types into a binary string."""
    option = "N" if compress.value == CompressionOption.no_compression.value else "Z"
    try:
        data = encoder[type(obj)](obj)
        if compress.value == CompressionOption.compression.value: data = zlib.compress(data)
        return "%s%s%s" % (HEADER, option, data)
    except KeyError, e:
        if (phase == 1):
            try:
                data = obj2Dict(obj)
                return dumps(data,compress,phase+1)
            except:
                raise EncodeError, "Type not supported. (%s) during phase #%2d" % (e,phase)
        else:
            raise EncodeError, "Type not supported. (%s) during phase #%2d" % (e,phase)
## </encoding functions> ##

## <decoding functions> ##
def build_sequence(data, cast=list):
    size = unpack('!L', data.read(4))[0]
    items = []
    data_tell = data.tell
    data_read = data.read
    items_append = items.append
    start_position = data.tell()
    while (data_tell() - start_position) < size:
        T = data_read(1)
        value = decoder[T](data)
        items_append(value)
    return cast(items)

@register_decoder_for_type(TupleType)
def dec_tuple_type(data):
    return build_sequence(data, cast=tuple)

@register_decoder_for_type(ListType)
def dec_list_type(data):
    return build_sequence(data, cast=list)

@register_decoder_for_type(DictType)
def dec_dict_type(data):
    return build_sequence(data, cast=dict)

@register_decoder_for_type(lists.HashedLists2)
def dec_HashedLists2_type(data):
    return build_sequence(data, cast=lists.HashedLists2)

@register_decoder_for_type(LongType)
def dec_long_type(data):
    size = unpack('!L', data.read(4))[0]
    value = long(data.read(size),16)
    return value

@register_decoder_for_type(StringType)
def dec_string_type(data):
    size = unpack('!L', data.read(4))[0]
    value = str(data.read(size))
    return value

@register_decoder_for_type(ApexDatetime)
def dec_apex_datetime_type(data):
    value = dec_string_type(data)
    return ApexDatetime.fromSfIso(value.split('+')[0])

@register_decoder_for_type(FloatType)
def dec_float_type(data):
    value = unpack('!d', data.read(8))[0]
    return value

@register_decoder_for_type(IntType)
def dec_int_type(data):
    value = unpack('!i', data.read(4))[0]
    return value

@register_decoder_for_type(NoneType)
def dec_none_type(data):
    return None

@register_decoder_for_type(BooleanType)
def dec_bool_type(data):
    value = int(data.read(1))
    return bool(value)

@register_decoder_for_type(UnicodeType)
def dec_unicode_type(data):
    size = unpack('!L', data.read(4))[0]
    value = data.read(size).decode('utf-8')
    return value

def loads(data,beSilent=False):
    """
    Decode a binary string into the original Python types.
    """
    buffer = StringIO(data)
    header = buffer.read(len(HEADER))
    if (not beSilent):
        assert header == HEADER
    option = buffer.read(1)
    decompress = False
    if option == "Z":
        buffer = StringIO(zlib.decompress(buffer.read()))
    try:
        value = decoder[buffer.read(1)](buffer)
    except KeyError, e:
        raise DecodeError, "Type prefix not supported. (%s)" % e

    value = dict2Obj(value)
    return value
## </decoding functions> ##

class PickleMethods(Enum):
    none = 0
    useBsdDbShelf = 2**0
    useStrings = 2**1
    useMarshal = 2**2
    useSafeSerializer = 2**3 # (+++) this is very slow !  Make this run faster !
    useSimpleJSon = 2**4
    useCerealizer = 2**5
    useLegacyFileMode = 2**10 # this performs no filename munging - takes the filename given and opens it...
    use_lzma = 2**14
    use_zlib = 2**15

class NormalizedKeyOptions(Enum):
    via_list = 0
    via_dict = 1
    use_hash1 = 2**14
    use_hash2 = 2**15

_class_tag = lambda name:''.join([ch for ch in name if (ch.isupper()) or (ch.isdigit())])
class_tag = lambda cls:_class_tag(ObjectTypeName__typeName(cls))

unlistify = lambda item:item if (not misc.isList(item)) else item[0]

class PickledHash(CooperativeClass.Cooperative):
    '''PickledHash is a persistent hash with unique keys, see PickledHash2 for the persistent hash that handles duplicated keys with lists for values.

    dbx = PickledHash(fileName, method=PickleMethods.useStrings)

    PickleMethods.useBsdDbShelf     = 54x
    PickleMethods.useStrings        = 26x
    PickleMethods.useSafeSerializer = 4x
    PickleMethods.useMarshal        = 1x
    '''
    def __init__(self, fileName, method=PickleMethods.useStrings,has_bsddb=False):
        from vyperlogix.crypto.Encryptors import Encryptors
        self.__method = method
        self.has_bsddb = has_bsddb
        self.__isPickleMethodUseStrings = ((method.value & PickleMethods.useStrings.value) != 0)
        self.__isPickleMethodUseLZMA = ((method.value & PickleMethods.use_lzma.value) != 0)
        self.__isPickleMethodUseBsdDbShelf = ((method.value & PickleMethods.useBsdDbShelf.value) != 0)
        self.__isPickleMethodUseMarshal = ((method.value & PickleMethods.useMarshal.value) != 0)
        self.__isPickleMethodUseSafeSerializer = ((method.value & PickleMethods.useSafeSerializer.value) != 0)
        self.__isPickleMethodUseCerealizer = ((method.value & PickleMethods.useCerealizer.value) != 0)
        self.__isPickleMethodUseSimpleJSon = ((method.value & PickleMethods.useSimpleJSon.value) != 0)
        self.__isPickleMethodUseZLIB = (not self.isPickleMethodUseLZMA) and ((method.value & PickleMethods.use_zlib.value) != 0)
        self.__isPickleMethodUseLegacyFileMode = ((method.value & PickleMethods.useLegacyFileMode.value) != 0)

        self.__fileName = fileName
        if (not self.isPickleMethodUseLegacyFileMode) and (not isFilenameMungedAlready(fileName)):
            self.__fileName = self.tag_filename(fileName)
        self.__isOpened = False

        self.open()

    def tag_classname(self):
        return class_tag(self)

    def tag_filename(self, fname):
        return '%s%s%s_%s.%s' % (os.path.dirname(fname),os.sep,os.path.basename(fname).split('.')[0],self.tag_classname(),os.path.basename(fname).split('.')[-1])

    def __repr__(self):
        return '(%s) on "%s" storing %d keys using the "%s" method; issue the appropriate method to turn this object into the string you want this to be however there may be a lot of date once this is done.' % (str(self.__class__),self.fileName,len(self.keys()),str(self.method))

    def method():
        doc = "method"
        def fget(self):
            return self.__method
        return locals()
    method = property(**method())

    def isOpened():
        doc = "isOpened"
        def fget(self):
            return self.__isOpened
        return locals()
    isOpened = property(**isOpened())

    def fileName():
        doc = "fileName"
        def fget(self):
            return self.__fileName
        return locals()
    fileName = property(**fileName())

    def db():
        doc = "db"
        def fget(self):
            return self.__db
        return locals()
    db = property(**db())

    def unPickleItem(self,glob):
        return Unpickler(StringIO(glob)).load()

    def pickleItem(self,glob):
        io = StringIO()
        Pickler(io, -1).dump(glob)
        return io.getvalue()

    def unlistify(self,item):
        return unlistify(item)

    def __getitem__(self, key):
        from vyperlogix.crypto.Encryptors import Encryptors
        try:
            val = self.__db[key]
            if (not self.isPickleMethodUseSafeSerializer):
                if (self.isPickleMethodUseZLIB):
                    val = zlib.decompress(val)
                elif (self.isPickleMethodUseLZMA):
                    val = pylzma.decompress(val)
            if (self.isPickleMethodUseStrings):
                val = val.split(',')
                if (len(val) > 1):
                    val = [tuple(x.split('|')) if x.find('|') > -1 else x for x in val]
            elif (self.isPickleMethodUseBsdDbShelf):
                val = self.unPickleItem(val)
            elif (self.isPickleMethodUseMarshal):
                val = marshal.loads(hexToStr(val))
            elif (self.isPickleMethodUseSafeSerializer):
                try:
                    val = loads(val,beSilent=True)
                except:
                    pass
                if (isinstance(val,dict)):
                    d_val = HashedLists2()
                    d_val.fromDict(val)
                    val = d_val
            elif (self.isPickleMethodUseCerealizer):
                val = cerealizer.loads(val)
        except Exception, details:
            val = 'UNKNOWN value for key (%s) of type "%s" due to ERROR "%s".' % (key,str(key.__class__),str(details))
        return val

    def __setitem__(self, key, value):
        from vyperlogix.crypto.Encryptors import Encryptors
        from vyperlogix.misc import GenPasswd

        key = key if (misc.isString(key)) else str(key)
        if (self.has_key(key)) and (value == None):
            self.__delitem__(key)
        else:
            if (misc.isList(value)):
                value = [v if (not lists.can_asDict(v)) else v.asDict() for v in value]
            else:
                value = value if (not lists.can_asDict(value)) else value.asDict()
            if (self.isPickleMethodUseStrings):
                if (not misc.isString(value)):
                    if not misc.isList(value):
                        value = list(value) if (not isinstance(value,dict)) else [(k,v) for k,v in value.iteritems()]
                    val = ['|'.join([str(x) for x in v]) if isinstance(v,tuple) else str(v) for v in value]
                    if (len(val) > 0):
                        value = ','.join(val) if (len(val) > 1) else val[0]
                    else:
                        value = ''
            elif (self.isPickleMethodUseMarshal):
                value = strToHex(marshal.dumps(value,2))
            elif (self.isPickleMethodUseBsdDbShelf):
                value = self.pickleItem(value)
            elif (self.isPickleMethodUseSafeSerializer):
                value = dumps(value,CompressionOption.compression)
            elif (self.isPickleMethodUseCerealizer):
                #cls = eval(ObjectTypeName.typeClassName(value))
                #if (not cerealizer.isRegistered(cls)):
                    #cerealizer.register(cls)
                value = cerealizer.dumps(value)
            if (not self.isPickleMethodUseSafeSerializer):
                if (self.isPickleMethodUseZLIB):
                    value = zlib.compress(value,zlib.Z_BEST_COMPRESSION)
                elif (self.isPickleMethodUseLZMA):
                    value = pylzma.compress(value, eos=1)
            self.__db[key] = value

    def __delitem__(self, key):
        del self.__db[key]

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self.keys())

    def has_key(self, key):
        return self.__db.has_key(key)

    def keys(self):
        try:
            return self.__db.keys()
        except:
            pass
        return []

    def values(self):
        try:
            return self.__db.values()
        except:
            pass
        return []

    def normalizedSortedKeys(self,options=NormalizedKeyOptions.via_list):
        '''
	Get a list of keys sorted in a fashion that allows for easier manipulation - 
	padded or normalized to allow sorting to work.

	options = see also NormalizedKeyOptions enumeration
	'''
        from vyperlogix.hash import lists

        try:
            _asDict = options.value & NormalizedKeyOptions.via_dict.value
        except:
            _asDict = False

        try:
            _useHash1 = options.value & NormalizedKeyOptions.use_hash1.value
        except:
            _asDict = False
            _useHash1 = False

        try:
            _useHash2 = options.value & NormalizedKeyOptions.use_hash2.value
        except:
            _useHash2 = False

        _useHash2 = ( (not _useHash1) and (not _useHash2) ) or _useHash2
        _useHash1 = False if (_useHash1 and _useHash2) else _useHash1

        d_keys = lists.HashedLists() if _useHash1 else lists.HashedLists2() if _useHash2 else {}

        def normalizeKey(k,m):
            toks = k.split(',')
            n = toks[0]
            del toks[0]
            getLen = lambda m,n:m-len(n)
            formatter = lambda p,m,n,f:p % (' '*getLen(m,n),f(n))
            _value = ''
            _isString = (misc.isString(n))
            _pattern = '%s%s' if _isString else '%s%d'
            _func = str if _isString else int
            _value = formatter(_pattern,m,n,_func)
            toks.insert(0,_value)
            s = ','.join(toks)
            if (_asDict):
                d_keys[s] = k
            return s

        l_keys = [len(k.split(',')[0]) for k in self.keys()]
        l_keys.sort()
        _max_len = l_keys[-1] if len(l_keys) > 0 else 0
        _keys = [normalizeKey(k,_max_len) for k in self.keys()]
        _keys.sort()
        _keys.reverse()
        return _keys if (not _asDict) else d_keys

    def sync(self):
        if (self.isOpened):
            self.__db.sync()

    def flush(self):
        self.sync()

    def iteritems(self):
        return ((k,self.__getitem__(k)) for k in self.keys())

    def close(self):
        if (self.isOpened):
            self.__db.close()
            self.__isOpened = False

    def queryANDitems(self,*args):
        recs = set()
        for arg in args:
            items = []
            if (self.has_key(arg)):
                items = self[arg]
                if (not misc.isList(items)):
                    items = [items]
            items = set(items)
            if len(recs) == 0:
                recs = items
            else:
                recs &= items
        return list(recs)

    def queryMostlyANDitems(self,*args):
        recs = set()
        for arg in args:
            items = []
            if (self.has_key(arg)):
                items = self[arg]
                if (not misc.isList(items)):
                    items = [items]
            items = set(items)
            if len(recs) == 0:
                recs = items
            elif len(recs & items) > 0:
                recs &= items
        return list(recs)

    def isPickleMethodUseStrings():
        doc = "isPickleMethodUseStrings boolean"
        def fget(self):
            return self.__isPickleMethodUseStrings
        return locals()
    isPickleMethodUseStrings = property(**isPickleMethodUseStrings())

    def isPickleMethodUseBsdDbShelf():
        doc = "isPickleMethodUseBsdDbShelf boolean"
        def fget(self):
            return self.__isPickleMethodUseBsdDbShelf
        return locals()
    isPickleMethodUseBsdDbShelf = property(**isPickleMethodUseBsdDbShelf())

    def isPickleMethodUseLZMA():
        doc = "isPickleMethodUseLZMA boolean"
        def fget(self):
            return self.__isPickleMethodUseLZMA
        return locals()
    isPickleMethodUseLZMA = property(**isPickleMethodUseLZMA())

    def isPickleMethodUseMarshal():
        doc = "isPickleMethodUseMarshal boolean"
        def fget(self):
            return self.__isPickleMethodUseMarshal
        return locals()
    isPickleMethodUseMarshal = property(**isPickleMethodUseMarshal())

    def isPickleMethodUseSafeSerializer():
        doc = "isPickleMethodUseSafeSerializer boolean"
        def fget(self):
            return self.__isPickleMethodUseSafeSerializer
        return locals()
    isPickleMethodUseSafeSerializer = property(**isPickleMethodUseSafeSerializer())

    def isPickleMethodUseCerealizer():
        doc = "isPickleMethodUseCerealizer boolean"
        def fget(self):
            return self.__isPickleMethodUseCerealizer
        return locals()
    isPickleMethodUseCerealizer = property(**isPickleMethodUseCerealizer())

    def isPickleMethodUseSimpleJSon():
        doc = "isPickleMethodUseSimpleJSon boolean"
        def fget(self):
            return self.__isPickleMethodUseSimpleJSon
        return locals()
    isPickleMethodUseSimpleJSon = property(**isPickleMethodUseSimpleJSon())

    def isPickleMethodUseZLIB():
        doc = "isPickleMethodUseZLIB boolean"
        def fget(self):
            return self.__isPickleMethodUseZLIB
        return locals()
    isPickleMethodUseZLIB = property(**isPickleMethodUseZLIB())

    def isPickleMethodUseLegacyFileMode():
        doc = "isPickleMethodUseLegacyFileMode boolean"
        def fget(self):
            return self.__isPickleMethodUseLegacyFileMode
        return locals()
    isPickleMethodUseLegacyFileMode = property(**isPickleMethodUseLegacyFileMode())

    def open(self):
        file_flag = lambda fname:'c' if (not os.path.exists(fname)) else 'rw'
        if (not self.isOpened):
            if ( (self.has_bsddb) and ( (self.isPickleMethodUseStrings) or (self.isPickleMethodUseMarshal) or (self.isPickleMethodUseSafeSerializer) ) ):
                self.__db = bsddb.btopen(self.fileName,file_flag(self.fileName))
                self.__isOpened = True
            elif (self.isPickleMethodUseBsdDbShelf):
                self.__db = shelve.BsdDbShelf(bsddb.btopen(self.fileName,file_flag(self.fileName)),0,True)
                self.__isOpened = True

    def reset(self):
        self.close()
        os.remove(self.fileName)
        self.__isOpened = False
        self.open()

    def dump(self,callback=None):
        if (self.isOpened):
            import pprint
            tName = os.sep.join([os.path.dirname(self.fileName),'.'.join([os.path.basename(self.fileName).split('.')[0],'txt'])])
            fHand = open(tName,'w')
            pp = pprint.PrettyPrinter(indent=4,width=80)
            print >>fHand, '(%s) :: (%s) :: dbx=(%s)' % (__name__,self.fileName,str(self))
            for k,v in self.iteritems():
                if (callback):
                    try:
                        print >>fHand, '%s :: %s' % (k,callback(v))
                    except:
                        print >>fHand, '%s :: %s' % (k,pp.pformat(v))
            print >>fHand
            print >>fHand, '='*60
            print >>fHand
            fHand.flush()
            fHand.close()

class PickledHash2(PickledHash):
    '''PickledHash2 allows keys to be duplicated with values being placed in lists when keys are duplicated.

    dbx = PickledHash2(fileName, method=PickleMethods.useStrings)

    PickleMethods.useBsdDbShelf     = 54x
    PickleMethods.useStrings        = 26x
    PickleMethods.useSafeSerializer = 4x
    PickleMethods.useMarshal        = 1x
    '''
    def __init__(self, fileName, method=PickleMethods.useBsdDbShelf,has_bsddb=False):
        _isProperType = lambda obj:(ObjectTypeName.typeClassName(obj).find('Enum.EnumInstance') > -1)
        isProperType = _isProperType(method)
        _isProperValue = lambda obj:((obj.value & PickleMethods.useBsdDbShelf.value) != 0)
        isProperValue = False
        if (isProperType):
            isProperValue = _isProperValue(method)
        if (not isProperType) or (not isProperValue):
            if (not isProperType):
                method = PickleMethods.useBsdDbShelf
                isProperValue = _isProperValue(method)
            if (not isProperValue):
                method |= PickleMethods.useBsdDbShelf
        return super(PickledHash2, self).__init__(fileName,method,has_bsddb=has_bsddb)

    def __getitem__(self, key):
        return [] if (not super(PickledHash2, self).has_key(key)) else super(PickledHash2, self).__getitem__(key)

    def __setitem__(self, key, value):
        key = key if (misc.isString(key)) else str(key)
        if (self.has_key(key)):
            bucket = super(PickledHash2, self).__getitem__(key)
            if (misc.isList(bucket)):
                bucket.append(value)
                super(PickledHash2, self).__setitem__(key,bucket)
            else:
                super(PickledHash2, self).__setitem__(key,[value])
        else:
            super(PickledHash2, self).__setitem__(key,value)

class PickledFastHash2(PickledHash2):
    '''PickledFastHash2 allows keys to be duplicated with values being placed in lists when keys are duplicated.

    dbx = PickledFastHash2(fileName) ... uses PickleMethods.useBsdDbShelf because this method runs faster than all the other methods.

    Works the same as lists.HashedLists()

    PickleMethods.useBsdDbShelf     = 54x
    PickleMethods.useStrings        = 26x
    PickleMethods.useSafeSerializer = 4x
    PickleMethods.useMarshal        = 1x
    '''
    def __init__(self, fileName, method=PickleMethods.useBsdDbShelf,has_bsddb=False):
        return super(PickledFastHash2, self).__init__(fileName,method,has_bsddb=has_bsddb)

class PickledFastCompressedHash2(PickledFastHash2):
    '''PickledFastCompressedHash2 allows keys to be duplicated with values being placed in lists when keys are duplicated.

    dbx = PickledFastCompressedHash2(fileName) ... uses PickleMethods.useBsdDbShelf because this method runs faster than all the other methods.

    Works the same as lists.HashedLists()

    PickleMethods.useBsdDbShelf     = 54x
    PickleMethods.useStrings        = 26x
    PickleMethods.useSafeSerializer = 4x
    PickleMethods.useMarshal        = 1x
    '''
    def __init__(self, fileName,has_bsddb=False):
        e = PickleMethods.useBsdDbShelf | PickleMethods.use_zlib
        super(PickledFastCompressedHash2, self).__init__(fileName,e,has_bsddb=has_bsddb)

class PickledLzmaHash2(PickledFastHash2):
    '''PickledLzmaHash2 allows keys to be duplicated with values being placed in lists when keys are duplicated.

    dbx = PickledLzmaHash2(fileName) ... uses PickleMethods.useBsdDbShelf because this method runs faster than all the other methods.

    Works the same as lists.HashedLists()

    PickleMethods.useBsdDbShelf     = 54x
    PickleMethods.useStrings        = 26x
    PickleMethods.useSafeSerializer = 4x
    PickleMethods.useMarshal        = 1x
    '''
    def __init__(self, fileName,has_bsddb=False):
        e = PickleMethods.useBsdDbShelf | PickleMethods.use_lzma
        super(PickledLzmaHash2, self).__init__(fileName,e,has_bsddb=has_bsddb)

__classes = [PickledHash, PickledHash2, PickledFastHash2, PickledFastCompressedHash2, PickledFastHash2, PickledLzmaHash2]
__classes_tags = ['_'+_class_tag(n.split('.')[len(n.split('.'))-1:][0]) for n in [ObjectTypeName._typeName(cls) for cls in __classes]]

def isFilenameMungedAlready(fname):
    return (any([fname.find(f) > -1 for f in __classes_tags]))

def getMungedFilenameFor(filename):
    _root = os.path.dirname(filename)
    fname = os.path.splitext(os.path.basename(filename))[0]
    ext = os.path.splitext(filename)[-1]
    _files = [os.sep.join([_root,f]) for f in os.listdir(_root) if (f.startswith(fname)) and (f.endswith(ext))]
    return filename if (len(_files) == 0) else _files[0]

def openPickledHashBasedOnFilename(filename, method=PickleMethods.none):
    '''Uses the filename to determine which class should be used to open the database file.  Fails with a list if filename has more than one variation present in the same folder.'''
    def deMungeFileName(fname):
        if (isFilenameMungedAlready(fname)):
            toks = fname.split('_')
            if (len(toks) > 2):
                while (len(toks) > 2):
                    toks[0] = '_'.join(toks[0:2])
                    del toks[1]
            _toks = toks[-1].split('.')
            _fname = '.'.join([toks[:len(toks)-1][0],_toks[-1]])
            _tag = '_'+_toks[0]
            return (fname,_fname,_tag)
        return (None, None)

    dname = os.path.dirname(filename)
    if (len(dname) == 0):
        dname = os.path.abspath('.')
    _obj = None
    _tag = ''
    fname = os.path.basename(filename)
    fname, _fname, _tag = deMungeFileName(fname)
    toks = fname.split('.')
    if (len(toks) > 1):
        toks[-1] = '.'+toks[-1]
    files = [deMungeFileName(f) for f in os.listdir(dname)]
    files = [f[1] for f in files if (f[0] == fname) and (f[-1] == _tag)]
    if (len(files) == 1):
        if (len(_tag) == 0):
            return openPickledHashBasedOnFilename(os.sep.join([dname,files[0]]),method=method)
        i = misc.findInListSafely(__classes_tags,_tag)
        if (i > -1):
            info_string = ''
            toks = ObjectTypeName._typeName(__classes[i]).split('.')
            className = toks[len(toks)-1:][0]
            try:
                s = '%s(filename,method=method)' % (className)
                _obj = eval(s)
            except TypeError:
                try:
                    s = '%s(filename)' % (className)
                    _obj = eval(s)
                except Exception, details:
                    info_string = str(details)
        else:
            raise ValueError('(%s) :: Cannot figure-out the class name based on "%s", recommend working this out on you own because you seemed to have written some bad code or maybe "%s".' % (misc.funcName(),_tag,info_string))
    else:
        raise ValueError('(%s) :: Too %s files (%d) named like "%s" %s for %s, recommend using the class name "%s" and open it yourself.' % (misc.funcName(),'many' if (len(files) > 1) else 'few',len(files),str(files),str(toks),filename,_tag))
    return _obj

def put_data(_fname,key,value,fOut=None,isUnique=True):
    dbx = PickledFastCompressedHash2(_fname)
    try:
        value = value if (not misc.isList(value)) else value[0]
        if (isUnique) and (dbx.has_key(key)):
            del dbx[key]
        dbx[key] = value
    except Exception, details:
        from vyperlogix.misc import _utils
        fOut = sys.stderr if (fOut is None) else fOut
        print >>fOut, _utils.formattedException(details)
    finally:
        dbx.close()

def get_data(_fname,key,fOut=None,isUnique=True):
    dbx = PickledFastCompressedHash2(_fname)
    value = None
    try:
        value = dbx[key]
        if (isUnique):
            value = value if (not misc.isList(value)) else None if (len(value) == 0) else value[0]
    except Exception, details:
        from vyperlogix.misc import _utils
        fOut = sys.stderr if (fOut is None) else fOut
        print >>fOut, _utils.formattedException(details)
    finally:
        dbx.close()
    return value
