import types

class cdict (dict):
    """ Case insensitive dictionary
    
    Keeps a separate map of lower case keys
    
    """
    def __new__(cls, d={}):
        return dict.__new__(cls, d)
    
    def __init__(self, d={}):
        """ Inits the dictionary, but first maps lowercase keys to their 
        original case
        """
        self.key_case_map = {}
        for key in d.keys():
            if type(key) == types.StringType:
                self.key_case_map[key.lower()] = key
                pass
            continue
        dict.__init__(self, d)
        return
    
    def __normalizeKey(self, key):
        nkey = key
        try:
            nkey = key.lower()
        except:
            pass
        return nkey
    
    def __setitem__ (self, key, value):
        nkey = self.__normalizeKey(key)
        # handle instance where we're setting a duplicate key of the same case
        if self.key_case_map.has_key(nkey) and key != self.key_case_map[nkey]:
            dict.__delitem__(self, self.key_case_map[nkey])
            pass
        # now, add the case mapping and set the item
        self.key_case_map[nkey] = key
        dict.__setitem__(self, key, value)

    def __getitem__ (self, key):
        nkey = self.__normalizeKey(key)
        return dict.__getitem__(self, self.key_case_map[nkey])
    
    def __delitem__(self, key):
        nkey = self.__normalizeKey(key)
        dict.__delitem__(self, self.key_case_map[nkey])
        self.key_case_map[nkey]
        return
    
    def __copy__(self):
        return cdict(self)
    
    def __deepcopy__(self, memo):
        return cdict(self)

    def get (self, key, default=None):
        okey = self.key_case_map.get(self.__normalizeKey(key), default)
        if okey is None or dict.__contains__(self, okey) is False:
            return default
        else:
            return dict.__getitem__(self, okey)

    def __contains__ (self, key):
        nkey = self.__normalizeKey(key)
        if self.key_case_map.has_key(nkey):
            return dict.has_key(self, self.key_case_map[nkey])
        return False
    
    def has_key(self, key):
        return self.__contains__(key)
    
    def clear(self):
        dict.clear(self)
        self.key_case_map = {}
        return

    def update(self, udict={}):
        for key, value in udict.items():
            self.__setitem__(key, value)
            continue
        return
    
    def popitem(self):
        (key, value) = dict.popitem(self)
        self.key_case_map[self.__normalizeKey(key)]
        return (key, value)
    
    def pop(self, key):
        value = self[key]
        del self[key]
        
    def copy(self):
        return self.__copy__()
    
    def extractSensitiveDict(self):
        """ Returns a plain case-sensitive dictionary with the current values
        
        All keys will have the case as initially inserted
        
        @return: dictionary of all values
        @rtype: Dictionary
        """ 
        return dict.copy(self)