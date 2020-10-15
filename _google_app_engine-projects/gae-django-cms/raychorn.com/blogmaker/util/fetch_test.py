''' Copyright (c) 2006-2007, PreFab Software Inc. '''


''' Tests for the fetch module.
    You must be running the blogcosm server in dev mode on port 8000
    when you run these tests.
'''

import unittest, urllib2
import fetch

from blogcosm.test import constants as c

class FetchTest(unittest.TestCase):
    def test_open_resource(self):
        f = fetch.open_resource('http://localhost:8000/test/simpleHomePage/')
        data = f.read()
        f.close()
        
        self.assertEquals(200, f.code)
        self.assertEquals('http://localhost:8000/test/simpleHomePage/', f.url)
        self.assert_(data)
        
        self.assertEquals(c.lastModified, f.headers['last-modified'])
    
        self.assertEquals(c.eTag, f.headers['etag'])
    
    def test_notModified(self):
        f = fetch.open_resource('http://localhost:8000/test/304/')
        self.assertEquals(304, f.status)

    def test_redirect(self):
        f = fetch.open_resource('http://localhost:8000/test/simpleHomePage')
        self.assertEquals(200, f.code)
        self.assertEquals(301, f.status)
        self.assertEquals('http://localhost:8000/test/simpleHomePage/', f.url)
        
        f = fetch.open_resource('http://localhost:8000/test/tempRedirect/')
        self.assertEquals(200, f.code)
        self.assertEquals(302, f.status)
        self.assertEquals('http://localhost:8000/test/simpleHomePage/', f.url)
        
    
if __name__ == '__main__':
    unittest.main()

