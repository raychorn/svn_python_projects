#!/usr/bin/env python
# coding: utf-8
#
# Copyright 2010 Alexandre Fiori
# based on the original Tornado by Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import cyclone.web
import cyclone.redis

import base64
import functools
from twisted.python import log
from twisted.internet import defer
from twisted.application import service, internet


def BasicAuth(method):
    @defer.inlineCallbacks
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            auth_type, auth_data = self.request.headers["Authorization"].split()
            assert auth_type == "Basic"
            usr, pwd = base64.b64decode(auth_data).split(":", 1)
        except:
            raise cyclone.web.HTTPAuthenticationRequired("Basic", realm="Restricted Access")

        try:
            # key=cyclone:username, value=password
            password = yield self.settings.redis.get("cyclone:%s" % usr)
        except Exception, e:
            log.err("redis failed to get('cyclone:%s'): %s" % (usr, e))
            raise cyclone.web.HTTPError(503, "Service Unavailable")

        if pwd != password:
            raise cyclone.web.HTTPError(401, "Unauthorized")

        defer.returnValue(method(self, *args, **kwargs))
        #yield defer.maybeDeferred(method, self, *args, **kwargs)
    return wrapper


class IndexHandler(cyclone.web.RequestHandler):
    @BasicAuth
    def get(self):
        self.finish("ok, but now you have to close the browser to logout\r\n")


class UsersHandler(cyclone.web.RequestHandler):
    # @BasicAuth
    @defer.inlineCallbacks
    def post(self, username):
        password = self.get_argument("p")
        try:
            yield self.settings.redis.set("cyclone:%s" % username, p.encode("utf-8"))
        except Exception, e:
            log.err("redis failed to set('cyclone:%s', '%s'): %s" % (username, repr(password), e))
            cyclone.web.HTTPError(503)
        self.finish("new username=%s, password=%s\r\n" % (username, password))


class Application(cyclone.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/u/(.+)", UsersHandler),
        ]

        redis = cyclone.redis.lazyRedisConnectionPool()
        #redis = cyclone.redis.lazyRedisConnectionPool(host, port, reconnect=True, pool_size=20, db=13)

        cyclone.web.Application.__init__(self, handlers, redis=redis)


application = service.Application("redis-basic")
internet.TCPServer(8888, Application(),
    interface="127.0.0.1").setServiceParent(application)
