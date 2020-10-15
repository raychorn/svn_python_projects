import unittest
import types
import copy
from pprint import pprint, pformat

from pyax.sobject.classfactory import ClassFactory
from pyax.sobject.batch import Batch
from pyax.exceptions import SObjectTypeError, ApiFault
from pyax.unpackomatic import Unpackomatic
from pyax.util import booleanize, listify


from support import TestSession, TestData

class large_query_test(unittest.TestCase):

    num_cases = 700

    def setUp(self):
        self.sfdc = TestSession().sfdc
        self.start_timestamp = self.sfdc.getServerTimestamp()
        self.sObjectType = 'Case'
        Case = ClassFactory(self.sfdc, self.sObjectType)

        objects = []
        objects = TestData.gen_cases(self.num_cases)
        saveResult = self.sfdc.create(Case, objects)
        caseIds = []
        for saveResultItem in saveResult:
            id = saveResultItem.get('id')
            caseIds.append(id)

        self.id_list = caseIds

    def test_simple_large_query(self):
        """ Test a simple query that should return list of results using queryMore"""
        query_str = "SELECT Id, Subject FROM Case WHERE subject LIKE '!@#$%'"
        queried = self.sfdc.query(query_str)
        self.assertEqual(type(queried), type(Batch(self.sfdc)))
    
    def test_query_count(self):
        """Test that we can SELECT COUNT() """
        query_str = "SELECT COUNT() FROM Case WHERE subject LIKE '!@#$%'"
        count_result = self.sfdc.query(query_str)
        self.assertEquals(count_result, len(self.id_list))
        
    def patchUnpackQueryResult(self, query_result):
        """Unpacks result returned from beatbox request.

        @param query_result: result from beatbox request.
        @return: tuple with:
                 - records: list of returned items,
                 - done: is all objects are returned,
                 - query_locator: locator of query on salesforce
                 - size: integer total number of rows found
        """
        query_result = Unpackomatic.unpack(query_result)
        records = listify(query_result.get('records')[0])
        done = booleanize(query_result.get('done'))
        query_locator = query_result.get('queryLocator')
        size = int(query_result.get('size', 0))
        return records, done, query_locator, size
        
    def test_single_result_with_query_more(self):
        """Ensure that queryMore properly collects results into a list when batch size is forced to 1
        """
        self.sfdc._unpackQueryResult = self.patchUnpackQueryResult
        query_str = "SELECT Id, Subject FROM Case WHERE subject LIKE '!@#$%'"
        queried = self.sfdc.query(query_str)
        self.assertEquals(len(queried), 2)
    
    def tearDown(self):
        """Clean up any objects created in the course of the test fixture
        """
        if len(self.id_list):
            self.sfdc.delete(self.id_list)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(large_query_test))
    return suite

if __name__ == "__main__":
    unittest.main()
    pass
