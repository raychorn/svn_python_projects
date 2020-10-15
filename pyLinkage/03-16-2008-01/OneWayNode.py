from vyperlogix import CooperativeClass

class OneWayNode(CooperativeClass.Cooperative):
    def __init__(self, data):
	self.__data = data
	self.__next = 0
    
    def __repr__(self):
	return '(%s) on %s.' % (str(self.__class__),self.data)
    
    def get_data(self):
	return self.__data
    
    def set_data(self,data):
	self.__data = data
    
    def get_next(self):
	return self.__next
    
    def set_next(self,ptr):
	self.__next = ptr
    
    data = property(get_data, set_data)
    next = property(get_next, set_next)

