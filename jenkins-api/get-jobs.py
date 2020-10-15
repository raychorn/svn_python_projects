import os, sys
from jenkinsapi.view import View
from jenkinsapi.jenkins import Jenkins

if (1):
    import socket
    from vyperlogix.sockets.proxies.socks import socks
    
    from vyperlogix.classes.SmartObject import SmartObject
    
    __proxy__ = SmartObject()
    
    __proxy__.proxy = '127.0.0.1:8888'.split(':')
    
    __proxy__.__default_proxy_before__ = socks._defaultproxy
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, __proxy__.proxy[0], int(__proxy__.proxy[-1]))
    __proxy__.__default_proxy_after__ = socks._defaultproxy
    __proxy__.__socket_socket_before__ = socket.socket
    socket.socket = socks.socksocket
    __proxy__.__socket_socket_after__ = socket.socket
    print 'proxy=%s' % (':'.join([str(p) for p in __proxy__.proxy]))

J = Jenkins('http://jenkins.vyperlogix.com/jenkins')
print J.items()

__is_jenkins_busy__ = False
for job in J.get_jobs_info():
    __job__ = J.get_job(job[-1])
    try:
        __build__ = build = __job__.get_last_build()
        __duration__ = __build__.get_duration()
        __is__ = __duration__.total_seconds() == 0 # this means there is a job in-process.
        print 'Job: %s, Build: %s, Duration: %s' % (__job__,__build__,__duration__)
        if (__is__):
            __is_jenkins_busy__ = True
            break
    except:
        pass

os.environ['__is_jenkins_busy__'] = '1' if (__is_jenkins_busy__) else '0'
if (__is_jenkins_busy__):
    print '__is_jenkins_busy__ is %s' % (__is_jenkins_busy__)
print
