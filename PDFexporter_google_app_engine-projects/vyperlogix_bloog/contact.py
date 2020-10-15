# The MIT License
# 
# Copyright (c) 2008 William T. Katz
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
contact.py
This module provides a simple form for entering a message and the
handlers for receiving the message through a HTTP POST.
TODO: Make this an Ajax form with built-in captcha.
"""
__author__ = 'William T. Katz'

from google.appengine.api import mail

import restful
import view
import config
import time
import string

RANDOM_TOKEN = '08yzek30krn4l' + config.blog['root_url']

class ContactHandler(restful.Controller):
    def get(self):
        view.ViewPage(cache_time=300).render(self, {'token': RANDOM_TOKEN, 'curtime': time.time()})

    def post(self):
        if self.request.get('token') != RANDOM_TOKEN or time.time() - string.atof(self.request.get('curtime')) < 2.0:
            self.error(403)

        reply_to = self.request.get('author') + ' <' + self.request.get('email') + '>'
        mail.send_mail(
            sender = config.blog['email'],
            reply_to = reply_to,
            to = config.blog['email'],
            subject = self.request.get('subject'),
            body = self.request.get('message')
        )

        view.ViewPage(cache_time=36000).render(self)