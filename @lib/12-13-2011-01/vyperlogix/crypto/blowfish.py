__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

                   All Rights Reserved.

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

def seedPassword(passPhrase=''):
    import random
    if (len(passPhrase) == 0):
        s = ''.join([chr(random.randint(0,254)) for ch in xrange(1024)])
    else:
        s = passPhrase
    #print 's=[%s]' % ','.join(['%d' % ord(ch) for ch in s])
    return s

#s = [110,111,119,105,115,116,104,101,116,105,109,101,102,111,114,97,108,108,103,111,111,100,109,101,110,116,111,99,111,109,101,116,111,116,104,101,97,105,100,111,102,116,104,101,105,114,99,111,117,110,116,114,121]
#_cipher_password = ''.join([chr(ch) for ch in s])
#_cipher_password = seedPassword('nowisthetimeforallgoodmentocometotheaidoftheircountry')

noramlize = lambda decrypted:''.join([ch for ch in decrypted if (ord(ch))])

def encryptData(data,passPhrase):
    from Crypto.Cipher import Blowfish
    cObj = Blowfish.new(passPhrase, Blowfish.MODE_ECB)
    m = len(data)
    n = 8-divmod(m,8)[-1]
    data += '\0'*n
    mm = len(data)
    eData = cObj.encrypt(data)
    sData = cObj.decrypt(eData)
    assert sData == data, 'Oops, something went wrong in "%s".' % functionName()
    return eData
 
def decryptData(data,passPhrase):
    from Crypto.Cipher import Blowfish
    cObj = Blowfish.new(passPhrase, Blowfish.MODE_ECB)
    sData = cObj.decrypt(data)
    return sData

def encryptCBC(key,iv,plain):
    from Crypto.Cipher import Blowfish
    obj = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    m = len(plain)
    n = 8-divmod(m,8)[-1]
    plain += '\0'*n
    print len(plain)
    return obj.encrypt(plain)

def decryptCBC(key,iv,cipher):
    from Crypto.Cipher import Blowfish
    obj = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    return ''.join([ch for ch in obj.decrypt(cipher) if (ord(ch) != 0)])

def test():
    key = '12345678'
    iv = '12345678'
    plain = 'now is the time for all good men to come to the aid of their country'
    cipher = encryptCBC(key,iv,plain)
    print cipher
    
    p = decryptCBC(key,iv,cipher)
    print p
    
    assert p==plain, 'Oops, something went wrong with the blowfish thingy.'
