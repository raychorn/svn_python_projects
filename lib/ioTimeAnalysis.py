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

def ioTimeAnalysis(iters=None):
	global _ioTime
	global _ioElapsedTime

	_ioElapsedTime = 0
	for k in _ioTime.keys():
		d = _ioTime[k]
		_tpi = ''
		if ( (iters) and (isinstance(iters,int)) ):
			_tpi = ' time/iters=(%2.10f)' % (d[0]/iters)
		print '(ioTimeAnalysis) :: Category: "%s" = (%s)%s' % (k,d[0],_tpi)
		_ioElapsedTime += d[0]
	return _ioElapsedTime

def ioTimeAnalysisReport(iters=None):
	ioAnalysis = ioTimeAnalysis(iters)
	print "\n\nTime spent doing I/O :: (%s)" % (str(ioAnalysis))
