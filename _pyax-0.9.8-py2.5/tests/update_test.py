import unittest
import types
import copy

from pyax.sobject.classfactory import ClassFactory
from pyax.sobject.batch import Batch
from pyax.util import booleanize, listify

from support import TestSession, TestData


class update_test(unittest.TestCase):
    
    def setUp(self):
        self.sfdc = TestSession().sfdc
        self.sObjectType = 'Case'
        Case = ClassFactory(self.sfdc, self.sObjectType)
    
        objects = TestData.gen_cases(2)
        saveResult = self.sfdc.create(Case, objects)

        caseIds = []
        for saveResultItem in saveResult:
            id = saveResultItem.get('id')
            caseIds.append(id)
            continue
 
        self.idList = caseIds
        return
    ## END setUp
    
    def dictCompare(self, dictA, dictB):
        self.assertEqual(len(dictA), len(dictB))
        
        for keyA in dictA.keys():
            itemA = dictA[keyA]
            
            self.assert_(dictB.has_key(keyA))
            itemB = dictB[keyA]
            self.assertEqual(itemA, itemB)
            continue
        return
    
    def testNoUpdate(self):
        """ Test calling update on a sObject that has no updates """
        testId = self.idList[0]
        retrievedCase = self.sfdc.retrieve(self.sObjectType, testId)

        saveResult = retrievedCase.update()
        self.failUnless(booleanize(saveResult.get('success',False)))
        return
    ## END testNoUpdate

    def testSingleUpdate(self):
        """ Test update of a single scalar sObject """
        testId = self.idList[0]
        retrievedCase = self.sfdc.retrieve(self.sObjectType, testId)

        updateDescrString = 'This description has been changed'
        retrievedCase['Description'] = updateDescrString
        saveResult = retrievedCase.update()
        self.failUnless(booleanize(saveResult.get('success',False)))
        
        reRetrievedCase = self.sfdc.retrieve(self.sObjectType, testId)
        self.assertEqual(updateDescrString, reRetrievedCase.get('Description'))
        return
    ## END testSingleUpdate

    def testBatchUpdate(self):
        """ Test update of a single scalar sObject """
        testIdList = [self.idList[0], self.idList[1]]
        retrievedCaseBatch = self.sfdc.retrieve(self.sObjectType, testIdList)

        updateDescrString = 'This description has been changed'
        updatePriority = 'Medium'
        
        retrievedCaseBatch[self.idList[0]]['Description'] = updateDescrString
        retrievedCaseBatch[self.idList[1]]['Priority'] = updatePriority
        
        saveResultBatch = retrievedCaseBatch.update()
        
        for saveResult in saveResultBatch:
            self.failUnless(booleanize(saveResult.get('success',False)))
            continue
        
        reRetrievedCase0 = self.sfdc.retrieve(self.sObjectType, self.idList[0])
        self.assertEqual(updateDescrString, reRetrievedCase0.get('Description'))
        
        reRetrievedCase1 = self.sfdc.retrieve(self.sObjectType, self.idList[1])
        self.assertEqual(updatePriority, reRetrievedCase1.get('Priority'))
        return
    ## END testBatchUpdate

    def testSingleFieldNull(self):
        """ Test nulling a field of a single scalar sObject """
        testId = self.idList[0]
        retrievedCase = self.sfdc.retrieve(self.sObjectType, testId)

        del retrievedCase['Description']
        saveResult = retrievedCase.update()
        self.failUnless(booleanize(saveResult.get('success',False)))
        
        reRetrievedCase = self.sfdc.retrieve(self.sObjectType, testId)
        self.assertEqual(None, reRetrievedCase.get('Description'))
        return
    ## END testSingleFieldNull

    def testMultiFieldNull(self):
        """ Test nulling multiple fields of a single scalar sObject """
        testId = self.idList[0]
        retrievedCase = self.sfdc.retrieve(self.sObjectType, testId)

        del retrievedCase['Description']
        del retrievedCase['Priority']
        saveResult = retrievedCase.update()
        self.failUnless(booleanize(saveResult.get('success',False)))
        
        reRetrievedCase = self.sfdc.retrieve(self.sObjectType, testId)
        self.assertEqual(None, reRetrievedCase.get('Description'))
        self.assertEqual(None, reRetrievedCase.get('Priority'))
        return
    ## END testMultiFieldNull

    def tearDown(self):
        """
        Clean up any objects created in the course of the test fixture

        """
        if len(self.idList):
            self.sfdc.delete(self.idList)
            pass
        return

    pass
## END class Create_test

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(update_test))
    return suite
    
if __name__ == "__main__":
    unittest.main()
    pass
