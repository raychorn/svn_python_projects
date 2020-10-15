import sys
import cStringIO as StringIO
import smtplib
import sets
import traceback

from vyperlogix.classes.CooperativeClass import Cooperative
from vyperlogix.misc import _utils
from vyperlogix import misc

from vyperlogix.daemon.daemon import Log

from vyperlogix.misc import ObjectTypeName

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

class MailServer(Cooperative):
    """
    This class contains the methods necessary for:

    """
    debug = 0
    def __init__(self, logger=None):
        self.__smtp_server__ = ''
        self.__smtp_port__ = -1
        self.__smtp_username__ = ''
        self.__smtp_password__ = ''
        self.__logger__ = None
        
        print 'You cannot use the %s class because this is an Abstract Class.  Try using one of the sub-classes instead.' % (ObjectTypeName.typeName(self))
        
    def __repr__(self):
        return '(%s) %s:%s @ %s' % (str(self.__class__),self.smtp_server,self.smtp_port,self.smtp_username)

    def logger():
        doc = "logger"
        def fget(self):
            return self.__logger__
        def fset(self, logger):
            self.__logger__ = logger
        return locals()
    logger = property(**logger())

    def smtp_server():
        doc = "smtp_server"
        def fget(self):
            return self.__smtp_server__
        def fset(self, value):
            self.__smtp_server__ = value
        return locals()
    smtp_server = property(**smtp_server())

    def smtp_port():
        doc = "smtp_port"
        def fget(self):
            return self.__smtp_port__
        def fset(self, value):
            self.__smtp_port__ = value if (isinstance(value,int)) else int(str(value))
        return locals()
    smtp_port = property(**smtp_port())

    def smtp_username():
        doc = "smtp_username"
        def fget(self):
            return self.__smtp_username__
        def fset(self, value):
            self.__smtp_username__ = value
        return locals()
    smtp_username = property(**smtp_username())

    def smtp_password():
        doc = "smtp_password"
        def fget(self):
            return self.__smtp_password__
        def fset(self, value):
            self.__smtp_password__ = value
        return locals()
    smtp_password = property(**smtp_password())

    def login(self):
        if (self.smtp_port < 1):
            toks = self.smtp_server.split(':')
            self.smtp_server = toks[0]
            self.smtp_port = -1 if (len(toks) != 2) else -1 if (not toks[-1].isdigit()) else int(toks[-1])
        if (len(self.smtp_server) > 0) and (isinstance(self.smtp_port,int)) and (self.smtp_port > -1):
            print '(%s.%s) :: smtpServer=[%s], port=[%s], username=[%s], password=[%s]' % (ObjectTypeName.typeName(self),misc.funcName(),self.smtp_server,self.smtp_port,self.smtp_username,self.smtp_password)
            try:
                self.mailServer = smtplib.SMTP(host=self.smtp_server,port=self.smtp_port)
                self.mailServer.set_debuglevel(self.debug)
                if (len(self.smtp_username) > 0) and (len(self.smtp_password) > 0):
                    self.mailServer.login(self.smtp_username,self.smtp_password)
            except Exception, details:
                tbinfofile = StringIO.StringIO()
                traceback.print_exc(None, tbinfofile)
                tbinfofile.seek(0)
                tbinfo = tbinfofile.read()
                _msg = '(%s.%s) :: ERROR due to "%s"\n%s.' % (ObjectTypeName.typeName(self),misc.funcName(),details,tbinfo)
                print >>sys.stderr, _msg
                raise smtplib.SMTPConnectError(_msg)
            self.log = self.logger
        else:
            _msg = '(%s.%s) :: WARNING :: Invalid SMTP Configuration that does not work, recommend checking your choices and attributes because something is wrong. smtpServer=[%s], port=[%s], username=[%s], password=[%s]' % (ObjectTypeName.typeName(self),misc.funcName(),self.smtp_server,self.smtp_port,self.smtp_username,self.smtp_password)
            print >>sys.stderr, _msg
            raise ValueError(_msg)

    def genEmailTxt(self, fromAddress, toArray, subject, buf, ccArray=None, bccArray=None):
        """
        Generates a text version of an e-mail using 'fromAddress',
        'toArray' (an array of e-mail addresses), 'subject', and
        'buf' (a buffer holding the e-mail text).
        """
        buf.seek(0)
        
        msgTxt = self.setEmailTxt(fromAddress, toArray, subject, buf.read(), ccArray, bccArray)
        
        return msgTxt

    def setEmailTxt(self, fromAddress, toArray, subject, msgStr, ccArray=None, bccArray=None):
        """
        Generates a text version of an e-mail using 'fromAddress',
        'toArray' (an array of e-mail addresses), 'subject', and
        """
        hdrBuf = StringIO.StringIO()
        hdrBuf.write('From: %s\r\n' % fromAddress)

        hdrBuf.write('To: %s\r\n' %','.join(toArray))

        if ccArray is not None:
            hdrBuf.write('CC: %s\r\n' %','.join(ccArray))
        
        if bccArray is not None:
            hdrBuf.write('BCC: %s\r\n' %','.join(bccArray))

        hdrBuf.write('Subject: %s\r\n' %subject)

        hdrBuf.write('\r\n') # Separator break btwn hdr and msg
            
        msgTxt = '%s%s' % (hdrBuf.getvalue(), msgStr.encode('ascii','replace'))

        if self.log is not None:
            self.log.log(5,'\n\n%s\n\n', msgTxt)
        
        return msgTxt

    def sendEmail(self, message, trial=False):
        """
        actually send the email message.

        message - Message object
        trial - if set to True, doesn't actually send email. Default: False
        """
        msgTxt = message.message

        if trial is True:
            if self.log is not None:
                self.log.debug('TRIAL email FROM:%s \tTO:%s', message.fromAdd, message.toAddList)
                self.log.debug('TRIAL email BODY:%s', msgTxt)
            
            return {'trial':[message.toAddList, msgTxt]}
        
        else:
            toSet = sets.Set(message.toAddList)
            ccSet = sets.Set(message.ccAddList)
            bccSet = sets.Set(message.bccAddList)
            sendToList = toSet | ccSet | bccSet # union 
            
            try:                
                mstat = self.mailServer.sendmail(message.fromAdd, sendToList, msgTxt.encode('ascii', 'replace'))
                toAlias = sendToList

                info_string = "Sent mail with Subject '%s' to %s" % (message.subject[:50],toAlias)
                if self.log is not None:                    
                    self.log.info(info_string)
                else:
                    print >>sys.stderr, info_string
                
                return mstat
            
            except smtplib.SMTPRecipientsRefused, details:
                info_string = 'Error mail not sent, problem in Recepients %s\n%s' % (sendToList,_utils.formattedException(details=details))
                if self.log is not None:
                    self.log.exception(info_string)
                else:
                    print >>sys.stderr, info_string
                
                return info_string

            except Exception, details:
                info_string = 'Error in delivering e-mail to one of %s\n%s' % (sendToList,_utils.formattedException(details=details))
                if self.log is not None:
                    self.log.exception(info_string)
                    self.log.exception(' %s ERROR:%s', Exception, e)
                else:
                    print >>sys.stderr, info_string
                
                return info_string

    def getSendResults(self, message, emailResults):
        """
        generic mail sending results printing
        accepts Message object and results structure
        """
        subject = message.subject
        
        toAddrDict = {}
        for toAddr in message.toAddList:
            if emailResults is None: 
                toAddrDict[toAddr] = False
                
            elif hasattr(emailResults, 'recipients'):
                bounces = emailResults.recipients
                
                if bounces.has_key(toAddr):
                    toAddrDict[toAddr] = False
                    
            else:                            
                toAddrDict[toAddr] = True
                
        if emailResults == {}:
            toAlias = message.toAddList
            
            msg = 'Sent TO %s AS %s' % (toAlias, subject[:80])
                
        else:
            for toAddr in toAddrDict.keys():
                if toAddrDict.get(toAddr):
                    msg = 'Sent TO %s AS %s' %(toAddr, subject[:80])
                        
                else:
                    msg = "Email to %s failed %s" %(toAddr, emailResults)
                    if self.log is not None:
                        self.log.error(msg)
                    
        return msg

