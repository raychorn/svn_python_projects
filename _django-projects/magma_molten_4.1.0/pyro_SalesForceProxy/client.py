__copyright__ = """\
(c). Copyright 1990-2020, Vyper Logix Corp., 

              All Rights Reserved.

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

__version__ = '''4.1.0'''

def main():
    from vyperlogix.pyro.sf_proxy import SalesForceProxy
    from config import ACCEPTED_ID
    sf = SalesForceProxy(__version__,ACCEPTED_ID)

    is_logged_in = sf.isLoggedIn()
    print "is_logged_in is %s." % (is_logged_in)
    
    end_points = sf.end_points()
    print "end_points is %s." % (end_points)
    
    getAllActiveUsers = sf.getAllActiveUsers()
    print "getAllActiveUsers returned %d items." % (len(getAllActiveUsers))

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)
    main()
