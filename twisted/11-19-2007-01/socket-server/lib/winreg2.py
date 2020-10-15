import _winreg as wreg

class KEY:
    'Mode Constants'
    QUERY_VALUE = 1
    SET_VALUE = 2
    CREATE_SUB_KEY = 4
    ENUMERATE_SUB_KEYS = 8
    NOTIFY = 16
    CREATE_LINK = 32
    WRITE = 131078
    EXECUTE = 131097
    READ = 131097
    ALL_ACCESS = 983103

################################################################################

class _Value(object):

    '_Value(value) -> _Value'

    def __init__(self, value):
        'Initialize the _Value object.'
        self.__value = value
        self.__repr = '%s(%r)' % (self.__class__.__name__, value)

    def __repr__(self):
        'Return the object\'s representation.'
        return self.__repr

    def __get_value(self):
        'Private class method.'
        return self.__value

    value = property(__get_value, doc='Value of this object.')

class REG_NONE(_Value): pass
class REG_SZ(_Value): pass
class REG_EXPAND_SZ(_Value): pass
class REG_BINARY(_Value): pass
class REG_DWORD(_Value): pass
class REG_DWORD_BIG_ENDIAN(_Value): pass
class REG_LINK(_Value): pass
class REG_MULTI_SZ(_Value): pass
class REG_RESOURCE_LIST(_Value): pass
class REG_FULL_RESOURCE_DESCRIPTOR(_Value): pass
class REG_RESOURCE_REQUIREMENTS_LIST(_Value): pass
class REG_QWORD(_Value): pass

################################################################################

