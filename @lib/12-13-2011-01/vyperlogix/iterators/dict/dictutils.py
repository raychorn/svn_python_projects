__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

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
from vyperlogix.misc import _utils

from vyperlogix.enum.Enum import Enum

class DictWalkOptions(Enum):
    keys_and_values = 1
    keys_only = 2
    values_only = 4
    keys_and_values_and_top = 8

encode = lambda value:''.join([c if (c != '_') else chr(ord(c)+128) for c in _utils.ascii_only(value)])

def flatten(d, parent_key='', delim='_'):
    '''
    Care must be taken to ensure keys do not have "_" or bad evil things can happen.
    '''
    items = []
    for k, v in d.items():
        try:
            items.extend(flatten(v, '%s%s%s' % (parent_key, k, delim)).items())
        except AttributeError:
            items.append(('%s%s' % (parent_key, k), v))
    return dict(items)

decode = lambda value:''.join([chr(ord(c)&127) for c in value])

def unflatten(d,delim='_'):
    '''
    Care must be taken to ensure keys do not have "_" or bad evil things can happen.
    '''
    ud = {}
    for k, v in d.items():
        context = ud
        for sub_key in k.split(delim)[:-1]:
            if sub_key not in context:
                context[sub_key] = {}
            context = context[sub_key]
        context[k.split(delim)[-1]] = v
    return ud

def walk(top,options=DictWalkOptions.values_only):
    from vyperlogix import misc
    try:
        __stack__ = []
        options = options if ( (options) and (options.value) ) else DictWalkOptions.values_only
        while (1):
            top = [top] if (not misc.isIterable(top)) else [top] if (misc.isDict(top)) else top
            for t in top:
                for k,v in t.iteritems():
                    __is__ = misc.isDict(v) or misc.isHashedDict(v[0] if (misc.isIterable(v)) else v)
                    if (__is__):
                        __stack__.append(v)
                    if (options) and (options.value):
                        if (options.value & DictWalkOptions.keys_and_values.value):
                            yield (k,v)
                        elif (options.value & DictWalkOptions.keys_only.value):
                            yield k if (__is__) else v
                        elif (options.value & DictWalkOptions.values_only.value):
                            if (__is__):
                                continue
                            else:
                                yield v
                    else:
                        yield k if (misc.isDict(v)) else v
            top = __stack__.pop() if (len(__stack__) > 0) else None
            if (not top):
                raise StopIteration
    except:
        raise StopIteration
    raise StopIteration
