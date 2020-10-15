#!/usr/bin/env python
# vim:ts=4:sw=4:et
# -*- coding: utf-8 -*-
# $Id: decoroute.py,v 77622ca1b640 2008/06/13 21:24:50 vsevolod $
#
# Pattern Matching based WSGI-enabled URL routing tool.
# Actual version on http://pypi.python.org/pypi/decoroute
# (C) 2008 by Vsevolod S. Balashov <vsevolod@balashov.name>
# under terms of GNU LGPL v2.1 http://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt

__author__ = "Vsevolod Balashov"
__email__ = "vsevolod at balashov dot name"

import re
from sets import ImmutableSet
import wsgistraw

__all__ = ['NotFound', 'App']

class NotFound(Exception):
    pass

_pattern_re = re.compile(r'''
    ([^<]+)                     # static rule data
    (?:<
        ([a-zA-Z][a-zA-Z0-9_]*) # variable name
        \:
        ([^>]+)                 # regexp constraint
    >)?
''', re.VERBOSE)

def pattern2regexp(pattern, f, s = lambda x: re.escape(x)):
    def parser():
        for t in _pattern_re.findall(pattern):
            yield s(t[0])
            if t[1] != '':
                yield f(t[1], t[2])
    return parser()

make_url_for = lambda p: ''.join(pattern2regexp(p, lambda v, r: '%%(%s)s' % v, lambda s: s))
make_variables = lambda p: filter(lambda x: x, pattern2regexp(p, lambda v, r: v, lambda s: None))
make_pattern = lambda p: r''.join(pattern2regexp(p, lambda v, r: r'(?P<%s>%s)' % (v, r)))
make_selector_fragment = lambda p: r''.join(pattern2regexp(p, lambda v, r: r'(?:%s)' % r))
make_selector = lambda i: r'(^%s$)' % r'$)|(^'.join(map(make_selector_fragment, i))

class UrlMap(object):
    def __init__(self):
        self._endpoints = {}
        self._patterns = {}
        self._pattern_selector = re.compile(make_selector(self._patterns.iterkeys()))
    
    def add(self, pattern, endpoint, **kw):
        if self._patterns.has_key(pattern):
            raise Exception('duplicate pattern', pattern)
        self._endpoints[(endpoint, ImmutableSet(make_variables(pattern)))] = make_url_for(pattern)
        self._patterns[pattern] = (re.compile(make_pattern(pattern)), endpoint, kw)
        self._pattern_selector = re.compile(make_selector(self._patterns.iterkeys()))
    
    def route(self, url):
        try:
            p = self._patterns.values()[re.match(self._pattern_selector, url).lastindex - 1]
            d = re.match(p[0], url).groupdict().copy()
            d.update(p[2])
            return p[1], d
        except:
            raise NotFound('route not found', url)
    
    def url_for(self, endpoint, **kw):
        return self._endpoints[(endpoint, ImmutableSet(kw.keys()))] % kw

class App(object):
    def __init__(self, prefix = '', key = 'decoroute.app'):
        self.map = UrlMap()
        self._prefix = (prefix, re.compile(r'^%s' % re.escape(prefix)))
        self._key = key
        self._not_found = lambda e: ('404 NOT FOUND', [("Content-Type", "text/plain")], [''])
        self._render = lambda x: x
    
    def route(self, env):
        env[self._key] = self
        path, n = self._prefix[1].subn('', env['PATH_INFO'])
        if n == 1:
            endpoint, kw = self.map.route(path)
        else:
            raise NotFound()
        return endpoint(env, **kw)
    
    def url_for(self, endpoint, **kw):
        return self._prefix[0] + self.map.url_for(endpoint, **kw)
    
    @wsgistraw.app
    def __call__(self, env):
        try:
            return self._render(self.route(env))
        except NotFound:
            return self._render(self._not_found(env))
    
    def expose(self, pattern, **kw):
        def decorate(f):
            self.map.add(pattern, f, **kw)
            return f
        return decorate
    
    def not_found(self):
        def decorate(f):
            self._not_found = f
            return f
        return decorate
    
    def render(self):
        def decorate(f):
            self._render = f
            return f
        return decorate
