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
def uniqueMACSignature():
    import uuid
    import time
    from vyperlogix.sockets import getMac
    from vyperlogix.misc import _utils
    u = ''.join(str(uuid.uuid4()).split('-'))
    print u
    m = ''.join(getMac.getHwAddr('eth0').split(':'))
    print m
    d = time.time()
    print '%s --> %s' % (d,time.ctime(d))
    md = '%s%s' % (m,d)
    len_u = len(u)
    len_md = len(md)
    if (len_u > len_md):
        md = '0'*(len_u-len_md)+md
    else:
        u = '0'*(len_md-len_u)+u
    s = ''.join([u[i]+md[i] for i in xrange(len_u)])
    return s

def unpackUniqueMACSignature(sig):
    import time
    u = ''
    md = ''
    for i in xrange(len(sig)):
        if ((i % 2) == 0):
            u += sig[i]
        else:
            md += sig[i]
    leading_zeros = ''
    has_leading_zeros = (md[0] == '0')
    if (has_leading_zeros):
        while (md[0] == '0'):
            leading_zeros += md[0]
            md = md[1:]
    m = md[0:12]
    d = float(md[12:])
    return (u,m,time.ctime(d))

if (__name__ == '__main__'):
    sig = uniqueMACSignature()
    print sig
    u,m,d = unpackUniqueMACSignature(sig)
    print u,m,d

