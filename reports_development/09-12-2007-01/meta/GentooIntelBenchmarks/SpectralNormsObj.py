class SpectralNormsObj(object):
	def __init__(self,id,name,cpu_rank,ram_use,gzip_bytes):
		self.id = id
		self.name = name
		self.cpu_rank = cpu_rank
		self.ram_use = ram_use
		self.gzip_bytes = gzip_bytes

def __repr__(self):
	return "<SpectralNorms(%r,%r,%r,%r,%r)>" % (self.id,self.name,self.cpu_rank,self.ram_use,self.gzip_bytes)
