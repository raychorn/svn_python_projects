''' Copyright (c) 2006-2007, PreFab Software Inc. '''


import unittest, sys
from blogmaker.util import strip_domain, strip_tlds

class util_tests(unittest.TestCase):
    def test_strip_domain(self):
        self.assertEquals('example.com', strip_domain('example.com'))
        self.assertEquals('example.com', strip_domain('www.example.com'))
        self.assertEquals('example.com', strip_domain('www2.example.com'))

        self.assertEquals('ww.example.com', strip_domain('ww.example.com'))
        self.assertEquals('wwww.example.com', strip_domain('wwww.example.com'))
        self.assertEquals('wwwexample.com', strip_domain('wwwexample.com'))
        
        self.assertEquals('example.com', strip_domain('http://example.com'))
        self.assertEquals('example.com', strip_domain('http://example.com/'))
        self.assertEquals('example.com', strip_domain('http://example.com./'))
        self.assertEquals('example.com', strip_domain('http://www.example.com'))
        self.assertEquals('example.com', strip_domain('http://www2.example.com'))
        
        self.assertEquals('example.com', strip_domain('http://example.com/foo/bar?baz=boo'))
        
        self.assertEquals('example.com', strip_domain('https://example.com'))
        self.assertEquals('example.com', strip_domain('https://www.example.com'))
        self.assertEquals('example.com', strip_domain('https://www2.example.com'))

        self.assertEquals('foo.example.com', strip_domain('foo.example.com'))
        self.assertEquals('foo.example.com', strip_domain('www.foo.example.com'))
        self.assertEquals('foo.example.com', strip_domain('foo.example.com'))
        self.assertEquals('foo.example.com', strip_domain('http://foo.example.com'))
        self.assertEquals('foo.example.com', strip_domain('http://www2.foo.example.com'))
        self.assertEquals('foo.example.com', strip_domain('https://foo.example.com'))


    def test_strip_tlds(self):
        self.assertEquals('example', strip_tlds('www.example.com'))
        self.assertEquals('example', strip_tlds('www.example.net'))
        self.assertEquals('example', strip_tlds('www.example.com.au'))
        self.assertEquals('example', strip_tlds('www.example.co.uk'))
        self.assertEquals('example', strip_tlds('http://www.example.co.uk/foo/'))
        
        
if __name__ == '__main__':
    unittest.main()