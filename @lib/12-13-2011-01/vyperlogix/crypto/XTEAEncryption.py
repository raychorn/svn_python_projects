""" 
XTEA Block Encryption Algorithm

Author: Paul Chakravarti (paul_dot_chakravarti_at_gmail_dot_com)
License: Public Domain

This module provides a Python implementation of the XTEA block encryption
algorithm (http://www.cix.co.uk/~klockstone/xtea.pdf). 

The module implements the basic XTEA block encryption algortithm
(`xtea_encrypt`/`xtea_decrypt`) and also provides a higher level `crypt`
function which symmetrically encrypts/decrypts a variable length string using
XTEA in OFB mode as a key generator. The `crypt` function does not use
`xtea_decrypt` which is provided for completeness only (but can be used
to support other stream modes - eg CBC/CFB).

This module is intended to provide a simple 'privacy-grade' Python encryption
algorithm with no external dependencies. The implementation is relatively slow
and is best suited to small volumes of data. Note that the XTEA algorithm has
not been subjected to extensive analysis (though is believed to be relatively
secure - see http://en.wikipedia.org/wiki/XTEA). For applications requiring
'real' security please use a known and well tested algorithm/implementation.

The security of the algorithm is entirely based on quality (entropy) and
secrecy of the key. You should generate the key from a known random source and
exchange using a trusted mechanism. In addition, you should always use a random
IV to seed the key generator (the IV is not sensitive and does not need to be
exchanged securely)

    >>> import os
    >>> iv = 'ABCDEFGH'
    >>> z = crypt('0123456789012345','Hello There',iv)
    >>> z.encode('hex')
    'fe196d0a40d6c222b9eff3'
    >>> crypt('0123456789012345',z,iv)
    'Hello There'

""" 
def iv(s):
    s = s[0:8]
    n = len(s)
    if (n < 8):
        n = 8-n
        s += ' '*n
    return s[0:8]

def encryptode(_key,data,_iv):
    from vyperlogix import oodb
    from vyperlogix.products import keys
    return keys._encode(oodb.crypt(_key,data,_iv))

def _encryptode(data,_iv):
    from vyperlogix import oodb
    from vyperlogix.products import keys
    return keys._encode(oodb.crypt(keys._key,data,_iv))

def f_encryptode(data,_iv):
    from vyperlogix import oodb
    from vyperlogix.products import keys
    return oodb.crypt(keys._key,data,_iv)

def decryptode(_key,data,_iv):
    from vyperlogix import oodb
    from vyperlogix.products import keys
    return oodb.crypt(_key,keys._decode(data),_iv)

def _decryptode(data,_iv):
    from vyperlogix import oodb
    from vyperlogix.products import keys
    return oodb.crypt(keys._key,keys._decode(data),_iv)

def f_decryptode(data,_iv):
    from vyperlogix import oodb
    from vyperlogix.products import keys
    return oodb.crypt(keys._key,data,_iv)

