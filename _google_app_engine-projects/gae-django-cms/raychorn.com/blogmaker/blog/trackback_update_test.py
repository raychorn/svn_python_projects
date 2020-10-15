''' Copyright (c) 2006-2007, PreFab Software Inc. '''


import unittest

from blogmaker.blog.trackback_update import triples


class trackback_update_tests(unittest.TestCase):
    def test_triples(self):
        self.assertEquals([], list(triples('')))
        self.assertEquals([('', 'a', '')], list(triples('a')))
        self.assertEquals([('', 'a', 'b'), ('a', 'b', '')], list(triples('ab')))
        self.assertEquals([('', 'a', 'b'), ('a', 'b', 'c'), ('b', 'c', '')], list(triples('abc')))
        
if __name__ == '__main__':
    unittest.main()