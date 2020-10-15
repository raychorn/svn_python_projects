import os, sys
import time
import json

normalize = lambda p:p.replace(os.sep,'/')

isUsingWindows = (sys.platform.lower().find('win') > -1) and (os.name.lower() == 'nt')
isUsingMacOSX = (sys.platform.lower().find('darwin') > -1) and (os.name.find('posix') > -1) and (not isUsingWindows)
isUsingLinux = (sys.platform.lower().find('linux') > -1) and (os.name.find('posix') > -1) and (not isUsingWindows) and (not isUsingMacOSX)

try:
    import win32api
    getCurrentWindowsLogicalDrives = [d for d in [d for d in win32api.GetLogicalDriveStrings().split("\x00")] if (len(d) > 0) and (os.path.isdir(d))] if (isUsingWindows) else []
except ImportError:
    getCurrentWindowsLogicalDrives = []

def _getframe_code():
    """ _getframe """
    import sys
    return sys._getframe(1).f_code
	    
def funcName():
    """ get name of function """
    return _getframe_code().co_name
	    
def callersName():
    """ get name of caller of a function """
    return _getframe_code().co_name
		

from vyperlogix.classes.CooperativeClass import Cooperative
class DjangoManager(Cooperative):
    def tops(self):
	top = self.__top__
	if (isinstance(self.__top__,list)):
	    top = self.__top__[self.__num__]
	    self.__num__ += 1
	    self.__num__ = 0 if (self.__num__ > len(self.__top__)) else self.__num__
	yield top

    def find(self,top,fname,target=0,pos=0):
	#print '(%s)-DEBUG.1: __find__("%s","%s",%s)' % (funcName(),top,fname,target)
	top = self.__find__(top,fname,target=target)
	#print '(%s)-DEBUG.2: top=%s' % (funcName(),top)
	if (not os.path.exists(top)):
	    print >> sys.stderr, '(%s)-ERROR: Cannot find %s in or under %s.' % (funcName(),fname,self.__top__)
	    sys.exit(1)
	    
	#print '(%s)-DEBUG.3: __replace__("%s","%s",%s)' % (funcName(),fname,top,pos)
	self.__replace__(fname,top,pos=pos)
	
	return top

    def __checkpoint__():
	doc = "__checkpoint__"
	def fget(self):
	    return os.path.abspath('./.%s'%(__name__))
	return locals()
    __checkpoint__ = property(**__checkpoint__())

    def __app_lib_symbol__():
	doc = "__app_lib_symbol__"
	def fget(self):
	    return '__app_lib__'
	return locals()
    __app_lib_symbol__ = property(**__app_lib_symbol__())
   
    def __django_lib_symbol__():
	doc = "__django_lib_symbol__"
	def fget(self):
	    return '__django_lib__'
	return locals()
    __django_lib_symbol__ = property(**__django_lib_symbol__())
    
    def __vyperlogix_lib_symbol__():
	doc = "__vyperlogix_lib_symbol__"
	def fget(self):
	    return '__vyperlogix_lib__'
	return locals()
    __vyperlogix_lib_symbol__ = property(**__vyperlogix_lib_symbol__())
    
    def __version_dots__():
	doc = "__version_dots__"
	def fget(self):
	    return '.'.join(['%d'%(n) for n in sys.version_info[0:2]])
	return locals()
    __version_dots__ = property(**__version_dots__())
    
    def __version_underscore__():
	doc = "__version_underscore__"
	def fget(self):
	    return '_'.join(['%d'%(n) for n in sys.version_info[0:2]])
	return locals()
    __version_underscore__ = property(**__version_underscore__())
    
    def __init__(self,tops=[],app=None):
	self.__num__ = 0
	__is__ = (isinstance(tops,list)) and (len(tops) > 0)
	if (__is__):
	    self.__top__ = tops
	if (not isUsingWindows):
	    if (not __is__):
		self.__top__ = [
		    '/usr/local'
		]
	else:
	    if (not __is__):
		self.__top__ = [
		    'J:/@Vyper Logix Corp/@Projects/python-projects/@lib/12-13-2011-01',
		    'J:/@Vyper Logix Corp/@Projects/python-projects/_Django-1.5.1',
		    'J:/@Vyper Logix Corp/@Projects/python-projects/_django-projects'
		]
	    _foundCount = 0
	    for drive in getCurrentWindowsLogicalDrives:
		for i in xrange(len(self.__top__)):
		    t = self.__top__[i]
		    dd = os.path.splitdrive(t)[0]
		    tt = normalize(str(t).replace(dd,drive))
		    if (os.path.exists(tt)) and (os.path.isdir(tt)):
			_foundCount += 1
			self.__top__[i] = tt
			break
		if (_foundCount):
		    break
	    if (_foundCount < 1):
		print >>sys.stdout, 'WARNING: Cannot locate "%s".' % (tt)
		os._exit(0)

	self.__has_vyperlogix_lib__ = True
	try:
	    from vyperlogix import misc
	    from vyperlogix.misc import _utils
	except ImportError, ex:
	    self.__has_vyperlogix_lib__ = False

	if (app):
	    self.__appID__ = app.split('/')[-1]
	    if (not isUsingWindows):
		self.__app__ = app
		self.__loggingPath__ = '/var/log/%s' % (self.__appID__)
	    else:
		self.__app__ = app
		self.__loggingPath__ = '%s/logs' % (os.path.abspath('.'))
	    self.__loggingPath__ = normalize(self.__loggingPath__)
	else:
	    print >>sys.stdout, 'WARNING: Cannot proceed without an app, as you can see "%s" is not useable.' % (app)
	    os._exit(0)
	    
	###############################################################################################
	self.fCheckpoint = None
	self.dCheckpoint = {}
	self.dChanges = {}
	e = os.path.exists(self.__checkpoint__)
	#print 'DEBUG: os.path.exists("%s")=%s' % (self.__checkpoint__,e)
	if (e):
	    i = os.path.isdir(self.__checkpoint__)
	    #print 'DEBUG: os.path.isdir("%s")=%s' % (self.__checkpoint__,i)
	    if (i):
		print 'DEBUG: remove_all_under_and_including("%s") !!!' % (self.__checkpoint__)
		self.remove_all_under_and_including(self.__checkpoint__)
	    i = os.path.isfile(self.__checkpoint__) and (self.fileSize(self.__checkpoint__) > 0)
	    #print 'DEBUG: os.path.isfile("%s")=%s' % (self.__checkpoint__,i)
	    if (i):
		self.fCheckpoint = open(self.__checkpoint__,'r')
		#print 'DEBUG: fCheckpoint=%s' % (self.fCheckpoint)
		try:
		    self.dCheckpoint = json.loads(''.join(self.fCheckpoint.readlines()))
		except Exception, ex:
		    print 'DEBUG: ex=%s' % (ex)
		    self.dCheckpoint = {}
		finally:
		    self.fCheckpoint.close()
	
	self.retirees = []
	for k,v in self.dCheckpoint.iteritems():
	    self.dChanges[k] = ''
	    if (not os.path.exists(v)):
		self.retirees.append(k)
	
	while (len(self.retirees) > 0):
	    k = self.retirees.pop()
	    del self.dCheckpoint[k]
	    del self.dChanges[k]
	
	_top = top = self.tops().next()
	if (not self.__has_vyperlogix_lib__):
	    __is__ = dCheckpoint.has_key(self.__vyperlogix_lib_symbol__)
	    #print 'DEBUG: dCheckpoint.has_key("%s")=%s' % (self.__vyperlogix_lib_symbol__,__is__)
	    if (__is__):
		self.__vyperlogix_lib__ = normalize(self.dCheckpoint[self.__vyperlogix_lib_symbol__])
		#print 'DEBUG: __vyperlogix_lib__=%s' % (self.__vyperlogix_lib__)
	    else:
		self.__vyperlogix_lib__ = 'vyperlogix_%s.zip' % (self.__version_underscore__)
		
		top = self.__find__(_top,self.__vyperlogix_lib__,target=2)
		assert (top) and os.path.exists(top), 'ERROR: Cannot find %s in (%s) because somebody forgot to build and/or deploy it, maybe ???' % (self.__vyperlogix_lib__,_top)
		if (os.path.exists(top)):
		    if (top.endswith(self.__vyperlogix_lib__)):
			self.__vyperlogix_lib__ = top
		    else:
			self.__vyperlogix_lib__ = normalize(os.sep.join([top,self.__vyperlogix_lib__]))
		else:
		    print >> sys.stderr, 'ERROR: Cannot find %s in or under %s.' % (self.__vyperlogix_lib__,self.__top__)
		    sys.exit(1)
		dChanges[self.__vyperlogix_lib_symbol__] = dCheckpoint.get(self.__vyperlogix_lib_symbol__,None)
		dCheckpoint[self.__vyperlogix_lib_symbol__] = normalize(__vyperlogix_lib__)
		dChanges[self.__vyperlogix_lib_symbol__] = '*' if (dChanges.get(self.__vyperlogix_lib_symbol__,None) != dCheckpoint.get(self.__vyperlogix_lib_symbol__,None)) else ''
		#print 'DEBUG: dCheckpoint["%s"]=%s' % (self.__vyperlogix_lib_symbol__,dCheckpoint[self.__vyperlogix_lib_symbol__])
	
	    _is_ = os.path.exists(__vyperlogix_lib__)
	    print 'DEBUG _is_=%s' % (_is_)
	    if (_is_):
		self.__replace__('vyperlogix',__vyperlogix_lib__,remove=_top)
	    
	try:
	    from vyperlogix import misc
	    from vyperlogix.misc import _utils
	except ImportError, ex:
	    print >> sys.stderr, 'ERROR: Cannot import any vyperlogix modules !!!'
	    sys.exit(1)
	
	self.__django_lib__ = '_Django-1.5.1'
	
	_top = top = self.tops().next()
	__is__ = self.dCheckpoint.has_key(self.__django_lib_symbol__)
	#print 'DEBUG: dCheckpoint.has_key("%s")=%s' % (self.__django_lib_symbol__,__is__)
	if (__is__):
	    self.__django_lib__ = normalize(self.dCheckpoint[self.__django_lib_symbol__])
	    assert (self.__django_lib__) and os.path.exists(self.__django_lib__), 'ERROR: Cannot find %s in (%s) because somebody forgot to build and/or deploy it, maybe ???' % (__django_lib__,_top)
	    i = self.__find_in_sys_path__('vyperlogix')
	    self.__replace__(self.__django_lib__,top,pos=0 if (i < 0) else i)
	    #print 'DEBUG: __django_lib__=%s' % (self.__django_lib__)
	else:
	    #print '(+++) DEBUG: find(%s,%s,%s) !!!' % (top,self.__django_lib__,0)
	    top = normalize(self.find(_top,self.__django_lib__,target=0))
	    assert (top) and os.path.exists(top), 'ERROR: Cannot find %s in (%s) because somebody forgot to build and/or deploy it, maybe ???' % (self.__django_lib__,_top)
	    self.dChanges[self.__django_lib_symbol__] = self.dCheckpoint.get(self.__django_lib_symbol__,None)
	    self.dCheckpoint[self.__django_lib_symbol__] = top
	    self.dChanges[self.__django_lib_symbol__] = '*' if (self.dChanges.get(self.__django_lib_symbol__,None) != self.dCheckpoint.get(self.__django_lib_symbol__,None)) else ''
	    print 'DEBUG: dCheckpoint["%s"]=%s' % (self.__django_lib_symbol__,self.dCheckpoint[self.__django_lib_symbol__])
	
	_top = top = self.tops().next()
	__is__ = (self.dCheckpoint.has_key(self.__app_lib_symbol__)) and (self.dCheckpoint[self.__app_lib_symbol__].find(self.__appID__) > -1)
	#print 'DEBUG: dCheckpoint.has_key("%s")=%s' % (self.__app_lib_symbol__,__is__)
	if (__is__):
	    self.__app__ = normalize(self.dCheckpoint[self.__app_lib_symbol__])
	    assert (self.__app__) and os.path.exists(self.__app__), 'ERROR: Cannot find %s in (%s) because somebody forgot to build and/or deploy it, maybe ???' % (self.__app__,_top)
	    self.__replace__(top,self.__app__,pos=0)
	    #print '(+++) DEBUG: __app__=%s' % (self.__app__)
	else:
	    #print '(+++) DEBUG: find(%s,%s,%s,%s) !!!' % (top,self.__app__,0,1)
	    top = normalize(self.find(_top,self.__app__,target=0,pos=1))
	    assert (top) and os.path.exists(top), 'ERROR: Cannot find %s in (%s) because somebody forgot to build and/or deploy it, maybe ???' % (self.__app__,_top)
	    self.dChanges[self.__app_lib_symbol__] = self.dCheckpoint.get(self.__app_lib_symbol__,None)
	    self.dCheckpoint[self.__app_lib_symbol__] = top
	    self.dChanges[self.__app_lib_symbol__] = '*' if (self.dChanges.get(self.__app_lib_symbol__,None) != self.dCheckpoint.get(self.__app_lib_symbol__,None)) else ''
	    #print 'DEBUG: dCheckpoint["%s"]=%s' % (self.__app_lib_symbol__,self.dCheckpoint[self.__app_lib_symbol__])
	
	if (not os.path.exists(self.__loggingPath__)):
	    try:
		p = self.__loggingPath__
		if (not os.path.isdir(self.__loggingPath__)):
		    p = os.path.dirname(self.__loggingPath__)
		os.mkdir(p)
	    except:
		pass
	
	_is_ = os.environ.has_key('DJANGO_SETTINGS_MODULE')
	print '2._is_=%s' % (_is_)
	if (not _is_):
	    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
	
	from vyperlogix.django import django_utils
	print django_utils.socket.gethostname()
	
	import django
	print 'django.VERSION=',django.VERSION
	assert list(django.VERSION)[0:3] == [1,5,1], 'Oops, something went wrong with the Django installation...'
	
	if (any(len(v) > 0 for v in self.dChanges.values())):
	    #print 'DEBUG: Writing %s' % (self.__checkpoint__)
	    self.fCheckpoint = open(self.__checkpoint__,'w')
	    try:
		self.fCheckpoint.write(json.dumps(self.dCheckpoint))
	    except Exception, ex:
		print 'DEBUG: ex=%s' % (_utils.formattedException(details=ex))
	    finally:
		self.fCheckpoint.flush()
		self.fCheckpoint.close()
	else:
	    print 'DEBUG: Did NOT Write %s because nothing changed.' % (self.__checkpoint__)
	###############################################################################################

    def fileSize(self,fname):
	if (os.path.exists(fname)):
	    st = os.stat(fname)
	    return st.st_size
	return -1

    def remove_all_under_and_including(self,top):
	for root, dirs, files in os.walk(top, topdown=False):
	    for name in files:
		p = os.path.join(root, name)
		#print 'DEBUG: os.remove("%s") !!!' % (p)
		os.remove(p)
	    for name in dirs:
		p = os.path.join(root, name)
		#print 'DEBUG: os.rmdir("%s") !!!' % (p)
		os.rmdir(p)

    def __find__(self,top,fname,target=0):
	fname = str(fname).replace('/',os.sep)
	#print '(%s)-DEBUG.1: top=%s, fname=%s, target=%s' % (funcName(),top,fname,target)
	if (top):
	    for dpath,dnames,filenames in os.walk(top,followlinks=True):
		_target_ = None
		if (target == 0):
		    _target_ = dpath
		elif (target == 1):
		    _target_ = dnames
		elif (target == 2):
		    _target_ = filenames
		_is_ = False
		#print '(%s)-DEBUG.2: _target_=%s' % (funcName(),_target_)
		if (isinstance(_target_,list)):
		    _is_ = fname in _target_
		else:
		    _is_ = _target_.find(fname) > -1
		#print '(%s)-DEBUG.3: _is_=%s' % (funcName(),_is_)
		if (_is_):
		    f = normalize(os.sep.join([dpath,fname]))
		    if (os.path.exists(f)) and (os.path.isfile(f)):
			return f
		    return dpath
	return None
		
    def __find_in_sys_path__(self,pattern):
	pat = str(pattern).lower()
	for i in xrange(0,len(sys.path)-1):
	    p = normalize(sys.path[i])
	    if (p.lower().find(pat) > -1):
		return i
	return -1
		
    def __replace__(self,pattern,target,pos=0,remove=None):
	if (remove):
	    i = self.__find_in_sys_path__(remove)
	    if (i > -1):
		del sys.path[i]
	i = self.__find_in_sys_path__(pattern)
	if (i > -1):
	    del sys.path[i]
	sys.path.insert(pos, target)
		    
