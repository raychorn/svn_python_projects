import urllib
import httplib
from vyperlogix.hash import lists
from vyperlogix.html.parsers.HTMLParsers import TargetedHTMLParser

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

def performGoogleSearch(searchString,start=-1):
    results = lists.HashedLists()
    __failedSearch_symbol='\xe4\xe9\xe4\xa0\xee\xef\xf4\xa0\xed\xe1\xf4\xe3\xe8\xa0\xe1\xee\xf9\xa0\xe4\xef\xe3\xf5\xed\xe5\xee\xf4\xf3'
    failedSearch_symbol = ''.join([chr(ord(ch)&127) for ch in __failedSearch_symbol])
    __failedSearch2_symbol = "\xce\xef\xa0\xf3\xf4\xe1\xee\xe4\xe1\xf2\xe4\xa0\xf7\xe5\xe2\xa0\xf0\xe1\xe7\xe5\xf3\xa0\xe3\xef\xee\xf4\xe1\xe9\xee\xe9\xee\xe7\xa0\xe1\xec\xec\xa0\xf9\xef\xf5\xf2\xa0\xf3\xe5\xe1\xf2\xe3\xe8\xa0\xf4\xe5\xf2\xed\xf3\xa0\xf7\xe5\xf2\xe5\xa0\xe6\xef\xf5\xee\xe4\xae"
    failedSearch2_symbol = ''.join([chr(ord(ch)&127) for ch in __failedSearch2_symbol])

    __url="\xf7\xf7\xf7\xae\xe7\xef\xef\xe7\xec\xe5\xae\xe3\xef\xed\xba\xb8\xb0"
    url = ''.join([chr(ord(ch)&127) for ch in __url])

    __term = "\xaf\xf3\xe5\xe1\xf2\xe3\xe8\xbf\xf1\xbd\xa5\xf3\xa6\xe9\xe5\xbd\xf5\xf4\xe6\xad\xb8\xa6\xef\xe5\xbd\xf5\xf4\xe6\xad\xb8\xa6\xe1\xf1\xbd\xf4\xa6\xf2\xec\xf3\xbd\xef\xf2\xe7\xae\xed\xef\xfa\xe9\xec\xec\xe1\xba\xe5\xee\xad\xd5\xd3\xba\xef\xe6\xe6\xe9\xe3\xe9\xe1\xec\xa6\xe3\xec\xe9\xe5\xee\xf4\xbd\xe6\xe9\xf2\xe5\xe6\xef\xf8\xad\xe1"
    _term = ''.join([chr(ord(ch)&127) for ch in __term])

    if (start > -1):
        _term += '&start=%s' % start

    print 'url="%s"' % url
    print '_term="%s"' % _term

    conn = httplib.HTTPConnection(url)
    conn.request("GET", _term % (urllib.quote(searchString)))
    isError = False
    try:
        r1 = conn.getresponse()
    except:
        isError = True
    if ( (isError == False) and (r1.status == 200) and (r1.reason == 'OK') ):
        data1 = r1.read()
        myParser = TargetedHTMLParser()
        myParser.targetTag('a')
        myParser.feed(data1)
        fname = urllib.quote(searchString).replace('/','+')
        if ( (data1.find(failedSearch_symbol) == -1) and (data1.find(failedSearch2_symbol) == -1) and (myParser.tagCount > 0) ):
            pass
        else:
            results['data'] = data1.split('\n')
        results['search'] = searchString
        results['parser'] = myParser
    return results
