import unittest
import types
import copy

from pyax.sobject.classfactory import ClassFactory
from pyax.exceptions import SObjectTypeError
from pyax.sobject.batch import Batch
from pyax.exceptions import ApiFault
from pyax.datatype.apexdatetime import ApexDatetime, ApexDate
from pyax.util import booleanize, listify

from support import TestSession, TestData


class retrieve_test(unittest.TestCase):
    
    def setUp(self):
        self.sfdc = TestSession().sfdc
        self.sObjectType = 'Case'
        self.Case = ClassFactory(self.sfdc, self.sObjectType)
    
        self.objects = TestData.gen_cases(5)
        saveResult = self.sfdc.create(self.Case, self.objects)
        caseIds = []
        for saveResultItem in saveResult:
            id = saveResultItem.get('id')
            caseIds.append(id)
 
        self.id_list = caseIds
        return

    
    
    def compare_result(self, compare_SObjectType, retrieved_SObjects, ids):
        compare_SObject = ClassFactory(self.sfdc, compare_SObjectType)
        compare_SObject_instance = compare_SObject()
        
        compare_Batch = Batch(self.sfdc)
        
        if type(retrieved_SObjects) == type(compare_SObject_instance):
            self.compare_result_unit(retrieved_SObjects, compare_SObject_instance, ids)
        elif type(retrieved_SObjects) == type(compare_Batch):
            ct = 0
            for retrieved_SObject in retrieved_SObjects:
                self.compare_result_unit(retrieved_SObject, compare_SObject_instance, ids[ct])
                ct += 1

        else:
            errmsg = 'retrieved Type %s not one of %s or %s type' \
                     %(type(retrieved_SObjects), type(compare_SObject_instance), type(compare_Batch))
            self.fail(errmsg)

        return
    

    def compare_result_unit(self, retrievedSObject, compareSObjectInstance, compareId):
        self.assertEqual(type(retrievedSObject), type(compareSObjectInstance))
        self.assertEqual(retrievedSObject.get('Id'), compareId)
        return
    
    
    def test_single_retrieve(self):
        """ Test retrieve of a single scalar sObjectListId """
        testId = self.id_list[0]
        retrieved = self.sfdc.retrieve(self.sObjectType, testId)
        self.compare_result(self.sObjectType, retrieved, testId)
        return


    def test_retrieved_types(self):
        """ Test data types of a few fields"""
        testId = self.id_list[0]
        retrieved = self.sfdc.retrieve(self.sObjectType, testId)
        self.assertEqual(type(retrieved['isClosed']), types.BooleanType) 
        self.assert_(isinstance(retrieved['LastModifiedDate'], ApexDatetime))
        return


    def test_single_list_retrieve(self):
        """ Test retrieve of a list of a single sObjectListId """
        testIdList = self.id_list[:1]
        retrieved = self.sfdc.retrieve(self.sObjectType, testIdList)
        self.compare_result(self.sObjectType, retrieved, testIdList)
        return
    

    def test_list_retrieve(self):
        """ Test retrieve of a list of muliple sObjectListIds """
        retrieved = self.sfdc.retrieve(self.sObjectType, self.id_list)
        self.compare_result(self.sObjectType, retrieved, self.id_list)
        return


    def test_duplicate_list_retrieve(self):
        """ Test retrieve of a list of muliple sObjectListIds with a duplicated Id """
        num_ids = len(self.id_list)
        
        # Adjust the source and destination of the record to be duplicated
        # based on the size of the test fixture
        insert_idx = num_ids
        source_idx = 0
        if num_ids > 2:
            insert_idx = -1
        elif num_ids > 3:
            source_idx = 1
        else:
            pass
        
        test_id_list = copy.copy(self.id_list)
        test_id_list.insert(insert_idx, self.id_list[source_idx])
        retrieved = self.sfdc.retrieve(self.sObjectType, test_id_list)
        self.compare_result(self.sObjectType, retrieved, self.id_list)   
        return


    def test_textarea_retrieve(self):
        """ Test retrieve of a textarea containing a newline"""
        fields = ['Description']
        retrieved = self.sfdc.retrieve(self.sObjectType, self.id_list, fields)
        retrieved_descriptions = [r["Description"] for r in retrieved]
        objects_descriptions = [o["Description"] for o in self.objects]
        for description in retrieved_descriptions:
            self.assertTrue(description in objects_descriptions)


    def test_field_retrieve(self):
        """ Check that we get just the fields we asked for"""
        fields = ['Id', 'CaseNumber', 'Subject', 'Origin', 'Priority', 'Type']
        retrieved = self.sfdc.retrieve(self.sObjectType, self.id_list, fields)
        retrieved_keys = retrieved[0].keys()
        retrieved_keys.sort()
        fields.sort()
        self.assertEqual(fields, retrieved_keys)
        return


    def test_invalid_field_retrieve(self):
        """ Asking for a non-existent field name should raise ApiFault: INVALID_FIELD"""
        fields = ['Id', 'Slkjflui', 'Subject', 'Origin', 'Priority']
        try:
            retrieved = self.sfdc.retrieve(self.sObjectType, self.id_list, fields)
        except ApiFault, f:
            self.assertEqual(f.exception_code, "INVALID_FIELD")
        except Exception, exc:
            self.fail("Query with invalid field raised exception other than ApiFault: %s" %exc)
        return


    def test_invalid_type_retrieve(self):
        """ Check that we error on an invalid type """
        fields = ['Id', 'CaseNumber', 'Subject', 'Origin', 'Priority']
        self.assertRaises(SObjectTypeError, self.sfdc.retrieve, "Glark", self.id_list, fields)
        return



    def tearDown(self):
        """
        Clean up any objects created in the course of the test fixture

        """
        if len(self.id_list):
            self.sfdc.delete(self.id_list)
            pass
        return




def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(retrieve_test))
    return suite
    
if __name__ == "__main__":
    unittest.main()
    pass
