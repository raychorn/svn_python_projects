import unittest

from pyax.sobject.classfactory import ClassFactory

from support import TestSession, TestData

from pyax.util import booleanize, listify

class create_test(unittest.TestCase):
    
    def setUp(self):
        self.sfdc = TestSession().sfdc
        self.idList = []
        return

    def checkSaveResult(self, saveResult):
        idList = []
        saveResult = listify(saveResult)
        
        for saveResultItem in saveResult:
            self.assertEqual(booleanize(saveResultItem.get('success')), True)
            id = saveResultItem.get('id')
            
            self.assertNotEqual(id, None)
            idList.append(id)
            continue

        return idList
    
    def testSingleCreate(self):
        """ Create a single Case sObject """
        Case = ClassFactory(self.sfdc, 'Case')
        saveResult = self.sfdc.create(Case, TestData.gen_cases(1))
        self.idList = self.checkSaveResult(saveResult)
        return
    
    def testMultipleCreate(self):
        """ Create multiple Case sObjects in batch """
        Case = ClassFactory(self.sfdc, 'Case')
        objects = TestData.gen_cases(5)
        saveResult = self.sfdc.create(Case, objects)
        self.idList = self.checkSaveResult(saveResult)
        return

    def testObjectCreate(self):
        """ Create a Case sObject by calling the create class method on the 
            Case sObjectClass """
        Case = ClassFactory(self.sfdc, 'Case')
        saveResult = Case.create(TestData.gen_cases(1))
        self.idList = self.checkSaveResult(saveResult)
        return
    
    def testSingleCreateWithNone(self):
        """ Create a single Case sObject with a None value field """
        Case = ClassFactory(self.sfdc, 'Case')
        objects = TestData.gen_cases(1)
        objects[0]['Description'] = None
        saveResult = self.sfdc.create(Case, objects)
        self.idList = self.checkSaveResult(saveResult)
        return
    
    def testMultipleCreateWithNone(self):
        """ Create a multiple Case sObject with a None value field """
        Case = ClassFactory(self.sfdc, 'Case')
        objects = TestData.gen_cases(5)
        objects[2]['Description'] = None
        saveResult = self.sfdc.create(Case, objects)
        self.idList = self.checkSaveResult(saveResult)
        return
    
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
    suite.addTest(unittest.makeSuite(create_test))
    return suite
    
if __name__ == "__main__":
    unittest.main()
    pass
