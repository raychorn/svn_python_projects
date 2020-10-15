import sys

class PrettyPrint:
	def __init__(self,title,items,orient,delim=' '):
		self.lines = []
		if (not isinstance(title,str)):
			print >>sys.stderr, '(PrettyPrint).ERROR :: title cannot be "%s", it must however be a string instance.' % str(title)
		else:
			if (not isinstance(items,list)):
				print >>sys.stderr, '(PrettyPrint).ERROR :: items cannot be "%s", it must however be a list instance.' % str(items)
			else:
				if (not isinstance(orient,bool)):
					print >>sys.stderr, '(PrettyPrint).ERROR :: orient cannot be "%s", it must however be a bool instance.' % str(orient)
				else:
					if (not isinstance(delim,str)):
						print >>sys.stderr, '(PrettyPrint).ERROR :: delim cannot be "%s", it must however be a string instance.' % str(delim)
					else:
						self.title = title
						self.items = items
						print title
						n = 0
						for p in items:
							if ( (isinstance(p,list)) or (isinstance(p,tuple)) ):
								n = max(n,len(p))
						stats = []
						for i in xrange(len(items)):
							stats.append(0)
						for i in xrange(len(items)):
							p = items[i]
							if ( (isinstance(p,list)) or (isinstance(p,tuple)) ):
								for ii in xrange(len(p)):
									stats[i] = max(stats[i],len(p[ii])+len(delim))
						self.lines = []
						for i in xrange(len(items)):
							p = items[i]
							if ( (isinstance(p,list)) or (isinstance(p,tuple)) ):
								aLine = []
								for ii in xrange(len(p)):
									if (not orient):
										s = '%s%s' % (' '*(stats[ii]-len(p[ii])),p[ii])
									else:
										s = '%s%s' % (p[ii],' '*(stats[ii]-len(p[ii])))
									if (ii == (len(p)-1)):
										s = s.rstrip()
									aLine.append(s)
								self.lines.append(delim.join(aLine))
					
	def pprint(self):
		print '\n'.join(self.lines)

	def __repr__(self):
		return 'PrettyPrint for "%s"' % (self.title)
