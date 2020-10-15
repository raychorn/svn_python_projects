class Session(dict):
    def __init__(self, *args):
	import tempfile
        dict.__init__(self, args)
	self.__filename__ = tempfile.NamedTemporaryFile().name
	print self.__filename__
	
    def __getKey__(self,key):
	from vyperlogix.misc.hex import strToHex
	return strToHex(key)
    
    def __delete__(self,key):
	import os
	import simplejson
	fname = self.__dict__['__filename__']
	if (os.path.exists(fname)):
	    f = open(fname,'r')
	    json = f.read()
	    f.close()
	    f = open(fname,'w')
	else:
	    f = open(fname,'w')
	    json = '{}'
	try:
	    obj = simplejson.loads(json)
	except:
	    obj = {}
	__key__ = self.__getKey__(key)
	if (obj.has_key(__key__)):
	    del obj[__key__]
	json = simplejson.dumps(obj)
	f.write(json)
	f.flush()
	f.close()

    def __write__(self,key,value):
	if (key == '__filename__'):
	    self.__dict__[key] = value
	    return 
	import os
	import simplejson
	fname = self.__dict__['__filename__']
	if (os.path.exists(fname)):
	    f = open(fname,'r')
	    json = f.read()
	    f.close()
	    f = open(fname,'w')
	else:
	    f = open(fname,'w')
	    json = '{}'
	try:
	    obj = simplejson.loads(json)
	except:
	    obj = {}
	__key__ = self.__getKey__(key)
	obj[__key__] = value
	json = simplejson.dumps(obj)
	f.write(json)
	f.flush()
	f.close()

    def __read__(self,key):
	if (key == '__filename__'):
	    return self.__dict__[key]
	import os
	import simplejson
	fname = self.__dict__['__filename__']
	if (os.path.exists(fname)):
	    f = open(fname,'r')
	    json = f.read()
	else:
	    json = '{}'
	try:
	    obj = simplejson.loads(json)
	except:
	    obj = {}
	__key__ = self.__getKey__(key)
	value = obj[__key__] if (obj.has_key(__key__)) else None
	f.close()
	return value
    
    def keys(self):
	import os
	import simplejson
	from vyperlogix.misc.hex import hexToStr
	fname = self.__dict__['__filename__']
	if (os.path.exists(fname)):
	    f = open(fname,'r')
	    json = f.read()
	else:
	    json = '{}'
	try:
	    obj = simplejson.loads(json)
	except:
	    obj = {}
	f.close()
	return [hexToStr(k) for k in obj.keys()]

    def __getitem__(self,key):
	return self.__read__(key)

    def __setitem__(self,key,value):
	self.__write__(key, value)

    def __getattr__(self,key):
	return self.__read__(key)

    def __setattr__(self,key,value):
	self.__write__(key, value)

    def __get__(self,key):
	return self.__read__(key)

    def __set__(self,key,value):
	self.__write__(key, value)
	
    def __delattr__(self,key):
	self.__delete__(key)

    def __delitem__(self,key):
	self.__delete__(key)

