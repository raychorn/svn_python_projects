from kombu.mixins import ConsumerMixin
from kombu.log import get_logger
from kombu import Queue, Exchange

import json

logger = get_logger(__name__)


class Worker(ConsumerMixin):
    task_queue = Queue('notifications.info', Exchange('nova', 'topic', durable=False), durable=False)

    def __init__(self, connection, notifications={}):
        self.connection = connection
        self.notifications = notifications
        if (options.log):
            logger.debug('Worker connection: %s, Notifications: %s' % (connection,notifications))

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=[self.task_queue],
                         accept=['json'],
                         callbacks=[self.process_task])]

    def process_task(self, body, message):
        try:
            __data__ = json.loads(body)
            for k,v in self.notifications.iteritems():
                if (k):
                    if (__data__.has_key(k)):
                        print("NOTIFICATION: %r" % (body, ))
        except Exception, ex:
            logger.exception(ex)
        if (options.log):
            logger.debug('message: %s, body: %s' % (message,body))
        message.ack()

if (__name__ == '__main__'):
    from kombu import Connection
    from kombu.utils.debug import setup_logging
    # setup root logger
    setup_logging(loglevel='DEBUG', loggers=[''])

    from optparse import OptionParser
    
    parser = OptionParser("usage: %prog [options]")
    parser.add_option("-u", "--username",action="store", help="username for AMQP", type="string", dest="username")
    parser.add_option("-p", "--password",action="store", help="password for AMQP", type="string", dest="password")
    parser.add_option("-a", "--address",action="store", help="address:port for AMQP", type="string", dest="address")
    parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
    parser.add_option("-n", "--notification",action="store", help="notice certain nova notifications (vm creation via event_type=compute.instance.create.start and event_type=compute.instance.create.end) also disables -l option.", type="string", dest="notification")
    parser.add_option('-l', '--log', dest='log', help="log", action="store_true")
    
    # "event_type=compute.instance.create.start"
    # "event_type=compute.instance.create.end"
    
    options, args = parser.parse_args()
    
    if (options.log) and (not options.notification):
        import logging
        fh = logging.FileHandler('./kombu.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        print 'Logging to "%s".' % (fh.stream.name)
    else:
        options.log = None
        
    __username__ = '__guest'
    __password__ = '__peekab00'
    __address__ = '__localhost'
    __port__ = '__5672'
    
    if (options.username):
        __username__ = options.username
    if (options.log):
        logger.info('username is "%s".' % (__username__))
    
    if (options.password):
        __password__ = options.password
    if (options.log):
        logger.info('password is "%s".' % (__password__))
        
    if (options.address):
        toks = options.address.split(':')
        __address__ = toks[0]
        if (len(toks) == 2):
            __port__ = toks[-1]
    if (options.log):
        logger.info('address is "%s".' % (__address__))
    if (options.log):
        logger.info('port is "%s".' % (__port__))

    __notifications__ = {}
    if (options.notification):
        toks = options.notification.split('=')
        __notifications__[toks[0]] = toks[-1]
            
    with Connection('amqp://%s:%s@%s:%s/%%2F' % (__username__,__password__,__address__,__port__)) as conn:
        try:
            print(conn)
            if (options.log):
                logger.debug('Connection: %s' % (conn))
            worker = Worker(conn,__notifications__)
            worker.run()
        except KeyboardInterrupt:
            print('bye bye')
