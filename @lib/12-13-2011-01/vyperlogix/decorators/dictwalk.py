from vyperlogix.iterators.dict.dictutils import DictWalkOptions

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

def walk_into(bucket,options=DictWalkOptions.values_only):
    '''
    Python walk_into Decorator
    
    Invokes the deeply-nested Dict walk Generator; works for json structures or other deeply nested dict trees.
    
    Usage:
    
    @walk_into(bucket,options=DictWalkOptions.keys_only)
    def method(item):
        print item
    '''
    def decorator(f):
        from vyperlogix.iterators.dict import dictutils
        
        for item in dictutils.walk(bucket,options=options):
            if (callable(f)):
                f(item)
            else:
                raise ValueError('callback is not callable.')
        return f
    return decorator

