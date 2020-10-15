'''(c). Copyright 1990-2014, Vyper Logix Corp., All Rights Reserved.

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
    sf_account__.append({'username': "7DFB1A0C90316EAF4D527A5F6B1145EB682EC6F184C70867AD98F2B081C032E1",
                         'password': "50F1CC2321C1194782A31407682120E47329BB39E6C40F2D71B217127DA7CCF22856B6D5F6BBE51F"
                         })
    sf_account__.append({'username': "41724B16F7C21561F725C962C5094CEBA9525EA437EB6A8E",
                         'password': "9DFB3B1654788DE239F464554FCFE3A89DED2466D8E86DF117A3EABEC597E4F76DD620716D885198"
                         })
    sf_account__.append({'username': "41724B16F7C21561F725C962C5094CEB2810E9EC42389FAF",
                         'password': "9DFB3B1654788DE2031AC3A1833560C392094C5DFAFE6360877EC164911D844FE62E05BDE8F0989F"
                         })
    sf_account__.append({'username': "41724B16F7C21561F725C962C5094CEBA9525EA437EB6A8E",
                         'password': "9DFB3B1654788DE239F464554FCFE3A89DED2466D8E86DF117A3EABEC597E4F76DD620716D885198"
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

