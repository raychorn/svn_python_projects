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
    if (x < -3.14159265):
        x += 6.28318531
    elif (x >  3.14159265):
        x -= 6.28318531
    return x

___sine1___ = lambda sin:.225 * (sin *-sin - sin) + sin
___sine2___ = lambda sin:.225 * (sin * sin - sin) + sin
___sine___ = lambda sin:___sine1___(sin) if (sin < 0) else ___sine2___(sin)

__sine1__ = lambda x:1.27323954 * x + .405284735 * x * x
__sine2__ = lambda x:1.27323954 * x - 0.405284735 * x * x
__sine__ = lambda x:__sine1__(x) if (x < 0) else __sine2__(x)

def _sine(x):
    '''
    Low precision sine/cosine (~14x faster)
    http://lab.polygonal.de/2007/07/18/fast-and-accurate-sinecosine-approximation/
    '''
    return __sine__(normalize(x))

def sine(x):
    '''
    High precision sine/cosine (~8x faster)
    http://lab.polygonal.de/2007/07/18/fast-and-accurate-sinecosine-approximation/
    '''
    x = normalize(x)
    return ___sine___(__sine1__(x)) if (x < 0) else ___sine___(__sine2__(x))

