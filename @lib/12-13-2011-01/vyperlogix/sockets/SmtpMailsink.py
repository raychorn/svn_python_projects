import os, sys, asyncore, threading, socket, smtpd, time
import types
import logging
import traceback

from vyperlogix.misc import ReportTheList

from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc.ObjectTypeName import __typeName as ObjectTypeName__typeName
from vyperlogix.misc import _utils
from vyperlogix import misc
from vyperlogix.hash import lists
from vyperlogix.daemon.daemon import Log
from vyperlogix.logging import standardLogging
from vyperlogix.enum import Enum

__version__ = '1.1'

const_DEFAULT_HOST = '127.0.0.1'
const_DEFAULT_PORT = 25

const_from_symbol = 'From:'
const_to_symbol = 'To:'
const_subject_symbol = 'Subject:'
const_body_symbol = 'Body'
const_headers_symbol = 'Headers'

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

def dummy_callback():
    pass

def logMessage(info_string, fromObjName, fromFunc, _logging=standardLogging.LoggingLevels.info):
    info_string = '%s.%s %s' % (fromObjName,fromFunc,info_string)
    print >> sys.stdout, info_string
    if (_logging.value == standardLogging.LoggingLevels.info.value):
        logging.info(info_string)
    elif (_logging.value == standardLogging.LoggingLevels.warning.value):
        logging.warning(info_string)
    elif (_logging.value == standardLogging.LoggingLevels.error.value):
        logging.error(info_string)
    elif (_logging.value == standardLogging.LoggingLevels.debug.value):
        logging.debug(info_string)

