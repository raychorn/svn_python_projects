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

def isString(s):
    return (isinstance(s,str)) or (isinstance(s,unicode))

def tempFile(prefix,useTemporaryFile=False):
    '''Get the name of a temp file based on where such files are being kept. See also appDataFolder() for a similar use.'''
    import os
    import tempfile as tfile
    common = ''
    prefix = str(prefix) if not isString(prefix) else prefix
    if (os.environ.has_key('TEMP')):
        common = os.environ['TEMP']
    elif (os.environ.has_key('TMP')):
        common = os.environ['TMP']
    if (len(common) == 0) or (useTemporaryFile):
        f = tfile.TemporaryFile()
        common = os.path.abspath(os.sep.join(f.name.split(os.sep)[0:-1]))
        f.close()
    return os.sep.join([common,prefix])

def _makeDirs(_dirName):
    """ make all folders for a path, front to back, without considering the _dirName to be a fully qualified file path. """
    import os
    if (not os.path.exists(_dirName)):
        try:
            os.makedirs(_dirName)
        except:
            pass

def makeDirs(fname):
    """ make all folders for a path, front to back, fname is considered to be a fully qualified file path name rather than the name of a folder. """
    import os
    _dirName = fname if (os.path.isdir(fname)) else os.path.dirname(fname)
    _makeDirs(_dirName)

def safely_mkdir(fpath='.',dirname='logs'):
    import os

    _path = os.path.abspath(os.sep.join([fpath,dirname]))
    if (not os.path.exists(_path)):
        try:
            os.mkdir(_path)
        except:
            os.makedirs(_path)
    return _path

def writeFileFrom(fname,contents,mode='w'):
    dname = os.path.dirname(fname)
    safely_mkdir(fpath=dname,dirname='')
    fOut = open(fname,mode)
    try:
        fOut.write(contents)
    finally:
        fOut.flush()
        fOut.close()

def callersName():
    """ get name of caller of a function """
    import sys
    return sys._getframe(2).f_code.co_name

def formattedException(details='',_callersName=None):
    _callersName = _callersName if (_callersName is not None) else callersName()
    import sys, traceback
    exc_info = sys.exc_info()
    info_string = '\n'.join(traceback.format_exception(*exc_info))
    return '(' + _callersName + ') :: "' + str(details) + '". ' + info_string

def findFirstMatching(_list,_item):
    if (isinstance(_list,list)):
        i = 0
        for l in _list:
            if (str(l).lower() == str(_item).lower()):
                return i
            i += 1
    return -1

##### END OF Vyper Logix Hacks #####

import sys, os, re
import imp
import zipfile
import tarfile
import pickle
from cStringIO import StringIO
from hashlib import sha256

re_url_ok = re.compile(r'^http://|^ftp://|^https://')
re_url_split = re.compile('^(.+):\/\/(.+?)(?::(\d+))?(\/.*)$')

settings = sys.__dict__.setdefault(
    'urlimport_settings',
    {'ssl_cert': '', 'ssl_key': '', 'debug': 4, 'rsa_pub': '',
        'paranoid': False}
)

def debug(s, pf='| |', lvl=1):
    _lvl = settings.get('debug')
    #print >>sys.stderr, 'lvl=%s, _lvl=%s' % (lvl,_lvl)
    if lvl <= _lvl:
        print "%s %s" % (pf, s)

def verify_sign(source, filename):
    PUB = settings.get('rsa_pub')
    if not isinstance(PUB, dict):
        pub_key = pickle.load(open(PUB))
    else:
        pub_key = PUB

    def check_hash(myzip, filename, signname):
        file_data = myzip.read(filename)
        signed_hash = myzip.read(signname)

        hash = verify(signed_hash, pub_key)
        file_hash = sha256(file_data).hexdigest()
        if hash == file_hash:
            return file_data
        else:
            return None

    zipfileIO = StringIO(source)
    myzip = zipfile.ZipFile(zipfileIO)

    first = check_hash(myzip, filename[:-4], 'sign')
    try:
        second = check_hash(myzip, filename[:-4]+'-data.tar', 'data-sign')
        print "data ok"
        tarfileIO = StringIO(second)
        mytar = tarfile.TarFile(fileobj=tarfileIO)
        mytar.extractall()
    except:
        second = True
    myzip.close()

    if first and second:
        return first
    else:
        return None

