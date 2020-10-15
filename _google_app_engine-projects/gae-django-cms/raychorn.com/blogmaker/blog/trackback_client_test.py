''' Copyright (c) 2006-2007, PreFab Software Inc. '''


import unittest
from trackback_client import discover, postTrackback, TrackbackError

class trackback_client_test(unittest.TestCase):
    def test_postTrackback(self):
        self.assertRaises(TrackbackError, postTrackback, 'http://localhost:8000/test/emptyFeed/', '')

        postTrackback('http://localhost:8000/test/trackbackOk/', '')
        
        self.assertRaises(TrackbackError, postTrackback, 'http://localhost:8000/test/trackbackError/', '')
        
        try:
            postTrackback('http://localhost:8000/test/trackbackError/', '')
        except TrackbackError, e:
            self.assert_('1' in str(e))
            self.assert_('Missing URL' in str(e))


    def test_discover(self):
        # RDF link
        tb, data = discover('http://localhost:8000/test/simpleHomePage/')
        self.assertEquals('http://localhost:8000/test/simpleHomePage/trackback/', tb)
        
        # <a> with rel="trackback"
        tb, data = discover('', '<a rel="trackback" href="http://www.ryanblock.com/2007/08/an-open-letter/tb/">TrackBack? this entry</a>')
        self.assertEquals('http://www.ryanblock.com/2007/08/an-open-letter/tb/', tb)
            
        tb, data = discover('', 
        '''<a rel="trackback" href="http://www.ryanblock.com/2007/08/an-open-letter/tb/">TrackBack? this entry</a>
           <a rel="trackback" href="http://www.ryanblock.com/2007/08/another-letter/tb/">TrackBack? this entry</a>
        ''')
        self.assertEquals(None, tb)
            
        # <a> with trackback
        # Just one
        tb, data = discover('', '<a href="http://www.ryanblock.com/2007/08/an-open-letter/trackback/">TrackBack? this entry</a>')
        self.assertEquals('http://www.ryanblock.com/2007/08/an-open-letter/trackback/', tb)
            
        # Two identical
        tb, data = discover('',
        '''<a href="http://www.ryanblock.com/2007/08/an-open-letter/trackback/">TrackBack this entry</a>
           <a href="http://www.ryanblock.com/2007/08/an-open-letter/trackback/">TrackBack this entry</a>
        ''')
        self.assertEquals('http://www.ryanblock.com/2007/08/an-open-letter/trackback/', tb)
        
        # Two different links -> ambiguous -> no trackback
        tb, data = discover('',
        '''<a href="http://www.ryanblock.com/2007/08/an-open-letter/trackback/">TrackBack this entry</a>
           <a href="http://www.ryanblock.com/2007/08/another-letter/trackback/">TrackBack this entry</a>
        ''')
        self.assertEquals(None, tb)
        
        # Haloscan link
        tb, data = discover('',
        '''<a style="outline-color: invert; outline-style: dotted; outline-width: 1px; outline-offset: 0pt;" class="comment-link" href="http://www.haloscan.com/tb/spreeeziee/6205091737292372171/" onclick='HaloScanTB("6205091737292372171");return false;'>
        <script type="text/javascript">postCountTB('6205091737292372171');</script>Trackback (1)
        </a>''')
        self.assertEquals("http://www.haloscan.com/tb/spreeeziee/6205091737292372171/", tb)
        
        # Links in plain text
        tb, data = discover('',
        '''Not a trackback: http://www.example.com
           Trackback URL: http://www.ryanblock.com/2007/08/an-open-letter/trackback/
        ''')
        self.assertEquals('http://www.ryanblock.com/2007/08/an-open-letter/trackback/', tb)
            
        tb, data = discover('',
        '''Not a trackback: http://www.example.com
           Trackback URL: http://www.ryanblock.com/2007/08/an-open-letter/trackback/
           Trackback URL: http://www.ryanblock.com/2007/08/another-letter/trackback/
        ''')
        self.assertEquals(None, tb)
            

            
    def setUp(self):
        pass

    
if __name__ == '__main__':
    unittest.main()