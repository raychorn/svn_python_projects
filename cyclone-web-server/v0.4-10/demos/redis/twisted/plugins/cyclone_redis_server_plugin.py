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

from zope.interface import implements
from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application import service, internet

import myapp

class Options(usage.Options):
    optParameters = [
        ["redis-host", "", "127.0.0.1", "hostname or ip address of the redis server"],
        ["redis-port", "", 6379, "port number of the redis server"],
        ["redis-pool", "", 10, "connection pool size"],
        ["redis-db", "", 0, "redis database"],
        ["port", "p", 8888, "port number to listen on"],
        ["listen", "l", "127.0.0.1", "interface to listen on"],
    ]

class ServiceMaker(object):
    implements(service.IServiceMaker, IPlugin)
    tapname = "cyclone_redis_server"
    description = "cyclone redis server demo"
    options = Options

    def makeService(self, options):
        return internet.TCPServer(options["port"],
            myapp.Application(options["redis-host"], int(options["redis-port"]),
                int(options["redis-pool"]), int(options["redis-db"])),
            interface=options["listen"])

serviceMaker = ServiceMaker()
