''' Copyright (c) 2006-2007, PreFab Software Inc. '''


import datetime, unittest
import blogcosm.django_tst_setup
from django.contrib.auth.models import User
from blogmaker.blog.models import Entry, TrackbackStatus

class EntryTest(unittest.TestCase):
    def test_entry(self):
        # Test link finding
        text = '''<a href="http://www.example.com">One link</a>
more &quot;text&quot;<a href="/profile/foo">Internal link</a>
<a 
href='http://www.example.com/foo'>This one has 
<b>mixed</b>content</a>
<a href="#foo">anchor</a>
'''
        entry = Entry(body=text)
        
        self.assertEquals(set(["http://www.example.com", 'http://www.example.com/foo']), entry.links)
        
        # Test excerpt
        # Where does the whitespace come from? markdown, apparently...
        self.assertEquals('''One link\n   more "text"Internal link\n   This one has \n   mixedcontent\n   anchor\n''', entry.excerpt)

        # Test markdown links
        text = '''[One link](http://www.example.com)
        more text [Internal link](/profile/foo)
        [This one has 
        *mixed* content](http://www.example.com/foo "Title") and a title.
        <a href="#foo">anchor</a>
'''
        entry = Entry(body=text)
        
        self.assertEquals(set(["http://www.example.com", 'http://www.example.com/foo']), entry.links)

        # Test duplicate links
        text = '''<a href="http://www.example.com">One link</a>
        [duplicate link](http://www.example.com)
        '''
        entry = Entry(body=text)
        self.assertEquals(set(["http://www.example.com"]), entry.links)

        # Test excerpt with UTF-8 text
        entry = Entry(body='Amazon&#8217;s Kindle press release: The Kindle e-reader ISN\xe2\x80\x99T ugly?')
        self.assertEquals(u'Amazon\u2019s Kindle press release: The Kindle e-reader ISN\u2019T ugly?\n', entry.excerpt)
        
    def test_trackbacks(self):
        Entry.objects.all().delete()
        TrackbackStatus.objects.all().delete()

        try:
            user = User.objects.get(username='test')
        except User.DoesNotExist:
            user = User(username='test', password='test')
            user.save()
        
        text = '''<a href='http://www.example.com/foo'>link</a>
        <a href='http://www.example.com/foo2'>link2</a>
        <a href='http://www.example.com/?foo2'>link2</a>
        <a href='http://www.example.com'>no path</a>
        <a href='http://www.example.com/'>no path</a>
        <a href='http://www.example.com/blog/'>blog path</a>
        <a href='http://www.quantcast.com/blogcosm.com'>excluded site</a>
'''
        entry = Entry(body=text, pub_date=datetime.date.today(), user_id=user.id)
        entry.save()
        
        # Saving the entry harvests trackback links for URLs with a path or query component
        self.assertEquals(3, entry.trackbacks.all().count())
        self.assertEquals(3, TrackbackStatus.objects.all().count())
        tbLinks = [ item['link'] for item in entry.trackbacks.all().values('link')]
        self.assert_('http://www.example.com/foo' in tbLinks)
        self.assert_('http://www.example.com/foo2' in tbLinks)
        self.assert_('http://www.example.com/?foo2' in tbLinks)
        
        # Unused trackbacks are deleted if the links are deleted from the entry
        tb = entry.trackbacks.get(link='http://www.example.com/foo')
        tb.status = 'Success'
        tb.save()
        
        entry.body = ''
        entry.save()
 
        self.assertEquals(1, entry.trackbacks.all().count())
        self.assertEquals(1, TrackbackStatus.objects.all().count())
        self.assertEquals('http://www.example.com/foo', entry.trackbacks.all()[0].link)
        
        user.delete()
        
    def setUp(self):
        pass

    
if __name__ == '__main__':
    unittest.main()