from vyperlogix import misc
from vyperlogix.misc import _utils

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

# Table mapping response codes to messages; entries have the
# form {code: (shortmessage, longmessage)}.
responses = {
    100: ('Continue', 'Request received, please continue'),
    101: ('Switching Protocols',
          'Switching to new protocol; obey Upgrade header'),

    200: ('OK', 'Request fulfilled, document follows'),
    201: ('Created', 'Document created, URL follows'),
    202: ('Accepted',
          'Request accepted, processing continues off-line'),
    203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
    204: ('No Content', 'Request fulfilled, nothing follows'),
    205: ('Reset Content', 'Clear input form for further input.'),
    206: ('Partial Content', 'Partial content follows.'),

    300: ('Multiple Choices',
          'Object has several resources -- see URI list'),
    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    302: ('Found', 'Object moved temporarily -- see URI list'),
    303: ('See Other', 'Object moved -- see Method and URL list'),
    304: ('Not Modified',
          'Document has not changed since given time'),
    305: ('Use Proxy',
          'You must use proxy specified in Location to access this '
          'resource.'),
    307: ('Temporary Redirect',
          'Object moved temporarily -- see URI list'),

    400: ('Bad Request',
          'Bad request syntax or unsupported method'),
    401: ('Unauthorized',
          'No permission -- see authorization schemes'),
    402: ('Payment Required',
          'No payment -- see charging schemes'),
    403: ('Forbidden',
          'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
          'Specified method is invalid for this server.'),
    406: ('Not Acceptable', 'URI not available in preferred format.'),
    407: ('Proxy Authentication Required', 'You must authenticate with '
          'this proxy before proceeding.'),
    408: ('Request Timeout', 'Request timed out; try again later.'),
    409: ('Conflict', 'Request conflict.'),
    410: ('Gone',
          'URI no longer exists and has been permanently removed.'),
    411: ('Length Required', 'Client must specify Content-Length.'),
    412: ('Precondition Failed', 'Precondition in headers is false.'),
    413: ('Request Entity Too Large', 'Entity is too large.'),
    414: ('Request-URI Too Long', 'URI is too long.'),
    415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
    416: ('Requested Range Not Satisfiable',
          'Cannot satisfy request range.'),
    417: ('Expectation Failed',
          'Expect condition could not be satisfied.'),

    500: ('Internal Server Error', 'Server got itself in trouble'),
    501: ('Not Implemented',
          'Server does not support this operation'),
    502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
    503: ('Service Unavailable',
          'The server cannot process the request due to a high load'),
    504: ('Gateway Timeout',
          'The gateway server did not receive a timely response'),
    505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
}

def get(url):
    import urllib2
    try:
        response = urllib2.urlopen(url)
        html = response.read()
    except:
        html = ''
    return html

def parse_href_into_parms(href):
    return [[x.split('=') for x in tt] for tt in [t.split('&') for t in href.split('?')]]

def strip_xml_header(content):
    import re

    _re_xml_header = re.compile(r"<\?xml(.*?)\?>")
    _re_divs = re.compile("<div (.*?)>")

    _content = content
    for match in _re_xml_header.finditer(_content):
        _content = _content[0:match.start()] + _content[match.end():]
    return _content

def authenticate_request(request,username,password):
    import base64

    base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
    authheader =  "Basic %s" % base64string
    request.add_header("Authorization", authheader)

def handle_response(request,logging=None):
    import sys
    import urllib2

    try:
        response = urllib2.urlopen(request)
    except IOError, e:
        info_string = "It looks like the username or password is wrong."
        try:
            logging.warning(info_string)
        except:
            pass
        return None
    return response.read()

def http_get_authenticated(url,username,password,logging=None):
    import re
    import sys
    import urllib2

    req = urllib2.Request(url)
    try:
        handle = urllib2.urlopen(req)
    except IOError, e:
        info_string = _utils.formattedException(details=e)
        try:
            logging.error(info_string)
        except:
            pass
    else:
        info_string = "This page isn't protected by authentication."
        try:
            logging.warning(info_string)
        except:
            pass

    if not hasattr(e, 'code') or e.code != 401:
        # we got an error - but not a 401 error
        info_string = "This page isn't protected by authentication.  But we failed for another reason."
        try:
            logging.warning(info_string)
        except:
            pass

    authline = e.headers['www-authenticate']
    # this gets the www-authenticate line from the headers
    # which has the authentication scheme and realm in it

    authobj = re.compile(
        r'''(?:\s*www-authenticate\s*:)?\s*(\w*)\s+realm=['"]([^'"]+)['"]''',
        re.IGNORECASE)
    # this regular expression is used to extract scheme and realm
    matchobj = authobj.match(authline)

    if not matchobj:
        # if the authline isn't matched by the regular expression
        # then something is wrong
        info_string = 'The authentication header is badly formed.'
        try:
            logging.warning(info_string)
        except:
            pass

    scheme = matchobj.group(1)
    realm = matchobj.group(2)
    # here we've extracted the scheme
    # and the realm from the header
    if scheme.lower() != 'basic':
        info_string = 'This example only works with BASIC authentication.'
        try:
            logging.warning(info_string)
        except:
            pass

    authenticate_request(req,username,password)
    return handle_response(req)

def http_post(url,parms,username=None,password=None,logging=None):
    import urllib, urllib2
    
    data = urllib.urlencode(parms)
    request = urllib2.Request(url, data)
    if (misc.isString(username)) and (misc.isString(password)):
        authenticate_request(request,username,password)
    return handle_response(request,logging=logging)

def http_post_authenticated(url,parms,username,password,logging=None):
    return http_post(url,parms,username=username,password=password,logging=logging)
