import dns.resolver

answers = dns.resolver.query('vyperlogix.com', 'CNAME')
for rdata in answers:
    print 'Host', rdata.strings