class UrlFinder:
    def __init__(self, path):
        if (not self.accept_url(path)):
            for k,v in settings.iteritems():
                if (path.lower().find(k.lower()) > -1):
                    path = path.lower().replace(k.lower(),v).replace('/'+os.sep,'/').replace(os.sep,'/')
                    break
            if (not self.accept_url(path)):
                debug("UrlFinder: rejecting non-url path item: '%s'" % path, lvl=3)
                raise ImportError

    def accept_url(self,path):
        if re_url_ok.match(path):
            debug("UrlFinder: accepting '%s'." % path, lvl=2)
            self.path = path
            if not self.path.endswith("/"):
                self.path += '/'
            return True
        return False
    
    def find_module(self, fullname, mpath=None):
        """try to locate the remote module, do this:
         a) try to get fullname.py from http://self.path/
         b) try to get fullname.py.zip from http://self.path/ (signed)
         c) try to get __init__.py from http://self.path/fullname/
         d) try to get __init__.py.zip from http://self.path/fullname/
        """

        fullname = fullname.split('.')[-1]

        for url, path in [
         (self.path + fullname + '.py',          None),
         (self.path + fullname + '.py.zip',      None),
         (self.path + fullname + '/__init__.py', self.path + fullname + '/'),
         (self.path + fullname + '/__init__.py.zip', self.path + fullname + '/')]:
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
        A checksum on the server would help to allow the following code
        to determine when to actually perform the download function versus
        retrieving the source from the local file cache in case there was a file
        in the local cache.
        The local file cache will be encrypted and only encrypted at runtime and then
        only long enough to allow the source file to be imported after which the plaintext
        file will be removed in a fail-safe manner.
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
        
        if url[-3:] == 'py':
            src = src.replace("\r\n", "\n")    
        return src

class UrlLoader:
    def __init__(self, url, path, source):
        self.url = url
        filename = self.url.split('/')[-1]
        if self.url[-3:] == 'zip':
            source = verify_sign(source, filename)
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

        i = 1
        debug('='*40, pf='|>|', lvl=4)
        for line in self.source.split('\n'):
            debug(line, pf='|%d>|' % (i), lvl=4)
            i += 1
        debug('='*40, pf='|>|', lvl=4)

        debug("load_module: executing %s's source..." % fullname, lvl=2)

        _toks = fullname.split('.')
        _base = _toks[0]
        if (not settings.has_key('__base__')):
            settings['__base__'] = {}
        d_base = settings['__base__']
        if (not d_base.has_key(_base)):
            d_base[_base] = tempFile(__name__,useTemporaryFile=True)
            i_base = findFirstMatching(sys.path,d_base[_base])
            if (i_base == -1):
                debug('sys.path.append(%s)...' % (d_base[_base]), lvl=2)
                sys.path.append(d_base[_base])
        p_base = d_base[_base]
        tname = []
        _init_ = '__init__.py'
        for t in _toks:
            tname.append(t)
            pname = os.sep.join([p_base,os.sep.join(tname)])
            makeDirs(pname)
            fname = os.sep.join([pname,_init_])
            if (not os.path.exists(fname)):
                writeFileFrom(fname,'# Automated file creation from "%s".\n' % (__file__))
        fname = self.url.replace(self.path,'')
        fname = os.sep.join([p_base,os.sep.join(_toks),fname])
        writeFileFrom(fname,self.source)

        debug('load_module: executing %s\'s source from "%s"...' % (fullname,fname), lvl=2)
        
        #exec self.source in mod.__dict__
        try:
            mod = __import__(fullname, globals(), locals(), [])
        except Exception, e:
            debug('ERROR: %s' % (formattedException(details=e)), lvl=2)

        #mod = sys.modules[fullname]
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

