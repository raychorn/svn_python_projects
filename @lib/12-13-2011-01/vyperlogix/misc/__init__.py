__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
import os, sys

__introspect__ = lambda o:['%s --> %s'%(a,type(o.__getattribute__(a))) for a in dir(o)]

__describe__ = lambda something,delim:'%s --> %s' % (typeClassName(something),delim.join(__introspect__(something)))

def is_camel_case(s):
    return (s != s.lower() and s != s.upper())

def introspect(something,fout=sys.stderr,delim='\n'):
    print >> fout, '='*40
    print >> fout, 'BEGIN: %s' % (something)
    print >> fout, '-'*40
    print >> fout, __describe__(something,delim)
    print >> fout, '-'*40
    try:
        for item in something:
            if (item):
                print >> fout, '%s --> %s' % (item,__describe__(something,delim))
    except:
        pass
    print >> fout, 'END!!!'
    print >> fout, '='*40

unpack = lambda s:s[0] if (isList(s)) else s
_unpack_ = lambda s:unpack(s) if (len(s) == 1) else s
__unpack__ = lambda s:unpack(s) if (len(s) > 0) else s

def asCSV(item,allowEmptyCells=True):
    return ','.join(['"%s"'%(t) for t in item if (allowEmptyCells) or (len(str(t)) > 0)]) if (isinstance(item,tuple)) or (isinstance(item,list)) else item

#from vyperlogix.decorators import TailRecursive
#@TailRecursive.tail_recursion
#def flatten(s,t):
    #for item in s:
	#if (isList(item)) or (isIterable(item)):
	    #l = item
	    #if (not isList(item)):
		#l = list(item)
	    #flatten(l,t)
	#else:
	    #t.append(item)

def normalize_as_float(val):
    _val = val
    try:
	_val = float(_val)
    except:
	pass
    return _val

def isValidFolder(s):
    return isString(s) and os.path.exists(s) and os.path.isdir(s)

def isValidFile(s):
    return isString(s) and os.path.exists(s) and os.path.isfile(s)

def isString(s):
    return (isinstance(s,str)) or (isinstance(s,unicode))

isStringValid = lambda s:(s) and isString(s) and (len(s) > 0)

def isBoolean(s):
    return (isinstance(s,bool))

def isBooleanString(s):
    d = {'True': True, 'False': False,}
    t = str(s).lower().capitalize()
    if (isString(t) and (t in d.keys())):
	return d[t]
    return False

def isInteger(s):
    return (isinstance(s,int))

def isFloat(s):
    return (isinstance(s,float))

def isDate(s):
    from datetime import date
    return isinstance(s,date)

def isSimpleDict(s):
    return (isinstance(s,dict))

def isHashedDict(s):
    return (ObjectTypeName.typeName(s).find('HashedLists') > -1)

def isDict(s):
    _has_key = False
    try:
	_has_key = callable(s.has_key)
    except:
	_has_key = False
    return (isSimpleDict(s)) or (_has_key)

def isList(obj):
    try:
        return callable(obj.append)
    except:
        pass
    return False

def isTuple(obj):
    try:
	if (len(obj) == 0):
	    obj += (1)
	if (len(obj) > 0):
	    obj[0] = obj[0]
    except:
        return True
    return False

def isIterable(obj):
    try: 
        return hasattr(obj,'__iter__')
    except TypeError: 
        return False

def isRePattern(obj):
    from vyperlogix.misc import ObjectTypeName
    try: 
        return ObjectTypeName.typeClassName(obj) == '_sre.SRE_Pattern'
    except TypeError: 
        return False

def clone(l):
    return copy(l)

def append(l,item):
    if (isList(l)):
	if (not isList(item)):
	    item = [item]
	for it in item:
	    l.append(it)
    return l

def copy(l):
    if (isList(l)):
	return [item for item in l]
    return l

def findAllContaining(lst,s_search,callback=None,returnIndexes=False,returnOne=False,itemHandler=None):
    def doCallback(_item,_callback):
        try:
            return _callback(_item,s_search)
        except:
            pass
        return False
    i = 0
    l = []
    if (isList(lst)):
	compare_func = lambda item,search:item.find(search) > -1
	compare_func_re = lambda item,search:search.search(item)
	compare_func = compare_func
	if (isRePattern(s_search)):
	    compare_func = compare_func_re
	for item in lst:
	    if (itemHandler) and (callable(itemHandler)):
		try:
		    item = itemHandler(item)
		except:
		    pass
	    if ((compare_func(item,s_search)) if (not callable(callback)) else doCallback(item,callback)):
		l.append(item if (not returnIndexes) else i)
		if (returnOne):
		    break
	    i += 1
    return l

