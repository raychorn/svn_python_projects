import sys
import urlimport

_lib_root = r'z:\python projects\@lib'

sys.path.insert(0,_lib_root)

from vyperlogix.lists.ListWrapper import ListWrapper

l = ListWrapper([p.lower() for p in sys.path])
removable = [p.lower() for p in sys.path if (p.lower().find(r'z:\python projects') > -1) and (p.lower().find('urlimport') == -1) and (p.lower().find('_pyax-') == -1)]
if (len(removable) > 0):
    print 'removable: ', removable
    while (len(removable) > 0):
        p = removable.pop()
        i = l.findFirstContaining(p)
        if (i > -1):
            print 'Removed: ', sys.path[i]
            del sys.path[i]
            #sys.path.insert(i,'http://secure-code.vyperlogix.com/')
            l = ListWrapper(sys.path)

_lib_url = 'http://secure-code.vyperlogix.com/'

sys.path.append(_lib_url)

for p in sys.path:
    print p
    
urlimport.settings[_lib_root] = _lib_url
print urlimport.settings

sys.path_importer_cache.clear()

from vyperlogix import misc

print misc.callersName()

from vyperlogix.products import keys

s = 'now is the time'
e = keys._encode(s)
p = keys._decode(e)
print e, p
assert s == p, 'Oops, cannot validate that product keys can be encoded/decoded.'

from vyperlogix.enum import Enum

class MyTypes(Enum.EnumLazy):
    none = 0
    one = 1
    two = 2
    
print MyTypes.none, MyTypes.one, MyTypes.two
