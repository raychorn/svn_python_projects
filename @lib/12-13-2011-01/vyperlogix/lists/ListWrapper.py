import UserList

from vyperlogix import misc

class ListWrapper(UserList.UserList):
    def appendAll(self,item_or_list):
	item_or_list = item_or_list if (misc.isList(item_or_list)) else [item_or_list]
	for anItem in item_or_list:
	    self.append(anItem)
    
    def reverse(self):
	l = misc.reverse(self.data)
	while (len(self) > 0):
	    self.pop()
	for item in l:
	    self.append(item)
	return self
    
    def reverseCopy(self):
	return ListWrapper(misc.reverseCopy(self.data))
    
    def reverseDigits(self):
	self.data = misc.reverseDigitsList(self.data)
	return self
    
    def sort(self):
	self.data = misc.sort(self.data)
	return self
    
    def sortCopy(self):
	return ListWrapper(misc.sortCopy(self.data))
    
    def insert(self,index,value):
	return misc.insert(self.data,index,value)
    
    def insertCopy(self,index,value):
	return ListWrapper(misc.insertCopy(self.data,index,value))
    
    def find(self,item):
	return misc.findInListSafely(self.data,item)

    def findFirstContaining(self,s_search,callback=None,returnIndexes=True):
	return misc.findFirstContaining(self.data,s_search,callback=callback,returnIndexes=returnIndexes)
    
    def findAllContaining(self,s_search,callback=None,returnIndexes=False,itemHandler=None):
	return misc.findAllContaining(self.data,s_search,callback=callback,returnIndexes=returnIndexes,itemHandler=None)
    
    def findFirstMatching(self,s_search,callback=None,returnIndexes=True):
	return misc.findFirstMatching(self.data,s_search,callback=callback,returnIndexes=returnIndexes)
    
    def findAllMatching(self,s_search,callback=None,returnIndexes=False):
	return misc.findAllMatching(self.data,s_search,callback=callback,returnIndexes=returnIndexes)
    
    def asSet(self):
	return set(self.data)

    def copy(self):
	return ListWrapper(misc.copy(self.data))
    
    def copy_excluding_with(self,index,selector):
	_tags = []
	d = {}
	_contents = []
	_contents.append(self[index])
	for _i in xrange(0,len(self)):
	    if (_i != index):
		_tag_ = eval('self[_i].%s' % (selector))
		_tags.append(_tag_)
		d[_tag_] = self[_i]
	_tags = misc.sortCopy(_tags)
	for aTag in _tags:
	    _contents.append(d[aTag])
	return _contents

class CircularList(ListWrapper):
    def next(self):
        try:
            return self.__cycler__.next()
        except AttributeError:
            import itertools 
            self.__cycler__ = itertools.cycle(self)
            return self.next()

class SeqentialList(ListWrapper):
    def next(self):
        try:
            return self.__cycler__.next()
        except AttributeError:
	    def iterate():
		for item in self:
		    yield item
		yield None
            self.__cycler__ = iterate()
            return self.next()
	except StopIteration:
	    return None

class SmartList(ListWrapper):
    def findFirstMatching(self,s_search,callback=None,returnIndexes=True):
	return misc.findFirstMatching(self.data,s_search,callback=callback,returnIndexes=returnIndexes)
