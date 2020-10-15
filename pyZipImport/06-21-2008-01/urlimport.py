"""
[ urlimport.py ]
Enables remote module importing.

version:   0.42b
author:    Jure Vrscaj <jure@codeshift.net>
homepage:  http://urlimport.codeshift.net
license:   GNU GPL

editedBy:    Daniel Garcia <dani@danigm.net>

== history ==
v0.42b.1 2009-03-26 - added support for RSA sign and zipped modules (by danigm)
v0.42b 2006-12-30 - added support for DOS-style source files - eval() chokes on "\r\n"
v0.42  2006-06-26 - added verbose mode setting
v0.41  2006-06-05 - client ssl certificate support
v0.32  2006-05-10 - ftp, https support :)
v0.31  2006-02-24 - recursion patch: non-packages now have no __path__
                  - load_module now returns the module from sys.modules,
                    in case the module itself was messing with sys.modules
v0.30  2006-02-23 package importing now possible
v0.02  2006-02-23 remote modules now first check own url when they have to import sth
v0.01  2006-02-19 made basic (single-file) importing
v0.00  2006-02-18 playing with path_hooks
"""

"""
RSA module Added here from http://stuvel.eu/rsa, we don't need another
module file

Module for calculating large primes, and RSA encryption, decryption,
signing and verification. Includes generating public and private keys.

__author__ = "Sybren Stuvel, Marloes de Boer and Ivo Tamboer"
__date__ = "2009-01-22"
"""

# NOTE: Python's modulo can return negative numbers. We compensate for
# this behaviour using the abs() function

from cPickle import dumps, loads
import base64
import math
import os
import random
import sys
import types
import zlib

def int2bytes(number):
    """Converts a number to a string of bytes
    
    >>> bytes2int(int2bytes(123456789))
    123456789
    """

    if not (type(number) is types.LongType or type(number) is types.IntType):
        raise TypeError("You must pass a long or an int")

    string = ""

    while number > 0:
        string = "%s%s" % (chr(number & 0xFF), string)
        number /= 256
    
    return string

def fast_exponentiation(a, p, n):
    """Calculates r = a^p mod n
    """
    result = a % n
    remainders = []
    while p != 1:
        remainders.append(p & 1)
        p = p >> 1
    while remainders:
        rem = remainders.pop()
        result = ((a ** rem) * result ** 2) % n
    return result

def encrypt_int(message, ekey, n):
    """Encrypts a message using encryption key 'ekey', working modulo
    n"""

    if type(message) is types.IntType:
        return encrypt_int(long(message), ekey, n)

    if not type(message) is types.LongType:
        raise TypeError("You must pass a long or an int")

    if message > 0 and \
            math.floor(math.log(message, 2)) > math.floor(math.log(n, 2)):
        raise OverflowError("The message is too long")

    return fast_exponentiation(message, ekey, n)

def unpicklechops(string):
    """base64decodes and unpickes it's argument string into chops"""

    return loads(zlib.decompress(base64.decodestring(string)))

def gluechops(chops, key, n, funcref):
    """Glues chops back together into a string.  calls
    funcref(integer, key, n) for each chop.

    Used by 'decrypt' and 'verify'.
    """
    message = ""

    chops = unpicklechops(chops)
    
    for cpart in chops:
        mpart = funcref(cpart, key, n)
        message += int2bytes(mpart)
    
    return message

def verify(cypher, key):
    """Verifies a cypher with the public key 'key'"""

    return gluechops(cypher, key['e'], key['n'], encrypt_int)

##### END OF RSA #####

import sys, os, re
import imp
import zipfile
import pickle
import tempfile
from hashlib import sha256

re_url_ok = re.compile(r'^http://|^ftp://|^https://')
re_url_split = re.compile('^(.+):\/\/(.+?)(?::(\d+))?(\/.*)$')

settings = sys.__dict__.setdefault(
    'urlimport_settings',
    {'ssl_cert': '', 'ssl_key': '', 'debug': 1, 'rsa_pub': '',
        'paranoid': False}
)

def debug(s, pf='| |', lvl=1):
    if lvl <= settings.get('debug'):
        print "%s %s" % (pf, s)

def verify_sign(zipfilename, filename):
    PUB = settings.get('rsa_pub')
    if not isinstance(PUB, dict):
        pub_key = pickle.load(open(PUB))
    else:
        pub_key = PUB

    myzip = zipfile.ZipFile(zipfilename)
    file_data = myzip.read(filename[:-4])
    signed_hash = myzip.read('sign')
    myzip.close()

    hash = verify(signed_hash, pub_key)

    file_hash = sha256(file_data).hexdigest()

    if hash == file_hash:
        return file_data
    else:
        return None

