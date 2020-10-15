import unittest

from pyax.collections.clist import clist


class clist_test(unittest.TestCase):
    
    def setUp(self):
        self.cl = clist()
        self.cl.extend(["ZERO", "One", "TwO", "thREE", "FoUr"])
        return
        
    
    def test_index(self):
        self.assertEquals(self.cl.index("two"), 2)
        
    def test_contains(self):
        self.assert_("three" in self.cl)
        
    def test_repr(self):
        repr(self.cl)
        
    pass

    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(clist_test))
    return suite
    
if __name__ == "__main__":
    unittest.main()
    pass
