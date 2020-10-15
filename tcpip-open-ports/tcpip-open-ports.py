import socket
import errno
import contextlib

reserved_ports = set()

def check_tcpip_port(lowest_port = 0, highest_port = None, bind_address = '', *socket_args, **socket_kwargs):
    if highest_port is None:
        highest_port = lowest_port + 100
    while lowest_port < highest_port:
        if lowest_port not in reserved_ports:
            try:
                with contextlib.closing(socket.socket(*socket_args, **socket_kwargs)) as my_socket:
                    my_socket.bind((bind_address, lowest_port))
                    this_port = my_socket.getsockname()[1]
                    reserved_ports.add(this_port)
                    return this_port
            except socket.error as error:
                if not error.errno == errno.EADDRINUSE:
                    raise
                assert not lowest_port == 0
                #reserved_ports.add(lowest_port)
        lowest_port += 1
    raise Exception('Could not find open port')

def run_length_encoding(items):
    items = list(items)
    items.sort()
    i = items[0]
    n = 1
    m = len(items)-1
    bag = [i]
    response = []
    if (n < m):
        while (n < m):
            if (items[n] - bag[-1]) == 1:
                bag.append(items[n])
            else:
                if (bag[0] == bag[-1]):
                    response.append('%s' % (bag[0]))
                else:
                    response.append('%s-%s' % (bag[0],bag[-1]))
                bag = [items[n]]
            n += 1
    return response

if (__name__ == '__main__'):
    print 'BEGIN:'
    for i in xrange(0,65536):
        try:
            port_num = check_tcpip_port(lowest_port=i, highest_port=i+1, bind_address='0.0.0.0')
            #print 'OPEN: %s (%s)' % (port_num,len(reserved_ports))
        except:
            pass
    print 'RECAP: There are %s reserved ports.' % (len(reserved_ports))
    all_ports = set([i for i in xrange(0,65536)])
    open_ports = all_ports - reserved_ports
    print 'RECAP: There are %s open ports, as follows:' % (len(open_ports))
    if (0):
        print '='*20
        for p in open_ports:
            print p
        print '='*20
        print
    __ports__ = run_length_encoding(open_ports)
    print '='*20
    for p in __ports__:
        print p
    print '='*20
    print 'END!!!'
