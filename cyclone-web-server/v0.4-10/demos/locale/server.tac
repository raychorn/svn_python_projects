#!/usr/bin/env twistd -ny
# coding: utf-8

import os.path
import cyclone.web
import cyclone.locale
from twisted.application import service, internet

class BaseHandler(cyclone.web.RequestHandler):
    def get_user_locale(self):
        # could get it from self.current_user.prefs["language"]
        # or any other cookie
        return None


class IndexHandler(BaseHandler):
    def get(self, apples=1):
        self.render("index.html",
            apples=apples,
            locale=self.locale.code,
            languages=cyclone.locale.get_supported_locales())

    def post(self):
        language = self.get_argument("language")
        apples = self.get_argument("apples")
        apples = apples.isdigit() and int(apples) or 1

        # set self._locale OR use get_user_locale()
        self._locale = cyclone.locale.get(language)

        # render html
        self.get(apples)


class Application(cyclone.web.Application):
    def __init__(self):
        # load locales
        cwd = os.path.dirname(__file__)
        cyclone.locale.load_translations(os.path.join(cwd, "locale"), "mytest")

        # uri handlers
        handlers = [
            (r"/", IndexHandler),
        ]

        # app settings
        settings = dict(
            template_path=os.path.join(cwd, "templates"),
        )

        # init app
        cyclone.web.Application.__init__(self, handlers, **settings)

application = service.Application("cyclone_locale_demo")
srv = internet.TCPServer(8888, Application())
srv.setServiceParent(application)
