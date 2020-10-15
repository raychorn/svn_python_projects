class ymlAttr():
    def __str__(self):
	return '%s=%s' % (self.key, self.value)

class ymlObject():
    def __init__(self,name):
	self.name = name
	self.attrs = []
    
    def attrNamed(self,name):
        for a in self.attrs:
            if (a.key == name):
                return a
        return None
        
    def attrValueForName(self,name):
	_value = ''
	try:
	    a = self.attrNamed(name)
	    if (a != None):
		_value = a.value
	except Exception, details:
	    print 'ERROR in determining the "%s" due to (%s)' % (name,str(details))
	return _value
        
    def attrsForName(self,name):
	attrs = []
	for y in self.attrs:
	    if (y.key == name):
		attrs.append(y)
	return attrs
        
    def dumpAttrs(self):
        s = '';
        i = 1
        n = len(self.attrs)
        for t in self.attrs:
            s += str(t)
            if (i < n):
                s += ','
            i += 1
        return s
    
    def __str__(self):
        return 'name=%s, (%s)' % (self.name, self.dumpAttrs())

    def add(self,key,value):
        a = ymlAttr()
        a.key = key.strip()
        a.value = value.strip()
        self.attrs.append(a)

    def ymlAttrs(self):
        return self.attrs

class ymlReader(object):
    def __init__(self,fname):
        self.fname = fname
        self.objects = []
        self.curObj = None
        
    def objectsNamed(self,name):
        list = []
        for o in self.objects:
            if (o.name == name):
                list.append(o)
        return list
    
    def pruneToks(self,toks):
        n = len(toks)
        while (n > 0) and (len(toks[n-1]) == 0):
            toks.pop()
            n = len(toks)
        return toks
        
    def parseLine(self,line):
        toks = line.split('#')
        return toks[0].strip()

    def splitFirst(self,s,delim):
	toks = []
	i = s.find(delim)
	if (i > -1):
	    toks.append(s[0:i])
	else:
	    i = 0
	toks.append(s[i+1:len(s)])
	return toks
    
    def read(self):
        inObject = False
        isError = False
        try:
            fhand = open(self.fname, 'r')
        except Exception, details:
            print 'ERROR - (%s)' % str(details)
            isError = True
        if (isError == False):
            try:
                for line in fhand:
                    buf = self.parseLine(line)
		    toks = self.splitFirst(buf,':')
                    toks = self.pruneToks(toks)
                    if (inObject == False):
                        inObject = (len(toks) == 1)
                        if ( (inObject) and (self.curObj == None) ):
                            self.curObj = ymlObject(toks[0])
                    else:
                        if (len(toks) >= 2):
                            self.curObj.add(toks[0],toks[1])
                            #print '[%s] buf=(%s)' % (str(len(buf)),buf)
                        else:
                            if (self.curObj != None):
                                self.objects.append(self.curObj)
                                self.curObj = None
                            inObject = False
            finally:
                if (self.curObj != None):
                    self.objects.append(self.curObj)
                    self.curObj = None
                fhand.close()

if __name__ == "__main__":
    import cProfile
    import gc
    y = ymlReader('../database.yml')
    #gc.disable()
    #cProfile.run('for i in xrange(1000): y.read()')
    y.read()
    print str(y)
    print str(y.objects)
    print '\n'
    for y in y.objects:
        print str(y)
        print '==========' * 2
    