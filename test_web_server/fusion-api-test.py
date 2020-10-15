import requests
import simplejson

def pretty_print(d):
    print '%s BEGIN %s' % ('='*10,'='*30)
    try:
        for k,v in d.iteritems():
            print '%s --> %s' % (k,v)
    except:
        print d
    print '%s END   %s' % ('='*10,'='*30)
    print

if (__name__ == '__main__'):
    __ip__ = '16.83.121.200'
    __username__ = 'Administrator'
    __password__ = 'Compaq123'
    r = requests.post("https://%s/rest/login-sessions" % (__ip__), data=simplejson.dumps({'userName':__username__,'password':__password__}), headers={'Content-Type':'application/json','Accept':'application/json'}, verify=False)
    d = simplejson.loads(r.content)
    __sessionID__ = d['sessionID'] if (d.has_key('sessionID')) else None
    assert len(d['sessionID']) > 0, 'Oops, something went horribly wrong !!!'
    print r.url
    print r.request.method
    pretty_print(d)
    
    
    r = requests.get("https://%s/rest/version" % (__ip__), headers={'Content-Type':'application/json','Accept':'application/json'}, verify=False)
    d = simplejson.loads(r.content)
    print r.url
    print r.request.method
    pretty_print(d)

    r = requests.get("https://%s/rest/datacenters" % (__ip__), headers={'Content-Type':'application/json','Accept':'application/json','auth':__sessionID__}, verify=False)
    d = simplejson.loads(r.content)
    print r.url
    print r.request.method
    pretty_print(d)

