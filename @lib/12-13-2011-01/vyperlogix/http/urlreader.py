import urllib
import httplib
import urlparse

from vyperlogix.hash import lists 

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

def read_from_url(host,url):
    toks = host.split(':')
    host = toks[0]
    port = 80 if (len(toks) != 2) else toks[-1]
    conn = httplib.HTTPConnection(host,port=port)
    conn.request("GET", url)
    isError = False
    try:
        resp = conn.getresponse()
    except:
        isError = True
    data = ''
    if ( (isError == False) and (resp.status == 200) and (resp.reason == 'OK') ):
        data = resp.read()
    else:
        d = lists.HashedFuzzyLists2(resp.msg.dict)
        location = d['location']
        if (resp.status == 302):
            foo = urlparse.urlparse(location)
            return read_from_url(foo[1],foo[2])
    return data
