import unittest
import types
import copy
from pprint import pprint, pformat

from pyax.sobject.classfactory import ClassFactory
from pyax.sobject.batch import Batch
from pyax.exceptions import SObjectTypeError, ApiFault
from pyax.util import booleanize, listify

from support import TestSession, TestData

class query_test(unittest.TestCase):

    def setUp(self):
        self.sfdc = TestSession().sfdc
        self.start_timestamp = self.sfdc.getServerTimestamp()
        self.sObjectType = 'Case'
        Case = ClassFactory(self.sfdc, self.sObjectType)

        objects = []
        objects = TestData.gen_cases(5)
        saveResult = self.sfdc.create(Case, objects)
        caseIds = []
        for saveResultItem in saveResult:
            id = saveResultItem.get('id')
            caseIds.append(id)

        self.id_list = caseIds

    def test_simple_query(self):
        """ Test a simple query that should return list of results"""
        query_str = "SELECT Id, Subject FROM Case WHERE subject LIKE '!@#$%'"
        queried = self.sfdc.query(query_str)
        self.assertEqual(type(queried), type(Batch(self.sfdc)))

    def test_simple_query_single(self):
        """ Test a simple query that should return one result"""
        query_str = ("SELECT Id, Subject FROM Case "
                     "WHERE subject LIKE '!@#$% Subject 3' LIMIT 1")
        queried = self.sfdc.query(query_str)
        self.assertEqual(type(queried), type(Batch(self.sfdc)))
        self.assertEqual(len(queried), 1)

    def test_query_invalid(self):
        """ Test a simple query that should throw an ApiFault code MALFORMED_QUERY"""
        query_str = ("SEQECT Id, Zorchplox FROM Case "
                     "WHERE subject LIKE '!@#$% Subject 3' LIMIT 1")
        try:
            self.sfdc.query(query_str)
        except ApiFault, f:
            self.assertEqual(f.exception_code, "MALFORMED_QUERY")
        except Exception, f:
            self.fail("Invalid query raised exception "
                      "other than ApiFault: %s" %type(f))

    def test_query_invalid_field(self):
        """ Test a simple query that should throw an ApiFault code INVALID_FIELD"""
        query_str = ("SELECT Id, Zorchplox FROM Case "
                     "WHERE subject LIKE '!@#$% Subject 3' LIMIT 1")
        #self.assertRaises(ApiFault, self.sfdc.query, query_str)
        try:
            self.sfdc.query(query_str)
        except ApiFault, f:
            self.assertEqual(f.exception_code, "INVALID_FIELD")
        except Exception, f:
            self.fail("Query with invalid field raised "
                      "exception other than ApiFault: %s" %type(f))

    def test_query_all(self):
        """Test that queryAll can return deleted records where query cannot"""
        query_str = "SELECT Id FROM Case WHERE subject LIKE '!@#$%' " +\
            "AND CreatedDate >= %s" %self.start_timestamp
        query_deleted_str = "%s AND isDeleted = true" %query_str
        del_id_list = [self.id_list[1], self.id_list[3]]
        self.sfdc.delete(del_id_list)

        query_result_batch = self.sfdc.query(query_str)
        query_all_result_batch = self.sfdc.queryAll(query_str)
        query_deleted_result_batch = self.sfdc.queryAll(query_deleted_str)

        # regular query should only see three of the five cases
        self.assertEqual(len(query_result_batch), 3)
        # query all should see all five cases
        self.assertTrue(len(query_all_result_batch) >= 5)
        # query all for isDeleted=true should see the two deleted cases
        self.assertEqual(len(query_deleted_result_batch), 2)

    def test_pprint_batch(self):
        """Test that an sobject batch can be pprinted"""
        query_str = "SELECT Id, Subject FROM Case WHERE subject LIKE '!@#$%'"
        queried = self.sfdc.query(query_str)
        self.assertTrue(len(queried) > 0)
        self.assertTrue(isinstance(queried, Batch))
        try:
            pformat(queried)
        except Exception, e:
            self.fail(e)
    
    def test_query_count(self):
        """Test that we can SELECT COUNT() """
        query_str = "SELECT COUNT() FROM Case WHERE subject LIKE '!@#$%'"
        count_result = self.sfdc.query(query_str)
        self.assertEquals(count_result, len(self.id_list))
        
    def test_query_count_none(self):
        """Test that we can SELECT COUNT() where we expect zero rows back"""
        query_str = "SELECT COUNT() FROM Case WHERE subject = 'xxx!@#$xxx%'"
        count_result = self.sfdc.query(query_str)
        self.assertEquals(count_result, 0)
        
    def tearDown(self):
        """Clean up any objects created in the course of the test fixture
        """
        if len(self.id_list):
            self.sfdc.delete(self.id_list)