class RegistryError(Exception):
    """ An exception class for Registry """
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    
class Registry(object):
    """ A class which abstracts away operations on Windows
    registry. This class provides a way to work with Windows
    registry without using _winreg directly.

    A Windows registry key is represented by the internal
    class named RegistryKey. A number of operations of this
    class returns and works with instances of RegistryKey.
    """
    
    def __init__(self):
        pass

    def map_key(self, key):
        """ Map key names to Windows registry key constants """
        
        if type(key) is not str:
            raise RegistryError,"key must be a string object"
        else:
            try:
                return eval('wreg.' + key)
            except AttributeError:
                return None
            
    class RegistryKey(object):
        """ An internal class of Registry which abstracts a Windows
        registry key """

        def __init__(self):
            # The actual PyHKEY object returned by _winreg
            self._hkey = None
            # The name of the key
            self._keyname = ''
            self.TYPES = REG_NONE, REG_SZ, REG_EXPAND_SZ, REG_BINARY, REG_DWORD, REG_DWORD_BIG_ENDIAN, REG_LINK, REG_MULTI_SZ, REG_RESOURCE_LIST, REG_FULL_RESOURCE_DESCRIPTOR, REG_RESOURCE_REQUIREMENTS_LIST, REG_QWORD
            
        def open(self, key, subkey):
            """ Opens a Windows registry key. The first param is one of the
            Windows HKEY names or an already open key. The second param
            is the actual key to open. """
            
            if type(key) is str:
                hkey = Registry.map_key(key)
            else:
                hkey = key
                
            if not hkey: raise RegistryError,"could not find registry key for %s" % key
            try:
                self._hkey = wreg.OpenKey(hkey, subkey)
                self._keyname = subkey
            except EnvironmentError, e:
                raise RegistryError, e
            
        def create(self, key, subkey):
            """ Creates or opens a Windows registry key. The first param
            is one of the Windows HKEY names or an already open key. The
            second param is the actual key to create/open. """
            
            if type(key) is str:
                hkey = Registry.map_key(key)
            else:
                hkey = key
                
            if not hkey: raise RegistryError,"could not find registry key for %s" % key
            try:
                self._hkey = wreg.CreateKey(hkey, subkey)
                self._keyname = subkey
            except EnvironmentError, e:
                raise RegistryError, e

        def openkey(self, index, sam=):
            """ Open the sub-key at the given index and return
            the created RegistryKey object """

            # NOTE: The index is starting from 1,not zero!
            
            subkey = self.enumkey(index-1)
            if subkey:
                r = Registry.RegistryKey()
                r.setkey(wreg.OpenKey(self._hkey, subkey))
                r.setkeyname(subkey)
                return r
            else:
                raise RegistryError,'No sub-key found at index %d!' % index
            
        def enumkey(self, index):
            """ Enumerate the subkeys of the currently open key """
            
            if not self._hkey: raise RegistryError,"Error: null key"
            try:
                return wreg.EnumKey(self._hkey, index)
            except EnvironmentError, e:
                raise RegistryError, e

        def enumvalue(self, index):
            """ Enumerate the values of the currently open key """

            if not self._hkey: raise RegistryError,"Error: null key"
            try:
                t = wreg.EnumValue(self._hkey, index)
                return t[0], self.TYPES[t[-1]](t[1])
            except EnvironmentError, e:
                raise RegistryError, e

        def keys(self):
            """ Return the subkeys of the current key as a list """

            # This method works just like the 'keys' method
            # of a dictionary object.
            keylist, idx = [], 0
            while True:
                try:
                    subkey=self.enumkey(idx)
                    keylist.append(subkey)
                    idx += 1
                except RegistryError:
                    break

            return keylist

        def values(self):
            """ Return the subvalues of the current key as a list """

            # This method works just like the 'values' method
            # of a dictionary object.
            valuelist, idx = [], 0
            while True:
                try:
                    value=self.enumvalue(idx)
                    valuelist.append(value)
                    idx += 1
                except RegistryError:
                    break

            return valuelist

        def items(self):
            """ Return a list of (key,value) pairs for each subkey in the
            current key """

            # This method works just like the 'items' method
            # of a dictionary object.
            items, idx = [], 0
            while True:
                try:
                    key, value = self.enumkey(idx), self.enumvalue(idx)
                    items.append((key, value))
                    idx += 1
                except RegistryError:
                    break

            return items
            
        def iterkeys(self):
            """ Return an iterator over the list of subkeys of the current key """

            # Note: this is a generator
            # This method works just like the 'iterkeys' method
            # of a dictionary object.            
            idx = 0
            while True:
                try:
                    yield self.enumkey(idx)
                    idx += 1
                except RegistryError:
                    break

        def itervalues(self):
            """ Return an iterator over the list of subvalues of the current key """
               
            # Note: this is a generator
            # This method works just like the 'itervalues' method
            # of a dictionary object.                        
            idx = 0
            while True:
                try:
                    yield self.enumvalue(idx)
                    idx += 1
                except RegistryError:
                    break

        def iteritems(self):
            """ Return an iterator over the (subkey,subvalue) pairs of the current key"""

            # Note: this is a generator
            # This method works just like the 'iteritems' method
            # of a dictionary object.                        
            idx = 0
            while True:
                try:
                    yield (self.enumkey(idx), self.enumvalue(idx))
                    idx += 1
                except RegistryError:
                    break

        def getvalue(self, name=''):
            """ Return the value of an item inside the current key,
            given its name """
            
            try:
                if name:
                    return wreg.QueryValueEx(self._hkey, name)
                else:
                    return wreg.QueryValue(self._hkey, '')
            except (WindowsError, EnvironmentError), e:
                raise RegistryError, e

        def setvalue(self, name, value):
            """ Sets the named value """
            try:
                if isinstance(value, self.TYPES):
                    wreg.SetValueEx(self._hkey, name, 0, list(self.TYPES).index(value.__class__), value.value)
                else:
                    wreg.SetValueEx(self._hkey, name, 0, wreg.QueryValueEx(self._hkey, name)[1], value)

            except (WindowsError, EnvironmentError), e:
                raise RegistryError, e

        def hasvalue(self, name=''):
            """ Return True if the current key has a value named
            'name', False otherwise """
            
            try:
                if name:
                    wreg.QueryValueEx(self._hkey, name)
                else:
                    wreg.QueryValue(self._hkey, '')
                return True
            except (WindowsError, EnvironmentError), e:
                return False
            
        def getkey(self):
            """ Return the embedded PyHKEY object of this key """
            
            return self._hkey

        def getkeyname(self):
            """ Return the name of this key """
            
            return self._keyname
        
        def setkey(self, hkey):
            """ Set the PyHKEY object of this key """
            
            self._hkey = hkey

        def setkeyname(self, keyname):
            """ Set the keyname for this key """

            self._keyname = keyname
            
        def close(self):
            """ Close this key """
            
            if self._hkey:
                wreg.CloseKey(self._hkey)

    def open(self, key, subkey):
        """ Open a windows registry key. Same
        as OpenKey of _winreg """
        
        regkey = Registry.RegistryKey()
        regkey.open(key, subkey)
        return regkey

    def create(self, key, subkey):
        """ Create a windows registry key. Same
        as CreateKey of _winreg """
        
        regkey = Registry.RegistryKey()
        regkey.create(key, subkey)
        return regkey

    def delete(self, key, subkey):
        """ Deletes a windows registry key. Same
        as DeleteKey of _winreg """
        
        if type(key) is str:
            hkey = self.map_key(key)
        else:
            hkey = key
            
        if not hkey: raise RegistryError,"could not find registry key for %s" % key
        try:
            wreg.DeleteKey(hkey, subkey)
        except EnvironmentError, e:
            raise RegistryError, e

    def rdelete(self, key, subkey):
        """ Recursively delete a Windows registry key.
        This function will remove a key, even if it
        has child keys. There is no equivalent in
        _winreg. """
        
        if type(key) is str:
            hkey = Registry.map_key(key)
        elif type(key) is Registry.RegistryKey:
            hkey = key.getkey()
        else:
            hkey = key
            
        if type(subkey) is str:
            subkey  = self.open(hkey, subkey)
                
        # test2
        childkeys = subkey.keys()
        for keyname in childkeys:
            # print 'Child=>',keyname
            childkey = self.open(subkey.getkey(), keyname)
            self.rdelete(subkey, childkey)

        # print subkey.getkeyname()
        wreg.DeleteKey(hkey, subkey.getkeyname())

    open = classmethod(open)
    create = classmethod(create)
    delete = classmethod(delete)
    map_key = classmethod(map_key)
    rdelete = classmethod(rdelete)    
    
if __name__=="__main__":
    key = Registry.open('HKEY_LOCAL_MACHINE', "SOFTWARE\\Python")
    # Prints the RegistryKey instance
    print 'key=(%s)' % str(key)
    # Prints the key name and the wrapped up PyHKEY instance
    print 'key.getkeyname()=(%s)' % str(key.getkeyname())
    print 'key.getkey()=(%s)' % str(key.getkey())
    corekey = key.openkey(1)

    idx = 0
    while True:
        try:
            keyname = corekey.enumkey(idx)
            idx += 1
            print '(%s) :: keyname=(%s)' % (idx,keyname)
            if (float(str(keyname)) > 0.0):
                keyVersion = corekey.openkey(idx)
                print 'keyVersion=(%s)' % keyVersion
                print 'keyVersion.getkeyname()=(%s)' % keyVersion.getkeyname()
                keyPath = keyVersion.openkey(2)
                print 'keyPath=(%s)' % keyPath
                print 'keyPath.getkeyname()=(%s)' % keyPath.getkeyname()
                print 'Install path is %s' % keyPath.getvalue()
                keyPath.close()
                keyVersion.close()
                break
        except RegistryError:
            break

    corekey.close()
    key.close()

