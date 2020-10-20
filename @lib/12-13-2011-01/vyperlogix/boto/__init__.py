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
import os, sys

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash.lists import HashedLists2
from vyperlogix.crypto import blowfish
from vyperlogix.classes import SmartObject

from vyperlogix.enum import Enum

from vyperlogix import oodb

from vyperlogix import ssl

__passphrase__ = 'V~scHqj]V$HdCe/)34"3dN:gAcT`uJrk&-Kt1}mqb"_y;0W=5$jnVi|_'

#__url__ = 'http://cdn-python.s3-website-us-east-1.amazonaws.com/credentials_secure.txt'

#x = oodb.strToHex(blowfish.encryptData(__url__, __passphrase__))

__url__ = '2E7BC64BCDCBED1751A179A330C9BB772091684720523EAE3567C79B9272F129763242FC370DB7E3183CECCC6A4878D6E301ED66B2EFF878B078325025A27B20169FECC6FF4456755B43E0812B060B8C'

class Methods(Enum.Enum):
    none = 0
    default = 2^0
    improved = 2^2

decrypt = lambda encrypted:_utils.ascii_only(blowfish.decryptData(oodb.hexToStr(encrypted), __passphrase__))

def _url_():
    return decrypt(__url__)

def unweave_from(contents):
    from vyperlogix.iterators import iterutils
    target = []
    phrase = []
    for t in iterutils.itergroup([i for i in contents.strip()], 4):
        _t_ = list(t)
        n = len(_t_)/2
        target.append(''.join(_t_[0:n]))
        phrase.append(''.join(_t_[n:]))
    return (''.join(target),''.join(phrase))

def __get_aws_credentials__(contents,method=Methods.default):
    from vyperlogix.iterators import iterutils
    _contents_,passphrase = (contents,None)
    if (method is Methods.improved):
        _contents_,passphrase = unweave_from(contents)
        passphrase = oodb.hexToStr(passphrase) if (misc.isString(passphrase)) else __passphrase__
        assert passphrase == __passphrase__, 'WARNING: Something has gone wrong with the passPhrase.'
        contents = blowfish.decryptData(oodb.hexToStr(_contents_), passphrase)
        contents = contents.split(chr(0x00))[0]
    d = HashedLists2(fromDict=dict([tt.split('=') for tt in [t.strip() for t in contents.split('\n')] if (len(tt) > 0)]))
    if (method is not Methods.improved):
        for k,v in d.iteritems():
            _k_ = _utils.ascii_only(blowfish.decryptData(oodb.hexToStr(k), __passphrase__))
            d[_k_] = _utils.ascii_only(blowfish.decryptData(oodb.hexToStr(v), __passphrase__))
            del d[k]
    return SmartObject.SmartFuzzyObject(args=d.asDict(isCopy=True))

def get_aws_credentials(filename=None,url=_url_()):
    tuples = []
    if (not filename):
        try:
            c = ssl.fetch_from_web(url)
        except Exception, ex:
            c = None
    if (filename) or (c):
        c = _utils.readBinaryFileFrom(filename) if (filename) else c
        for l in [l.split('=') for l in c.splitlines() if (len(l) > 0)]:
            tuples.append(tuple([decrypt(l[0]),decrypt(l[-1])]))
    return SmartObject.SmartFuzzyObject(args=dict(tuples))

def weave_into(target,phrase):
    from vyperlogix.iterators import iterutils
    normalize = lambda foo,m:foo+('00'*(m-(len(foo)/2)) if ((len(foo)/2) < m) else '')
    results = []
    target = _utils.ascii_only(target)
    phrase = _utils.ascii_only(phrase)
    m = max(len(target)/2,len(phrase)/2)
    m += m % 2
    target = normalize(target,m)
    phrase = normalize(phrase,m)
    assert len(target) == len(phrase), 'ERROR: Something went wrong with the normalization in %s' % (misc.funcName())
    pGen = (pCh for pCh in iterutils.itergroup([p for p in phrase], 2))
    for t in iterutils.itergroup([i for i in target], 2):
        results.append(''.join(t))
        results.append(''.join(pGen.next()))
    return ''.join(results)