class SmtpMailsinkServer(smtpd.SMTPServer):
    __version__ = 'Python SMTP Mail Sink version 0.1'
    _count_messages = 0

    def __init__( self, *args, **kwargs):
        self.callback = dummy_callback
        smtpd.SMTPServer.__init__( self, *args, **kwargs )
        self.mailboxFile = None
        self.multi_file = True
        self.is_debugging = False
        self.use_html = True
	self.author = 'Vyper Logix Corp. <http://www.vyperlogix.com>'
	self.__author__ = self.author
	self.copyright = '(c). Copyright 1990-%s, Vyper Logix Corp., All Right Reserved., You must ontain the right to use.' % (_utils.timeStamp(format=_utils.formatDate_YYYY()))
	self.__copyright__ = self.copyright
	self.cwd = os.path.abspath(os.curdir)

    def setMailsinkFile( self, mailboxFile ):
        self.mailboxFile = mailboxFile
        
    def parseMessage(self,data):
	from vyperlogix.lists.ListWrapper import ListWrapper

	def fuzzyCompare(_item,s_search):
	    f = lambda _item,s_search:_item.lower().find(s_search.lower()) > -1
	    does_match = f(_item,s_search)
	    return does_match
	
	def emptyCompare(_item,s_search):
	    f = lambda _item,s_search:str(_item).strip() == s_search
	    does_match = f(_item,s_search)
	    return does_match
	
	def parse_for_target(_toks,_target,callback=None):
	    _val = ''
	    i = _toks.findFirstContaining(_target,callback=callback)
	    if (i > -1):
		_val = [_toks[i].split(_target)[-1]]
	    return _val
	
	toks = ListWrapper(data.split('\n'))
	
        d = lists.HashedLists2()

	_f = toks.findFirstContaining('',callback=emptyCompare)
	if (_f > -1):
	    _f -= 1
	
	d[const_headers_symbol] = tuple([t.strip() for t in toks[0:_f]])
	d[const_body_symbol] = tuple([t.strip() for t in toks[_f+1:]])

	d[const_from_symbol] = parse_for_target(toks,const_from_symbol,callback=fuzzyCompare)

	d[const_to_symbol] = parse_for_target(toks,const_to_symbol,callback=fuzzyCompare)
	
	d[const_subject_symbol] = parse_for_target(toks,const_subject_symbol,callback=fuzzyCompare)

        return d
    
    def renderHTML(self,subj,body):
	from vyperlogix.html import myOOHTML as oohtml
	h_html = oohtml.Html()
	
	def renderBody(_body):
	    h = oohtml.Html()
	    h_html = h.tag(oohtml.oohtml.HTML)
	    h_body = h_html.tag(oohtml.oohtml.BODY)
	    h_Content = h_body.tag(oohtml.oohtml.DIV, id="content", style="background-color: white")
	    _body = _body[0] if (misc.isList(_body)) and (len(_body) == 1) else _body
	    h_Content.text(_body[0])
	    if (len(_body) > 1):
		for b in _body[1:]:
		    h_Content.tagOp(oohtml.oohtml.BR)
		    h_Content.text(b)
	    return h_Content.toHtml()
	    

	if (not misc.isString(subj)):
	    subj = str(subj)
	if (not misc.isList(body)):
	    body = [body]
	if (misc.isString(subj)) and (misc.isList(body)):
	    h_html.text(oohtml.oohtml.DOCTYPE_40_TRANSITIONAL)
	    
	    _title = "Vyper Logix SMTP Email Proxy (%s v.%s)" % (ObjectTypeName.typeName(self),__version__)
	    html_html = h_html.tag(oohtml.oohtml.HTML)
	    head_html = html_html.tag(oohtml.oohtml.HEAD)
	    head_html.tagOp(oohtml.oohtml.META, http_equiv=oohtml.oohtml.CONTENT_TYPE, content=oohtml.oohtml.TEXT_HTML_CHARSET_ISO_8859_1)
	    head_html.metas(
		    (oohtml.oohtml.AUTHOR, '%s :: %s' % (self.author,self.__author__)),
		    (oohtml.oohtml.KEYWORDS, _title),
		    (oohtml.oohtml.DESCRIPTION, "The contents of this email are considered to be confidential unless otherwise specified."),
		    (oohtml.oohtml.ROBOTS, oohtml.oohtml.ALL))
	    head_html.tagTITLE('&copy;%s, Vyper Logix Corp., All Rights Reserved., %s' % (_utils.timeStamp(format=_utils.formatDate_YYYY()),_title))
	    body_html = html_html.tag(oohtml.oohtml.BODY)
	    idContent = body_html.tag(oohtml.oohtml.DIV, id="content", style="background-color: white")
    
	    rows = []
	    rows.append(tuple(['%s' % (subj)]))
	    rows.append(tuple([renderBody(body)]))
	    rows.append(tuple(['<BR/><BR/><BR/><BR/>']))
	    rows.append(tuple([self.copyright if (misc.isString(self.copyright)) and (len(self.copyright) > 0) else self.__copyright__]))
	    idContent.html_table(rows)
	    pass
	else:
	    logMessage('subj must be of type str and body must be of type list rather than of types "%s" and "%s", respectively.' % (type(subj),type(body)),ObjectTypeName.typeName(self),misc.funcName(),_logging=standardLogging.LoggingLevels.warning)
	return h_html.toHtml()
        
    def process_message(self, peer, mailfrom, rcpttos, data):
	f_unpack = lambda foo,key:foo[key][0] if (misc.isList(foo[key])) else foo[key]
        try:
	    SmtpMailsinkServer._count_messages += 1
	    try:
		d = self.parseMessage(data)
	    except:
		exc_info = sys.exc_info()
		info_string = '\n'.join(traceback.format_exception(*exc_info))
		logMessage(info_string,ObjectTypeName.typeName(self),misc.funcName(),_logging=standardLogging.LoggingLevels.error)
	    if (self.multi_file):
		_toAddr = f_unpack(d,const_to_symbol)
		_path = _utils.safely_mkdir(fpath=self.cwd,dirname=os.sep.join(['mailboxes',_toAddr]))
		_fMbx = self.mailboxFile
		self.mailboxFile = open('%s.%s' % (os.sep.join([_path,_utils.timeStamp().replace(':','')]),'html' if (self.use_html) else 'txt'),'w')
	    info_string = 'DEBUG: self.mailboxFile is "%s".' % (self.mailboxFile)
	    logMessage(info_string,ObjectTypeName.typeName(self),misc.funcName(),_logging=standardLogging.LoggingLevels.error)
            if self.mailboxFile is not None:
		#_utils.print_stderrout("Mail From is %s\n" % mailfrom)
		try:
		    io_buffer = _utils.stringIO()
		    if (self.is_debugging):
			d.prettyPrint(prefix='',title='Mail Parts',fOut=io_buffer)
		    else:
			if (self.use_html):
			    print >>io_buffer, self.renderHTML(f_unpack(d,const_subject_symbol),f_unpack(d,const_body_symbol))
			else:
			    print >>io_buffer, '%s' % (f_unpack(d,const_subject_symbol))
			    print >>io_buffer, '%s' % ('\n'.join(f_unpack(d,const_body_symbol)))
		    s = io_buffer.getvalue()
		    self.mailboxFile.write( s )
		except:
		    exc_info = sys.exc_info()
		    info_string = '\n'.join(traceback.format_exception(*exc_info))
		    logMessage(info_string,ObjectTypeName.typeName(self),misc.funcName(),_logging=standardLogging.LoggingLevels.error)
		#self.mailboxFile.write( "="*80 )
		#self.mailboxFile.write( "\n\n" )
		self.mailboxFile.flush()
		if (self.multi_file):
		    self.mailboxFile.close()
		    self.mailboxFile = _fMbx
	    else:
		print >>sys.stderr, 'ERROR: self.mailboxFile is "%s".' % (self.mailboxFile)
	    
	    if (callable(self.callback)):
		try:
		    info_string = 'DEBUG: mailfrom is "%s", rcpttos is "%s".' % (mailfrom,rcpttos)
		    logMessage(info_string,ObjectTypeName.typeName(self),misc.funcName(),_logging=standardLogging.LoggingLevels.error)
		    self.callback(d,mailfrom,rcpttos,data)
		except:
		    exc_info = sys.exc_info()
		    info_string = '\n'.join(traceback.format_exception(*exc_info))
		    logMessage(info_string,ObjectTypeName.typeName(self),misc.funcName(),_logging=standardLogging.LoggingLevels.error)
	    else:
		logMessage('Cannot issue callback because callback is not callable.',ObjectTypeName.typeName(self),misc.funcName(),_logging=standardLogging.LoggingLevels.warning)

	    info_string = 'SmtpMailsinkServer._count_messages=%d' % (SmtpMailsinkServer._count_messages)
	    logMessage(info_string,ObjectTypeName.typeName(self),misc.funcName(),_logging=standardLogging.LoggingLevels.info)
        except:
            exc_info = sys.exc_info()
            info_string = '\n'.join(traceback.format_exception(*exc_info))
            logMessage(info_string,ObjectTypeName.typeName(self),misc.funcName(),_logging=standardLogging.LoggingLevels.error)

