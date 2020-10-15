class clist(list):
    """ case insensitive list
    
    does not consider case when executing __contains__ or index
    """
    def __normalize_elt(self, elt):
        nelt = elt
        if type(elt) == types.StringType:
            nelt = elt.lower()
            pass
        return nelt
    
    def __contains__(self, value):
        return str(value).lower() in self.__lower_list()
    
    def index(self, value):
        lowerlist = self.__lower_list()
        return lowerlist.index(str(value).lower())
    
    def __lower_list(self):
        list_as_str = '\v'.join(self).lower()
        return list_as_str.split('\v')
    
    def __repr__(self):
        return "clist(%s)" % (','.join([str(item) for item in self]))
        
    pass
        