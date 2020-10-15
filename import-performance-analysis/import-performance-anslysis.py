from vyperlogix.misc import ioTimeAnalysis

import cProfile, pprint, StringIO

def profile(func):
    def wrapper(*args, **kwargs):
	prof = cProfile.Profile()
	retval = prof.runcall(func, *args, **kwargs)
	fOut = StringIO.StringIO()
	pprint.pprint(prof.getstats(),fOut)
	print fOut.getvalue()
	return retval
    return wrapper        

reason = 'without'
ioTimeAnalysis.initIOTime(reason)
ioTimeAnalysis.ioBeginTime(reason)
n = 100000
def __without__():
    x = 0
    for x in xrange(0,n):
	x += 1
__without__()
ioTimeAnalysis.ioEndTime(reason)

@profile
def __withoutProfiled__():
    x = 0
    for x in xrange(0,n):
	x += 1
__withoutProfiled__()

reason = 'with'
ioTimeAnalysis.initIOTime(reason)
ioTimeAnalysis.ioBeginTime(reason)
def __with__():
    x = 0
    for x in xrange(0,n):
	import time
	x += 1
__with__()
ioTimeAnalysis.ioEndTime(reason)

@profile
def __withProfiled__():
    x = 0
    for x in xrange(0,n):
	import time
	x += 1
__withProfiled__()

analysis = {}
ioElapsed = -1
def __callback__(*args,**kwargs):
    et = kwargs.get('ioElapsedTime',None)
    if (et is None):
	analysis[kwargs.get('category','UNKNOWN')] = kwargs.get('elapsed',-1)
    if (et is not None):
	ioElapsed = et

fOut = _utils.stringIO()
ioTimeAnalysis.ioTimeAnalysisReport(fOut=fOut,callback=__callback__)
print fOut.getvalue()

items = sorted(analysis.items(), key=lambda x:x[1])

for item in items:
    print item
    
diff = items[-1][-1] - items[0][-1]
diff_per_iteration = diff / n
print 'Difference is %2.4f or %2.8f per iteration for %d iterations.' % (diff,diff_per_iteration,n)
    
