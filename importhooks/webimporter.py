"""
Stupid Python Trick - import modules over the web.
Author: Christian Wyglendowski
License: MIT (http://dowski.com/mit.txt)

Note: This works to a degree however the challenge comes from instances of import within the modules being imported that do not use
the WebImporter method for doing imports.

http://www.mail-archive.com/cx-freeze-users@lists.sourceforge.net/msg00484.html
"""

import imp
import os
import sys
import marshal
import requests

class WebImporterImportError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return '%s' % (self.message)

def register_domain(name,alias=None,proxies=None):
    WebImporter.registered_domains.add(name)
    if (alias):
        WebImporter.aliases[name] = alias
    if (proxies):
        WebImporter.proxies = proxies
    parts = reversed(name.split('.'))
    whole = []
    for part in parts:
        whole.append(part)
        WebImporter.domain_modules.add(".".join(whole))

class WebImporter(object):
    domain_modules = set()
    registered_domains = set()
    aliases = {}
    proxies = {}
    __fpath__ = None
    __i__ = -1

    def find_module(self, fullname, path=None):
        if fullname in self.domain_modules:
            return self
        if fullname.rsplit('.')[0] not in self.domain_modules:
            return None
        try:
            r = self._do_request(fullname, method="HEAD")
        except ValueError:
            return None
        else:
            if (r):
                if (WebImporter.__fpath__):
                    if (os.path.exists(r)):
                        return self
                    raise WebImporterImportError('Cannot import "%s" from "%s" due to cannot find file.' % (fullname,r))
                r.close()
                if r.status == 200:
                    return self
                else:
                    raise WebImporterImportError('Cannot import "%s" from "http://%s/%s" due to status of %s.' % (fullname,self.__host__,self.__path__,r.status))
        return None

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        mod = imp.new_module(fullname)
        mod.__loader__ = self
        sys.modules[fullname] = mod
        __code__ = None
        if fullname not in self.domain_modules:
            if (os.path.exists(self.__host__)):
                fp = os.sep.join([self.__host__,self.__path__])
                if (os.path.exists(fp)):
                    mod.__file__ = fp
                    try:
                        fhand = open(mod.__file__,'rb')
                        __code__ = fhand.read()
                        fhand.close()
                    except Exception, details:
                        print >>sys.stderr, _utils.formattedException(details=details)
            else:
                url = "http://%s%s" % (self.__host__,self.__path__)
                mod.__file__ = url
                try:
                    r = requests.get('http://%s/%s' % (self.__host__,self.__path__))
                    if (r.status_code == 200):
                        __code__ = r.content
                        assert response.status == 200
                        response.close()
                except Exception, details:
                    print >>sys.stderr, _utils.formattedException(details=details)
            if (__code__):
                try:
                    exec __code__ in mod.__dict__
                except TypeError:
                    magic = __code__[:4]
                    if magic != imp.get_magic():
                        raise ImportError, "Bad magic number in %s" % url
                    mod.code = marshal.loads(__code__[8:])
                except Exception, details:
                    print >>sys.stderr, _utils.formattedException(details=details)
        else:
            mod.__file__ = "[fake module %r]" % fullname
            mod.__path__ = []
        return mod

    def _do_request(self, fullname, method="GET"):
        tuples = []
        
        tuples.append(self._get_host_and_path(fullname,is_module=True if (not fullname.endswith('.py')) else False,use_alias=True if (WebImporter.aliases) else False))
        tuples.append(self._get_host_and_path(fullname,is_module=True if (not fullname.endswith('.py')) else False,use_alias=True if (WebImporter.aliases) else False,is_sourceless=True))

        if (WebImporter.__i__ > -1):
            t = tuples[WebImporter.__i__]
            del tuples[WebImporter.__i__]
            tuples.insert(0,t)
        for i in xrange(len(tuples)):
            h,p = tuples[i]
            if (os.path.exists(WebImporter.__fpath__)):
                fpath = os.sep.join([WebImporter.__fpath__,p])
                if (os.path.exists(fpath)):
                    self.__host__ = WebImporter.__fpath__
                    self.__path__ = p
                    return fpath
                return None
            else:
                url = 'http://%s%s' % (h,p)
                print 'url=%s' % (url)
                try:
                    if (WebImporter.proxies):
                        r = requests.get(url,proxies=WebImporter.proxies)
                    else:
                        r = requests.get(url)
                    if (r.status_code == 200):
                        self.__i__ = i
                        self.__host__, self.__path__ = tuples[i]
                        return r
                except Exception, details:
                    #print >>sys.stderr, _utils.formattedException(details=details)
                    print 'Failed !!!'
        return None

    def _get_host_and_path(self, fullname, is_sourceless=False, is_module=False, use_alias=False):
        toks = fullname.split('.')
        host = []
        rest = []
        for t in toks:
            if (len(rest) == 0):
                host.append(t)
                _host = '.'.join(host)
                if (not _host in self.domain_modules):
                    rest.append(toks.pop())
                    del host[-1]
            else:
                rest.append(t)
        if (is_module):
            rest.append('__init__')
        toks = [h for h in host]
        toks.reverse()
        h = ".".join(toks)
        if (WebImporter.aliases.has_key(h) and os.path.exists(WebImporter.aliases[h])):
            WebImporter.__fpath__ = h = WebImporter.aliases[h]
            path = "%s.py%s" % (os.sep.join(rest),'c' if (is_sourceless) else '')
        else:
            path = "/%s.py%s" % ('/'.join(rest),'c' if (is_sourceless) else '')
        return h, path

sys.meta_path = [WebImporter()]

if (__name__ == '__main__'):
    from vyperlogix.misc import _utils
    #import webimport
    #webimport.register_domain('dowski.com')
    proxies = {"http": "socks5://127.0.0.1:8888"}
    #register_domain('cdn.python.vyperlogix.com',alias='cdn-python.s3-website-us-east-1.amazonaws.com') #,proxies=proxies)
    register_domain('cdn.python.vyperlogix.com',alias=r'J:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01') #,proxies=proxies)
    try:
        from com.vyperlogix.python.cdn import vyperlogix
        pass
    except ImportError, details:
        print >> sys.stderr, _utils.formattedException(details=details)
    except WebImporterImportError, details:
        print >> sys.stderr, _utils.formattedException(details=details)