class SmtpMailsink( threading.Thread ):
    TIME_TO_WAIT_BETWEEN_CHECKS_TO_STOP_SERVING = 0.001
    DEFAULT_PORT = const_DEFAULT_PORT

    def __init__( self, host=const_DEFAULT_HOST, port=const_DEFAULT_PORT, cwd=os.path.abspath(os.curdir), mailboxFile=None, threadName=None, callback=dummy_callback, author=None, copyright=None ):
        self.__host__ = host if (len(host) > 0) else const_DEFAULT_HOST
        self.__port__ = port if isinstance(port,int) and (port > -1) else SmtpMailsink.DEFAULT_PORT
        self.throwExceptionIfAddressIsInUse( self.host, self.port )
        self.initializeThread( threadName )
        self.initializeSmtpMailsinkServer( self.host, self.port, cwd, mailboxFile, callback=callback, author=author, copyright=copyright )
        
    def __str__(self):
	try:
	    return '(%s) on %s using "%s".' % (ObjectTypeName__typeName(self.__class__),self.hostPort(),self.mailboxFile.name)
	except:
	    pass
	return '(%s) on %s.' % (ObjectTypeName__typeName(self.__class__),self.hostPort())

    def hostPort(self):
        return '%s:%s' % (self.host,self.port)
    
    def host_port():
        doc = "host name and port in the form of host:port"
        def fget(self):
            return self.hostPort()
        def fset(self,hostname):
            toks = hostname.split(':')
            self.__host__ = toks[0]
            self.__port__ = int(toks[-1]) if (len(toks) > 1) and (str(toks[-1]).isdigit()) and (int(toks[-1]) > -1) else SmtpMailsink.DEFAULT_PORT
        return locals()    
    host_port = property(**host_port())

    def host():
        doc = "host name"
        def fget(self):
            return self.__host__
        def fset(self,hostname):
            self.host_port = hostname
        return locals()    
    host = property(**host())

    def port():
        doc = "port number"
        def fget(self):
            return self.__port__
        def fset(self,port):
            self.__port__ = port if isinstance(port,int) and (port > -1) else SmtpMailsink.DEFAULT_PORT
        return locals()    
    port = property(**port())

    def throwExceptionIfAddressIsInUse( self, host, port ):
        testSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        testSocket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR,
                               testSocket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) | 1 )
        testSocket.bind( ( host, port ) )
        testSocket.close()

    def initializeThread( self, threadName ):
        self._stopevent = threading.Event()
        self.threadName = threadName
        if self.threadName is None:
            self.threadName = SmtpMailsink.__class__
        threading.Thread.__init__( self, name = self.threadName )
        
    def initializeSmtpMailsinkServer( self, host, port, cwd, mailboxFile, callback=dummy_callback, author=None, copyright=None ):
        self.smtpMailsinkServer = SmtpMailsinkServer( ( host, port ), None)
        self.smtpMailsinkServer.callback = callback 
	self.smtpMailsinkServer.cwd = cwd
	self.smtpMailsinkServer.author = author
	self.smtpMailsinkServer.copyright = copyright
        self.resetMailbox( mailboxFile )
        smtpd.__version__ = SmtpMailsinkServer.__version__ 
                
    def resetMailbox( self, mailboxFile = None ):
        self.mailboxFile = mailboxFile
        if self.mailboxFile is None:
            self.mailboxFile = _utils.stringIO()
        self.smtpMailsinkServer.setMailsinkFile( self.mailboxFile )

    def getMailboxContents( self ):
        return self.mailboxFile.getvalue()
    
    def getMailboxFile( self ):
        return self.mailboxFile
    
    def run( self ):
        while not self._stopevent.isSet():
            asyncore.loop( timeout = SmtpMailsink.TIME_TO_WAIT_BETWEEN_CHECKS_TO_STOP_SERVING, count = 1 )

    def stop( self, timeout=None ):
        self._stopevent.set()
        threading.Thread.join( self, timeout )
        self.smtpMailsinkServer.close()
        
if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
    
