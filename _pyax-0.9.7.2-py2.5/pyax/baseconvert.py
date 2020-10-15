""" Base conversion function and related base constants """
import string

BASE2  = string.digits[:2]
BINARY = BASE2

BASE8  = string.octdigits
OCTAL = BASE8

BASE10 = string.digits
DECIMAL = BASE10

BASE16 = string.digits + string.ascii_uppercase[:6]
HEX = BASE16

def baseconvert(number,fromdigits,todigits):
    """
    convert a number from one base to another

    Parameters:
    number - the number for which we wish to change the base
    fromdigits - digit domain that number is in
    todigits - digit domain we wish the number to be in
    """
    
    if str(number)[0]=='-':
        number = str(number)[1:]
        neg = True
    else:
        neg = False

    # make an integer out of the number
    x=long(0)
    for digit in str(number):
       x = x*len(fromdigits) + fromdigits.index(digit)
    
    # create the result in base 'len(todigits)'
    res=''
    while x>0:
        digit = x % len(todigits)
        res = todigits[digit] + res
        x /= len(todigits)
    if len(res) == 0:
        res = 0
    if neg:
        res = "-%s" %res

    return res
## END baseconvert
