import os
import subprocess
import errno
import time
import sys

PIPE = subprocess.PIPE

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.classes.CooperativeClass import Cooperative

__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

              All Rights Reserved.

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

if subprocess.mswindows:
    from win32file import ReadFile, WriteFile
    from win32pipe import PeekNamedPipe
    import msvcrt
else:
    import select
    import fcntl

class Popen(subprocess.Popen):
    def recv(self, maxsize=None):
        return self._recv('stdout', maxsize)
    
    def recv_err(self, maxsize=None):
        return self._recv('stderr', maxsize)

    def send_recv(self, input='', maxsize=None):
        return self.send(input), self.recv(maxsize), self.recv_err(maxsize)

    def get_conn_maxsize(self, which, maxsize):
        if maxsize is None:
            maxsize = 1024
        elif maxsize < 1:
            maxsize = 1
        return getattr(self, which), maxsize
    
    def _close(self, which):
        getattr(self, which).close()
        setattr(self, which, None)
    
    if subprocess.mswindows:
        def send(self, input):
            if not self.stdin:
                return None

            try:
                x = msvcrt.get_osfhandle(self.stdin.fileno())
                (errCode, written) = WriteFile(x, input)
            except ValueError:
                return self._close('stdin')
            except (subprocess.pywintypes.error, Exception), why:
                if why[0] in (109, errno.ESHUTDOWN):
                    return self._close('stdin')
                raise

            return written

        def _recv(self, which, maxsize):
            conn, maxsize = self.get_conn_maxsize(which, maxsize)
            if conn is None:
                return None
            
            try:
                x = msvcrt.get_osfhandle(conn.fileno())
                (read, nAvail, nMessage) = PeekNamedPipe(x, 0)
                if maxsize < nAvail:
                    nAvail = maxsize
                if nAvail > 0:
                    (errCode, read) = ReadFile(x, nAvail, None)
            except ValueError:
                return self._close(which)
            except (subprocess.pywintypes.error, Exception), why:
                if why[0] in (109, errno.ESHUTDOWN):
                    return self._close(which)
                raise
            
            if self.universal_newlines:
                read = self._translate_newlines(read)
            return read

    else:
        def send(self, input):
            if not self.stdin:
                return None

            if not select.select([], [self.stdin], [], 0)[1]:
                return 0

            try:
                written = os.write(self.stdin.fileno(), input)
            except OSError, why:
                if why[0] == errno.EPIPE: #broken pipe
                    return self._close('stdin')
                raise

            return written

        def _recv(self, which, maxsize):
            conn, maxsize = self.get_conn_maxsize(which, maxsize)
            if conn is None:
                return None
            
            flags = fcntl.fcntl(conn, fcntl.F_GETFL)
            if not conn.closed:
                fcntl.fcntl(conn, fcntl.F_SETFL, flags| os.O_NONBLOCK)
            
            try:
                if not select.select([conn], [], [], 0)[0]:
                    return ''
                
                r = conn.read(maxsize)
                if not r:
                    return self._close(which)
    
                if self.universal_newlines:
                    r = self._translate_newlines(r)
                return r
            finally:
                if not conn.closed:
                    fcntl.fcntl(conn, fcntl.F_SETFL, flags)

message = "Other end disconnected!"

def recv_some(p, t=.1, e=1, tr=5, stderr=0):
    if tr < 1:
        tr = 1
    x = time.time()+t
    y = []
    r = ''
    pr = p.recv
    if stderr:
        pr = p.recv_err
    while time.time() < x or r:
        r = pr()
        if r is None:
            if e:
                raise Exception(message)
            else:
                break
        elif r:
            y.append(r)
        else:
            time.sleep(max((x-time.time())/tr, 1))
    return ''.join(y)
    
def send_all(p, data):
    while len(data):
        sent = p.send(data)
        if sent is None:
            raise Exception(message)
        data = buffer(data, sent)
	time.sleep(1)
        