# The GMailServer MailServer subclass does the job - don't use the others for anything other than testing...
class GMailServer(MailServer):
    def __init__(self,username,password,server='smtp.gmail.com',port=587,logger=None):
        self.__smtp_server__ = server
        self.__smtp_port__ = port

        toks = server.split(':')
        if (len(toks) > 1):
            self.__smtp_server__ = toks[0]
            self.__smtp_port__ = 25 if (len(toks) == 1) else toks[-1] if (not toks[-1].isdigit()) else int(toks[-1])

        self.__smtp_username__ = username
        self.__smtp_password__ = password
        self.__logger__ = logger

    def _sendEmail(self, _from, _to, _message, isDebug=False):
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        if (isDebug):
            server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.ehlo()
        if (len(self.smtp_username) > 0) and (len(self.smtp_password) > 0):
            server.login(self.smtp_username, self.smtp_password)
        server.sendmail(_from, _to, _message)
        server.quit()
    
    def sendEmail(self, email_message, trial=False, isDebug=False):
        self._sendEmail(email_message.fromAdd, email_message.toAddList, email_message.message, isDebug=isDebug)

class SMTPServer(GMailServer):
    def _sendEmail(self, _from, _to, _message, isDebug=False):
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        if (isDebug):
            server.set_debuglevel(1)
        if (len(self.smtp_username) > 0) and (len(self.smtp_password) > 0):
            server.login(self.smtp_username, self.smtp_password)
        server.sendmail(_from, _to, _message)
        server.quit()

