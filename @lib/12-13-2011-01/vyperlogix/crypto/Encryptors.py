try:
    from ext.crypto import coder
    _encode = coder.encode
    _decode = coder.decode
except ImportError:
    from vyperlogix.products import keys
    _encode = keys.encode
    _decode = keys.decode
from vyperlogix.enum import Enum
import uuid

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

class Encryptors(Enum.Enum):
    none = uuid.UUID('7e1867ee-b50f-465b-a6ed-9c7bb58b2b3c')
    simple = uuid.UUID('2ad6b9a5-2ed6-4d3a-b53d-38962bb2ef42')
    xtea = uuid.UUID('0756a000-5056-4659-a3e4-f6853ac9e293')
    blowfish = uuid.UUID('4a275787-ee54-4b11-9348-05d3aee877a5')

def encryptSimple(str):
    return _encode(str)
    
def decryptSimple(str):
    return _decode(str)
