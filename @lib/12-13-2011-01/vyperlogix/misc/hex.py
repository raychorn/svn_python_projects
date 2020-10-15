from vyperlogix.hash import lists

def dec2hex(n):
    """return the hexadecimal string representation of integer n"""
    val = '0%X' % n
    return val[len(val)-2:]

def hex2dec(s):
    """return the integer value of a hexadecimal string s"""
    return int(s, 16)

hex_digits = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','a','b','c','d','e','f']

def isHexDigits(s):
    if (len(s) > 1):
        for ch in s:
            if (not ch in hex_digits):
                return False
        return True
    return s in hex_digits

_base2hex = [(i,dec2hex(i)) for i in xrange(0,256)]

d_dec2hex = dict(_base2hex)

d_chr2hex = dict([(chr(t[0]),t[-1]) for t in _base2hex])

d_hex2dec = lists.asDict(d_dec2hex,insideOut=True)

def __init_data__():
    for k,v in d_hex2dec.iteritems():
        d_hex2dec[k] = chr(v)
__init_data__()

def strToHex(str):
    return ''.join([d_chr2hex[ch] for ch in str])

def hexToStr(hex):
    return ''.join([d_hex2dec[hex[i:i+2]] for i in xrange(0,len(hex),2)])
