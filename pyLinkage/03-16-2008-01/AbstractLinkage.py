from vyperlogix import CooperativeClass

class AbstractLinkage(CooperativeClass.Cooperative):
    def __dumpNodes__(self, head):
	print head
	if (head.next):
	    self.__dumpNodes__(head.next)

