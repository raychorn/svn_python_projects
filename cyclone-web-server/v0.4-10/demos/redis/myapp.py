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

from twisted.python import log
from twisted.internet import defer, reactor

from collections import defaultdict

import cyclone.web
import cyclone.escape

import cyclone.redis
from cyclone.redis.protocol import SubscriberProtocol


class textHandler(cyclone.web.RequestHandler):
    @defer.inlineCallbacks
    def get(self, key):
        try:
            data = yield self.settings.redis.get(key)
        except Exception, e:
            log.msg("redis failed to get('%s'): %s" % (key, e))
            raise cyclone.web.HTTPError(503)

        self.set_header("Content-Type", "text/plain")
        self.finish((data or "")+"\r\n")
 
    @defer.inlineCallbacks
    def post(self, key):
        value = self.get_argument("value")
        try:
            yield self.settings.redis.set(key, value)
        except Exception, e:
            log.msg("redis failed to set('%s', '%s'): %s" % (key, data, e))
            raise cyclone.web.HTTPError(503)

        self.set_header("Content-Type", "application/json")
        self.finish(cyclone.escape.json_encode({key: value})+"\r\n")

    @defer.inlineCallbacks
    def delete(self, key):
        try:
            yield self.settings.redis.delete(key)
        except Exception, e:
            log.msg("redis failed to del('%s'): %s" % (key, e))
            raise cyclone.web.HTTPError(503)

        self.set_header("Content-Type", "text/plain")
        self.finish("OK\r\n")


class queueHandler(cyclone.web.RequestHandler):
    @cyclone.web.asynchronous
    def get(self, channels):
        try:
            channels = channels.split(",")
        except Exception, e:
            log.msg("cannot split channel names")
            raise cyclone.web.HTTPError(503)

        self.set_header("Content-Type", "text/plain")
        self.notifyFinish().addCallback(self.remove_peer)

        for channel in channels:
            if "*" in channel and self.settings.queue.current_connection is not None:
                self.settings.queue.current_connection.psubscribe(channel)
            else:
                self.settings.queue.current_connection.subscribe(channel)

            self.settings.queue.peers[channel].append(self)
            self.write("subscribed: %s\r\n" % channel)
            self.flush()

    def remove_peer(self, ignore):
        for chan, peers in self.settings.queue.peers.items():
            try:
                members = self.settings.queue.peers[chan]
                members.pop(members.index(self))
            except:
                pass
            else:
                if not members and self.settings.queue.current_connection is not None:
                    if "*" in chan:
                        self.settings.queue.current_connection.punsubscribe(chan)
                    else:
                        self.settings.queue.current_connection.unsubscribe(chan)
                

    @defer.inlineCallbacks
    def post(self, channel):
        message = self.get_argument("message")

        if self.settings.queue.current_connection is None:
            raise cyclone.web.HTTPError(503)

        try:
            n = yield self.settings.redis.publish(channel, message.encode("utf-8"))
        except Exception, e:
            log.msg("redis failed to publish('%s', '%s'): %s" % (channel, repr(message), e))
            raise cyclone.web.HTTPError(503)

        self.set_header("Content-Type", "text/plain")
        self.finish("OK %d\r\n" % n)


class QueueProtocol(SubscriberProtocol):
    def messageReceived(self, pattern, channel, message):
        if pattern:
            peers = self.factory.peers[pattern]
        else:
            peers = self.factory.peers[channel]

        for peer in peers:
            peer.write("%s: %s\r\n" % (channel, message))
            peer.flush()

    def connectionMade(self):
        self.factory.current_connection = self
        for chan in self.factory.peers:
            if "*" in chan:
                self.psubscribe(chan)
            else:
                self.subscribe(chan)

    def connectionLost(self, reason):
        self.factory.current_connection = None


class QueueFactory(cyclone.redis.SubscriberFactory):
    maxDelay = 20
    continueTrying = True # auto reconnect
    protocol = QueueProtocol
    peers = defaultdict(lambda: [])
    current_connection = None


class Application(cyclone.web.Application):
    def __init__(self, redis_host, redis_port, redis_pool, redis_db):
        handlers = [
            (r"/text/(.+)", textHandler),
            (r"/queue/(.+)", queueHandler),
        ]

        settings = {
            "redis": cyclone.redis.lazyRedisConnectionPool(
                redis_host, redis_port, pool_size=redis_pool, db=redis_db),
            "queue": QueueFactory(),
        }

        reactor.connectTCP(redis_host, redis_port, settings["queue"])
        cyclone.web.Application.__init__(self, handlers, **settings)
