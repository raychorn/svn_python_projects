import time
import pprint

def timing(f, n, a):
    print f.__name__,
    r = range(n)
    t1 = time.clock()
    for i in r:
	f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a)
    t2 = time.clock()
    return round(t2-t1, 3)

def f1(list):
    string = ""
    for item in list:
	string = string + chr(item)
    return string

def f1a(list):
    return "".join(chr(i) for i in list)

def f2(list):
    return reduce(lambda string, item: string + chr(item), list, "")

def f3(list):
    string = ""
    for character in map(chr, list):
	string = string + character
    return string

def f4(list):
    string = ""
    lchr = chr
    for item in list:
	string = string + lchr(item)
    return string

def f5(list):
    string = ""
    for i in range(0, 256, 16): # 0, 16, 32, 48, 64, ...
	s = ""
	for character in map(chr, list[i:i+16]):
	    s = s + character
	string = string + s
    return string

import string
def f6(list):
    return string.joinfields(map(chr, list), "")

import array
def f7(list):
    return array.array('B', list).tostring()

def listToDict(items,master):
    d = {}
    for t in items:
	d[master[len(d)].__name__] = t
    return d

testdata = range(256)
print `testdata`
print '\n'
testfuncs = f1, f1a, f2, f3, f4, f5, f6, f7
#for f in testfuncs: print f.func_name, f(testdata)
t1 = [timing(f, 100, testdata) for f in testfuncs]

d1 = listToDict(t1,testfuncs)

print '\n'
pprint.pprint(t1)

import psyco
psyco.full()
print '\n'
print 'Psyco...'
t2 = [timing(f, 100, testdata) for f in testfuncs]

d2 = listToDict(t2,testfuncs)

print '\n'
pprint.pprint(t2)

print '\n'
print 'Analysis...'

longest = -1
for f in testfuncs:
    longest = max(len(f.__name__),longest)

for f in testfuncs:
    sDiff = '-'
    sX = ''
    _d1 = d1[f.__name__]
    _d2 = d2[f.__name__]
    diff = _d2 - _d1
    if (diff < 0):
	sDiff = '+'
	x = _d1/_d2
	sPadN = (3-len(str(x).split('.')[0]))
	sPad = ' '*sPadN
	sX = ' %s%s%4.2f%stimes ' % (sDiff,sPad,x,' ')
    elif (diff == 0):
	sDiff = ''
    else:
	x = _d2/_d1
	sPadN = (3-len(str(x).split('.')[0]))
	sPad = ' '*sPadN
	sX = ' %s%s%4.2f%stimes ' % (sDiff,sPad,x,' ')
    pcent = abs(diff) / _d1
    sPadN = (3-len(str(pcent*100).split('.')[0]))
    sPad = ' '*sPadN
    print '%-3s is %s%3.2f%s %s' % (f.__name__,sPad,(pcent*100),'%',sX)
    