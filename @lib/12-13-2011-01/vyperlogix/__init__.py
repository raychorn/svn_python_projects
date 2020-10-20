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
from misc import _utils

from misc._utils import DeCamelCaseMethods

class Str(str):
    def de_camel_case(self,delim=' ',method=DeCamelCaseMethods.default):
	return _utils.de_camel_case(self,delim=delim,method=method)

# BEGIN: The following code causes problems for isinstance(foo,str)...
#import __builtin__
#__builtin__.str = Str
# END!  The following code causes problems for isinstance(foo,str)...

__version__ = '1.0.0.0'

#print 'Loaded... %s v%s' % (str(__name__).capitalize(),__version__)
