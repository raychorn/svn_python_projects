from vyperlogix.enum.Enum import Enum

class ProductVersion(Enum):
    nothing = 0
    community_version = 2**1
    professional_version = 2**2
    enterprise_version = 2**3
    
def explain_version(vers):
    if (vers == ProductVersion.community_version):
        return 'Community Edition'
    elif (vers == ProductVersion.professional_version):
        return 'Professional Edition'
    elif (vers == ProductVersion.enterprise_version):
        return 'Enterprise (Unlimited)'

def explain_ports_limits(vers):
    if (vers == ProductVersion.community_version):
        return 3
    elif (vers == ProductVersion.professional_version):
        return 6
    elif (vers == ProductVersion.enterprise_version):
        return 0

def explain_address_limits(vers):
    if (vers == ProductVersion.community_version):
        return '127.0.0.1'
    elif (vers == ProductVersion.professional_version):
        return '127.0.0.1'
    elif (vers == ProductVersion.enterprise_version):
        return '0.0.0.0 or 127.0.0.1'

def test_address_limits(vers,ip):
    if (vers == ProductVersion.community_version):
        return ip == explain_address_limits(vers)
    elif (vers == ProductVersion.professional_version):
        return ip == explain_address_limits(vers)
    elif (vers == ProductVersion.enterprise_version):
        return ip in explain_address_limits(vers).split(' or ')
