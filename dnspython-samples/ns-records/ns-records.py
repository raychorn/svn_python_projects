import dns.resolver

answers = dns.resolver.query('vyperlogix.com', 'NS')
for rdata in answers:
    print 'Host', rdata.target