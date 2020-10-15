"""
As part of your screening, please provide a sample project for review:
1. The project should provide a RESTful web service.
  a. The web service accepts a number, n, as input and returns the first n Fibonacci numbers, starting from 0. I.e. given n = 5, appropriate output would represent the sequence "0 1 1 2 3".
  b. Given a negative number, it will respond with an appropriate error.
  c. The service should return the values in an XML document.  Create an XSD that can be used to validate the output.

<fibonacci>
            <value index="0">0</value>
            <value index="1">1</value>
            <value index="2">1</value>
            <value index="3">2</value>
</fibonacci>

2. Set this project up on Github.  Include whatever instructions are necessary to build and deploy/run the project, where "deploy/run" means the web service is accepting requests and responding to them as appropriate.
3. While this project is admittedly trivial, approach it as representing a more complex problem that you'll have to put into production and maintain for 5 years.
"""
import sys
import web

import Queue
import threading

urls = (
    '/', 'Index',
    '/(\d+)', 'View',
    '/XML/(\d+)', 'ViewXML',
)

# Templates
render = web.template.render('templates', base='base')

web.template.Template.globals.update(dict(
    datestr=web.datestr,
    render=render
))


def notfound():
    return web.notfound("Sorry, the page you were looking for was not found.  This message may be seen whenever someone tries to issue a negative number as part of the REST URL Signature and this is just not allowed at this time.")


class Index:

    def GET(self):
        """ Show page """
        return render.index()


class View:

    def GET(self, num):
        from utils import get_fibonacci_nums
        items = get_fibonacci_nums(num)
        return render.view(items)


class ViewXML:

    def __render__(self, values):
        from utils import dict2xml
        __data__ = {}
        __data__['fibonacci'] = {}
        count = 0
        for v in values:
            __data__['fibonacci']['value'] = v
            #__items__.append('<value index="%s">%s</value>' % (count,v))
            count += 1
        xml = dict2xml(__data__)
        return xml.display()

    def GET(self, num):
        from utils import get_fibonacci_nums
        items = get_fibonacci_nums(num)
        web.header('Content-Type', 'application/xml')
        return self.__render__(items)

app = web.application(urls, globals())
app.notfound = notfound

def unit_tests():
    import time
    import urllib2
    from xml.dom import minidom

    def begin_tests(url):
        print url
        foo = urllib2.urlopen(url).read()
        print 'Test #1'
        try:
            assert foo == '<fibonacci><value index="0">0</value><value index="1">1</value><value index="2">1</value><value index="3">2</value><value index="4">3</value></fibonacci>', 'ERROR: Test #1 FAILED !!!'
            try:
                print 'Test #2 - Determine if the XML can be parsed ?!?',
                xmldoc = minidom.parseString(foo)
                print ' PASSED !!!  Able to parse the XML so it must be well formed or so the theory goes at this point.'
                nodes = xmldoc.firstChild.childNodes
                print 'Test #3 - Determine if the XML contains 5 nodes ?!?'
                assert len(nodes) == 5, 'ERROR: Test #3 FAILED !!!'
                print 'Unit Test Recap - (1) The XML was exactly as expected AND it is seemingly well-formed therfore all is right in the universe.'
            except Exception, ex:
                print " FAILED (Reason: %s) !!!  Not-Able to parse the XML so it must NOT be all that well formed, and that's just too bad, isn't it ?" % (ex)
        except:
            pass
        print foo
        print 'Unit test(s) are done !!!'
        try:
            t._Thread__stop()
            print 'Thread Terminated !!!'
        except:
            pass

    if (len(sys.argv) > 1):
        port = sys.argv[1]
    else:
        port = 19999
    url = 'http://127.0.0.1:%s/XML/5' % (port)
    t = threading.Thread(target=begin_tests, args=[url])
    t.daemon = False
    print 'Unit Test(s) begin in 5 secs...'
    time.sleep(5)
    t.start()

if __name__ == '__main__':
    def begin_web_server():
        app.run()

    t = threading.Thread(target=begin_web_server)
    t.daemon = False
    t.start()

    unit_tests()