if (__name__ == '__main__'):
    ##################################################
    # BEGIN: Gen a new passphrase 
    ##################################################
    #from vyperlogix.misc import GenPasswd
    #_pass_ = GenPasswd.GenPasswd(length=448/8,chars=GenPasswd.chars_printable)
    #print _pass_
    ##################################################
    # END!    Gen a new passphrase 
    ##################################################

    #toks = _url_().split('/')
    #t2 = oodb.strToHex(blowfish.encryptData(toks[-2], __passphrase__))
    #print '%s=%s' % (toks[-2],t2)
    #t1 = oodb.strToHex(blowfish.encryptData(toks[-1], __passphrase__))
    #print '%s=%s' % (toks[-1],t1)
    #_u_ = oodb.strToHex(blowfish.encryptData(_url_(), __passphrase__))
    #print _u_

    #if (0):
        #fname = os.path.abspath('./credentials.txt')
        #toks = list(os.path.splitext(fname))
        #toks[0] += '_secure'
        #fnameOut = ''.join(toks)
        #method = Methods.default
        #if (not os.path.exists(fnameOut)):
            #io = _utils.stringIO()
            #if (os.path.exists(fname)):
                #c = _utils.readBinaryFileFrom(fname)
                #d = HashedLists2(fromDict=dict([tt.split('=') for tt in [t.strip() for t in c.split('\n')] if (len(tt) > 0)]))
            #else:
                #soCredentials = get_aws_credentials(url=_url_(),filename=None)
                #d = HashedLists2(fromDict=soCredentials.asPythonDict())
                #method = Methods.improved
            #f_out = open(fnameOut, mode='wb', buffering=1)
            #dE = d.asDict(isCopy=True)
            #for k,v in dE.iteritems():
                #_k_ = oodb.strToHex(blowfish.encryptData(k, __passphrase__))
                #del dE[k]
                #_v_ = oodb.strToHex(blowfish.encryptData(v, __passphrase__))
                #dE[_k_] = _v_
                #print >>io, '%s%s%s' % (k,'=',v)
            #_contents_ = weave_into(oodb.strToHex(blowfish.encryptData(io.getvalue(), __passphrase__)),oodb.strToHex(__passphrase__))
            #print >> f_out, _contents_
            #f_out.flush()
            #f_out.close()
            #soCredentials2 = __get_aws_credentials__(_contents_,method=method)
            #assert soCredentials.AWSAccessKeyId == soCredentials2.AWSAccessKeyId, 'WARNING: Something is wrong with the Improved method.'
            #assert soCredentials.AWSSecretKey == soCredentials2.AWSSecretKey, 'WARNING: Something is wrong with the Improved method.'
            #dP = HashedLists2(fromDict=dE).asDict()
            #for k,v in dP.iteritems():
                #_k_ = _utils.ascii_only(blowfish.decryptData(oodb.hexToStr(k), __passphrase__))
                #dP[_k_] = _utils.ascii_only(blowfish.decryptData(oodb.hexToStr(v), __passphrase__))
                #del dP[k]
                #assert dP[_k_] == d[_k_], 'WARNING: Expected %s to match %s.' % (dP[_k_],d[_k_])
        #if (os.path.exists(fnameOut)):
            #soCredentials = get_aws_credentials(filename='./credentials_secure.txt',method=method)

    if (1):
        soCredentials = get_aws_credentials(url=_url_(),filename=None,method=Methods.default)
        soCredentials2 = get_aws_credentials(url=_url2_(),filename=None,method=Methods.improved)
        assert soCredentials.AWSAccessKeyId == soCredentials2.AWSAccessKeyId, 'WARNING: Something is wrong with the Improved method.'
        assert soCredentials.AWSSecretKey == soCredentials2.AWSSecretKey, 'WARNING: Something is wrong with the Improved method.'

    from boto.s3 import connection
    aConnection = connection.S3Connection(aws_access_key_id=soCredentials2.AWSAccessKeyId, aws_secret_access_key=soCredentials2.AWSSecretKey)
    buckets = aConnection.get_all_buckets()
    print 'buckets=%s' % (buckets)
    pass