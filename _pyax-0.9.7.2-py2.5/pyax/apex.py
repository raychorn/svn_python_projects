""" Provides for calling Apex code methods from pyax

Highly experimental at present...

Not intende
"""
from pyax.unpackomatic import Unpackomatic

class Apex:
    """ Apex class isn't intended to be instantiated directly, rather an
    instance is created and stored as a property of the Connection object
    """
    def __init__(self, cxn):
        self.cxn = cxn
        pass
    
    def execute(self, pkg, method, args=None, is_array=False):
        pkg = pkg.replace(".", "/")    
        
        sobject_ns = "http://soap.sforce.com/schemas/package/%s" %pkg
        
        nsmap = [{"ns":sobject_ns, "prefix":""}]

        if args is None:
            args = {}

        param_list = [] 
            
        is_real_array = True
        if is_array is False:
            is_real_array = False
            
        url = "/services/Soap/package/%s" %pkg
        
        packed_result = self.cxn.svc._invoke(method, args, is_real_array, nsmap, 
                                             url, sobject_ns, sobject_ns)
        result = Unpackomatic.unpack(packed_result)
        return result

