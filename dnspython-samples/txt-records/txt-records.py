import dns.resolver

answers = dns.resolver.query('vyperlogix.com', 'TXT')
for rdata in answers:
    print 'Host', rdata.strings