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

import hashlib
import txmongo
from twisted.internet import defer, reactor

@defer.inlineCallbacks
def main():
    mongo = yield txmongo.MongoConnection()

    admin = yield mongo.mydb.users.find_one({"u":"cyclone"})
    if admin:
        print "user 'cyclone' with password 'cyclone' already exists: %s" % admin["_id"]
    else:
        objid = yield mongo.mydb.users.insert({"u":"cyclone", "p":hashlib.md5("cyclone").hexdigest()}, safe=True)
        print "user 'cyclone' with password 'cyclone' has been created: %s" % objid

if __name__ == "__main__":
    main().addCallback(lambda ign: reactor.stop())
    reactor.run()
