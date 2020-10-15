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

import base64
import functools
from twisted.application import service, internet

def BasicAuth(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            auth_type, auth_data = self.request.headers["Authorization"].split()
            assert auth_type == "Basic"
            usr, pwd = base64.b64decode(auth_data).split(":", 1)
            assert usr == "user@domain"
            assert pwd == "password"
        except:
            raise cyclone.web.HTTPAuthenticationRequired
        else:
            return method(self, *args, **kwargs)
    return wrapper


class IndexHandler(cyclone.web.RequestHandler):
    @BasicAuth
    def get(self):
        self.finish("ok\r\n")


class Application(cyclone.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
        ]

        cyclone.web.Application.__init__(self, handlers)


application = service.Application("auth-basic")
internet.TCPServer(8888, Application(),
    interface="127.0.0.1").setServiceParent(application)
