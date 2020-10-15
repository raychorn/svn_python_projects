import OneWayNode
import AbstractLinkage

class OneWayLinkage(AbstractLinkage.AbstractLinkage):
    def __init__(self, data):
	self.__head = OneWayNode.OneWayNode(data)
	self.__tail = self.__head

    def append(self, data):
	self.tail.next = OneWayNode.OneWayNode(data)
	self.__tail = self.tail.next

    def get_head(self):
	return self.__head
    
    def get_tail(self):
	return self.__tail
    
    def dumpNodes(self):
	self.__dumpNodes__(self.head)
    
    head = property(get_head)
    tail = property(get_tail)
