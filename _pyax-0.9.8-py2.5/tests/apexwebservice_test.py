import unittest
import types
import copy
from pprint import pprint

from pyax.sobject.classfactory import ClassFactory
from pyax.sobject.batch import Batch
from pyax.exceptions import SObjectTypeError, ApiFault
from pyax.util import booleanize, listify
from pyax.datatype.apexdatetime import ApexDate, ApexDatetime

from support import TestSession, TestData


class apexwebservice_test(unittest.TestCase):
    def setUp(self):
        self.sfdc = TestSession().sfdc
        return
    
    def test_datetime_return(self):
        r = self.sfdc.apex.execute("PyaxApexTestMethods", "DatetimeTest")
        # result must be convertible to an ApexDatetime
        try:
            adt = ApexDatetime.fromSfIso(r)
        except Exception, e:
            self.fail(e)

    def test_boolean_return(self):
        r = self.sfdc.apex.execute("PyaxApexTestMethods", "BooleanTest")
        self.assertTrue(isinstance(r, bool))
        
    def test_string_list_return(self):
        ceo = 'ceo'
        salesforce = 'salesforce'
        com = 'com'
        email = "%s@%s.%s" %(ceo, salesforce, com)
        r = self.sfdc.apex.execute("PyaxApexTestMethods", 
                                   "MultipleStringReturnTest", 
                                   {'email': email})
        self.assertTrue(isinstance(r, list))
        self.assertEqual(len(r), 3)
        self.assertEqual(r[0], ceo)
        self.assertEqual(r[1], salesforce)
        self.assertEqual(r[2], com)

    def test_multiple_string_args(self):
        part1 = "foo"
        part2 = "bar"
        combo = "%s%s" %(part1, part2)
        r = self.sfdc.apex.execute("PyaxApexTestMethods", 
                                   "MultipleStringArgTest", 
                                   {'part1':part1, 'part2':part2})
        self.assertEqual(r, combo)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(apexwebservice_test))
    return suite
    
if __name__ == "__main__":
    unittest.main()
    pass