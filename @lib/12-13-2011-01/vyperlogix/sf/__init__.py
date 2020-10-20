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
__expected_pyax_version__ = '0.9.7.2'

msg = 'Please download and use pyax version %s from http://code.google.com/p/sfpyax/.' % (__expected_pyax_version__)

_actual_pyax_version = 'MISSING'
try:
    import pyax
    assert pyax.__version__ == __expected_pyax_version__, 'WARNING: %s.' % (msg)
    _actual_pyax_version = pyax.__version__
except ImportError:
    print 'ERROR: %s.' % (msg)
    import sys
    sys.exit(1)
    
#print 'pyax version %s is loaded as expected.' % (_actual_pyax_version)
