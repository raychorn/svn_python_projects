import types
import copy

class odict(dict):
    """ Ordered dictionary class - the best of both worlds?
    """
    def __init__(self, d={}):
        self._keys = d.keys()
        dict.__init__(self, d)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._keys.remove(key)
        return

    def __setitem__(self, key, item):
        dict.__setitem__(self, key, item)
        # a peculiar sharp edge from copy.deepcopy
        # we'll have our set item called without __init__
        if not hasattr(self, '_keys'):
            self._keys = [key,]
        if key not in self._keys:
            self._keys.append(key)
        return
    
    def __iter__(self):
        return iter(self.values())
    
    def clear(self):
        dict.clear(self)
        self._keys = []
        return
    
    def items(self):
        for i in self._keys:
            yield i, self[i]
        return
    
    def keys(self):
        return self._keys
    
    def popitem(self):
        if len(self._keys) == 0:
            raise KeyError('dictionary is empty')
        else:
            key = self._keys[-1]
            val = self[key]
            del self[key]
            return key, val
        
    def setdefault(self, key, failobj = None):
        dict.setdefault(self, key, failobj)
        if key not in self._keys:
            self._keys.append(key)
        return
    
    def update(self, d):
        for key in d.keys():
            if not self.has_key(key):
                self._keys.append(key)
        dict.update(self, d)
        return
    
    def insert(self, idx, key, item):
        if key in self._keys:
            remIdx = self._keys.index(key)
            self._keys[remIdx]
            del self[key]
        self._keys.insert(idx, key)
        self[key] = item
        return
    
    def values(self):
        valList = []
        for i in self._keys:
            valList.append(copy.copy(self[i]))
            continue
        return valList
    
    def move(self, key, index):

        """ Move the specified to key to *before* the specified index. """

        try:
            cur = self._keys.index(key)
        except ValueError:
            raise KeyError(key)
        self._keys.insert(index, key)
        # this may have shifted the position of cur, if it is after index
        if cur >= index: cur = cur + 1
        del self._keys[cur]
        return
    
    def reverse(self):
        self._keys.reverse()
        return
    
    def sort(self, cmpFunc=None):
        self._keys.sort(cmpFunc)
        return
    
    def index(self, key):
        if not self.has_key(key):
            raise KeyError(key)
        return self._keys.index(key)

                
            
