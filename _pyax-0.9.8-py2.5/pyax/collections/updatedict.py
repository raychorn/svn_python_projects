import copy
from pyax.collections.cdict import cdict

FTN_KEY = 'fieldsToNull'

class UpdateDict(object):
    """A Dictionary that tracks changes to its items
    
    @note: deletion of dictionary items is handled in a way specific to
           Salesforce.com in that deleted fields are kept track in a 
           separate item named 'fieldsToNull'
    """
 
    def __init__(self, init_dict={}):
        self._initialize(init_dict)
        return
    
    def _initialize(self, init_dict):
        """A super-update of the instance
        
        @param initDict: Dictionary with which to replace all instance data 
        
        @postcondition: __origDataMap will contain only data from initDict     
        """
        self.__orig_data_dict = cdict()
        self.__orig_data_dict.update(dict(init_dict))

        self.clear()
        return
    ## END _initialize
    
    def _mergeView(self):
        """ Current view of the dictionary (including all updates)
        
        @return: union of the original dictionary plus any updates
        @rtype: cdict
        """
        merge_data_dict = copy.deepcopy(self.__orig_data_dict)
        update_copy = copy.deepcopy(self.__update_dict)
        fieldsToNull = update_copy.get(FTN_KEY)
        if fieldsToNull is not None:
            del update_copy[FTN_KEY]

            for field in fieldsToNull:
                update_copy[field] = None
                continue
            pass
            
        merge_data_dict.update(update_copy)
        
        return cdict(merge_data_dict)
    ## END _mergeView
    
    def clear(self, key=None):
        """Clear any stored updates leaving only the original data
        
        @param key: (optional) only clear updates to the specified field
        """
        if key is None:
            # clear all updates
            self.__fields_to_null = []
            self.__update_dict = cdict({FTN_KEY: self.__fields_to_null})

        else:
            # clear change to just a single field
            if key in self.__fields_to_null:
                self.__fields_to_null.remove(key)
                pass
            
            if self.__update_dict.has_key(key):
                del self.__update_dict[key]
                pass
        return
    
    def getUpdates(self):
        """ Returns a case-sensitive copy of the pending updates dictionary
        
        @return: Uncommited updates
        @rtype: Dictionary
        """
        #return copy.deepcopy(self.__update_dict)
        return self.__update_dict.extractSensitiveDict()
    ## END getUpdates
    
    def commit(self):
        """ Incorporate all pending updates into the original data
        
        @postcondition: instance will be re-initialized with the merged
                        original data plus any updates
        """
        self._initialize(self._mergeView())
        return
    ## END commit
    
    def __str__(self):
        return str(self._mergeView())
    ## END __str__
    
    def __repr__(self):
        return str(self)
    ## END __repr__
    
    def __len__(self):
        return len(self.keys())
    ## END __len__
    
    def __getitem__(self, key):
        if key in self.__update_dict[FTN_KEY]:
            return None
        elif self.__update_dict.has_key(key):
            return self.__update_dict[key]
        elif self.__orig_data_dict.has_key(key):
            return self.__orig_data_dict[key]
        else:
            raise KeyError("Key '%s' not found" %key)
        
        return None # should never reach here
    ## END __getitem__
    
    def __setitem__(self, key, value):
        global FTN_KEY
        # don't allow external manipulation of fieldsToNull
        if key == FTN_KEY:
            raise KeyError
        
        # if we had set this field to null previously, unset it
        if key in self.__fields_to_null:
            self.__fields_to_null.remove(key)
            pass

        self.__update_dict[key] = value
        return
    ## END __setitem__
        
    def __delitem__(self, key):
        """ Marks a field to be nulled. 
        
        Unlike a regular dictionary, if the key doesn't exist in the 
        UpdateDict instance anywhere, it is still added to the __fieldsToNull
        member and KeyError will not be raised.
        
        @param key: field name to clear when update is issued
        """
        global FTN_KEY
        # don't allow deletion of fieldsToNull
        if key == FTN_KEY:
            # FIXME - is this the right exception?
            raise KeyError

        if self.__update_dict.has_key(key):
            del self.__update_dict[key]
            pass
        
        if key not in self.__fields_to_null:
            self.__fields_to_null.append(key)
            pass
        
        return
    ## END __delitem__
        
    def __contains__(self, key):
        return key in self.keys()
    ## END contains
        
    def update(self, update_src_dict):
        self.__update_dict.update(update_src_dict)
        return
    ## END update
    
    def setdefault(self, key, default_value=None):
        if not self.has_key(key):
            self[key] = default_value
            pass
        
        return self.get(key)
    ## END setdefault
    
    def get(self, key, default_value=None):
        retval = default_value
        if self.has_key(key):
            retval = self.__getitem__(key)
            pass
        return retval
    ## END get
        
    # pop & popitem don't make sense for this dictionary-like mapping object
    
    def keys(self):
        return self._mergeView().keys()
    ## END keys
    
    def __iter__(self):
        return iter(self.keys())
    ## END __iter__
    
    # also make __iter__ available as iterkeys
    iterkeys = __iter__
    
    def values(self):
        return self._mergeView().values()
    ## END values
        
    def itervalues(self):
        return iter(self.values())
    ## END itervalues

    def items(self):
        return self._mergeView().items()
    ## END items
    
    def iteritems(self):
        return iter(self.items())
    ## END iteritems

    def copy(self):
        raise NotImplementedError
    ## END copy
    
    def has_key(self, key):
        return key in self
    ## END has_key
