__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

                   All Rights Reserved.

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
"""
__typeName = lambda cls:(cls if (isinstance(cls,str)) or (isinstance(cls,unicode)) else str(cls.__class__)).split()[-1].replace("'",'').replace('>','') # [1:-2]

def _typeName(obj):
    from vyperlogix import misc
    callersName = misc.callersName()
    if (any([(callersName.find(n) > -1) for n in ['__str__','__repr__']])):
        raise UserWarning('(%s) :: Cannot call this function from a __str__ function - recode this yourself using the helper function.' % (misc.funcName()))
    return __typeName(str(obj)).replace("'",'').replace('>','')

def typeName(obj):
    from vyperlogix import misc
    callersName = misc.callersName()
    if (any([(callersName.find(n) > -1) for n in ['__str__','__repr__']])):
        raise UserWarning('(%s) :: Cannot call this function from a __str__ function - recode this yourself using the helper function.' % (misc.funcName()))
    return __typeName(obj).replace("'",'').replace('>','')

def typeClassName(obj):
    from vyperlogix import misc
    callersName = misc.callersName()
    if (any([(callersName.find(n) > -1) for n in ['__str__','__repr__']])):
        raise UserWarning('(%s) :: Cannot call this function from a __str__ function - recode this yourself using the helper function.' % (misc.funcName()))
    try:
        sObj = str(obj.__class__)
    except AttributeError:
        sObj = str(obj)
    except:
        return typeName(obj)
    toks = sObj.replace('<','').replace('>','').replace("'",'').replace('object at','object_at').split()
    i = misc.findInListSafely(toks,'object_at')
    if (i > 0):
        i -= 1
    else:
        return toks[-1]
    return toks[0]

def objectSignature(obj):
    from vyperlogix import misc
    return '(%s.%s)' % (__typeName(obj),misc.callersName())

def type_is_class(obj):
    '''Returns True when the type(obj) looks to be a class definition otherwise False is returned.'''
    t = type(obj)
    return (str(t).startswith("<class '") and str(t).endswith("'>"))
