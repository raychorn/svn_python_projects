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

def normalize(x):
    x += 1.57079632
    if (x >  3.14159265):
        x -= 6.28318531
    return x

___cosine1___ = lambda cos:.225 * (cos *-cos - cos) + cos
___cosine2___ = lambda cos:.225 * (cos * cos - cos) + cos
___cosine___ = lambda cos:___cosine1___(cos) if (cos < 0) else ___cosine2___(cos)

__cosine1__ = lambda x:1.27323954 * x + 0.405284735 * x * x
__cosine2__ = lambda x:1.27323954 * x - 0.405284735 * x * x
__cosine__ = lambda x:__cosine1__(x) if (x < 0) else __cosine2__(x)

def _cosine(x):
    '''
    Low precision sine/cosine (~14x faster)
    http://lab.polygonal.de/2007/07/18/fast-and-accurate-sinecosine-approximation/
    '''
    return __cosine__(normalize(x))

def cosine(x):
    '''
    High precision sine/cosine (~8x faster)
    http://lab.polygonal.de/2007/07/18/fast-and-accurate-sinecosine-approximation/
    '''
    x = normalize(x)
    return ___cosine___(__cosine1__(x)) if (x < 0) else ___cosine___(__cosine2__(x))

