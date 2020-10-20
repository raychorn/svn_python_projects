from vyperlogix.misc import ObjectTypeName
from vyperlogix import misc
from vyperlogix.hash import lists
from vyperlogix.classes.CooperativeClass import Cooperative

import sys
import logging

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

real_k = lambda foo:str(foo) if (foo is None) else foo[0 if not foo.startswith('__') else 2:len(foo) if not foo.endswith('__') else len(foo)-2]

isSmartObject = lambda obj:ObjectTypeName.typeClassName(obj).find('.SmartObject') > -1

def asPythonDict(obj):
    try:
        return obj.asPythonDict()
    except:
        try:
            return obj.asDict(cls=dict)
        except:
            pass
    return obj

class SmartObject(Cooperative):
    def __init__(self,args={}):
        '''Populate from a dict object.'''
        self.__dict__ = {}
        self.fromDict(args)
    
    def fromDict(self, args):
        if (lists.isDict(args)):
            try:
                __iter__ = args.iteritems()
            except:
                try:
                    __iter__ = args.asPythonDict().iteritems()
                except:
                    try:
                        __iter__ = args.asDict().iteritems()
                    except:
                        __iter__ = None
            for ak,av in __iter__:
                try:
                    for k,v in av.iteritems():
                        self.__dict__['%s_%s' % (ak,k)] = v
                except:
                    self.__dict__[ak] = av if (not misc.isList(av)) else [item if (not lists.isDict(item)) else self.__class__(item) for item in av]
        else:
            logging.warning('(%s.%s) :: Illegal args variable, expected type "dict" but got type "%s".' % (ObjectTypeName.typeName(self),misc.funcName(),ObjectTypeName.typeName(args)))
    
    def __str__(self):
        ascii_only = lambda s:''.join([ch for ch in s if (ord(ch) >= 32) and (ord(ch) <= 127)])
        _vars = []
        for k,v in self.__dict__.iteritems():
            _vars.append('%s="%s"' % (real_k(k),ascii_only(v) if (misc.isString(v)) else str(v)))
        return '(%s) %s' % (str(self.__class__),', '.join(_vars))
    
    def asDict(self,cls=lists.HashedLists2):
        '''cls can also be dict to allow for normal native dict objects to be returned for safe pickling using the standard Python pickle methods.'''
        d = cls()
        for k,v in self.__dict__.iteritems():
            if (k == '__dict__'):
                continue
            _name = real_k(k)
            toks = _name.split('_')
            if (len(toks) > 1):
                d_name = toks[0]
                _name = '_'.join(toks[1:])
                try:
                    if (not d.has_key(d_name)):
                        d[d_name] = cls()
                    d[d_name][_name] = v if (not misc.isList(v)) else [asPythonDict(item) for item in v]
                except:
                    if (not d.has_key(k)):
                        d[k] = cls()
                    d[k] = v if (not misc.isList(v)) else [asPythonDict(item) for item in v]
            else:
                d[_name] = v if (not misc.isList(v)) else [asPythonDict(item) for item in v]
        return d
    
    def asPythonDict(self):
        return self.asDict(cls=dict)

    def keys(self):
        return self.__dict__.keys()
    
    def has_key(self,key):
        return self.__dict__.has_key(key)
    
    def iteritems(self):
        return [(k,v) for k,v in self.__dict__.iteritems() if (k != '__dict__')]
    
    def prettyPrint(self,prefix='',title='',tab_width=4,delay_end=False,fOut=sys.stdout):
        return self.asDict().prettyPrint(prefix=prefix,title=title,tab_width=tab_width,delay_end=delattr,fOut=fOut)
    
    def __getitem__(self, name):
        return self.__getattr__(name)
        
    def __setitem__(self,name,value):
        self.__setattr__(name,value)
    
    def __getattr__(self, name):
        if (self.__dict__.has_key(name)):
            return self.__dict__[name]
        else:
            return None
        
    def __getstate__(self):
        return self.asPythonDict()

    def __setstate__(self,state):
        return self.fromDict(state)

    def __setattr__(self, name, value):
        __is__ = False
        try:
            __is__ = (value == None)
        except:
            pass
        if (__is__) and (self.__dict__.has_key(name)):
            del self.__dict__[name]
        else:
            self.__dict__[name] = value
            
    def __len__(self):
        return len(self.keys())
        
class SmartJsonObject(SmartObject):
    def __getattr__(self, name):
        v = super(SmartJsonObject, self).__getattr__(name)
        if (v == None):
            v = '{}'
        return v

class StrictSmartObject(SmartObject):
    def __getattr__(self, name):
        v = super(StrictSmartObject, self).__getattr__(name)
        if (v == None):
            raise KeyError('Cannot determine value of "%s" from %s' % (name,self.__dict__.keys()))
        return v

class SmartFuzzyObject(SmartObject):
    def __init__(self,args={}):
        '''Populate from a dict object.'''
        super(SmartFuzzyObject, self).__init__(args)

    def __getattr__(self, name):
        values = []
        keys = [k for k in self.__dict__.keys() if (str(k).lower() == str(name).lower())]
        for key in keys:
            values.append(super(SmartFuzzyObject, self).__getattr__(key))
        return values if (len(values) > 1) else values[0] if (misc.isList(values)) and (len(values) > 0) else values

    def __setattr__(self, name, value):
        keys = [k for k in self.__dict__.keys() if (str(k).lower() == str(name).lower())]
        if (len(keys) > 0):
            for key in keys:
                super(SmartFuzzyObject, self).__setattr__(key,value)
        else:
            super(SmartFuzzyObject, self).__setattr__(name,value)
        
    def __getitem__(self, name):
        value = super(SmartFuzzyObject, self).__getitem__(name)
        if (value is None):
            raise AttributeError('INVALID use of the method that treats %s as if it were a dictionary.  Try to use this object as if it had instance variables rather than key,value pairs or use the right key name next time.' % (ObjectTypeName.objectSignature(self)))
        return value

    def __setitem__(self,name,value):
        self.__setattr__(name,value)
        
class SmartObject2(SmartObject):
    def fromDict(self, args):
        if (lists.isDict(args)):
            for ak,av in args.iteritems():
                if (lists.isDict(av)):
                    self.__dict__[ak] = SmartObject(av)
                else:
                    self.__dict__[ak] = av if (not misc.isList(av)) else [item if (not lists.isDict(item)) else self.__class__(item) for item in av]
        else:
            logging.warning('(%s.%s) :: Illegal args variable, expected type "dict" but got type "%s".' % (ObjectTypeName.typeName(self),misc.funcName(),ObjectTypeName.typeName(args)))

class PyroSmartObject(SmartObject2):
    def asDict(self,cls=lists.HashedLists2):
        '''cls can also be dict to allow for normal native dict objects to be returned for safe pickling using the standard Python pickle methods.'''
        d = cls()
        for k,v in self.__dict__.iteritems():
            d[real_k(k)] = [asPythonDict(item) for item in v] if (misc.isList(v)) else asPythonDict(v) if (lists.isDict(v)) else v.asPythonDict() if (isSmartObject(v)) else v
        return d
