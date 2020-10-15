import urllib2

def main():
    theurl = 'http://pypi.python.org/pypi?%3Aaction=login'
    req = urllib2.Request(theurl)
    try:
        handle = urllib2.urlopen(req)
    except IOError, e:
        if hasattr(e, 'code'):
            if e.code != 401:
                print 'We got another error'
                print e.code
            else:
                print e.headers
                print e.headers['www-authenticate']

if (__name__ == '__main__'):
    main()