class Shell(Cooperative):
    '''Shell processor.'''
    def __init__(self,commands,shell=None,env=None,isExit=False,isWait=False,isVerbose=False,fOut=sys.stderr,onExit=None):
        '''
        isVerbose=True and fOut=something work together otherwise there will be no putput from the commands that were issued.
        fOut=something callable to get callbacks rather than waiting for the end result.
        '''
        self.isVerbose = isVerbose
        self.fOut = fOut
        self.__onExit__ = onExit
	self.__delayed__ = []
	self.__has_issued_callback__ = False
        if (callable(fOut)):
            self.isVerbose = True
        if (not misc.isList(commands)):
            commands = [commands]
        if sys.platform == 'win32':
            shell, commands, self.tail = ('cmd' if (shell is None) else shell, commands, '\r\n')
        else:
            shell, commands, self.tail = ('sh' if (shell is None) else shell, commands, '\n')

        e = os.environ if (env == None) else env
        self.proc = Popen(shell, env=e, stdin=PIPE, stdout=PIPE)
        if (self.isVerbose):
            if (callable(fOut)):
                try:
                    fOut(recv_some(self.proc))
                except Exception, details:
                    info_string = _utils.formattedException(details=details)
                    print >> sys.stdout, info_string
            else:
                print >>self.fOut, recv_some(self.proc),
        for cmd in commands:
            send_all(self.proc, str(cmd) + self.tail)
            if (self.isVerbose):
                __lines__ = []
                data = recv_some(self.proc)
		__toks__ = str(data).split(os.linesep)
		# there is still a timing issue - wait 30 secs or count nothing returned something like 10 times...
		_begin_ = time.time()
		_num_ = 0
		_max_ = 30
                while ((time.time() - _begin_) < _max_) and (_num_ < _max_):
		    if (len(__toks__) > 1):
			misc.append(__lines__,__toks__)
		    else:
			_num_ += 1
		    time.sleep(1)
                    data = recv_some(self.proc)
		    __toks__ = str(data).split(os.linesep)
		self.__has_issued_callback__ = True
		if (callable(fOut)):
		    try:
			fOut(os.linesep.join(__lines__))
		    except Exception, details:
			info_string = _utils.formattedException(details=details)
			print >> _target_[0:2], info_string
		else:
		    print >>self.fOut, recv_some(self.proc),
	while (len(self.__delayed__) > 0):
	    if (callable(self.__delayed__[-1])):
		callee = self.__delayed__.pop()
		try:
		    callee()
		except Exception, details:
		    info_string = _utils.formattedException(details=details)
		    print >> _target_[0:2], info_string
        if (isExit):
	    if (not self.__has_issued_callback__):
		self.__delayed__.append(self.doExit)
	    else:
		self.doExit()
        if (isWait):
            self.doWait()
    
    def doSend(self,data):
        try:
            send_all(self.proc, data)
        except:
            pass
        if (self.isVerbose):
            if (callable(self.fOut)):
                try:
                    self.fOut(recv_some(self.proc))
                except Exception, details:
                    info_string = _utils.formattedException(details=details)
                    print >> _target_[0:2], info_string
            else:
                print >>self.fOut, recv_some(self.proc, e=0)
            
    def doSendWithTail(self,data):
        self.doSend(data + self.tail)
            
    def doExit(self):
	try:
	    send_all(self.proc, 'exit' + self.tail)
	    if (self.isVerbose):
		if (callable(self.fOut)):
		    try:
			data = recv_some(self.proc)
		    except:
			data = None
		    if (data is not None) and (len(data) > 0):
			try:
			    self.fOut(data)
			except Exception, details:
			    info_string = _utils.formattedException(details=details)
			    print >> _target_[0:2], info_string
		else:
		    try:
			data = recv_some(self.proc, e=0)
		    except:
			data = None
		    if (data is not None) and (len(data) > 0):
			print >>self.fOut, data
	except:
	    pass # suppress because the other side may have become disconnected simply because we have all the content from it...
        if (callable(self.__onExit__)):
            try:
                self.__onExit__()
            except Exception, details:
                info_string = _utils.formattedException(details=details)
                print >> sys.stderr, info_string

    def doWait(self):
        self.proc.wait()
            