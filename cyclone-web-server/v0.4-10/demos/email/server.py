#!/usr/bin/env twistd -ny
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
import cyclone.mail
from twisted.internet import defer
from twisted.application import service, internet

class EmailHandler(cyclone.web.RequestHandler):
    @defer.inlineCallbacks
    def post(self):
        to_addrs = self.get_argument("to_addrs").split(",")
        subject = self.get_argument("subject")
        message = self.get_argument("message")
        content_type = self.get_argument("content_type")

        # message may also be an html template
        # message = self.render_string("email.html", key=value, ...)

        msg = cyclone.mail.Message(
            from_addr="your@email.com",
            to_addrs=to_addrs,
            subject=subject,
            message=message,
            mime=content_type, # optional, default text/plain
            charset="utf-8")   # optional, default utf-8

        msg.attach("./static/me.png", mime="image/png")
        msg.attach("./static/info.txt", mime="text/plain", charset="utf-8")
        msg.attach("fake.txt", mime="text/plain", charset="utf-8", content="some text here")

        try:
            result = yield cyclone.mail.sendmail(self.settings.email, msg)
            self.finish(str(result))
        except Exception, e:
            self.finish(str(e))


class EmailApplication(cyclone.web.Application):
    def __init__(self):
        handlers = [
            (r"/", cyclone.web.RedirectHandler, {"url": "/static/index.html"}),
            (r"/sendmail", EmailHandler),
        ]

        email_settings = {
            "host": "smtp.gmail.com",   # mandatory
            "port": 587,                # optional, default 25 or 587 for TLS
            "tls": True,                # optional, default False
            "username": "user",         # optional
            "password": "secret",       # optional
        }

        settings = {
            "static_path": "./static",
            "template_path": "./template",
            "email": email_settings,
        }

        cyclone.web.Application.__init__(self, handlers, **settings)

application = service.Application("cyclone")
internet.TCPServer(8888, EmailApplication(),
    interface="0.0.0.0").setServiceParent(application)
