from vyperlogix import oodb

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

_encode = lambda str:''.join([oodb.strToHex(chr(ord(ch))) for ch in str])
encode = lambda str:''.join([oodb.strToHex(chr(ord(ch)|128)) for ch in str])
decode = lambda str:''.join([chr(ord(ch)&127) for ch in oodb.hexToStr(str)])
_decode = lambda str:''.join([chr(ord(ch)) for ch in oodb.hexToStr(str)])

_schema = [2, 1, 2, 1, 2]

_key = decode('F3E9F3EBEFC0B7B6B6B0A4E2B7B6B6B0')[0:16]

def reverseKey(key):
    from vyperlogix import misc

    c_schema = misc.reverseCopy(_schema)
    _parts = []
    _valid_until = []
    toks = key.split('-')
    for t in toks:
        c = c_schema.pop()
        _valid_until.append(t[len(t)-c:])
        _parts.append(t[0:len(t)-c])
    _valid_until[1] += _valid_until[2][0]
    _valid_until[2] = _valid_until[2][-1]
    _valid_until[2] += _valid_until[3]
    del _valid_until[3]
    _valid_until[2] += _valid_until[3]
    del _valid_until[3]
    return ('-'.join(_parts),'-'.join(_valid_until))
