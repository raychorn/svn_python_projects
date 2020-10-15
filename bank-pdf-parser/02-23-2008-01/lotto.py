# (c). Copyright 2007-2008, Ray C Horn (raychorn@hotmail.com) and Hierarchical Applications Limited, Inc., All Rights Reserved.
# This software may not be used for any commercial purpose whatsoever however it may be used for educational purposes so long as the
# end-goal or end-product is of a non-commercial purpose.

# The person(s) who win any lotto or other gambling or wagering system using this program must agree to give 20% of their winnings to the author of
# this program as specified by the copyright notice given above.

# This version uses real data from the California Mega Lotto Drawing History from 06-24-2005 thru 02-15-2008 to determine which numbers
# have been picked in terms of which numbers may possibly be picked next.

#
# This could be easily made into a professional-looking Lotto Picks Generator by using a frequency distribution technique that populates
# the list of numbers to pick from based on the number of times numbers had been picked in the past per number slot.
#
import os
import sys
import time
from random import choice
from random import shuffle
from vyperlogix import PrettyPrint
from vyperlogix import Args
from vyperlogix import _psyco
from vyperlogix import _utils

def listify(d,key,value):
    bucket = value
    if ( (isinstance(d,dict)) and (d.has_key(key)) ):
	bucket = d[key]
	if (not isinstance(bucket,list)):
	    bucket = [bucket]
	bucket.append(value)
    return bucket

def analyzePicks(picks):
    f = {}
    m = {}
    for p in picks:
	for n in p[0:-1]:
	    _n = int(n)
	    f[_n] = listify(f,_n,_n)
	_n = int(p[-1])
	m[_n] = listify(m,_n,_n)
    return (f,m)

def _loadWinningNumbers(f,m):
    fx = {}
    mx = {}
    c1 = []
    c2 = []
    for k,v in f.iteritems():
	_n = len(v) if (isinstance(v,list)) else 1
	fx[k] = _n
	for n in xrange(0,_n):
	    c1.append(k)
    for k,v in m.iteritems():
	_n = len(v) if (isinstance(v,list)) else 1
	mx[k] = _n
	for n in xrange(0,_n):
	    c2.append(k)
    shuffle(c1)
    shuffle(c2)
    return (f,m,fx,mx,c1,c2)

def loadWinningNumbers(fname):
    d = {}
    f = {}
    m = {}
    fx = {}
    mx = {}
    c1 = []
    c2 = []
    if (os.path.exists(fname)):
	fHand = open(fname,'r')
	for l in fHand.readlines():
	    toks = l.split()
	    d[toks[0]] = toks
	    aPick = [int(n) for n in toks[2:-1]]
	    for n in aPick:
		f[n] = listify(f,n,n)
	    _n = int(toks[-1])
	    aPick.append(_n)
	    m[_n] = listify(m,_n,_n)
	    d[','.join([str(n) for n in aPick])] = toks
	fHand.close()
	f,m,fx,mx,c1,c2 = _loadWinningNumbers(f,m)
    return (d,f,m,fx,mx,c1,c2)

def reshuffleWinningNumbers(db,choices):
    if (len(db) == 7):
	d, f, m, fx, mx, c1, c2 = db
    elif (len(db) == 6):
	f, m, fx, mx, c1, c2 = db
    fx = {}
    c1 = []
    for k,v in f.iteritems():
	if (k not in choices):
	    _n = len(v) if (isinstance(v,list)) else 1
	    fx[k] = _n
	    for n in xrange(0,_n):
		c1.append(k)
    shuffle(c1)
    if (len(db) == 7):
	return (d,f,m,fx,mx,c1,c2)
    return (f,m,fx,mx,c1,c2)

def purelyRandomPick(ignore=False):
    _pick = []
    if (not ignore):
	print 'Purely Random Selection:'
    s_numbers = set(numbers)
    s_choices = set()
    for n in xrange(0,num_numbers):
	aChoice = choice(list(s_numbers.difference(s_choices)))
	s_choices.add(aChoice)
	_pick.append(aChoice)
    if (not ignore):
	choices = list(s_choices)
	choices.sort()
	for c in choices:
	    print '(%s)' % c
    
    for n in xrange(0,num_total-num_numbers):
	aChoice = choice(megas)
	if (not ignore):
	    print 'Mega=(%s)' % aChoice
	_pick.append(aChoice)
    if (not ignore):
	print '='*30
	print
    _pick.sort()
    return _pick

def weightedRandomPick(db,ignore=False):
    _pick = []
    if (not ignore):
	print 'Weighted Random Selection:'
    numbers = db[-2]
    megas = db[-1]
    s_numbers = set(numbers)
    s_choices = set()
    for n in xrange(0,num_numbers):
	aChoice = choice(list(s_numbers.difference(s_choices)))
	s_choices.add(aChoice)
	_pick.append(aChoice)
	db = reshuffleWinningNumbers(db,list(s_choices))
	numbers = db[-2]
	megas = db[-1]
	s_numbers = set(numbers)
    if (not ignore):
	choices = list(s_choices)
	choices.sort()
	for c in choices:
	    print '(%s)' % c
    
    for n in xrange(0,num_total-num_numbers):
	aChoice = choice(megas)
	_pick.append(aChoice)
	if (not ignore):
	    print 'Mega=(%s)' % aChoice
    if (not ignore):
	print '='*30
	print
    _pick.sort()
    return _pick

