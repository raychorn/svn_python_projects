import unittest

from pyax.beatbox import SoapFaultError

from pyax.context import Context

from support import TestSession

import types
import datetime
from pprint import pprint

class Context_test(unittest.TestCase):
    
    def setUp(self):
        self.context = Context()
        
    def testDefaultContext(self):
        """Context should have sane default values"""
        self.assertEqual(self.context.force_http,
                         self.context._Context__default_force_http)

        self.assertEqual(self.context.instance,
                         self.context._Context__default_instance)
        
        # prior to login, the login endpoint and endpoint are the same
        self.assertEqual(self.context.login_endpoint,
                         self.context.endpoint)    
            
        self.assertEqual(self.context.gzip_request,
                         self.context._Context__default_gzip_request)
            
        self.assertEqual(self.context.gzip_response,
                         self.context._Context__default_gzip_response)   
        
        self.assertEqual(self.context.assignment_rule_id,
                         self.context._Context__assignment_rule_id)
        
        self.assertEqual(self.context.use_default_assignment_rule,
                         self.context._Context__use_default_assignment_rule)
        
        self.assertEqual(self.context.batch_size,
                         self.context._Context__default_batch_size)
        return


        
    pass
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Context_test))
    return suite
    
if __name__ == "__main__":
    unittest.main()
