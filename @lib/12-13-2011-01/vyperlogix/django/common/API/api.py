from vyperlogix import misc

from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.classes.SmartObject import SmartObject, SmartFuzzyObject

from vyperlogix.hash.lists import HashedFuzzySmartLists

class API(SmartFuzzyObject):
    @classmethod
    def make_key(self,name,version):
        isVersionValid = version is not None
        return '%s%s%s'%(version if (isVersionValid) else '','@' if (isVersionValid) else '',name)
    
    def __init__(self,source,secure_endpoint,insecure_endpoint,key=None):
        self.__secure_endpoint__ = secure_endpoint
        self.__insecure_endpoint__ = insecure_endpoint
	self.__specific__ = False
        d = self.__prepare__(source,self.__secure_endpoint__,self.__insecure_endpoint__,key)
        super(API, self).__init__(d)

    def __prepare__(self,source,secure_endpoint,insecure_endpoint,key=None):
        import urlparse
        d = {}
        ch = API.make_key('','')
        for k,v in source.iteritems():
            try :
                isNotProcessed = k.find(ch) == -1
                if (isNotProcessed):
		    if (v.url != '/'):
			toks = urlparse.urlparse(v.url if (v.url is not None) else v)
			if ( (len(toks.netloc) == 0) or ( (secure_endpoint.find(toks.netloc) == -1) and (insecure_endpoint.find(toks.netloc) == -1) ) ):
			    p_toks = toks.path.split('/')
			    if (len([p for p in p_toks if (len(p) > 0)]) > 0) and (len(p_toks[-1]) == 0):
				p_toks.insert(1,key)
				toks = urlparse.ParseResult(toks.scheme,toks.netloc,'/'.join(p_toks),toks.params,toks.query,toks.fragment)
			    if (v.url is not None):
				v.url = urlparse.urlunparse(toks)
			    else:
				v = urlparse.urlunparse(toks)
                d[API.make_key(k,key) if (isNotProcessed) else k] = v
            except:
                pass
        return d
    
    def __append__(self,source,key=None,noPrepare=False):
        d = self.__prepare__(source,self.__secure_endpoint__,self.__insecure_endpoint__,key=key) if (not noPrepare) else source
        for k,v in d.iteritems():
            try :
                self[k] = v
            except:
                pass
            
    def __getattr__(self, name):
        value = super(API, self).__getattr__(name)
        if (value is None) or (len(value) == 0): # and (name != '/'):
	    _d_ = HashedFuzzySmartLists({})
	    _values_ = []
	    for k in self.keys():
		if (misc.isDict(super(API, self).__getattr__(k))) and (super(API, self).__getattr__(k).has_key('url')):
		    _k_ = super(API, self).__getattr__(k)['url'].replace('/'+k.split('@')[0],'')
		    _d_[_k_] = SmartFuzzyObject(super(API, self).__getattr__(k))
            l = ListWrapper(_d_.keys())
	    _name_ = name.split(API.make_key('',''))[-1]
	    if (not self.__specific__):
		while (len(_name_) > 0):
		    _list_ = l.findAllContaining(_name_) if (_name_ != '/') else l.findAllMatching(_name_)
		    _items_ = [item for item in _list_ if (item.endswith(_name_))]
		    x = l.findFirstMatching(_items_[0] if (len(_items_) > 0) else _name_) if ( (len(_list_) > 0) or (_name_ == '/') ) else l.findFirstContaining(_items_[0] if (len(_items_) > 0) else _name_)
		    if (x > -1):
			for v in _d_[l[x]]:
			    _values_.append(v)
			break
		    else:
			x = l.findFirstContaining(_name_)
			if (x > -1):
			    for v in _d_[l[x]]:
				_values_.append(v)
			    break
			else:
			    _l_ = _name_.split('/')
			    del _l_[-2 if (len(_l_[-1]) == 0) else -1]
			    _name_ = '/'.join(_l_)
        return value if (len(_values_) == 0) else _values_

    def __getitem__(self, name):
        return self.__getattr__(name)
    
    def asDict(self,into={}):
	for k,v in self.__dict__.iteritems():
	    if (not misc.isSimpleDict(v)):
		try:
		    into[k] = v.asDict() if (callable(v.asDict)) else v
		except:
		    into[k] = v
	    else:
		into[k] = v
        return into

    def asPythonDict(self):
	_d_ = {}
        return self.asDict(into=_d_)
    
    def asMap(self,noIgnore=False):
        from vyperlogix.hash import lists
        ch = API.make_key('','')
        d = self.asDict()
        d2 = {}
        for k,v in d.iteritems():
            if (not noIgnore) and (k in ['__dict__','__secure_endpoint__','__insecure_endpoint__']):
                continue
            elif (k in ['__dict__']):
                continue
            try:
                v.url = v.url if (v.url != []) else None
                v.key = v.key if (v.key != []) else None
                isObject = (v.url is not None) or (v.key is not None)
                _v_ = v.url if (isObject and v.url) else v.key if (isObject and v.key) else v
                if (not noIgnore) and ( (k.find(ch) == -1) or ( (isObject and v.url) and (not _v_.startswith('/')) and (not _v_.endswith('/')) ) ):
                    pass
                else:
                    if (isObject):
                        v.url = None
                        v.key = k
                        d2[_v_] = v if (not noIgnore) else v.key
                    else:
                        d2[_v_] = k
            except:
                d2[k] = v
        return d2
    
    def isAPI():
        doc = "isAPI is True when this object is an API object."
        def fget(self):
            return True
        return locals()    
    isAPI = property(**isAPI())

class APIVersion1000(API):
    __version__ = '1.0.0.0'
    def __init__(self,source,secure_endpoint,insecure_endpoint):
        super(APIVersion1000, self).__init__(source,secure_endpoint,insecure_endpoint,key=APIVersion1000.__version__)

    def appendVersion1000(self,source):
        super(APIVersion1000, self).__append__(source,key=APIVersion1000.__version__)
        
    def __getattr__(self, name):
        value = super(API, self).__getattr__(name)
        if (value is None) or (value == []):
            l = ListWrapper(self.keys())
            x = l.findFirstContaining(API.make_key(name.split(API.make_key('',''))[-1],APIVersion1001.__version__) if (name.startswith('/') and name.endswith('/')) else name)
            if (x > -1):
                return super(API, self).__getattr__(l[x])
            else:
                return super(APIVersion1000, self).__getattr__(name)
        return value
        
class APIVersion1001(APIVersion1000):
    __version__ = '1.0.0.1'
    def __init__(self,source,secure_endpoint,insecure_endpoint):
        super(APIVersion1000, self).__init__(source,secure_endpoint,insecure_endpoint,key=APIVersion1001.__version__)

    def appendVersion1001(self,source):
        super(APIVersion1001, self).__append__(source,key=APIVersion1001.__version__)
        
    def __getattr__(self, name):
        value = super(API, self).__getattr__(name)
        if (value is None) or (value == []):
            l = ListWrapper(self.keys())
            x = l.findFirstContaining(API.make_key(name.split(API.make_key('',''))[-1],APIVersion1001.__version__) if (name.startswith('/') and name.endswith('/')) else name)
            if (x > -1):
                return super(API, self).__getattr__(l[x])
            else:
                return super(APIVersion1001, self).__getattr__(name)
        return value
