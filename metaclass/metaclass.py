# metaclass programming samples

# Method 1

class _TempMetaclass(type):
    pass

class B:
    __metaclass__ = _TempMetaclass # or: type('temp', (type, ), {})
    
    
class MetaClass(type):
    def __init__(cls, *a, **kw):
        super(MetaClass, cls).__init__(*a, **kw)
        cls._actual_init(*a, **kw)
    def _actual_init(cls, *a, **kw):
        # actual initialization goes here
        pass
        
        
B.__class__ = MetaClass
MetaClass._actual_init(B, B.__name__, B.__bases__, B.__dict__)

# This method simple performs a type-cast for the object.


# Simpler method...
# Maintain data for each Class in the form of a Python dict and then either shallow or deep copy the contents from one object instance into another to perform a quick type-cast.


# Another method - this method takes more runtime to complete for each dynamic metaclass change than the simpler method.

import types
NewClass = types.ClassType('NewClass', (object, ), {'__metaclass__':MetaClass})

# Then just copy all the old methods over:

for item in dir(OldClass):
    setattr(NewClass, item, getattr(OldClass, item))
    
# Subclass method.

# You can simply subclass to make a dynamic change to a metaclass.  Class objects can be created dynamically and methods can be injected into newly created object instances.

# See also: https://blog.ionelmc.ro/2015/02/09/understanding-python-metaclasses/
