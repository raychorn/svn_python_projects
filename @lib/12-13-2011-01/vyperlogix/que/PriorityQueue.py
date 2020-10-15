import bisect

class PriorityQueue:
	def __init__(self):
		self.queue = []
	def append(self,data,priority):
		"""append a new element to the queue according to its priority"""
		bisect.insort(self.queue,(priority,data))
	def pop(self,n):
		"""pop the hightest element of the queue. The n argument is
		here to follow the standard queue protocol """
		return self.queue.pop(0)[1]
