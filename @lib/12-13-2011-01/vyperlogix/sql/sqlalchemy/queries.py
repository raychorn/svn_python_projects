import UserList

class QueryWrapper(UserList.UserList):
    '''This Class exists to facilitate the process of choosing items from a SQLAlchemy Query Object.'''
    def __init__(self, qry):
        self.__qry__ = qry

    def __getitem__(self, i):
        return self.qry[i]
    
    def __setitem__(self, i, item): 
        raise NotImplementedError('Cannot set an item at this time.  This is a Wrapper that facilitates choosing items from a Query Object.')
        
    def __delitem__(self, i): 
        raise NotImplementedError('Cannot delete an item at this time.  This is a Wrapper that facilitates choosing items from a Query Object.')

    def __len__(self): 
        return int(self.qry.count())

    def qry():
        doc = "qry"
        def fget(self):
            return self.__qry__
        return locals()
    qry = property(**qry())