def findFirstContaining(lst,s_search,callback=None,returnIndexes=True):
    r = -1
    if (isList(lst)):
	r = findAllContaining(lst,s_search,callback=callback,returnIndexes=returnIndexes,returnOne=True)
    return -1 if (len(r) == 0) else r[0]

def findAllMatching(lst,s_search,callback=None,returnIndexes=False,returnOne=False):
    def doCallback(_item,_callback):
        try:
            return _callback(_item,s_search)
        except:
            pass
        return False
    i = 0
    l = []
    if (isList(lst)):
	compare_func = lambda item,search:item == search
	compare_func_re = lambda item,search:search.search(item)
	if (isString(s_search)) or (isRePattern(s_search)):
	    compare_func = compare_func
	    if (isRePattern(s_search)):
		compare_func = compare_func_re
	    for item in lst:
		if (compare_func(item,s_search) if (not callable(callback)) else doCallback(item,callback)):
		    l.append(item if (not returnIndexes) else i)
		    if (returnOne):
			break
		i += 1
	elif (isList(s_search)):
	    for i in xrange(0,len(lst)-len(s_search)):
		if (lst[i:i+len(s_search)] == s_search):
		    l.append(s_search if (not returnIndexes) else i)
		    if (returnOne):
			break
	else: # to allow for any type of search to be performed even when strings are not being used...
	    compare_func = compare_func
	    if (isRePattern(s_search)):
		compare_func = compare_func_re
	    for item in lst:
		if (compare_func(item,s_search) if (not callable(callback)) else doCallback(item,callback)):
		    l.append(item if (not returnIndexes) else i)
		    if (returnOne):
			break
		i += 1
    return l

def findFirstMatching(lst,s_search,callback=None,returnIndexes=True):
    r = -1
    if (isList(lst)):
	r = findAllMatching(lst,s_search,callback=callback,returnIndexes=returnIndexes,returnOne=True)
    return -1 if (len(r) == 0) else r[0]

def insert(lst,index,value):
    if (isList(lst)):
	try:
	    lst.insert(index,value)
	    return lst
	except:
	    pass
    return lst

def insertCopy(lst,index,value):
    if (isList(lst)):
	try:
	    _lst = [i for i in lst]
	    return insert(_lst,index,value)
	except:
	    pass
    return lst

def reverse(l):
    if (isList(l)):
	try:
	    ll = copy(l)
	    ll.reverse()
	    return ll
	except:
	    pass
    return l

def reverseCopy(l):
    if (isList(l)):
	try:
	    _l = [i for i in l]
	    return reverse(_l)
	except:
	    pass
    return l

def reverseDigitsList(foo):
    if (isList(foo)):
	try:
	    return ''.join([t.strip() for t in str(reverse(eval(foo) if (isString(foo)) else foo)).split()])
	except:
	    return None
    return None
    
def removeAll(items):
    if (isList(items)):
	while (len(items) > 0):
	    items.pop()

def sort(l):
    try:
        l.sort()
        return l
    except:
        pass
    return l

def sortCopy(l):
    try:
        _l = [i for i in l]
        return sort(_l)
    except:
        pass
    return l

def funcName():
    """ get name of function """
    import sys
    return sys._getframe(1).f_code.co_name

def callersName():
    """ get name of caller of a function """
    import sys
    return sys._getframe(2).f_code.co_name

def findInListSafely(l,item):
    try:
        return l.index(item)
    except:
        pass
    return -1

def formattedException(details='',_callersName=None,depth=None,delims='\n'):
    _callersName = _callersName if (_callersName is not None) else callersName()
    import sys, traceback
    exc_info = sys.exc_info()
    stack = traceback.format_exception(*exc_info)
    stack = stack if ( (depth is None) or (not isInteger(depth)) ) else stack[0:depth]
    try:
	info_string = delims.join(stack)
    except:
	info_string = '\n'.join(stack)
    return '(' + _callersName + ') :: "' + str(details) + '". ' + info_string
