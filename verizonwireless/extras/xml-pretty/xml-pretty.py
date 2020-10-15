if (__name__ == '__main__'):
    import os, sys
    import urllib
    from vyperlogix.misc import _utils

    #fname = r'Z:\python projects\_django-projects\@projects\verizonwireless\extras\global-nav-sniffer\LoggedOutState.xml'
    fname = r'Z:\python projects\_django-projects\@projects\verizonwireless\extras\global-nav-sniffer\LoggedInState.xml'
    xml = _utils.readFileFrom(fname)
    xml = xml.replace('&',urllib.quote_plus('&'))
    print 'Reading "%s".' % (fname)
    
    from BeautifulSoup import BeautifulStoneSoup
    soup = BeautifulStoneSoup(xml)
    
    print soup.prettify()
