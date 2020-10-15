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

import sys
import cyclone.web
import cyclone.auth
import cyclone.escape
from twisted.python import log
from twisted.internet import reactor


class Application(cyclone.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/auth/login", AuthHandler),
        ]
        settings = dict(
            cookie_secret="32oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
        )
        cyclone.web.Application.__init__(self, handlers, **settings)


class BaseHandler(cyclone.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return cyclone.escape.json_decode(user_json)


class MainHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        name = cyclone.escape.xhtml_escape(self.current_user["name"])
        self.write("Hello, " + name)


class AuthHandler(BaseHandler, cyclone.auth.GoogleMixin):
    @cyclone.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self._on_auth)
            return
        self.authenticate_redirect()
    
    def _on_auth(self, user):
        if not user:
            raise cyclone.web.HTTPError(500, "Google auth failed")
        self.set_secure_cookie("user", cyclone.escape.json_encode(user))
        self.redirect("/")


def main():
    reactor.listenTCP(8888, Application())
    reactor.run()

if __name__ == "__main__":
    log.startLogging(sys.stdout)
    main()
