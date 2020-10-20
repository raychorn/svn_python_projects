__copyright__ = """\
(c). Copyright 1990-2020, Vyper Logix Corp., 

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

__version__ = '''4.1.0'''

def main():
    from vyperlogix.pyro.zone_proxy import ZoneEditProxy
    from config import ACCEPTED_ID
    zo = ZoneEditProxy('10.1.10.55:8888',__version__,ACCEPTED_ID)

    from config import _username as username
    from config import _password as password
    
    print username,password
    zo.login(username,password)
    zones = zo.zones()
    print type(zones)
    for zone in zones:
        print zone

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)
    main()