if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    
    from vyperlogix.oodb import *
    from win32api import GetComputerName
    from random import choice
    from vyperlogix.misc import GenPasswd
    import uuid
    
    u = uuid.uuid4()
    print u
    pass

    iv = 'ABCDEFGH'
    _key = '0123456789012345'
    _original = 'Hello There'
    z = crypt(_key,_original,iv)
    _secret = z.encode('hex')
    assert _secret == 'fe196d0a40d6c222b9eff3', 'Oops, something went wrong because _secret is now "%s"!' % _secret
    print '_secret=(%s)' % _secret
    _plain = crypt(_key,z,iv)
    print '_plain=(%s)' % _plain
    assert _plain == _original, 'Oops, something went wrong again !'

    print 'Now using a random "iv".'
    iv = GenPasswd.GenPasswd(8,''.join([chr(x) for x in xrange(128,255)]))
    print 'iv=(%s) [%s]' % (iv,','.join([str(ord(x)) for x in iv]))
    z = crypt(_key,_original,iv)
    _secret = z.encode('hex')
    print '_secret=(%s)' % _secret
    _plain = crypt(_key,z,iv)
    print '_plain=(%s)' % _plain
    assert _plain == _original, 'Oops, something went wrong again !  Got "%s" but expected to get "%s"' % (_plain,_original)

    print 'Now using a random "key" and random "iv".'
    iv = GenPasswd.GenPasswd(8,''.join([chr(x) for x in xrange(128,255)]))
    print 'iv=(%s) [%s]' % (iv,','.join([str(ord(x)) for x in iv]))
    _key = GenPasswd.GenPasswd(16,''.join([chr(x) for x in xrange(128,255)]))
    print '_key=(%s) [%s]' % (_key,','.join([str(ord(x)) for x in _key]))
    z = crypt(_key,_original,iv)
    _secret = z.encode('hex')
    print '_secret=(%s)' % _secret
    _plain = crypt(_key,z,iv)
    print '_plain=(%s)' % _plain
    assert _plain == _original, 'Oops, something went wrong again !  Got "%s" but expected to get "%s"' % (_plain,_original)

    def getSchema(s):
        x = [chr(ord(ch)-128) for ch in s]
        print 'x=(%s)' % x
        return ''.join(x)
    
    def makeSchema():
        _choice = []
        _pattern = [ord('v'),ord('k'),ord('s')]
        while len(_choice) < 3:
            _choice.append(choice(_pattern))
            _pattern = list(set(_pattern).difference(set(_choice)))
        return ''.join([chr(ch+128) for ch in _choice])
    
    def getEncodedStream(schemaHex,keyHex,vHex,secretHex):
        _schema_str = hexToStr(schemaHex)
        _schema = getSchema(_schema_str)
        key = [ch for ch in hexToStr(keyHex)]
        iv = [ch for ch in hexToStr(vHex)]
        secret = [ch for ch in hexToStr(secretHex)]
        #plain = ''.join([chr(ord(ch)-128) for ch in crypt(key,secret,iv)])
        j = 0
        stream = [ch for ch in _schema_str]
        while ( (len(key) > 0) or (len(iv) > 0) or (len(secret) > 0) ):
            x = _schema[j]
            if ( (x == 's') and (len(secret) > 0) ):
                stream.append(secret[0])
                del secret[0]
            elif ( (x == 'v') and (len(iv) > 0) ):
                stream.append(iv[0])
                del iv[0]
            elif ( (x == 'k') and (len(key) > 0) ):
                stream.append(key[0])
                del key[0]
            j += 1
            if (j == 3):
                j = 0
        return ''.join(stream)
    
    def unEncodeStream(stream):
        plainStream = []
        _stream = [ch for ch in stream]
        _schema_str = _stream[0:3]
        _schema = getSchema(_schema_str)
        del _stream[0:3]
        _key = []
        _iv = []
        _secret = []
        _key_len = 16
        _iv_len = 8
        j = 0
        while (len(_stream) > 0):
            ch = _stream[0]
            x = _schema[j]
            if (x == 's'):
                _secret.append(ch)
            elif ( (x == 'v') and (len(_iv) <= _iv_len) ):
                _iv.append(ch)
            elif ( (x == 'k') and (len(_key) <= _key_len) ):
                _key.append(ch)
            del _stream[0]
            j += 1
            if (j == 3):
                j = 0
        return ''.join(plainStream)
    
    _original = '%s%ssisko@7660$boo' % (GetComputerName().lower(),'\t')
    
    _schema = makeSchema()
    
    _bar = '='*30
    print '\n%s\n' % _bar
    print 'Now using a random readable ASCII "key" and random "iv".'
    _schema_hex = strToHex(_schema)
    print '_schema=(%s)=(%s)=(%s)' % (_schema,getSchema(_schema),_schema_hex)
    _schema_from_hex = hexToStr(_schema_hex)
    print '_schema=(%s)=(%s)' % (getSchema(_schema_from_hex),_schema_from_hex)
    iv = GenPasswd.GenPasswd(8,''.join([chr(x) for x in xrange(128,255)]))
    iv_hex = strToHex(iv)
    print 'iv=(%s) [%s]' % (iv,iv_hex)
    _key = GenPasswd.GenPasswd(16,''.join([chr(x) for x in xrange(128,255)]))
    _key_hex = strToHex(_key)
    print '_key=(%s) [%s]' % (_key,_key_hex)
    z = crypt(_key,''.join([chr(ord(ch)+128) for ch in _original]),iv)
    _secret = z.encode('hex')
    print '_secret=(%s)' % _secret
    z_hex = strToHex(z)
    print '\t(%s)\t(%s)\t(%s)\t(%s)' % (len(z),z,len(z_hex),z_hex)
    _secret_hex = strToHex(hexToStr(_secret))
    print '\t(%s)\t(%s)\t(%s)\t(%s)' % (len(hexToStr(_secret)),hexToStr(_secret),len(_secret_hex),_secret_hex)
    _plain = ''.join([chr(ord(ch)-128) for ch in crypt(_key,z,iv)])
    print '_plain=(%s)' % _plain
    assert _plain == _original, 'Oops, something went wrong again !  Got "%s" but expected to get "%s"' % (_plain,_original)

    print
    s = getEncodedStream(_schema_hex,_key_hex,iv_hex,z_hex)
    print 's=(%s)' % s

    print
    x = unEncodeStream(s)
    print 'x=(%s)' % str(x)
 