class UrlFinder:
    def __init__(self, path):
        if re_url_ok.match(path):
            debug("UrlFinder: accepting '%s'." % path, lvl=2)
            self.path = path
            if not self.path.endswith("/"):
                self.path += '/'
        else:
            debug("UrlFinder: rejecting non-url path item: '%s'" % path, lvl=3)
            raise ImportError

    def find_module(self, fullname, mpath=None):
        """try to locate the remote module, do this:
         a) try to get fullname.py from http://self.path/
         b) try to get fullname.py.zip from http://self.path/ (signed)
         c) try to get __init__.py from http://self.path/fullname/
        """

        fullname = fullname.split('.')[-1]

        for url, path in [
         (self.path + fullname + '.py',          None),
         (self.path + fullname + '.py.zip',      None),
         (self.path + fullname + '/__init__.py', self.path + fullname + '/')]:
            try:
                source = self.get_source(url)
            except Exception, e:
                debug("find_module: failed to get '%s'. (%s)" % (url, e), lvl=3)
            else:
                debug("find_module: got '%s'." % url, lvl=1)
                return UrlLoader(url, path, source)

        return None

    def get_source(self, url):
        """Download the source from given url.
        """
        from urllib2 import urlopen

        src = ''

        key = settings.get('ssl_key')
        cert = settings.get('ssl_cert')
        proto, host, port, path = re_url_split.findall(url)[0]
        try:
            port = int(port)
        except:
            port = 443
        
        if proto == 'https' and cert:
            # handle http over ssl with client certificate
            import httplib
            
            conn = httplib.HTTPSConnection(
            	host=host,
            	port=port,
            	key_file=key,
            	cert_file=cert,
            )
            
            conn.putrequest('GET', path)
            conn.endheaders()
            response = conn.getresponse()
            if response.status != 200:
                raise StandardError, "HTTPS Error: %d"%response.status
            src = response.read()
        else:
            # handle everything else
            src = urlopen(url).read()
        
        src = src.replace("\r\n", "\n")    
        return src

class UrlLoader:
    def __init__(self, url, path, source):
        self.url = url
        filename = self.url.split('/')[-1]
        if self.url[-3:] == 'zip':
            fd, zipfilename = tempfile.mkstemp('.zip')
            f = open(zipfilename, 'w')
            f.write(source)
            f.close()
            source = verify_sign(zipfilename, filename)
            os.remove(zipfilename)
            if source is None:
                raise Exception("ERROR: Code not verified: %s" % self.url)
        else:
            if settings.get('paranoid'):
                raise Exception("ERROR: Code not verified: %s" % self.url)
            debug("WARNING: %s is not signed" % url, lvl=1)
        self.path = path
        self.source = source
        self._files = {}

    def load_module(self, fullname):
        """add the new module to sys.modules,
        execute its source and return it
        """

        mod = sys.modules.setdefault(fullname, imp.new_module(fullname))

        mod.__file__ = "%s" % self.url
        mod.__loader__ = self
        if self.path:
            mod.__path__ = [self.path]

        for line in self.source.split('\n'):
            debug(line, pf='|>|', lvl=4)

        debug("load_module: executing %s's source..." % fullname, lvl=2)

        exec self.source in mod.__dict__

        mod = sys.modules[fullname]
        return mod
      
def config(**kwargs):
    """config(key=value) - Set key to value.
       config()          - Display settings.
    """
    settings.update(kwargs)
    for k,v in (kwargs or settings).iteritems():
        debug(" "+str(k)+"="+repr(v), lvl=0 )

# register The Hook
sys.path_hooks = [x for x in sys.path_hooks if x.__name__ != 'UrlFinder']
sys.path_hooks.append(UrlFinder)

#sys.path_importer_cache.clear()

debug("Url importing enabled. Add urls to sys.path.", lvl=0)
debug("Use urlimport.config(key=value) to manipulate settings:", lvl=0)

# print settings
rsa_pub = {'e': 9014953624700897882911674183894826454301096894103531987521048872413703873207778742547469759939862044786216901925337650791306479667213905483308222956554119L, 'n': 8803279709929490976082577889477093971080803288015637631471251711917954032764397342312919862594036148354123390627635251696340508618355139251106101014511907356796193260188797321327096461169551577029384273529690001565790409697704579029194903989518530269000965306814520324500199611985602596265986360751278680489937495644249401763439396316707013318169173524486150025291633483416505651621001440854092827304543460025017575040366721918502540152543100561610781283616262428383456352065285152729801475786235467157030863242876560911730795882700836213811640989811350117018670340886371188270519216369403016824160215951655463443163L}

config(rsa_pub=rsa_pub, paranoid=False)
# if paranoid is true all modules need to be signed
# rsa_pub could be a dict or a filename generated by server_sign.py

debug("", lvl=0)
debug("This stuff is experimental, use at your own risk. Enjoy.", lvl=0)

