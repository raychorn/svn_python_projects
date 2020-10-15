#!/usr/bin/env python

''' purpose : Intercepting messages that pass around nova-services directly from rabbitmq
author: Prosunjit Biswas
Date: Nov 8, 2013

'''

import pika
import sys

global messageno
messageno = 0

parameters = pika.URLParameters('amqp://admin:password@localhost:5672/%2F')
connection = pika.BlockingConnection(parameters)

exchange_name="nova"
queue_name = "simple_queue"
binding_key = "#"

channel = connection.channel()
channel.exchange_declare(exchange = exchange_name, type='topic')

result = channel.queue_declare(exclusive=True)
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)

print ' [*] Waiting for logs. To exit press CTRL+C'

def callback(ch, method, properties, body):
    global messageno
    messageno = messageno + 1
    print "\n\n"
    print ("----------------{}th message -----------------\n".format(messageno))
    print " [x] %r:%r" % (method.routing_key, body,)
