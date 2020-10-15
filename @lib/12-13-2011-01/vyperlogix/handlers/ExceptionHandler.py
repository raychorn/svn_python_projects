import os, sys
import traceback
from StringIO import StringIO
import time
from vyperlogix.mail import message
from vyperlogix.mail import mailServer
import socket
import types

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

def dummy(args):
    pass

class ExceptionHandler:
    def __init__(self, logPath='.', emailsTo='support@vyperlogix.com', notifyMachineNames=[]):
        import os, sys
        self.__notifyMachineNames__ = notifyMachineNames if isinstance(notifyMachineNames,list) else [notifyMachineNames]
        self.__notifyMachineNames__ = [str(cn).lower() for cn in self.__notifyMachineNames__]
        self.__logPath__ = os.path.abspath(logPath)
        self.__emailsTo__ = emailsTo
        self.__callback__ = dummy
        sys.excepthook = self.__excepthook

    def callback():
        doc = "callback"
        def fget(self):
            return self.__callback__
        def fset(self,func):
            self.__callback__ = func if (callable(func)) else dummy
        return locals()    
    callback = property(**callback())

    def notifyMachineNames():
        doc = "notifyMachineNames"
        def fget(self):
            return self.__notifyMachineNames__
        def fset(self,names):
            self.__notifyMachineNames__ = names
        return locals()    
    notifyMachineNames = property(**notifyMachineNames())

    def logPath():
        doc = "logPath"
        def fget(self):
            return self.__logPath__
        def fset(self,fpath):
            self.__logPath__ = fpath
        return locals()    
    logPath = property(**logPath())

    def emailsTo():
        doc = "emailsTo"
        def fget(self):
            return self.__emailsTo__
        def fset(self,email_addr):
            self.__emailsTo__ = email_addr
        return locals()    
    emailsTo = property(**emailsTo())

    def __excepthook(self, excType, excValue, tracebackobj):
        """
	Global function to catch unhandled exceptions.

	@param excType exception type
	@param excValue exception value
	@param tracebackobj traceback object
	"""
        _computer_name = socket.gethostbyname_ex(socket.gethostname())[0]

        logFile = os.path.join(self.logPath, "%s.log" % sys.argv[0].split('.')[0])
        timeString = time.strftime("%Y-%m-%d, %H:%M:%S")

        separator = '='*80
        versionInfo = ("\nPlatform: %s (%s)\n%s\n") % (sys.platform, _computer_name, sys.version)
        tbinfofile = StringIO()
        traceback.print_tb(tracebackobj, None, tbinfofile)
        tbinfofile.seek(0)
        tbinfo = tbinfofile.read()
        errmsg = '%s: \n%s' % (str(excType), str(excValue))
        sections = [separator,timeString, errmsg, tbinfo,versionInfo,separator]
        msg = '\n'.join(sections)
        hasSentEmail = False
        if (_computer_name.lower() in self.notifyMachineNames):
            notice = \
                   """An unhandled exception occurred. Please report the problem"""\
                   """ using the error reporting dialog or via email to <%s>."""\
                   """ A log has been written to "%s".\n\nError information:\n""" % \
                   (self.emailsTo, logFile)
            try:
                msg = message.Message('do-not-reply@vyperlogix.com', 'support@vyperlogix.com', '%s\n%s' % (notice,msg), 'Error Handler from "%s".' % sys.argv[0])
                smtp = mailServer.MailServer(mailServer.development_config)
                smtp.sendEmail(msg)
                hasSentEmail = True
            except Exception, details:
                exc_info = sys.exc_info()
                info_string = '\n'.join(traceback.format_exception(*exc_info))
                print >> sys.stderr, 'EMAIL_ERROR :: Unable to send email due to "%s\n%s".' % (details,info_string)
                sections.insert(len(sections)-1,'EMAIL_ERROR=[%s]' % info_string)
            sections.insert(len(sections)-1,'hasSentEmail=[%s]' % hasSentEmail)
        else:
            print >> sys.stderr, msg

        if (callable(self.callback)):
            try:
                self.callback(sections)
            except:
                exc_info = sys.exc_info()
                info_string = '\n'.join(traceback.format_exception(*exc_info))
                print >> sys.stderr, 'CALLBACK_ERROR :: Unable to fire callback due to "%s\n%s".' % (details,info_string)
                sections.insert(len(sections)-1,'CALLBACK_ERROR=[%s]' % info_string)

        msg = '\n'.join(sections)
        try:
            f = open(logFile, "a")
            f.write(msg)
        except IOError:
            pass
        finally:
            f.flush()
            f.close()
