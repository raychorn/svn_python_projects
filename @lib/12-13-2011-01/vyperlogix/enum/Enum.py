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

"""Enumeration metaclass.
"""
Enum = None        #initialize before definition
EnumLazy = None    #initialize before definition

from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc.ObjectTypeName import __typeName as ObjectTypeName__typeName
from vyperlogix import misc

class EnumMetaClass(type):
    """Metaclass for enumeration.
    To define your own enumeration, do something like
    class Color(Enum):
        red = 1
        green = 2
        blue = 3
    Now, Color.red, Color.green and Color.blue behave totally
    different: they are enumerated values, not integers.

    Enumerations cannot be instantiated; however they can be
    subclassed.
    """
    def __new__(meta, name, bases, dict):
        """Constructor -- create an enumeration.
        Called at the end of the class statement.  The arguments are
        the name of the new class, a tuple containing the base
        classes, and a dictionary containing everything that was
        entered in the class' namespace during execution of the class
        statement.  In the above example, it would be {'red': 1,
        'green': 2, 'blue': 3}.
        """
        if Enum:
            for base in bases:
                if (not issubclass(base, Enum)):
                    raise TypeError, "Enumeration base class must be Enum or EnumLazy but not %s." % type(base)
        items = []
        for key, value in dict.items():
            if not key.startswith('_'):
                dict[key] = item = EnumInstance(dict, name, key, value)
                items.append(item)
        dict['_items_'] = items
        dict['_bases_'] = [base for base in bases if base is not Enum]
        return super(EnumMetaClass, meta).__new__(meta, name, bases, dict)

    def append(self,enum_instance):
        self._items_.append(enum_instance)

    def __repr__(self):
        s = self.__name__
        if self._bases_:
            s = s + '(' + ", ".join(map(lambda x: x.name, self._bases_)) + ')'
        if self._items_:
            list = []
            for item in self._items_:
                list.append("%s: %s" % (item.name, item))
            s = "%s: {%s}" % (s, ", ".join(list))
        return s

    def __iter__(self):
        return ((item.name, str(item)) for item in self._items_)

    def asDict(self):
        d = {self.__name__:None}
        if self._bases_:
            d[self.__name__] = map(lambda x: x.name, self._bases_)
        if self._items_:
            d[self.__name__] = [{item.name:item.value} for item in self._items_]
        return d

    def asJSON(self):
        sObj = ''
        if self._bases_:
            sObj = ','.join(['"%s"' % (t) for t in map(lambda x: x.name, self._bases_)])
        if self._items_:
            sObj = ','.join(['{"%s":"%s"}' % (item.name,item.value) for item in self._items_])
        d = '{"%s":%s}' % (self.__name__,sObj)
        return d

    def __contains__(self, item):
        for n,v in self:
            _v = str(v)
            t_v = _v.split('=')
            if (n == item) or (v == item) or (_v == item) or (t_v.index(item) > -1):
                return True
        return False

    def __len__(self):
        i = 0
        for n,v in self:
            i += 1
        return i

    def __call__(self, value):
        __is_name__ = lambda x,names:(str(x.name).lower() in names)
        __is__ = lambda x,value,s_value:(x.value == value) or (str(x.value) == value) or (x.name.find(s_value) > -1) or (len([f for f in str(x).split('=') if (f == s_value)]) > 0)
        mro = self.__mro__
        s_default = '-1'
        default = int(s_default)
        defaults = [str(n).lower() for n in ['default','unknown']]
        for cls in mro:
            if cls is Enum:
                break
            s_value = str(value)
            for x in cls._items_:
                if (__is__(x,value,s_value)):
                    return x
                elif (__is__(x,default,s_default)):
                    default = x
                elif (__is_name__(x,defaults)):
                    default = x
            return None if (default == -1) else default
        raise ValueError("%r is not a member of %s however (%s) are valid members." % (value, self.name,str(items)))

class EnumLazyMetaClass(EnumMetaClass):
    def __new__(meta, name, bases, dict):
        """Constructor -- create an enumeration.
        Called at the end of the class statement.  The arguments are
        the name of the new class, a tuple containing the base
        classes, and a dictionary containing everything that was
        entered in the class' namespace during execution of the class
        statement.  In the above example, it would be {'red': 1,
        'green': 2, 'blue': 3}.
        """
        if EnumLazy:
            for base in bases:
                if (not issubclass(base, EnumLazy)):
                    raise TypeError, "Enumeration base class must be Enum or EnumLazy but not %s." % type(base)
        items = []
        for key, value in dict.items():
            if not key.startswith('_'):
                dict[key] = item = EnumInstance(dict, name, key, value)
                items.append(item)
        dict['_items_'] = items
        dict['_bases_'] = [base for base in bases if base is not Enum]
        return super(EnumMetaClass, meta).__new__(meta, name, bases, dict)

    def __call__(self, value):
        mro = self.__mro__
        for cls in mro:
            if cls is Enum:
                break
            items = cls._items_
            try:
                i = items.index(value)
            except ValueError:
                items = [str(x).split('.')[-1] for x in cls._items_]
                try:
                    i = items.index(value)
                except ValueError:
                    pass
                else:
                    return cls._items_[i]
            else:
                return items[i]
            _val = 2**(len(items)-1)
            item = EnumInstance(cls, self.name, value, _val)
            cls._items_.append(item)
            return item
        raise ValueError("%r is not a member of %s however (%s) are valid members." % (value, self.name,str(items)))