def echoPrint(s):
    print s
    print >>sys.stderr, s
        
if (__name__ == '__main__'):
    if (_utils.getVersionNumber() >= 251):
	_psyco.importPsycoIfPossible()
	
	args = {'--help':'displays this help text.','--verbose':'output more stuff.','--random':'purely random mode.','--weighted':'weighted random mode.','--analysis':'count the number of instances of picks that match any past known winning picks.','--period=num_of_picks_per_choice':'controls the thought process, print most used sequences after this many picks.','--count=number_of_picks':'1 to some number greater than 1.'}
	_argsObj = Args.Args(args)
	
	_isRandom = True
	_isWeighted = False
	_isHelp = False
	_isAnalysis = False
	
	_period = 1
	_count = 1
	
	numbers = xrange(1,56)
	megas = xrange(1,46)
	
	num_numbers = 5
	num_total = num_numbers+1
	
	choices = []
	
	_count = 1
	
	try:
	    _isAnalysis = _argsObj.booleans['isAnalysis']
	except:
	    pass
    
	try:
	    _period = int(_argsObj.arguments['period'])
	except:
	    pass
    
	try:
	    _count = int(_argsObj.arguments['count'])
	except:
	    pass
    
	try:
	    _isVerbose = _argsObj.booleans['isVerbose']
	except:
	    _isVerbose = False
    
	try:
	    _isTimed = _argsObj.booleans['isTimed']
	except:
	    _isTimed = False
    
	try:
	    _isWeighted = _argsObj.booleans['isWeighted']
	except:
	    pass
    
	try:
	    _isHelp = _argsObj.booleans['isHelp']
	except:
	    pass
    
	try:
	    _isRandom = _argsObj.booleans['isRandom']
	except:
	    _isRandom = False
    
	if (_isHelp):
	    pArgs = [(k,args[k]) for k in args.keys()]
	    pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	    pPretty.pprint()
	    
	if (_isVerbose):
	    print >>sys.stderr
	    print >>sys.stderr, '_argsObj.booleans=(%s)' % str(_argsObj.booleans)
	    print >>sys.stderr, '_argsObj.arguments=(%s)' % str(_argsObj.arguments)
    
	if (not _isHelp):
	    if (_isRandom or _isWeighted):
		_db = loadWinningNumbers('MegaMillions.txt')
		
		if (_isAnalysis):
		    da = []
		    for k,v in _db[0].iteritems():
			dd = {}
			toks = k.split(',')
			if (isinstance(k,str)) and (len(toks) == num_total):
			    for n in toks[0:-1]:
				dd[n] = toks
			    da.append(dd)
		    i = 0
		    j = 0
		    t_total = 0.0
		    t_metrics = [2**31,0.0,-2**31]
		    n_metrics = [2**31,-2**31]
		    while (1):
			TIMEIT = "aPick = weightedRandomPick(_db,True)"
			t = time.time()
			exec TIMEIT
			et = time.time() - t
			etx = 1.0/et
			t_total += etx
			t_metrics[0] = min(t_metrics[0],etx)
			t_metrics[-1] = max(t_metrics[-1],etx)
			t_metrics[1] = t_total/float(i+1)
			_aPick = [str(n) for n in aPick]
			for d in da:
			    k = 0
			    for n in _aPick[0:-1]:
				if (d.has_key(n)):
				    k += 1
			    if (k == len(_aPick)-1):
				if (_aPick[-1] == d[_aPick[0]][-1]):
				    k += 1
			n_metrics[0] = min(n_metrics[0],k)
			n_metrics[-1] = max(n_metrics[-1],k)
			if (k > 0):
			    j += 1
			    print '*** #%s/%s %s (%s) (%s) (%s)' % (j,i,_aPick,k,n_metrics,t_metrics)
			elif ((i % 1000) == 0):
			    echoPrint('+ %s/%s (%s) (%s)' % (i,j,n_metrics,t_metrics))
			if (k == num_total):
			    break
			i += 1
		else:
		    for n in xrange(_count):
			if (_count > 1):
			    print '%s of %s' % (n+1,_count)
			    
			_picks = []
			for m in xrange(_period):
			    if (_isRandom):
				_picks.append(purelyRandomPick(True))
			    
			    if (_isWeighted):
				_picks.append(weightedRandomPick(_db,True))
				
			if (len(_picks) > 0):
			    f,m = analyzePicks(_picks)
			    p_db = _loadWinningNumbers(f,m)
			    print 'This pick is based on the previous %s picks that were based on the known winning picks.' % _period
			    weightedRandomPick(p_db)
			
			if (_isRandom):
			    purelyRandomPick()
			
			if (_isWeighted):
			    weightedRandomPick(_db)
	    else:
		print 'Nothing to do !'
		print 'Use the --help option to get online help.'
    else:
	print 'You seem to be using the wrong version of Python, try using 2.5.1 rather than "%s".' % sys.version.split()[0]
	