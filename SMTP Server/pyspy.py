# $Id: pyspy.py,v 1.3 2001/12/12 18:11:14 lsmithso Exp $
# A brain-dead Python SMTP Proxy based on the smtps, smtplib and DNS
# packages.
#
# Author: L. Smithson (lsmithson@open-networks.co.uk)
#
# DISCLAIMER
# You are free to use this code in any way you like, subject to the
# Python disclaimers & copyrights. I make no representations about the
# suitability of this software for any purpose. It is provided "AS-IS"
# without warranty of any kind, either express or implied. So there.
#
#
#

"""
spyspy.py -- A very simple & dumb Python SMTP proxy server. It uses
smtps for the server side and smtplib for the client side. Somewhere
in between it uses the DNS package to resolve the MX name. This is
intended for use as a proxy where sendmail and the like are
unavailable (e.g., on a Windows box).

This blocks, waiting for RFC821 messages from clients on the given
port. When a complete SMTP message is received, the TO: addresses are
resolved into MX hosts, and the message is then forwarded on to those
hosts. Along the way, a silly X-Header is inserted.

All processing is single threaded. It generally handles errors
badly. It fails especially badly if DNS or the resolved mail host
hangs. DNS or mailhost failures are not propagated back to the client,
which is bad news.

The mail address 'shutdown@shutdown.now' is interpreted
specially. This gets around a Python 1.5/Windows/WINSOCK bug that
prevents this script from being interrupted.
"""

import sys, smtps, DNS, string, smtplib, rfc822, StringIO

# Default DNS host, assumes the lack of /etc/resolv.conf
DNSHOST='10.0.0.2'

def mxlookup(host):
    global DNSHOST
    a = DNS.DnsRequest(host, qtype = 'mx', server=DNSHOST).req().answers
    l = map(lambda x:x['data'], a)
    l.sort()
    return l


#
# This extends the smtps.SMTPServerInterface and specializes it to
# proxy requests onwards. It uses DNS to resolve each RCPT TO:
# address, then uses smtplib to forward the client mail on the
# resolved mailhost.
#

class SMTPService(smtps.SMTPServerInterface):
    def __init__(self):
        self.savedTo = []
        self.savedMailFrom = ''
        self.shutdown = 0
        
    def mailFrom(self, args):
        # Stash who its from for later
        self.savedMailFrom = smtps.stripAddress(args)
        
    def rcptTo(self, args):
        # Stashes multiple RCPT TO: addresses
        self.savedTo.append(args)
        
    def data(self, args):
        # Process client mail data. It inserts a silly X-Header, then
        # does a MX DNS lookup for each TO address stashed by the
        # rcptTo method above. Messages are logged to the console as
        # things proceed. 
        data = self.frobData(args)
        for addressee in self.savedTo:
            toHost, toFull = smtps.splitTo(addressee)
            # Treat this TO address speciallt. All because of a
            # WINSOCK bug!
            if toFull == 'shutdown@shutdown.now':
                self.shutdown = 1
                return
            sys.stdout.write('Resolving ' + toHost + '...')
            resolved = mxlookup(toHost)
            if len(resolved):
                sys.stdout.write(' found. Sending ...')
                mxh = resolved[0][1]
                for retries in range(3):
                    try:
                        smtpServer = smtplib.SMTP(mxh)
                        smtpServer.set_debuglevel(0)
                        smtpServer.helo(mxh)
                        smtpServer.sendmail(self.savedMailFrom, toFull, data)
                        smtpServer.quit()
                        print ' Sent TO:', toFull, mxh
                        break
                    except Exception, e:
                        print '*** SMTP FAILED', retries, mxh, sys.exc_info()[1]
                        continue
            else:
                print '*** NO MX HOST for :', toFull
        self.savedTo = []
        
    def quit(self, args):
        if self.shutdown:
            print 'Shutdown at user request'
            sys.exit(0)

    def frobData(self, data):
        hend = string.find(data, '\n\r')
        if hend != -1:
            rv = data[:hend]
        else:
            rv = data[:]
        rv = rv + 'X-PySpy: Python SMTP Proxy Frobnication'
        rv = rv + data[hend:]
        return rv

def Usage():
    print """Usage pyspy.py port DNS
Where:
  port = Client SMTP Port number (ie 25)
  DNS = DNS host, as dotted IP."""
    sys.exit(1)
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        Usage()
    port = int(sys.argv[1])
    DNSHOST = sys.argv[2]
    service = SMTPService()
    server = smtps.SMTPServer(port)
    print 'Python SMPT Proxy Ready. $Id: pyspy.py,v 1.3 2001/12/12 18:11:14 lsmithso Exp $'
    server.serve(service)
