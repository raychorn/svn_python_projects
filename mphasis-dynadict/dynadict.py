from vyperlogix import misc
from vyperlogix.classes.MagicObject import MagicObject2

class DynaDict(MagicObject2):
    def __init__(self, dictionary):
        self.__dictionary__ = dictionary

    def __call__(self,*args,**kwargs):
	from vyperlogix.lists import ConsumeableList
	n = ConsumeableList(self.n)
	items = []
	for item in n:
	    if (item.startswith('__') and item.endswith('__')):
		break
	    items.append(item)
	s = 'self.__handler__(%s, *args,**kwargs)' % ('[%s]'%(','.join(['"%s"'%(i) for i in items])))
	try:
	    results = eval(s,globals(),locals())
	except Exception, details:
	    results = None
	    print >> sys.stderr, _utils.formattedException(details=details)
	return results

    def __getattr__(self,name):
	normalize = lambda n:'__%s__'%(n)
        if name in ('__str__','__repr__'): return lambda:'instance of %s at %s' % (str(self.__class__),id(self))
	__name__ = normalize(name)
	if (self.__dict__.has_key(__name__)):
	    self.__reset_magic__()
	    return self.__dict__[__name__]
        if not self.__dict__.has_key('n'):self.n=[]
	if (name == self.basename):
	    self.__reset_magic__()
	    self.n.append(name)
	    return self
        self.n.append(name)
        return self
        
    def __getitem__(self,name):
        self.n.append(name)
	c = self.__dictionary__
	for _n_ in self.n[0:-1]:
	    if (misc.isDict(c)) and (c.has_dict(_n_)):
		c = c[_n_]
        return self
        
    def __handler__(self,items,*args,**kwargs):
	uri = []
	parms = []
	uri.append(items[0])
	if (uri[0] == self.basename):
	    uri.append(self.username)
	    uri.append(self.password)
	    for item in items[1:]:
		uri.append(item)
	    for arg in args:
		uri.append(arg)
	    for k,v in kwargs.iteritems():
		parms.append('%s=%s'%(k,v))
	    if (len(parms) > 0):
		uri.append('?%s'%('&'.join(parms)))
	__uri__ = '/'.join(uri)
	print '\t --> %s' % (__uri__)
	r = requests.get(normalize_uri(self.uri)+__uri__)
	if (r.status_code != 200):
	    r.raise_for_status()
	d = r.json()
	status = d.get('status',None)
	if (str(status).upper() != 'SUCCESS'):
	    raise ValueError('Cannot retrieve the requested value at this time due to the following: %s' % (status))
	return SmartObject(d)

if (__name__ == '__main__'):
    d = {}
    p = DynaDict(d)
    print 'p["sample"]=%s' % (p['sample'])
