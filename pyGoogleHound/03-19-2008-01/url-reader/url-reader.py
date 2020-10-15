import urllib
from BeautifulSoup import BeautifulSoup

def fetchFromURL(url):
    import urllib2
    handle = urllib2.urlopen(url)
    try:
        html = handle.read().lower()
    finally:
        handle.close()
    return html

num = 0

def asTag(tag,verbose=False):
    values = []
    if (verbose):
        attrs = tag.attrs
        for attr in attrs:
            values.append('%s=%s'%(attr[0],attr[-1]))
    return '<%s%s%s>'%(tag.name,' ' if (len(values) > 0) else '',','.join(values))

def getChildren(aChild,target=[],verbose=False):
    global num
    try:
        chidren = aChild.childGenerator()
        for aChild in chidren:
            isCallable = False
            siblings = aChild.nextSiblingGenerator()
            for aSibling in siblings:
                if (aSibling):
                    num +=1
                    aTag = asTag(aSibling,verbose=verbose)
                    print '%s : %s' % (num,aTag)
                    target.append(aTag)
                    try:
                        if (callable(aSibling.childGenerator)):
                            getChildren(aSibling,target=target)
                    except:
                        pass
            try:
                if (callable(aChild.childGenerator)):
                    isCallable = True
                    getChildren(aChild,target=target)
            except:
                pass
            if (not isCallable):
                try:
                    aTag = asTag(aChild,verbose=verbose)
                    num +=1
                    print '%s : %s' % (num,aTag)
                    target.append(aTag)
                except:
                    pass
    except:
        pass

def getTagsFrom(url,target=[],verbose=False):
    try:
        html = fetchFromURL(url)
        soup = BeautifulSoup(html)
        getChildren(soup,target=target,verbose=verbose)
    except:
        pass

if (__name__ == '__main__'):
    target = []
    getTagsFrom('http://google.com',target=target,verbose=False)
    pass

