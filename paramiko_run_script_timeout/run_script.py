import os, sys

from vyperlogix import paramiko
from vyperlogix.paramiko import ParamikoSFTP

class ParamikoTestbed(ParamikoSFTP):
    def run_script(self, script_name):
        """ Run a script on the remote array and return the stdout
        """
        try:
            chan = self.transport.open_session()
            # five minute timeout on the channel communication
            chan.settimeout(5*60.0)
            script_contents = open(script_name).read().splitlines()
            #chan.exec_command('script')
            if chan.send_ready():
                chan.sendall("\n".join(script_contents))
                chan.send("\n.\n")
    
            results = StringIO()
            error = StringIO()
            bufsize = 1024
            while not chan.exit_status_ready():
                if chan.recv_ready():
                    data = chan.recv(bufsize)
                    while data:
                        results.write(data)
                        data = chan.recv(bufsize)
    
                if chan.recv_stderr_ready():
                    error_buf = chan.recv_stderr(bufsize)
                    while error_buf:
                        error.write(error_buf)
                        error_buf = chan.recv_stderr(bufsize)
    
            exit_status = chan.recv_exit_status()
            if exit_status == 0:
                return results.getvalue()
            else:
                raise ZfsScriptError(results.getvalue())
    
        except socket.timeout:
            logger.warn("%s: Timeout running %s" %(self.hostname, script_name))
            return None
    
        except paramiko.SSHException as e:
            logger.warn(
                "Couldn't execute script on array %s: %s" % (self.hostname, e))
            raise
    
        except AttributeError as e:
            logger.exception(e)
            raise
    
        except Exception:
            raise
    
        finally:
            results.close()
            error.close()
            chan.close()


if (__name__ == '__main__'):
    def callback(self):
        try:
            sftp = self.getSFTPClient
        
            # dirlist on remote host
            dirlist = sftp.listdir('.')
            print 'BEGIN: Dirlist.'
            for d in dirlist:
                print d
            print 'END!!! Dirlist.'
            
            responses = self.exec_command('ls -la')
            print 'BEGIN: responses.'
            for response in responses:
                print response
            print 'END!!! responses.'
        
            print 'Closing sftp session.'
            sftp.close()
            print 'Closing transport.'
            self.close()
            print 'Terminate program.'
            os._exit(0)
            
        except Exception, _details:
            info_string = _utils.formattedException(details=_details)
            print info_string

    logPath = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),'log')

    #vector = {'ip':'192.168.1.4','port':22,'username':'root','password':'Compaq123'}
    
    #vector = {'ip':'16.83.121.250','port':22,'username':'root','password':'Compaq@123'}
    
    #vector = {'ip':'54.84.17.141','port':22,'username':'root','proxy':'127.0.0.1:8888'}

    vector = {'ip':'10.0.0.185','port':22,'username':'root','proxy':'127.0.0.1:8888'}

    __host__ = vector.get('ip')
    __port__ = vector.get('port')
    __username__ = vector.get('username')
    __password__ = vector.get('password')
    
    print "%s:%s <-- %s/%s" % (__host__,__port__,__username__,__password__)

    from vyperlogix import misc
    from vyperlogix.misc import _utils
    from vyperlogix.classes import SmartObject

    if (vector.has_key('proxy')):
	__proxy__ = SmartObject.SmartObject()
	__proxy__.proxy = vector.get('proxy').split(':') if (vector.has_key('proxy')) else []
	try:
	    if (len(__proxy__.proxy) == 2):
		__proxy__.proxy[-1] = int(__proxy__.proxy[-1])
		if (misc.isInteger(__proxy__.proxy[-1])):
		    import socket
		    from vyperlogix.sockets.proxies.socks import socks

		    __proxy__.__default_proxy_before__ = socks._defaultproxy
		    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, __proxy__.proxy[0], int(__proxy__.proxy[-1]))
		    __proxy__.__default_proxy_after__ = socks._defaultproxy
		    __proxy__.__socket_socket_before__ = socket.socket
		    socket.socket = socks.socksocket
		    __proxy__.__socket_socket_after__ = socket.socket
		    print 'proxy=%s' % (':'.join([str(p) for p in __proxy__.proxy]))
		else:
		    print 'ERROR: Invalid proxy=%s, due to malformed port number.' % (__proxy__.proxy)
	    else:
		print 'ERROR: Invalid proxy=%s, due to missing ":" (--proxy=127.0.0.1:8080).' % (__proxy__.proxy)
	except Exception, ex:
	    info_string = _utils.formattedException(details=ex,depth=2,delims='\n\t')
	    print 'ERROR: Invalid proxy=%s, due to the following:\n%s.' % (__proxy__.proxy,info_string)
    
    #sftp = paramiko.ParamikoSFTP(__host__,__port__,__username__,password=__password__,callback=callback,auto_close=False,logPath=logPath)
    
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(__host__, username=__username__, password=__password__, timeout=30)
    ssh._transport.banner_timeout = 30
    sftp = ssh.open_sftp()
    sftp.close()    
