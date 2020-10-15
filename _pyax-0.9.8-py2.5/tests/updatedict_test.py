import unittest

from pyax.collections.updatedict import UpdateDict


class UpdateDict_test(unittest.TestCase):
    
    def setUp(self):
        self.td0 = {}
        self.td1 = {1: "one", 
               2: "two", 
               3: "three",
               4: "four",
               5: "five"}
        return
        
    
    def dictCompare(self, dictA, dictB):
        self.assertEqual(len(dictA), len(dictB))
        
        for keyA in dictA.keys():
            itemA = dictA[keyA]
            
            self.assert_(dictB.has_key(keyA))
            itemB = dictB[keyA]
            self.assertEqual(itemA, itemB)
            continue
        return
        
    def testEmptyInstantiate(self):
        """ Test instantiating an empty UpdateDict """
        d = UpdateDict(self.td0)
        self.dictCompare(d, self.td0)
        return

    def testInstantiate(self):
        """ Test instantiating an UpdateDict initialized with an dictionary of data """
        d = UpdateDict(self.td1)
        self.dictCompare(d, self.td1)
        return
    
    def testEmptySet(self):
        """ Test setting an element in an empty UpdateDict """
        d = UpdateDict(self.td0)
        d[6] = 'six'
        self.assertNotEqual(len(self.td0), len(d))
        self.td0[6] = 'six'
        self.dictCompare(d, self.td0)
        return

    def testSet(self):
        """ Test setting an element in an initialized UpdateDict """
        d = UpdateDict(self.td1)
        d[6] = 'six'
        self.assertNotEqual(len(self.td1), len(d))
        self.td1[6] = 'six'
        self.dictCompare(d, self.td1)
        return

    def testEmptyDel(self):
        """ Test deleting an element from an empty UpdateDict """
        d = UpdateDict(self.td0)
        del d[6]
        self.assertNotEqual(len(self.td0), len(d))
        self.td0[6] = None
        self.dictCompare(d, self.td0)
        return

    def testDel(self):
        """ Test deleting an element from an initialized UpdateDict """
        d = UpdateDict(self.td1)
        del d[6]
        self.assertNotEqual(len(self.td1), len(d))
        self.td1[6] = None
        self.dictCompare(d, self.td1)

        del d[2]
        self.td1[2] = None
        self.dictCompare(d, self.td1)
        return

    def testClear(self):
        """ Test clearing a modified UpdateDict back to the initialized state """
        d = UpdateDict(self.td1)
        del d[6]
        d[7] = 'seven'
        d[2] = 'dos'
        del d[3]
        self.assertNotEqual(len(self.td1), len(d))

        d.clear()
        self.dictCompare(d, self.td1)
        return

    pass

    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UpdateDict_test))
    return suite
    
if __name__ == "__main__":
    unittest.main()
    pass
