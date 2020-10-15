# change a hexadecimal string to decimal number and reverse
# check two different representations of the hexadecimal string
# negative values and zero are accepted

def dec2hex(n):
    """return the hexadecimal string representation of integer n"""
    val = "%X" % n
    val = ('0' if (len(val) == 1) else '') + val
    return val

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

#if (__name__ == '__main__'):
    #import cProfile
    
    #def test01():
        #val = ''.join([dec2hex(n) for n in xrange(255)])
        #for i in xrange(10000):
            #bool = isHexDigits(val)
            #if (not bool):
                #print 'Test Failed !'
                #break
        #print 'isHexChars(%s)=(%s)' % (val,isHexDigits(val))
    
    #print "dec2hex(255)  =", dec2hex(255)    # FF
    #print "hex2dec('FF') =", hex2dec('FF')   # 255

    #print "dec2hex(0)  =", dec2hex(0)    # 00
    #print "dec2hex(1)  =", dec2hex(1)    # 01
    
    #cProfile.run('test01()')
    #print
    
    #print "hex(255) =", hex(255)                # 0xff
    #print "hex2dec('0xff') =", hex2dec('0xff')  # 255
