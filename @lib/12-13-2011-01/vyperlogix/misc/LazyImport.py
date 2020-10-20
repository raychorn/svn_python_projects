from vyperlogix.classes.CooperativeClass import Cooperative
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc.ObjectTypeName import __typeName as ObjectTypeName__typeName
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

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

class LazyImport(Cooperative):

    """ LazyImport class.

        LazyImports are imported into the given namespaces whenever a
        non-special attribute (there are some attributes like __doc__
        that class instances handle without calling __getattr__) is
        requested. The module is then registered under the given name
        in locals usually replacing the import wrapper instance. The
        import itself is done using globals as global namespace.

        Example of creating a lazy import object:

        ISO = LazyImport('ISO',locals(),globals())

        Later, requesting an attribute from ISO will load the module
        automatically into the locals() namespace, overriding the
        LazyImport instance:

        t = ISO.Week(1998,1,1)

    """
    # Flag which inidicates whether the LazyImport is initialized or not
    __lazyimport_init = 0

    # Name of the module to load
    __lazyimport_name = ''

    # Flag which indicates whether the module was loaded or not
    __lazyimport_loaded = 0

    # Locals dictionary where to register the module
    __lazyimport_locals = None

    # Globals dictionary to use for the module import
    __lazyimport_globals = None

    def __init__(self, name, locals={}, globals=None):

        """ Create a LazyImport instance wrapping module name.

            The module will later on be registered in locals under the
            given module name.

            globals is optional and defaults to locals.
        
        """
        self.__dict__ = lists.HashedLists2(self.__dict__)
        self.__lazyimport_locals = lists.HashedLists2(locals)
        if (globals is None):
            globals = lists.HashedLists2(locals)
        elif (lists.isDict(globals)):
            globals = lists.HashedLists2(globals)
        self.__lazyimport_globals = globals
        mainname = globals.get('__name__', '') if (globals.has_key('__name__')) else None
        if (mainname):
            self.__name__ = mainname + '.' + name
            self.__lazyimport_name = name
        else:
            self.__name__ = self.__lazyimport_name = name
        self.__lazyimport_init = 1

    def __lazyimport_import(self):

        """ Import the module now.
        """
        # Load and register module
        name = self.__lazyimport_name
        if (self.__lazyimport_loaded):
            return self.__lazyimport_locals[name]
        if (_utils.isBeingDebugged) and (_utils.isVerbose):
            print '%s: Loading module %r' % (ObjectTypeName.typeName(self),name)
        self.__lazyimport_locals[name] \
             = module \
             = __import__(name,
                          self.__lazyimport_locals,
                          self.__lazyimport_globals,
                          '*')

        # Fill namespace with all symbols from original module to
        # provide faster access.
        self.__dict__.update(module.__dict__)

        # Set import flag
        self.__dict__['__lazyimport_loaded'] = 1

        if (_utils.isBeingDebugged) and (_utils.isVerbose):
            print '%s: Module %r loaded' % (ObjectTypeName.typeName(self),name)
        return module

    def __getattr__(self, name):

        """ Import the module on demand and get the attribute.
        """
        if (self.__lazyimport_loaded):
            raise AttributeError, name
        if (_utils.isBeingDebugged) and (_utils.isVerbose):
            print '%s: Module load triggered by attribute %r read access' % (ObjectTypeName.typeName(self),name)
        module = self.__lazyimport_import()
        try:
            return getattr(module, name)
        except:
            return module

    def __setattr__(self, name, value):

        """ Import the module on demand and set the attribute.
        """
        if (not self.__lazyimport_init):
            self.__dict__[name] = value
            return
        if (self.__lazyimport_loaded):
            self.__lazyimport_locals[self.__lazyimport_name] = value
            self.__dict__[name] = value
            return
        if (_utils.isBeingDebugged) and (_utils.isVerbose):
            print '%s: Module load triggered by attribute %r write access' % (ObjectTypeName.typeName(self),name)
        module = self.__lazyimport_import()
        setattr(module, name, value)

    def __repr__(self):
        return "<%s '%s'>" % (ObjectTypeName__typeName(self.__class__),self.__name__)
