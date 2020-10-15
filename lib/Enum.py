"""Enumeration metaclass.
"""
Enum = None        #initialize before definition

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
                if not issubclass(base, Enum):
                    raise TypeError, "Enumeration base class must be enumeration"
        items = []
        for key, value in dict.items():
            if not key.startswith('_'):
                dict[key] = item = EnumInstance(name, key, value)
                items.append(item)
        dict['_items_'] = items
        dict['_bases_'] = [base for base in bases if base is not Enum]
        return super(EnumMetaClass, meta).__new__(meta, name, bases, dict)

    def __repr__(self):
        s = self.__name__
        if self._bases_:
            s = s + '(' + ", ".join(map(lambda x: x.__name__, self._bases_)) + ')'
        if self._items_:
            list = []
            for item in self._items_:
                list.append("%s: %s" % (item.__name__, int(item)))
            s = "%s: {%s}" % (s, ", ".join(list))
        return s

    def __iter__(self):
        return ((item.__name__, int(item)) for item in self._items_)

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
        raise ValueError("%r is not a member of %s however (%s) are valid members." % (value, self.__name__,str(items)))

class EnumInstance(int):
    """Class to represent an enumeration value.

    EnumInstance('Color', 'red', 12) prints as 'Color.red' and behaves
    like the integer 12.
    """

    def __new__(cls, classname, enumname, value):
        self = super(EnumInstance, cls).__new__(cls, value)
        self.__classname = classname
        self.__enumname = enumname
        return self

    __name__ = property(lambda s: s.__enumname)        

    def __repr__(self):
        return "EnumInstance(%s, %s, %s)" % (`self.__classname`, `self.__enumname`,`int(self)`)

    def __str__(self):
        return "%s.%s" % (self.__classname, self.__enumname)

# Create the base class for enumerations.
# It is an empty enumeration.
class Enum(object):
    __metaclass__ = EnumMetaClass

if __name__ == '__main__':
    def _test():
    
        class Color(Enum):
            red = 1
            green = 2
            blue = 3
    
        print 'Color=(%s)' % str(Color)
        print '\n'
        print 'BEGIN: Iterate over the Enumeration:'
        for e in Color:
            print '\te=(%s)' % str(e)
        print 'END! Iterate over the Enumeration:\n'
            
        print 'Color.red=(%s), int(Color.red)=(%s)' % (Color.red,int(Color.red))
        print 'dir(Color)=(%s)' % str(dir(Color))
        print 'Color(1)=(%s)' % Color(1)
        try:
            print 'Color.orange=(%s)' % (Color.orange)
        except:
            print 'There is no Color.orange.'
        try:
            print 'Color(4)=(%s)' % (Color(4))
        except Exception, details:
            print 'There is no Color(4) due to "%s".' % str(details)
        x = 'Color.%s' % 'red'
        try:
            print '%s=(%s)' % (x,eval(x))
        except:
            print "There is no Color('red')."
    
        print 'Color.red == Color.red=(%s)' % Color.red == Color.red
        print 'Color.red == Color.blue=(%s)' % Color.red == Color.blue
        print 'Color.red == 1=(%s)' % (Color.red == 1)
        print 'Color.red == 2=(%s)' % (Color.red == 2)
    
        class ExtendedColor(Color):
            white = 0
            orange = 4
            yellow = 5
            purple = 6
            black = 7
    
        print 'ExtendedColor.orange=(%s)' % ExtendedColor.orange
        print 'ExtendedColor.red=(%s)' % ExtendedColor.red
    
        print 'Color.red == ExtendedColor.red=(%s)' % (Color.red == ExtendedColor.red)
    
        class OtherColor(Enum):
            white = 4
            blue = 5
    
        class MergedColor(Color, OtherColor):
            pass
    
        print 'MergedColor.red=(%s)' % MergedColor.red
        print 'MergedColor.white=(%s)' % MergedColor.white
    
        print 'Color=(%s)' % Color
        print 'ExtendedColor=(%s)' % ExtendedColor
        print 'OtherColor=(%s)' % OtherColor
        print 'MergedColor=(%s)' % MergedColor

    _test()
