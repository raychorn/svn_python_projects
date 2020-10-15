import json

__url__ = 'http://api.sba.gov/geodata/city_county_links_for_state_of/{{state}}.json'

states = [
"AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
"HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
"MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
"NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
"SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

from vyperlogix import misc

def __context__(request,data=None):
    __data__ = {
        "url": request.META.get('PATH_INFO','/'),
        "siteurl":"http://djangononrelsample2.vyperlogix.com",
        "sitename": "djangononrelsample2&trade;",
        "services": "VyperLogix",
        "company": "VyperLogix",
        "sitename2": "The djangononrelsample2&trade;"
    }
    if (misc.isDict(data)):
        for k,v in data.iteritems():
            __data__[k] = v
    return __data__

def fetch_data(url):
    __data__ = {}

    from google.appengine.api import urlfetch
    
    try:
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            __data__ = json.loads(result.content)
    except:
        __data__ = {}
    return __data__

def fetch_data_for(state):
    url = __url__.replace('{{state}}', str(state).lower())
    #print >>sys.stdout, 'INFO: Fetching data from "%s".' % (url)
    __data__ = fetch_data(url)
    return __data__

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL template in the form of: %s" % (__url__), type=str, nargs='?', default=__url__)
    args = parser.parse_args()
    
    if (args.url):
        __url__ = args.url

    fpath = os.path.abspath(os.sep.join(['.','data']))
    if (os.path.exists(fpath)):
        files = os.listdir(fpath)
        for f in files:
            fn = os.sep.join([fpath,f])
            if (os.path.exists(fn)):
                os.remove(fn)
        os.removedirs(fpath)
    if (not os.path.exists(fpath)):
        os.mkdir(fpath)
    
    def __main__():
        for state in states:
            __data__ = fetch_data_for(state)
            __json__ = json.dumps(__data__, indent=4)
            fname = os.sep.join([fpath,'%s.json' % (state)])
            print >> sys.stdout, 'Saving data in "%s".' % (fname)
            fOut = open(fname,'w')
            try:
                print >>fOut, __json__
            except:
                pass
            fOut.flush()
            fOut.close()
            print >> sys.stdout, '\n'
    
    __main__()
    