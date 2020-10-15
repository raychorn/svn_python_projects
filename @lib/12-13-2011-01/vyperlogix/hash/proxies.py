from vyperlogix.classes.CooperativeClass import Cooperative
from vyperlogix.hash import lists

class HashedListsProxy(Cooperative):
    def __init__(self):
        self.d_cache = lists.HashedLists()
    
    def get_item(self,key):
        return self.d_cache[key]
    
    def set_item(self,key,value):
        self.d_cache[key] = value

    def get_size(self):
        return len(self.d_cache)

    def get_keys(self):
        return self.d_cache.keys()
