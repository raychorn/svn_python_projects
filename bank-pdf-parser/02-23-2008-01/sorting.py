# This source code is being distributed for Educational purposes only and may
# not be used for any commercial purpose whatsoever.
# All modules whether expressed as source or object code are protected under U.S. Federal and State Copyright Laws.
# (c). Copyright 2006-2008, Ray C. Horn and Hierarchical Applications Limited, Inc., All Rights Reserved.
# http://raychorn.phpnet.us/
#
# Purpose:
# The purpose of this module is to provide the means to determine which sorting
# algorithm scales-up with the best performance versus the number of items to
# be sorted.
#
# It should be noted that the built-in sort method found in Python is fastest
# when the number of items to be sorted remains fairly small.  The persistent
# sorting technique scales best when the number of items grows beyond the ability
# to store the items in RAM otherwise consider using the built-in Python sorting
# function as shown below in this code sample.
#
import os
import sys
import time
from vyperlogix.sorting import heapsort,InsertionSort,HeapSort2,qsort
from vyperlogix.profiling import profileit
from vyperlogix import _psyco
from vyperlogix import oodb
from vyperlogix.hash import lists
from vyperlogix import WinProcesses

if (__name__ == '__main__'):
    _psyco.importPsycoIfPossible()
    IM = 139968 
    IA =   3877 
    IC =  29573 
    
    LAST = 42 
    def gen_random(max) : 
        global LAST 
        LAST = (LAST * IA + IC) % IM 
        return( (max * LAST) / IM ) 

    def initArray(N):
        ary = [None]*(N + 1) 
        for i in xrange(1, N + 1) : 
            ary[i] = gen_random(1.0) 
        return ary
    
    #@profileit.profileit(20)
    def persists(N):
        ary = initArray(N)
        fname = 'persisted.db'
        if (os.path.exists(fname)):
            os.remove(fname)
        dbx = oodb.PickledHash(fname,oodb.PickleMethods.useStrings)
        for item in ary:
            _item = item if item else 0.0
            val = '%0.10f' % _item
            dbx[val] = val
        i = dbx.keys()[-1]
        dbx.sync()
        dbx.close()
        return i
        
    #@profileit.profileit(20)
    def heapsorts(N):
        ary = initArray(N)
        heapsort.heapsort(N, ary) 
    
    #@profileit.profileit(20)
    def sorts(N):
        ary = initArray(N)
        ary.sort()
        
    #@profileit.profileit(20)
    def inserts(N):
        ary = initArray(N)
        InsertionSort.InsertionSort(ary)
        
    #@profileit.profileit(20)
    def heaps(N):
        ary = initArray(N)
        HeapSort2.HeapSort(ary)
        
    #@profileit.profileit(20)
    def qsorts(N):
        ary = initArray(N)
        qsort.qsort(ary)
        
    #@profileit.profileit(20)
    def searches(N):
        ary = initArray(N)
        i = -9999999
        for item in ary:
            i = max(item,i)
        return i
    
    def echoPrint(s):
        print s
        print >>sys.stderr, s
        
    ary = []
    d = {}
    
    def main() : 
        global ary
        global d

        if len(sys.argv) == 2 : 
            N = int(sys.argv[1]) 
        else : 
            N = 1000

	N = 1000000
    	win_proc = WinProcesses.WinProcesses()
	pid = win_proc.getProcessIdByName('python')
	procHandle = win_proc.openProcessForPID(pid)
	_memoryUsed1 = win_proc.getProcessMemoryUsageForHandle(procHandle)
        ary = initArray(N)
	_memoryUsed2 = win_proc.getProcessMemoryUsageForHandle(procHandle)
	_memoryUsedN = _memoryUsed2 - _memoryUsed1
	_memoryUsedNp = float(_memoryUsedN)/float(N)
	_max = 2**31
	_max_expected = int(_max * _memoryUsedNp)
	echoPrint('_memoryUsedN=(%s)' % (_memoryUsedN))
	echoPrint('_memoryUsedNp=(%s), _max_expected=(%s)' % (_memoryUsedNp,_max_expected))
	win_proc.closeProcessHandle(procHandle)

	N = 1000
	
        ruledOut = []
        
        ruledOutByCondition = {}
        ruledOutByCondition[1000000] = 'insertion-sort'
	
	sortingMethods = []
        
        isDone = False
        while (not isDone):
            d = {}
        
            echoPrint('='*30)
            echoPrint('N=(%s)\n' % N)

            if ('python native sort' not in ruledOut):
                TIMEIT = "sorts(N)"
                echoPrint('BEGIN: python native sort() %s :' % TIMEIT)
                t = time.time()
                exec TIMEIT
                d['python native sort'] = time.time() - t
		sortingMethods.append('python native sort')
                echoPrint('END! python native sort() %s' % d['python native sort'])
    
            if ('linear sort' not in ruledOut):
                TIMEIT = "searches(N)"
                echoPrint('BEGIN: linear sort() %s :' % TIMEIT)
                t = time.time()
                exec TIMEIT
                d['linear sort'] = time.time() - t
		sortingMethods.append('linear sort')
                echoPrint('END! linear sort() %s' % d['linear sort'])
    
            if ('recursive quick-sort' not in ruledOut):
                TIMEIT = "qsorts(N)"
                echoPrint('BEGIN: recursive quick-sort() %s :' % TIMEIT)
                t = time.time()
                exec TIMEIT
                d['recursive quick-sort'] = time.time() - t
		sortingMethods.append('recursive quick-sort')
                echoPrint('END! recursive quick-sort() %s' % d['recursive quick-sort'])
    
            if ('heap-sort-v1' not in ruledOut):
                TIMEIT = "heapsorts(N)"
                echoPrint('BEGIN: heap-sort-v1() %s :' % TIMEIT)
                t = time.time()
                exec TIMEIT
                d['heap-sort-v1'] = time.time() - t
		sortingMethods.append('heap-sort-v1')
                echoPrint('END! heap-sort-v1() %s' % d['heap-sort-v1'])
    
            if ('persists' not in ruledOut):
                TIMEIT = "persists(N)"
                echoPrint('BEGIN: persists() %s :' % TIMEIT)
                t = time.time()
                exec TIMEIT
                d['persists'] = time.time() - t
                echoPrint('END! persists() %s' % d['persists'])
    
            if ('heap-sort-v2' not in ruledOut):
                TIMEIT = "heaps(N)"
                echoPrint('BEGIN: heap-sort-v2() %s :' % TIMEIT)
                t = time.time()
                exec TIMEIT
                d['heap-sort-v2'] = time.time() - t
		sortingMethods.append('heap-sort-v2')
                echoPrint('END! heap-sort-v2() %s' % d['heap-sort-v2'])
    
            if ('insertion-sort' not in ruledOut):
                TIMEIT = "inserts(N)"
                echoPrint('BEGIN: insertion-sort() %s :' % TIMEIT)
                t = time.time()
                exec TIMEIT
                d['insertion-sort'] = time.time() - t
		sortingMethods.append('insertion-sort')
                echoPrint('END! insertion-sort() %s' % d['insertion-sort'])
    
            a = lists.HashedLists()
            for k,v in d.iteritems():
                a[str(v)] = k
                
            t = d.values()
            t.sort()
            echoPrint('(slowest) :: %s :: %s' % (t[-1],a[str(t[-1])]))
            echoPrint('(fastest) :: %s :: %s' % (t[0],a[str(t[0])]))
            try:
                echoPrint('(analysis) :: %s is %5.2f times faster than %s' % (a[str(t[0])],t[-1]/t[0],a[str(t[-1])]))
            except ZeroDivisionError, details:
                echoPrint('WARNING :: Error in Analysis due to  "%s".' % str(details))
            echoPrint('='*30)
            for k,v in d.iteritems():
                echoPrint('%s :: %s' % (k,v))
            echoPrint('='*30)
            
            _ratio = t[-1]/t[-2]
            if (_ratio > 5) and (t[-1] > 300):
                ruledOut.append(a[str(t[-1])][0])
                echoPrint('ruledOut=(%s), _ratio=(%s), t_last=(%s), t_last-1=(%s)' % (str(ruledOut)),_ratio,t[-1],t[-2])
            
            isDone = (a[str(t[0])][0] == 'persists') or ('persists' in ruledOut)
            N *= 10
            
            if (ruledOutByCondition.has_key(N)):
                ruledOut.append(ruledOutByCondition[N])
                echoPrint('ruledOutByCondition=(%s), (%s)' % (ruledOutByCondition[N],str(ruledOut)))
	    
	    if (N > _max_expected):
		for m in sortingMethods:
		    if (m not in ruledOut):
			ruledOut.append(m)

        if (0):
            print "%.10f" % ary[N] 
            print '='*30
            _last = [item for item in ary[-5:]]
            _last.reverse()
            for item in _last:
                print '\t%s' % item
            print '='*30
            _all = [item for item in ary]
            _all.reverse()
            for item in _all[0:10]:
                print '\t%s' % item
    
    main() 
