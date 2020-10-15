import re
import os, sys
import time
import socket,asyncore
import logging

# Design Notes:
#
#  List of Nodes to choose from.
#
# Incoming connects choose a Node then make the connection.
__regex_valid_ip__ = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
__regex_valid_ip_and_port__ = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):([0-9]{1,5})"

is_valid_ip = lambda value:re.compile(__regex_valid_ip__, re.MULTILINE).match(value) is not None
is_valid_ip_and_port = lambda value:re.compile(__regex_valid_ip_and_port__, re.MULTILINE).match(value) is not None

def is_ip_address_valid(ip):
    '''127.0.0.1 is the general form of an IP address'''
    if (is_valid_ip(ip) or is_valid_ip_and_port(ip)):
	if (is_valid_ip_and_port(ip)):
	    toks1 = ip.split(':')
	    toks2 = toks1[0].split('.')
	    return (len(toks2) == 4) and all([str(n).isdigit() for n in list(tuple(toks2+[toks1[-1]]))])
	elif (is_valid_ip(ip)):
	    toks = ip.split('.')
	    return (len(toks) == 4) and all([str(n).isdigit() for n in toks])
    return False

def make_number_valid_or_none(value,allow_float=True):
    value = str(value) if (value is not None) else value
    if (value and value.replace('.','').isdigit()):
	toks = value.split('.')
	if (len(toks) >= 2):
	    toks[1] = ''.join(toks[1:])
	    if (len(toks) > 2):
		del toks[2:]
	return float('.'.join(toks)) if (allow_float) else int(''.join(toks))
    return None

class ReverseProxy(asyncore.dispatcher):
    def __init__(self, ip, port, remotes=[],backlog=100,delay=None,isVerbose=False,logger=None):
        asyncore.dispatcher.__init__(self)
        self.__remote_addresses__ = []
        for remote in remotes:
            self.__remote_addresses__.append(remote)
        self.__remote_address_num__ = 0 if (len(self.__remote_addresses__) > 0) else -1
        self.__ip__ = ip
        self.__port__ = port
	self.__delay__ = make_number_valid_or_none(delay)
	self.__verbose__ = isVerbose
	self.__logger__ = logger
	info = ''
	if (self.delay):
	    info = 'delaying %s seconds' % (self.delay)
	msg = '%s is active %s.' % (str(self.__repr__()),info)
	if (self.logger):
	    self.logger.info(msg)
	else:
	    print >>sys.stdout, msg
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip,port))
        self.listen(backlog)
        
    def __repr__(self):
        return '<ReverseProxy> <%s:%s>' % (self.ip,self.port)

    def handle_accept(self):
        conn_addr = self.accept()
        if (conn_addr):
            conn, addr = conn_addr
            remote_ip = self.next_remote_address()
            if (remote_ip is not None):
                remote_addr = remote_ip.split(':')
		info = ''
		if (self.delay):
		    info = 'delaying %s seconds' % (self.delay)
		msg = '--- Connect <%s> to <%s> %s --- ' % (addr,remote_addr,info)
		if (self.logger):
		    self.logger.info(msg)
		else:
		    print >>sys.stdout, msg
                remoteip = remote_addr[0]
                remoteport = int(remote_addr[-1]) if (len(remote_addr) == 2) else -1
                if (is_ip_address_valid(remoteip)):
		    if (self.delay):
			time.sleep(self.delay)
                    sender(receiver(conn,isVerbose=self.__verbose__),remoteip,remoteport,isVerbose=self.__verbose__)
                else:
		    msg = 'Cannot form a connection to %s.' % (remote_addr)
		    if (self.logger):
			self.logger.warning(msg)
		    else:
			print >>sys.stderr, msg
            else:
		msg = 'Cannot form a connection for %s.' % (remote_ip)
		if (self.logger):
		    self.logger.warning(msg)
		else:
		    print >>sys.stderr, msg

    def ip():
        doc = "ip"
        def fget(self):
            return self.__ip__
        return locals()
    ip = property(**ip())

    def logger():
        doc = "logger"
        def fget(self):
            return self.__logger__
        return locals()
    logger = property(**logger())

    def delay():
        doc = "delay"
        def fget(self):
            return self.__delay__
        return locals()
    delay = property(**delay())

    def port():
        doc = "port"
        def fget(self):
            return self.__port__
        return locals()
    port = property(**port())

    def remote_addresses():
        doc = "remote_addresses"
        def fget(self):
            return self.__remote_addresses__
        return locals()
    remote_addresses = property(**remote_addresses())

    def remote_address_num():
        doc = "remote_address_num"
        def fget(self):
            return self.__remote_address_num__
        return locals()
    remote_address_num = property(**remote_address_num())

    def next_remote_address(self):
	if (self.__verbose__):
	    msg = '1. self.__remote_address_num__=%s' % (self.__remote_address_num__)
	    if (self.logger):
		self.logger.warning(msg)
	    else:
		print >>sys.stdout, msg
        if (self.__remote_address_num__ > -1):
            self.__remote_address_num__ += 1
	    if (self.__verbose__):
		msg = '2. self.__remote_address_num__=%s' % (self.__remote_address_num__)
		if (self.logger):
		    self.logger.warning(msg)
		else:
		    print >>sys.stdout, msg
            if (self.__remote_address_num__ > len(self.__remote_addresses__)):
                self.__remote_address_num__ = 0
	    if (self.__verbose__):
		msg = '3. self.__remote_addresses__=%s' % (self.__remote_addresses__)
		if (self.logger):
		    self.logger.warning(msg)
		else:
		    print >>sys.stdout, msg
            return self.__remote_addresses__[self.__remote_address_num__] if (self.__remote_address_num__ < len(self.__remote_addresses__)) else None
        return None
    