class SvnDynOSaurServer(MailServer):
    def __init__(self,logger=None):
        self.__smtp_server__ = 'svn.dyn-o-saur.com'
        self.__smtp_port__ = 25
        self.__smtp_username__ = ''
        self.__smtp_password__ = ''
        self.__logger__ = logger
        self.login()

class LocalhostServer8025(MailServer):
    def __init__(self,logger=None):
        self.__smtp_server__ = '127.0.0.1'
        self.__smtp_port__ = 8025
        self.__smtp_username__ = ''
        self.__smtp_password__ = ''
        self.__logger__ = logger
        self.login()

class LocalhostServer(MailServer):
    def __init__(self,logger=None):
        self.__smtp_server__ = '127.0.0.1'
        self.__smtp_port__ = 25
        self.__smtp_username__ = ''
        self.__smtp_password__ = ''
        self.__logger__ = logger
        self.login()

class AdhocServer(MailServer):
    def __init__(self,smtp_server,username='',password='',logger=None):
        toks = smtp_server.split(':')
        self.__smtp_server__ = toks[0]
        self.__smtp_port__ = 25 if (len(toks) == 1) else toks[-1] if (not toks[-1].isdigit()) else int(toks[-1])
        self.__smtp_username__ = username
        self.__smtp_password__ = password
        self.__logger__ = logger
        self.login()
        
class GoDaddyServer(Cooperative):
    def __init__(self,username,password,server='smtpout.secureserver.net:3535'):
        toks = server.split(':')
        self.__server__ = toks[0]
        self.__port__ = 25 if (len(toks) == 1) else toks[-1] if (not toks[-1].isdigit()) else int(toks[-1])
        self.__username__ = username
        self.__password__ = password
        self.__lastError__ = ''
        
    def sendEmail(self,to_addr,from_addr,subject,message):
        import os, sys
        import smtplib
        server = smtplib.SMTP(self.__server__)
        try:
            server.login(self.__username__, self.__password__)
        except smtplib.SMTPAuthenticationError, details:
            self.__lastError__ = str(details)
        
        msg = (
        "To: %s\r\n"
        "From: %s\r\n"
        "Subject: %s\r\n"
        "Content-type: text/plain\r\n"
        "\r\n"
        "%s\r\n" % (to_addr,from_addr,subject,message))
        
        try:
            server.sendmail(from_addr, to_addr, msg)
            server.quit()
        except smtplib.SMTPAuthenticationError, details:
            self.__lastError__ = str(details)
