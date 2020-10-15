from vyperlogix.win.registry import winreg2
from vyperlogix.win.registry.winreg2 import RegistryError

from vyperlogix.decorators import TailRecursive

#__hives__ = ['HKEY_LOCAL_MACHINE', 'HKEY_CLASSES_ROOT', 'HKEY_CURRENT_USER', 'HKEY_USERS', 'HKEY_CURRENT_CONFIG']

__hives__ = ['HKEY_LOCAL_MACHINE']

def enum_keys_from(corekey):
    i = 1
    keys = []
    while (True):
        try:
            keyname = corekey.enumkey(i)
            try:
                aKey = corekey.openkey(i)
                value = aKey.getvalue()
            except:
                aKey = None
                value = None
            finally:
                if (aKey):
                    aKey.close()
            keys.append([keyname,value])
        except:
            break
        i += 1
    return dict(keys)

#@TailRecursive.tail_recursion
def walk_node(hiveName,keyName,level):
    if (level > __max_levels__):
        return
    print '%s::%s' % (hiveName,keyName)
    root = winreg2.Registry.open(hiveName, keyName)
    i = 1
    for aKey in root.iterkeys():
        for value in root.values():
            print '\t%s=%s' % value
        try:
            corekey = root.open(keyName, aKey)
            keynames = enum_keys_from(corekey)
        except:
            corekey = None
            keynames = {}
        if (len(keynames) > 0):
            for aSubKey,aValue in keynames.iteritems():
                k = '%s\\%s' % (aKey,aSubKey)
                if (aValue):
                    print '%s::%s=%s' % (hiveName,k,aValue)
                else:
                    print '%s::%s' % (hiveName,k)
                try:
                    walk_node(hiveName, k, level+1)
                except:
                    pass
        if (corekey):
            corekey.close()
        i += 1
    root.close()

if __name__=="__main__":
    __max_levels__ = 1
    for aHiveName in __hives__:
        walk_node(aHiveName, 'SOFTWARE\Microsoft\Windows\CurrentVersion', 1)

