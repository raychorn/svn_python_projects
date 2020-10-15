import unittest
import types
import copy
from pprint import pprint

from pyax.sobject.classfactory import ClassFactory
from pyax.sobject.batch import Batch
from pyax.exceptions import SObjectTypeError, ApiFault
from pyax.util import booleanize, listify

from support import TestSession, TestData


class delete_test(unittest.TestCase):
    
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
            continue
 
        self.id_list = caseIds
        return
    ## END setUp
    
    def test_connection_delete(self):
        delete_result = self.sfdc.delete(self.id_list)
        deleted_ids = self.sfdc.resultToIdList(delete_result, 
                                               success_status=True)
        self.assertEqual(len(deleted_ids), len(self.id_list))
        case_batch_after = self.sfdc.retrieve("Case", self.id_list)
        self.assertEqual(len(case_batch_after), 0)
                
    def test_object_delete(self):
        Case = ClassFactory(self.sfdc, self.sObjectType)
        case_batch = Case.retrieve(self.id_list)
        for case in case_batch:
            try:
                case.delete()
            except Exception, e:
                self.fail(e)
        case_batch_after = Case.retrieve(self.id_list)
        self.assertEqual(len(case_batch_after), 0)

    def test_batch_delete(self):
        Case = ClassFactory(self.sfdc, self.sObjectType)
        case_batch = Case.retrieve(self.id_list)
        try:
            case_batch.delete()
        except Exception, e:
            self.fail(e)
        case_batch_after = Case.retrieve(self.id_list)
        self.assertEqual(len(case_batch_after), 0)      
        
    def test_undelete(self):
        Case = ClassFactory(self.sfdc, self.sObjectType)
        case_batch = Case.retrieve(self.id_list)
        deleted_ids = []
        try:
            delete_result = case_batch.delete()
            deleted_ids = self.sfdc.resultToIdList(delete_result, 
                                                   success_status=True)
        except Exception, e:
            self.fail(e)
        case_batch_mid = Case.retrieve(self.id_list)
        self.assertEqual(len(case_batch_mid), 0)      
        deleted_ids = self.sfdc.resultToIdList(delete_result, 
                                               success_status=True)
        undelete_result = self.sfdc.undelete(deleted_ids)
        self.assertEqual(len(undelete_result), len(self.id_list))

    def test_emptyRecycleBin(self):
        """ Test that emptyRecycleBin permanently removes deleted records"""
        query_str = "SELECT Id FROM Case WHERE subject LIKE '!@#$%' " +\
            "AND CreatedDate >= %s" %self.start_timestamp
        query_deleted_str = "%s AND isDeleted = true" %query_str
        del_id_list = [self.id_list[1], self.id_list[3]]
        self.sfdc.delete(del_id_list)

        erb_result_list = self.sfdc.emptyRecycleBin(del_id_list)

        for er in erb_result_list:
            self.assertEqual(er['success'], True)
            
        undelete_result_list = self.sfdc.undelete(del_id_list)

        # emptied records cannot be undeleted
        for ur in undelete_result_list:
            self.assertEqual(ur['success'], False)

        
    def tearDown(self):
        """
        Clean up any objects created in the course of the test fixture
        """
        if len(self.id_list):
            self.sfdc.delete(self.id_list)
            pass
        return
    pass
## END class Create_test

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(delete_test))
    return suite
    
if __name__ == "__main__":
    unittest.main()
    pass
