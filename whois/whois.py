"""
Whois client for python

transliteration of:
http://www.opensource.apple.com/source/adv_cmds/adv_cmds-138.1/whois/whois.c

Copyright (c) 2010 Chris Wolf

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

  Last edited by:  $Author$
              on:  $DateTime$
        Revision:  $Revision$
              Id:  $Id$
          Author:  Chris Wolf
"""
import os,sys
from vyperlogix.sockets import whois
import optparse
    
def parse_command_line(argv):
    """Options handling mostly follows the UNIX whois(1) man page, except
    long-form options can also be used.
    """
    flags = 0
    
    usage = "usage: %prog [options] name"
            
    parser = optparse.OptionParser(add_help_option=False, usage=usage)
    parser.add_option("-a", "--arin", action="store_const", 
                      const=whois.NICClient.ANICHOST, dest="whoishost",
                      help="Lookup using host " + whois.NICClient.ANICHOST)
    parser.add_option("-A", "--apnic", action="store_const", 
                      const=whois.NICClient.PNICHOST, dest="whoishost",
                      help="Lookup using host " + whois.NICClient.PNICHOST)
    parser.add_option("-b", "--abuse", action="store_const", 
                      const=whois.NICClient.ABUSEHOST, dest="whoishost",
                      help="Lookup using host " + whois.NICClient.ABUSEHOST)
    parser.add_option("-c", "--country", action="store", 
                      type="string", dest="country",
                      help="Lookup using country-specific NIC")
    parser.add_option("-d", "--mil", action="store_const", 
                      const=whois.NICClient.DNICHOST, dest="whoishost",
                      help="Lookup using host " + whois.NICClient.DNICHOST)
    parser.add_option("-g", "--gov", action="store_const", 
                      const=whois.NICClient.GNICHOST, dest="whoishost",
                      help="Lookup using host " + whois.NICClient.GNICHOST)
    parser.add_option("-h", "--host", action="store", 
                      type="string", dest="whoishost",
                       help="Lookup using specified whois host")
    parser.add_option("-i", "--nws", action="store_const", 
                      const=whois.NICClient.INICHOST, dest="whoishost",
                      help="Lookup using host " + whois.NICClient.INICHOST)
    parser.add_option("-I", "--iana", action="store_const", 
                      const=whois.NICClient.IANAHOST, dest="whoishost",
                      help="Lookup using host " + whois.NICClient.IANAHOST)
    parser.add_option("-l", "--lcanic", action="store_const", 
                      const=whois.NICClient.LNICHOST, dest="whoishost",
                      help="Lookup using host " + whois.NICClient.LNICHOST)
    parser.add_option("-m", "--ra", action="store_const", 
                      const=whois.NICClient.MNICHOST, dest="whoishost",
                      help="Lookup using host " + whois.NICClient.MNICHOST)
    parser.add_option("-p", "--port", action="store", 
                      type="int", dest="port",
                      help="Lookup using specified tcp port")
    parser.add_option("-Q", "--quick", action="store_true", 
                     dest="b_quicklookup", 
                     help="Perform quick lookup")
    parser.add_option("-r", "--ripe", action="store_const", 
                      const=whois.NICClient.RNICHOST, dest="whoishost",
                      help="Lookup using host " + whois.NICClient.RNICHOST)
    parser.add_option("-R", "--ru", action="store_const", 
                      const="ru", dest="country",
                      help="Lookup Russian NIC")
    parser.add_option("-6", "--6bone", action="store_const", 
                      const=whois.NICClient.SNICHOST, dest="whoishost",
                      help="Lookup using host " + whois.NICClient.SNICHOST)
    parser.add_option("-?", "--help", action="help")

        
    return parser.parse_args(argv)
    
if __name__ == "__main__":
    flags = 0
    nic_client = whois.NICClient()
    (options, args) = parse_command_line(sys.argv)
    if (options.b_quicklookup is True):
        flags = flags|whois.NICClient.WHOIS_QUICK
    domain = args[-1]
    results = nic_client.whois_lookup(options.__dict__, args[1], flags)
    import re
    __re__ = re.compile(r'No\smatch\sfor\s"(?P<domain>.*)"\.', re.MULTILINE)
    whois_result = __re__.findall(results)
    __is_invalid_domain__ = (len(whois_result) > 0) and (str(whois_result[0]).lower() == domain)
    if (__is_invalid_domain__):
        print 'DOMAIN INVALID'
    else:
        print 'DOMAIN VALID'
    print 'whois_result=%s' % (whois_result)
    print 'whois_lookup_validated=%s' % (whois.whois_lookup_validated(domain,options=options.__dict__,flags=flags))
    print results
    
