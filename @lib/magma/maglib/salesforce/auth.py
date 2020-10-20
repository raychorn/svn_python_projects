from vyperlogix.misc import _utils
from vyperlogix.enum.Enum import Enum
from vyperlogix.misc import ObjectTypeName
from vyperlogix.crypto import blowfish
from vyperlogix.products import keys

__copyright__ = """\
(c). Copyright 1990-2014, Vyper Logix Corp., All Rights Reserved.

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
    
magma_molten_passphrase = keys.decode('E9ECEFF6E5F4EFF7EFF2EBE1F4EDE1E7EDE1E4E5F3E9E7EEE1F5F4EFEDE1F4E9EFEEE1ECECE4E1F9ECEFEEE7')

class CredentialTypes(Enum): # The numbers here have to be linear to match the array below in the code.
    Magma_Production = 0
    Magma_Sandbox = 1
    Magma_RHORN_Production = 2
    Magma_RHORN_Sandbox = 3
    
_credentials_set = [CredentialTypes.Magma_Production.value,
                    CredentialTypes.Magma_Sandbox.value,
                    CredentialTypes.Magma_RHORN_Production.value,
                    CredentialTypes.Magma_RHORN_Sandbox.value]

__decode__ = lambda e,p:_utils.ascii_only(blowfish.decryptData(keys._decode(e).strip(),p))

__source__ = \
'''
from auth import CredentialTypes
from auth import _credentials_set
from vyperlogix.misc import ObjectTypeName
from auth import __decode__
from auth import magma_molten_passphrase
from vyperlogix.crypto import blowfish

def credentials(e_passphrase,using_set=CredentialTypes.Magma_Production.value):
    def _credentials(d):
        try:
            return {'username': __decode__(d['username'],e_passphrase),
                    'password': __decode__(d['password'],e_passphrase)
                    }
        except:
            return None

    using_set = using_set if (using_set in _credentials_set) else CredentialTypes.Magma_Production.value
    sf_account__ = []
    sf_account__.append({'username': "{{1}}",
                         'password': "{{2}}"
                         })
    sf_account__.append({'username': "{{3}}",
                         'password': "{{4}}"
                         })
    sf_account__.append({'username': "{{5}}",
                         'password': "{{6}}"
                         })
    sf_account__.append({'username': "{{7}}",
                         'password': "{{8}}"
                         })

    if (ObjectTypeName.typeClassName(using_set).find('.Enum.EnumInstance') > -1):
        using_set = using_set.value
    if (using_set >= 0) and (using_set < len(sf_account__)):
        return _credentials(sf_account__[using_set])
    return None

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
'''
if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

    #from vyperlogix.crypto import blowfish
    #from vyperlogix.products import keys
    #_encode = keys._encode
    #_decode = keys._decode
    
    #sf_account__ = []
    
    #u = _encode(blowfish.encryptData('molten_admin@magma-da.com',magma_molten_passphrase))
    #_u = __decode__(u,magma_molten_passphrase)
    #print '(P) username is "%s".' % (_u)
    #print '(P) username is "%s".' % (u)
    #print

    #p = _encode(blowfish.encryptData('u2cansleeprWI2X9JakDlxjcuAofhggFbaf',magma_molten_passphrase))
    #_p = __decode__(p,magma_molten_passphrase)
    #print '(P) password is "%s".' % (_p)
    #print '(P) password is "%s".' % (p)
    #print
    
    #sf_account__.append({'{{1}}': u,
                         #'{{2}}': p
                         #})
    
    #u = _encode(blowfish.encryptData('rhorn@magma-da.com',magma_molten_passphrase))
    #_u = __decode__(u,magma_molten_passphrase)
    #print '(P) username is "%s".' % (_u)
    #print '(P) username is "%s".' % (u)
    #print

    #p = _encode(blowfish.encryptData('Peek@b99YfFqyveSomw1B0FeB6ooaYCT2',magma_molten_passphrase))
    #_p = __decode__(p,magma_molten_passphrase)
    #print '(P) password is "%s".' % (_p)
    #print '(P) password is "%s".' % (p)
    #print
    
    #sf_account__.append({'{{5}}': u,
                         #'{{6}}': p
                         #})
    
    #u = _encode(blowfish.encryptData('rhorn@magma-da.com.stag',magma_molten_passphrase))
    #_u = __decode__(u,magma_molten_passphrase)
    #print '(P/S) username is "%s".' % (_u)
    #print '(P/S) username is "%s".' % (u)
    #print

    #p = _encode(blowfish.encryptData('Peek@b99LWmub1Zg0SwJAqczEdmntuuc',magma_molten_passphrase))
    #_p = __decode__(p,magma_molten_passphrase)
    #print '(P/S) password is "%s".' % (_p)
    #print '(P/S) password is "%s".' % (p)
    #print
    
    #sf_account__.append({'{{3}}': u,
                         #'{{4}}': p
                         #})
    
    #sf_account__.append({'{{7}}': u,
                         #'{{8}}': p
                         #})
    
    #import os, sys
    
    #dname = os.path.dirname(__file__)
    #print dname
    #fname = os.path.join(dname,'cred.py')
    #print fname
    
    #s = __source__
    #for item in sf_account__:
        #for k,v in item.iteritems():
            #s = s.replace(k,v)
    
    #print 'BEGIN: Writing source for "%s".' % (fname)
    #fOut = open(fname,'w')
    #try:
        #print >>fOut, "'''%s'''" % (__copyright__)
        #print >>fOut, s
    #finally:
        #fOut.flush()
        #fOut.close()
    #print 'END!   Writing source for "%s".' % (fname)
    
    #print
 
    import cred
    
    print cred.credentials(magma_molten_passphrase,CredentialTypes.Magma_Production.value)
    print
    print cred.credentials(magma_molten_passphrase,CredentialTypes.Magma_Sandbox.value)
    print
    print cred.credentials(magma_molten_passphrase,CredentialTypes.Magma_RHORN_Production.value)
    print
    print cred.credentials(magma_molten_passphrase,CredentialTypes.Magma_RHORN_Sandbox.value)
    print
 