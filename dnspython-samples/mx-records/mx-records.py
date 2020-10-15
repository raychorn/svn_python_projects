import dns.resolver

#from vyperlogix.misc import debug

answers = dns.resolver.query('vyperlogix.com', 'MX')
for rdata in answers:
    #debug.introspect(rdata)
    print 'Host', rdata.exchange, 'has preference', rdata.preference