class EnumInstance(str):
    """Class to represent an enumeration value.

    EnumInstance('Color', 'red', 12) prints as 'Color.red' and behaves
    like the integer 12.
    """

    _concat_symbol = '+'
    _boolOp_AND = '&'
    _boolOp_OR = '|'

    def __new__(cls, parent, classname, enumname, value):
        self = super(EnumInstance, cls).__new__(cls, str(value))
        self.__parent = parent
        self.__classname = classname
        if (misc.isString(enumname)):
            self.__enumname = enumname
            self.__value = value
        elif (misc.isList(enumname)):
            self.__value = 0
            for n in enumname:
                val = parent[n].value
                self.__value |= val
            assert self.__value == value, '(%s.%s) :: ERROR: Why the freak is the value of "%s" not equal to "%s"; the value that was stated to equate to "%s" cannot be correct according to the actual values from the parent of this %s object.' % (ObjectTypeName.typeName(self),misc.funcName(),self.__value,value,enumname,ObjectTypeName.typeName(self))
        else:
            print '(%s.%s) :: ERROR: What the freak is the meaning of enumname of "%s" of type "%s".' % (ObjectTypeName.typeName(self),misc.funcName(),enumname,ObjectTypeName.typeName(enumname))
        return self

    def name():
        doc = "name of this EnumInstance"
        def fget(self):
            return self.__enumname
        def fset(self,value):
            self.__enumname = value
        return locals()
    name = property(**name())

    def value():
        doc = "value of this EnumInstance"
        def fget(self):
            return self.__value
        def fset(self,value):
            self.__value = value
        return locals()
    value = property(**value())

    def classname():
        doc = "classname of this EnumInstance"
        def fget(self):
            return self.__classname
        return locals()
    classname = property(**classname())

    def parent():
        doc = "parent of this EnumInstance"
        def fget(self):
            return self.__parent
        return locals()
    parent = property(**parent())

    def __names__(self, value):
        items = self.__parent['_items_']
        names = [item.name for item in items if (item.value == value)]
        if (len(names) == 0):
            for item in items:
                if (value & item.value):
                    names.append(item.name)
        return names

    def __boolOp__(self, other, operation='&'):
        cname = ObjectTypeName.typeClassName(self).split('.')[-1]
        cls = eval(cname)
        if (isinstance(other,cls)):
            value = 0
            if (operation == EnumInstance._boolOp_AND):
                value = self.value & other.value
            elif (operation == EnumInstance._boolOp_OR):
                value = self.value | other.value
            else:
                print '(%s.%s) :: WARNING: Expected operation to be "%s" or "%s" but it is "%s".' % (ObjectTypeName.typeName(self),misc.funcName(),EnumInstance._boolOp_AND,EnumInstance._boolOp_OR,operation)
            names = self.__names__(value)
            e = cls(self.parent,self.classname,EnumInstance._concat_symbol.join(names),value)
            return e
        else:
            print '(%s.%s) :: ERROR: Expected other to be of type "%s" but it is of type "%s".' % (ObjectTypeName.typeName(self),misc.funcName(),ObjectTypeName.typeName(self),ObjectTypeName.typeName(other))
        return None

    def __and__(self, other):
        return self.__boolOp__(other, EnumInstance._boolOp_AND)

    def __or__(self, other):
        return self.__boolOp__(other, EnumInstance._boolOp_OR)

    def __repr__(self):
        return "%s(%s, %s, %s, %s)" % (ObjectTypeName__typeName(self.__class__),`self.classname`, `self.name`,`str(self)`,`self.value`)

    def __str__(self):
        try:
            n = self.__enumname
        except AttributeError:
            n = 'NO_NAME'
        try:
            v = self.__value
        except AttributeError:
            v = 'NO_VALUE'
        clsName = ObjectTypeName__typeName(self.__class__)
        return "%s.%s=%s" % (clsName, n, v)

class Enum(object):
    __metaclass__ = EnumMetaClass

class EnumLazy(object):
    __metaclass__ = EnumLazyMetaClass
