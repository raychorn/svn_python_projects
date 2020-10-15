__copyright__ = """\
(c). Copyright 1990-2008, Vyper Logix Corp., 

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

__version__ = '''4.0.1'''

from vyperlogix.classes.SmartObject import SmartObject2

def asSmartObjects(objects):
    items = []
    if (isinstance(objects,list)):
        for obj in objects:
            items.append(SmartObject2(obj))
    return items

def main():
    import Pyro.naming, Pyro.core
    import Pyro.errors
    
    from config import ACCEPTED_ID
    
    Pyro.core.initClient()
    ident = ACCEPTED_ID
    
    locator = Pyro.naming.NameServerLocator(identification=ident)  # note the ID
    print 'Searching Naming Service...',
    ns = locator.getNS()
    
    print 'Naming Service found at',ns.URI.address,'port',ns.URI.port
    
    print 'binding to object'
    try:
        URI = ns.resolve(':SalesForceProxy.version_%s' % (__version__.replace('.','_')))
        print 'URI:',URI
    except Pyro.core.PyroError,x:
        print 'Couldn\'t bind object, nameserver says:',x
        raise SystemExit
    
    sf_proxy = Pyro.core.getProxyForURI(URI)
    sf_proxy._setIdentification(ident)
    
    is_logged_in = sf_proxy.isLoggedIn()
    print "is_logged_in is %s." % (is_logged_in)
    
    end_points = sf_proxy.end_points()
    print "end_points is %s." % (end_points)
    
    getAllActiveUsers = asSmartObjects(sf_proxy.getAllActiveUsers())
    print "getAllActiveUsers returned %d items." % (len(getAllActiveUsers))

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)
    main()
