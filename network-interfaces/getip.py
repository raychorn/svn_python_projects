from vyperlogix.sockets import getip

if (__name__ == '__main__'):
    print getip.get_ip_address('eth0')