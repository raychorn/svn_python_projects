import dns.zone
from dns.exception import DNSException

domain = "vyperlogix.com"
print "Getting zone object for domain", domain
zone_file = "db.%s" % domain

try:
    zone = dns.zone.from_file(zone_file, domain)
    print "Zone origin:", zone.origin
except DNSException, e:
    print e.__class__, e