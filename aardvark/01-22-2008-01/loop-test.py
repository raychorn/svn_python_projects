import time

_ioTime = {}
_ioElapsedTime = 0

def initIOTime(reason):
	global _ioTime
	if (_ioTime.has_key(reason) == False):
		_ioTime[reason] = [0.0]

def ioBeginTime(reason):
	global _ioTime
	initIOTime(reason)
	_ioTime[reason].append(time.time())

def ioEndTime(reason):
	global _ioTime
	initIOTime(reason)
	d = _ioTime[reason]
	d.append(time.time())
	diff = d.pop() - d.pop()
	d[0] += diff
	_ioTime[reason] = d

def ioTimeAnalysis():
	global _ioTime
	global _ioElapsedTime

	_ioElapsedTime = 0
	for k in _ioTime.keys():
		d = _ioTime[k]
		print '(ioTimeAnalysis) :: Category: "%s" = (%s)' % (k,d[0])
		_ioElapsedTime += d[0]
	return _ioElapsedTime

if __name__ == '__main__':
	def main():
		ioBeginTime('foo')
		i = 0
		while (i < 10000):
			foo = [x for x in range(1000)]
			i += 1
		ioEndTime('foo')
		print foo
		print ioTimeAnalysis()
	
	import psyco

	psyco.bind(main)
	main()
		
	
	
