__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

import base64
from binascii import hexlify
import getpass
import os
import select
import socket
import sys
import threading
import time
import traceback

import paramiko

from vyperlogix.classes.CooperativeClass import Cooperative
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc import _utils

__pageant_warning__ = '(Are you sure you have Pageant Running with the host key installed ?)'

class ParamikoSFTP(Cooperative):
    def __init__(self,hostname,port,username,password=None,use_manual_auth=False,callback=None,auto_close=True,logger=None,logPath=os.path.abspath(os.path.dirname(sys.argv[0]))):
        self.__hostname__ = hostname
        self.__port__ = port
        self.__username__ = username
        self.__password__ = password
        self.__transport__ = None
        self.__callback__ = callback
        self.__autoclose__ = auto_close
        self.__logPath__ = logPath
        self.__use_manual_auth__ = use_manual_auth
        self.logger = paramiko.util.get_logger(__name__)
        if (logger):
            self.logger = logger
        else:
            if (self.__logPath__) and (os.path.exists(self.__logPath__)) and (os.path.isdir(self.__logPath__)):
                _utils._makeDirs(self.__logPath__)
                paramiko.util.log_to_file(os.path.join(self.__logPath__,'%s.log' % (ObjectTypeName.objectSignature(self))))
        if self.hostname.find(':') >= 0:
            self.__hostname__, portstr = hostname.split(':')
            self.__port__ = int(portstr)
        self.__open__()

    def __open__(self):
        try:
            self.__sock__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock__.connect((self.hostname, self.port))
        except Exception, _details:
            self.logger.exception('*** Connect failed !!')
            sys.exit(1)

        try:
            self.__transport__ = paramiko.Transport(self.__sock__)
            try:
                self.transport.start_client()
            except paramiko.SSHException:
                self.logger.exception('*** SSH negotiation failed.')
                sys.exit(1)
        
            try:
                keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
            except IOError:
                try:
                    keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
                except IOError, ex:
                    __info__ = _utils.formattedException(details=ex)
                    self.logger.error('*** Unable to open host keys file due to: %s' % (__info__))
                    keys = {}
        
            # check server's host key -- this is important.
            key = self.transport.get_remote_server_key()
            if not keys.has_key(self.hostname):
                self.logger.warning('*** WARNING: Unknown host key!  %s' % (__pageant_warning__))
            elif not keys[self.hostname].has_key(key.get_name()):
                self.logger.warning('*** WARNING: Unknown host key! %s' % (__pageant_warning__))
            elif keys[self.hostname][key.get_name()] != key:
                self.logger.warning('*** WARNING: Host key has changed!!! %s' % (__pageant_warning__))
                sys.exit(1)
            else:
                self.logger.info('*** Host key OK.')
        
            if (not self.__use_manual_auth__):
                self.agent_auth()
            if (self.__use_manual_auth__) or (not self.transport.is_authenticated()):
                self.manual_auth()
            if not self.transport.is_authenticated():
                self.logger.warning('*** Authentication failed. :(')
                t.close()
                sys.exit(1)
        
            self.__channel__ = self.transport.open_session()
            self.channel.get_pty()
            self.logger.info('*** Here we go!')
            #if (callable(self.__callback__)):
                #self.__callback__()
            if (self.__autoclose__):
                self.logger.info('*** Here we close channel and close transport !')
                self.channel.close()
                self.transport.close()
        
        except Exception, _details:
            self.logger.exception('Transport closed due to some kind of error.')
            try:
                self.transport.close()
            except:
                pass
            sys.exit(1)

    def __reopen__(self):
        self.__open__()
        return self
            
    def hostname():
        doc = "hostname"
        def fget(self):
            return self.__hostname__
        return locals()
    hostname = property(**hostname())
    
    def port():
        doc = "port"
        def fget(self):
            return self.__port__
        return locals()
    port = property(**port())
    
    def username():
        doc = "username"
        def fget(self):
            return self.__username__
        return locals()
    username = property(**username())
    
    def password():
        doc = "password"
        def fget(self):
            return self.__password__
        return locals()
    password = property(**password())
    
    def transport():
        doc = "transport"
        def fget(self):
            return self.__transport__
        return locals()
    transport = property(**transport())
    
    def channel():
        doc = "channel"
        def fget(self):
            return self.__channel__
        return locals()
    channel = property(**channel())
    
    def getSFTPClient():
        doc = "SFTPClient"
        def fget(self):
            from vyperlogix.decorators import inject
            
            client = paramiko.SFTPClient.from_transport(self.transport)

            @inject.addto(client)
            def isdir(self, path='.'):
                from paramiko.sftp import CMD_OPENDIR, CMD_CLOSE, CMD_HANDLE
                path = self._adjust_cwd(path)
                try:
                    t, msg = self._request(CMD_OPENDIR, path)
                    __is__ = t == CMD_HANDLE
                    handle = msg.get_string()
                    self._request(CMD_CLOSE, handle)
                except:
                    __is__ = False
                return __is__

            return client
        return locals()
    getSFTPClient = property(**getSFTPClient())
    
    def put(self,source,dest,callback=None):
	responses = []

	def __sftp__():
	    return ParamikoSFTP(self.hostname,self.port,self.username,password=self.password,callback=callback,use_manual_auth=self.manual_auth,auto_close=False,logger=self.logger)
	
	def __callback__(size, file_size):
	    pcent = size/file_size
	    if (pcent > 0.0):
		responses.append('%4.2f %%' % ((size/file_size)*100.0))

	try:
	    sftp = __sftp__()
	    client = sftp.getSFTPClient
	    client.put(source, dest, callback=__callback__ if (not callable(callback)) else callback)
	except paramiko.ChannelException:
	    count = 0
	    for line in open(source):
		if (len(str(line).strip()) > 0):
		    sftp = __sftp__()
		    ch = '>' if (count == 0) else '>>'
		    cmd = 'echo "%s" %s %s' % (line.replace('\$','$').replace('$','\$').replace('\>','>').replace('>','\>').rstrip(),ch,dest)
		    print 'DEBUG: cmd=%s' % (cmd)
		    resp = sftp.exec_command(cmd)
		    responses.append('%s --> %s' % (cmd,','.join(resp)))
		    count += 1
	return responses
    
    def agent_auth(self):
        """
        Attempt to authenticate to the given transport using any of the private
        keys available from an SSH agent.
        """
        
        agent = paramiko.Agent()
        agent_keys = agent.get_keys()
        if len(agent_keys) == 0:
            return
            
        for key in agent_keys:
            self.logger.info('Trying ssh-agent key %s' % hexlify(key.get_fingerprint()))
            try:
                self.transport.auth_publickey(self.username, key)
                return
            except paramiko.SSHException:
                self.logger.exception('ssh-agent keys failed.')
    
    def manual_auth(self):
        self.transport.auth_password(self.username, self.password)
        
    def read(self,sftp,fpath):
        return sftp.open(fpath, 'r').read()
    
    def write(self,sftp,fpath,data):
        sftp.open(fpath, 'w').write(data)
        
    def get_channel_response(self):
        responses = []
        while True:
            try:
                x = self.channel.recv(1024)
                if len(x) == 0:
                    #print '\r\n*** EOF\r\n',
                    break
                responses.append(str(x).strip())
            except socket.timeout:
                self.logger.exception('*** SOCKET TIMEOUT ***')
                responses.append('*** SOCKET TIMEOUT ***')
                break
        return responses

    def exec_command(self,command,sleep=10):
        responses = []
        try:
            self.logger.info('Issuing command: %s' % (command))
            __count__ = 0
            while (self.channel.closed):
                self.logger.info('Reopening the channel with sleep of %s.' % (sleep))
                self.__channel__ = self.transport.open_session()
                self.channel.get_pty()
                time.sleep(sleep)
            self.channel.exec_command(command)
            __responses__ = self.get_channel_response()
	    __lines__ = [r.split('\n') for r in __responses__]
	    responses = []
	    for l in __lines__:
		for ll in l:
		    responses.append(ll.strip())
        except Exception:
            self.logger.exception('"%s" failed to execute.' % (command))
        return responses
    
    def reopen(self):
        if (self.__channel__.closed):
            self.__channel__ = self.transport.open_session()
            self.channel.get_pty()
    
    def close(self):
        self.channel.close()
        self.transport.close()
