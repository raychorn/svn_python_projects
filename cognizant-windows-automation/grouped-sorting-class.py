import os,sys
import random
import UserList

def __ascending__(a,b):
    if (a < b):
        return -1
    elif (a > b):
        return 1
    return 0

def __descending__(a,b):
    if (a < b):
        return 1
    elif (a > b):
        return -1
    return 0

class GroupedSort(UserList.UserList):
    def sortOn(self,keys):
        self.__keys__ = keys
        iK = 0
        self.__grouping__ = [self]
        while (iK < len(self.__keys__)):
            __groups__ = []
            for group in self.__grouping__:
                _key_ = self.__keys__[iK].get('key','')
                __comparator__ = self.__keys__[iK].get('cmp',lambda a,b:0)
                group.sort(cmp=__comparator__,key=lambda d: d[_key_])
                keys = list(set([item.get(_key_,'') for item in group]))
                keys.sort(cmp=__comparator__)
                for key in keys:
                    subgroup = [item for item in group if (item.get(_key_,'') == key)]
                    __groups__.append(subgroup)
            self.__grouping__ = []
            for g in __groups__:
                self.__grouping__.append(g)
            iK +=1
        __groups__ = []
        for group in self.__grouping__:
            item = group
            if (isinstance(item,list)):
                item = item[0]
            __groups__.append(item)
        self.__grouping__ = __groups__

    def __repr__(self):
        import StringIO
        ioBuf = StringIO.StringIO()
        print >>ioBuf, 'BEGIN:'
        _t_ = self.grouping[0]['b']
        for group in self.grouping:
            if (group['b'] != _t_):
                print >>ioBuf, ''
                _t_ = group['b']
            print >>ioBuf, str(group)
        print >>ioBuf, 'END!!!'
        return ioBuf.getvalue()

    def grouping():
        doc = "returns __grouping__"
        def fget(self):
            return self.__grouping__
        return locals()
    grouping = property(**grouping())
    
if (__name__ == __main__):
    __data__ = GroupedSort()
    for i in xrange(20):
        __data__.append({'a':i+1,'b':random.choice(['a','b','c','d']),'type':random.choice(['Linux','Windows'])})
        
    __keys__ = []
    
    __keys__.append({'key':'type','cmp':__ascending__})
    __keys__.append({'key':'b','cmp':__descending__})
    __keys__.append({'key':'a','cmp':__ascending__})
    
    __data__.sortOn(__keys__)
    
    print str(__data__)

