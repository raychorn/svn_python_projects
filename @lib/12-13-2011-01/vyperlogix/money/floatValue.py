import decimal
from vyperlogix.enum.Enum import *

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

class Options(Enum):
    asFloat = 0
    asDollar = 1

def floatValue(sFloat,asDollars=Options.asFloat):
    n = 0
    asDollars = Options.asDollar if isinstance(asDollars,EnumInstance) and Options.asDollar.value == Options.asDollar.value else Options.asFloat
    try:
	x = str(sFloat).replace(',','').replace('$','')
	sign = -1 if x.find('-') > -1 else 1
	x = x.replace('-','').replace('+','')
	if (len(x) > 0):
	    if (asDollars.value == Options.asDollar.value):
		n = floatAsDollars(x)
	    else:
		n = float(x)
	    if (sign < 0):
		n = -n
    except:
	pass
    return n

def floatAsDollars(value):
    if (isinstance(value,float)):
	value = ('%10.2f' % value).strip()
    elif (isinstance(value,int)):
	value = ('%d' % value).strip()
    else:
	value = ('%s' % value).strip()
    precision = 0
    for t in value.split('.'):
	precision += len(t)
    return decimal.Context(prec=precision).create_decimal(value)