class receiver(asyncore.dispatcher):
    def __init__(self,conn,isVerbose=False,logger=None):
        asyncore.dispatcher.__init__(self,conn)
        self.from_remote_buffer=''
        self.to_remote_buffer=''
        self.sender=None
	self.__verbose__ = isVerbose
	self.__logger__ = logger

    def handle_connect(self):
        if (self.__verbose__):
	    msg = 'INFO: RECEIVER --> handle_connect()!'
	    if (self.__logger__):
		self.__logger__.warning(msg)
	    else:
		print >>sys.stdout, msg

    def handle_read(self):
        read = self.recv(4096)
	msg = '(%s.handle_read) %04i bytes -->' % (self.__class__,len(read))
	if (self.__logger__):
	    self.__logger__.warning(msg)
	else:
	    print >>sys.stdout, msg
        self.from_remote_buffer += read

    def writable(self):
        return (len(self.to_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.to_remote_buffer)
	msg = '(%s.handle_write) %04i bytes <--' % (self.__class__,sent)
	if (self.__logger__):
	    self.__logger__.warning(msg)
	else:
	    print >>sys.stdout, msg
        self.to_remote_buffer = self.to_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()
	if (self.__verbose__):
	    msg = 'INFO: RECEIVER --> handle_close()!'
	    if (self.__logger__):
		self.__logger__.warning(msg)
	    else:
		print >>sys.stdout, msg

class sender(asyncore.dispatcher):
    def __init__(self, receiver, remoteaddr,remoteport,isVerbose=False,logger=None):
        asyncore.dispatcher.__init__(self)
        self.receiver=receiver
	self.__verbose__ = isVerbose
	self.__logger__ = logger
        receiver.sender=self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((remoteaddr, remoteport))

    def handle_connect(self):
	if (self.__verbose__):
	    msg = 'INFO: SENDER --> handle_connect()!'
	    if (self.__logger__):
		self.__logger__.warning(msg)
	    else:
		print >>sys.stdout, msg

    def handle_read(self):
        read = self.recv(4096)
	msg = '(%s.handle_read) %04i bytes -->' % (self.__class__,len(read))
	if (self.__logger__):
	    self.__logger__.warning(msg)
	else:
	    print >>sys.stdout, msg
        self.receiver.to_remote_buffer += read

    def writable(self):
        return (len(self.receiver.from_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.receiver.from_remote_buffer)
	msg = '(%s.handle_write) %04i bytes <--' % (self.__class__,sent)
	if (self.__logger__):
	    self.__logger__.warning(msg)
	else:
	    print >>sys.stdout, msg
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        self.receiver.close()
	if (self.__verbose__):
	    msg = 'INFO: SENDER --> handle_close()!'
	    if (self.__logger__):
		self.__logger__.warning(msg)
	    else:
		print >>sys.stdout, msg

if (__name__ == '__main__'):
    from optparse import OptionParser
    
    program_name = __name__ if (__name__ != '__main__') else os.path.splitext(os.path.basename(sys.argv[0]))[0]
    LOG_FILENAME = './%s.log' % (program_name)
    logger = logging.getLogger(program_name)
    handler = logging.FileHandler(LOG_FILENAME)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler) 
    print 'Logging to "%s".' % (handler.baseFilename)
    
    ch = logging.StreamHandler()
    ch_format = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(ch_format)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    
    logging.getLogger().setLevel(logging.DEBUG)

    if (len(sys.argv) == 1):
	sys.argv.insert(len(sys.argv), '-h')
    
    parser = OptionParser("usage: %prog [options]")
    parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
    parser.add_option("-l", "--listen", action="store", type="string", help="IP Address Port for Reverse Proxy Head.", dest="listen")
    parser.add_option("-r", "--remote", action="store", type="string", help="IP Address Port for Remote Node.", dest="remote")
    parser.add_option("-d", "--delay", action="store", type="string", help="Delay Seconds, can be positive float or int value.", dest="delay")
    parser.add_option("-b", "--backlog", action="store", type="string", help="TCP/IP Backlog, larger number can produce beter results, typically 100 by default.", dest="backlog")
    
    options, args = parser.parse_args()
    
    _isVerbose = False
    if (options.verbose):
	_isVerbose = True
	
    _listen = None
    if (options.listen and is_ip_address_valid(options.listen)):
	_listen = options.listen.split(':')
	_listen[-1] = int(_listen[-1]) if (str(_listen[-1]).isdigit()) else _listen[-1]
    else:
	print >> sys.stderr, 'WARNING: Please make sure the value appearing after the -l option is a valid ip address and port in the form of 127.0.0.1:8888 however not this specific address unless this is your specific address.'
	
    _remote = None
    if (options.remote and is_ip_address_valid(options.remote)):
	_remote = options.remote
    else:
	print >> sys.stderr, 'WARNING: Please make sure the value appearing after the -r option is a valid ip address and port in the form of 127.0.0.1:8888 however not this specific address unless this is your specific address.'
	
    _delay = make_number_valid_or_none(options.delay)
    if (_delay is None):
	print >> sys.stderr, 'WARNING: Please make sure the value appearing after the -d option is a valid positive number of some kind.'
	    
    _backlog = make_number_valid_or_none(options.backlog,allow_float=False)
    if (_backlog is None):
	_backlog = 100
	print >> sys.stderr, 'WARNING: Please make sure the value appearing after the -b option is a valid positive integer of some kind, cannot be float. Backlog of 100 will be used at this time.'
		
    ReverseProxy(_listen[0],_listen[-1],remotes=[_remote],delay=_delay,backlog=_backlog)
    asyncore.loop()