class ClientQueryTestCase(unittest.TestCase):
    """
    Testing asynchronous queries with Twisted.

    Only one test method, because dealing with starting and stopping
    Twisted's reactor is too difficult. I think that trial can do it, somehow,
    but I want to avoid using it just for test two methods.
    
    """

    # Twisted timeout in seconds
    timeout = 30
    # Number of test cases to generate during each of test
    cases_count = 5

    def generateTestData(self):
        self.sfdc = TestSession().sfdc
        self.start_timestamp = self.sfdc.getServerTimestamp()
        Case = ClassFactory(self.sfdc, 'Case')

        objects = TestData.gen_cases(self.cases_count)
        saveResult = self.sfdc.create(Case, objects)
        self.id_list = []
        for saveResultItem in saveResult:
            self.id_list.append(saveResultItem.get('id'))

    def deleteTestData(self):
        if self.id_list:
            self.sfdc.delete(self.id_list)

    def setUp(self):
        from twisted.internet import reactor
        self.reactor = reactor

    def test(self):
        """Test asynchronous queries"""
        self.timer = self.reactor.callLater(self.timeout, self.failure)
        self.generateTestData()
        self.part_1()

    def part_1(self):
        """Checking query."""
        qry = """SELECT Id, Subject, Priority FROM Case WHERE
        Subject LIKE '!@#$%%' AND CreatedDate >= %s""" % self.start_timestamp
        self.sfdc.query(qry, callback=self.part_1_success)
        self.reactor.run()

    def assertQueryResult(self, result):
        self.assertEqual(len(result), self.cases_count)
        for case in result:
            self.assert_(case['Id'] in self.id_list)

    def part_1_success(self, result):
        self.assertQueryResult(result)
        self.deleteTestData()
        self.generateTestData()
        self.part_2()

    def part_2(self):
        """Check queryAll."""
        qry = """SELECT Id, Subject, Priority FROM Case WHERE
        Subject LIKE '!@#$%%' AND CreatedDate >= %s""" % self.start_timestamp

        self.sfdc.delete([self.id_list[0], self.id_list[1]])
        cases = self.sfdc.query(qry)
        self.assertEqual(len(cases), self.cases_count - 2)

        self.sfdc.queryAll(qry, callback=self.part_2_success)

    def part_2_success(self, result):
        self.assertQueryResult(result)
        #self.timer.cancel()
        #self.reactor.stop()
        self.deleteTestData()
        self.generateTestData()
        self.part_3()
        
    def part_3(self):
        qry = ("SELECT COUNT() from Case WHERE Subject LIKE '!@#$%%' "
               "AND CreatedDate >= %s" % self.start_timestamp)
        self.sfdc.query(qry, callback=self.part_3_success)
        pass
    
    def part_3_success(self, result):
        self.assertEqual(result, self.cases_count)
        self.timer.cancel()
        self.reactor.stop()
        self.deleteTestData()
        
    def failure(self):
        self.reactor.stop()
        self.fail("Query timeout.")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(query_test))
    try:
        import twisted
        suite.addTest(unittest.makeSuite(ClientQueryTestCase))
    except ImportError:
        pass
    return suite

if __name__ == "__main__":
    unittest.main()
    pass
