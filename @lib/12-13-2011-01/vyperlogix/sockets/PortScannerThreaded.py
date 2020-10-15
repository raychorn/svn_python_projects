# a simple portscanner with multithreading

import socket as sk
import os,sys

from vyperlogix.misc import threadpool

__Q__ = threadpool.ThreadQueue(50)

def usage():
    print "\npyScan 0.1"
    print "usage: pyScan <host> [start port] [end port]"
    
def __terminate__():
    from vyperlogix.misc import _utils
    
    from vyperlogix.win.WinProcesses import Win32Processes
    
    from vyperlogix import misc
    from vyperlogix.misc import ObjectTypeName

    __programName__ = (sys.argv[0].split(os.sep)[-1].split('.'))[0]
    try:
	p = Win32Processes()
	pid = p.getProcessIdByName(__programName__)
	if (misc.isList(pid)) and (len(pid) > 0):
	    pid = pid[0]
	elif (len(pid) == 0):
	    pid = os.getpid()
	if (misc.isInteger(pid)):
	    print 'DEBUG:  pid="%s"' % (pid)
	    print 'BEGIN:'
	    _utils.terminate()
	    print 'END !!!'
	else:
	    print 'DEBUG:  pid is not an Int because it is "%s" !!!' % (ObjectTypeName.typeClassName(pid))
    except Exception, ex:
	info_string = _utils.formattedException(details=ex)
	print info_string

class Scanner():
    def __init__(self, host, port,callback=None):
        # host and port
        self.host = host
        self.port = port
        self.__callback__ = callback
        # build up the socket obj
        self.sd = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

    @threadpool.threadify(__Q__)
    def start(self):
        try:
            # connect to the given host:port
            self.sd.connect((self.host, self.port))
            print "%s:%d OPEN" % (self.host, self.port)
            if (callable(self.__callback__)):
                try:
                    __callback__(self,host=self.host,port=self.port)
                except:
                    pass
            self.sd.close()
        except: pass

class pyScan(dict):
    def __init__(self, args=[], **vargs):
        # arguments vector
        self.args = args
        # start port and end port
        self.start, self.stop = 1, 1024
        # host name
        self.host = ""
        try:
            for k,v in vargs.iteritems():
                self[k] = v
        except:
            pass

        # check the arguments
        if len(self.args) == 4:
            self.host = self.args[1]
            try:
                self.start = int(self.args[2])
                self.stop = int(self.args[3])
            except ValueError:
                usage()
                return
            if self.start > self.stop:
                usage()
                return
        elif len(self.args) == 2:
            self.host = self.args[1]
        else:
            usage()
            return

        try:
            sk.gethostbyname(self.host)
        except:
            print "hostname '%s' unknown" % self.host
        self.scan(self.host, self.start, self.stop)

    def scan(self, host, start, stop):
        self.port = start
        while self.port <= stop:
            #print 'Scanning %s:%s' % (host, self.port)
            Scanner(host, self.port, callback=self.get('callback',None)).start()
            self.port += 1
        print 'All ports have been Queued for Scanning...'
        while (not __Q__.empty()):
            print 'Waiting for the Queue to empty (%s)...' % (__Q__.qsize())
        __shutdown__ = self.get('shutdown',None)
        if (callable(__shutdown__)):
            try:
                __shutdown__(self)
            except:
                pass
        print 'Queue joined.'
        __Q__.join()
        print 'Exiting...'
        __Q__.__shutdown__()
	print 'Terminating...'
	__terminate__()
        sys.exit(1)
        
if __name__ == "__main__":
    from vyperlogix import misc
    from vyperlogix.classes.SmartObject import SmartObject

    __credentials__ = [
        {'db':'rootdb','username':'raychorn','password':'peekab00','port':23337,'status':None},
        {'db':'githubManager','username':'root','password':'peekab00','port':33307,'status':None},
        {'db':'djangocloud','username':'raychorn','password':'peekab00','port':23337,'status':None},
        {'db':'cargochiefdb','username':'raychorn','password':'peekab00','port':23337,'status':None}
    ]
    __credentials__ = [SmartObject(c) for c in __credentials__]

    def __callback__(self,host=None,port=None):
	'''
                try:
                    import MySQLdb
                except ImportError:
                    print >> sys.stderr, 'ERROR: Cannot import MySQLdb and this is required.'
                for credential in __credentials__:
                    __failures__ = 0
                    if (port == credential.port) and (not credential.status):
                        try:
                            db = MySQLdb.connect(host=host, port=port,
                                                 user=credential.username,
                                                  passwd=credential.password,
                                                  db=credential.db)
                            print '#1 (%s:%s)@(%s) --> %s' % (host,port,credential,db)
                            db.close
                            for c in __credentials__:
                                if (c.port == port):
                                    c.status = True
                            break
                        except:
                            __failures__ += 1
                if (__failures__ == len(__credentials__)):
                    print 'INFO: %s:%s has NOTHING to do with MySQL or invalid credentials (%s) are being used!' % (host,port,credential)
	'''
        if (host and port):
            if (port in [c.port for c in __credentials__]):
		from vyperlogix.mysql import MySQLConnectionSniffer
		for credential in __credentials__:
		    __failures__ = 0
		    if (port == credential.port) and (not credential.status):
			success = MySQLConnectionSniffer(host, port, credential.db, credential.username, credential.password).exists()
			if (success):
			    for c in __credentials__:
				if (c.port == port):
				    c.status = True
			    break
			else:
			    __failures__ += 1
		if (__failures__ == len(__credentials__)):
		    print 'INFO: %s:%s has NOTHING to do with MySQL or invalid credentials (%s) are being used!' % (host,port,credential)
                    
    def __shutdown__(self):
	tests = [not c.status for c in __credentials__]
	i = 0
	for test in tests:
	    if (test):
		print 'Failed: %s' % (__credentials__[i])
	    i += 1
        assert(any(tests) == False)
    
    ports = list(set([c.port for c in __credentials__]))
    ports.sort()
    args = misc.copy(sys.argv)
    assert(len(args) == 4)
    assert(len(ports) >= 2)
    args[-2] = ports[0]
    args[-1] = ports[1]
    pyScan(args,callback=__callback__,shutdown=__shutdown__)

