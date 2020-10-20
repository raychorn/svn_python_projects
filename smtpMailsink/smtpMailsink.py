import os, sys, time
import types
import logging
import traceback
import socket

from vyperlogix import misc

from vyperlogix.mail import message
from vyperlogix.sockets import SmtpMailsink
from vyperlogix.sockets import sniffer

from vyperlogix.misc import ObjectTypeName

from vyperlogix import oodb
from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.daemon.daemon import Log
from vyperlogix.logging import standardLogging
from vyperlogix.enum import Enum

from vyperlogix.lists import ListWrapper

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix.misc.ReportTheList import reportTheList

const_DEFAULT_HOST = '127.0.0.1'
const_DEFAULT_PORT = 25

_timeout = lists.HashedLists2({'False':-1, 'True':-1}) # -1 means no timeout otherwise there is a timeout...

from vyperlogix.misc import threadpool

_Q_ = threadpool.ThreadQueue(5)

_retry_Q = [] # contains tuple list where t[0] is the message tuple and t[-1] is the number of seconds to wait before trying again...
_additions_Q = [] # contains tuple list where t[0] is the message tuple and t[-1] is the number of seconds to wait before trying again...

__product__ = 'SMTP Mail Sink'
__version__ = '1.0.0'

__copyright__ = """\
%s %s
(c). Copyright 1990-%s, Vyper Logix Corp., 

              All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only
unless a suitable Right to Use has been obtained., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
""" % (__product__,__version__,_utils.timeStamp(format=_utils.formatDate_YYYY()))

def reportTheRetryQueue(reports_path,lst):
    if (misc.isList(lst)):
	_files = os.listdir(reports_path)
	_files.sort()
	n = len(_files) if (len(_files) < 20) else 20
	for f in _files[0:len(_files)-n]:
	    _f = os.sep.join([reports_path,f])
	    if (os.path.exists(_f)):
		os.remove(_f)
	fOut = _utils.stringIO()
	reportTheList(lst,'Sendmail Retry Queue',fOut=fOut)
	fname = os.sep.join([reports_path,'Sendmail_Retry_Queue_%s.txt' % (_utils.timeStampForFileName())])
	_utils.writeFileFrom(fname,fOut.getvalue())
    else:
	info_string = 'Unable to report the retry queue using the parameter that is of type "%s" but is supposed to be a list.' % (type(lst))
	SmtpMailsink.logMessage(info_string,__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.error)

@threadpool.threadify(_Q_)
def retrySendmail(reports_path,retry_Q,_mailserver):
    _retry_Q = misc.copy(retry_Q)
    while (1):
	new_Q = []
	try:
	    reportTheRetryQueue(reports_path,_retry_Q)
	    for t in _retry_Q:
		isError_sendMail = False
		i = t[-1]
		i -= 1
		t[-1] = i
		if (t[-1] <= 0):
		    try:
			_from,_to,_body,_subj = t[0]
			msg = message.Message(_from,_to,_body,_subj)
			_mailserver.sendEmail(msg)
		    except:
			isError_sendMail = True
			exc_info = sys.exc_info()
			info_string = '\n'.join(traceback.format_exception(*exc_info))
			info_string = '(%s) :: Cannot retry redirect email from "%s" to "%s". Reason: %s' % (misc.funcName(),_from,_to,info_string)
			SmtpMailsink.logMessage(info_string,__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.error)
		    t[-1] = 30
		if (isError_sendMail):
		    new_Q.append(t)
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    info_string = '(%s) :: Cannot retry email. Reason: %s' % (misc.funcName(),info_string)
	    SmtpMailsink.logMessage(info_string,__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.error)
	while (len(_additions_Q) > 0):
	    item = _additions_Q.pop()
	    new_Q.append(item)
	while (len(_retry_Q) > 0):
	    item = _retry_Q.pop()
	for t in new_Q:
	    _retry_Q.append(t)
	time.sleep(5)

if (__name__ == '__main__'):
    _isVerbose = False

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--cwd=?':'the path the program runs from, defaults to the path the program runs from.',
	    '--host=?':'ths host:port for the mail server proxy to which users of this service connect to when sending emails.',
	    '--redirect=?':'the host:port for the out-going mail server, or "gmail" to use gmail.',
	    '--username=?':'the username for the email service stated by the --redirect= option.',
	    '--password=?':'the password for the email service stated by the --redirect= option.',
	    '--bcc=?':'email address to which a copy should be sent as a Bcc.',
	    '--debug':'debug some stuff.',
	    '--logging=?':'[logging.INFO,logging.WARNING,logging.ERROR,logging.DEBUG]',
	    '--console_logging=?':'[logging.INFO,logging.WARNING,logging.ERROR,logging.DEBUG]'}
    _argsObj = Args.Args(args)
    if (_isVerbose):
	print '_argsObj=(%s)' % str(_argsObj)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = _argsObj.programName
	_isVerbose = False
	try:
	    if _argsObj.booleans.has_key('isVerbose'):
		_isVerbose = _argsObj.booleans['isVerbose']
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    logging.warning('(%s) :: Cannot read --verbose option. Reason: %s' % (misc.funcName(),info_string))
	    _isVerbose = False
	    
	_isHelp = False
	try:
	    if _argsObj.booleans.has_key('isHelp'):
		_isHelp = _argsObj.booleans['isHelp']
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    logging.warning('(%s) :: Cannot read --help option. Reason: %s' % (misc.funcName(),info_string))
	
	if (_isHelp):
	    ppArgs()
	
	_isDebug = False
	try:
	    if _argsObj.booleans.has_key('isDebug'):
		_isDebug = _argsObj.booleans['isDebug']
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    logging.warning('(%s) :: Cannot read --debug option. Reason: %s' % (misc.funcName(),info_string))
	
	hostname = SmtpMailsink.const_DEFAULT_HOST
	_port = port = SmtpMailsink.const_DEFAULT_PORT
	try:
	    if _argsObj.arguments.has_key('host'):
		toks = _argsObj.arguments['host'].split(':')
		hostname = toks[0]
		port = int(toks[-1]) if (len(toks) > 1) else _port
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    logging.warning('(%s) :: Cannot read --host=? option. Reason: %s' % (misc.funcName(),info_string))
	
	is_using_redirect = False
	_redirect_hostname = SmtpMailsink.const_DEFAULT_HOST
	_redirect_port = SmtpMailsink.const_DEFAULT_PORT
	try:
	    if _argsObj.arguments.has_key('redirect'):
		toks = _argsObj.arguments['redirect'].split(':')
		_redirect_hostname = toks[0]
		_redirect_port = int(toks[-1]) if (len(toks) > 1) else _port
		is_using_redirect = True
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    logging.warning('(%s) :: Cannot read --redirect=? option. Reason: %s' % (misc.funcName(),info_string))

	_bcc = ''
	try:
	    if _argsObj.arguments.has_key('bcc'):
		_bcc = _argsObj.arguments['bcc']
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    logging.warning('(%s) :: Cannot read --bcc=? option. Reason: %s' % (misc.funcName(),info_string))

	_username = ''
	try:
	    if _argsObj.arguments.has_key('username'):
		_username = _argsObj.arguments['username']
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    logging.warning('(%s) :: Cannot read --username=? option. Reason: %s' % (misc.funcName(),info_string))

	_password = ''
	try:
	    if _argsObj.arguments.has_key('password'):
		_password = _argsObj.arguments['password']
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    logging.warning('(%s) :: Cannot read --password=? option. Reason: %s' % (misc.funcName(),info_string))

	__cwd__ = os.path.dirname(sys.argv[0])
	try:
	    __cwd = _argsObj.arguments['cwd'] if _argsObj.arguments.has_key('cwd') else __cwd__
	    if (len(__cwd) == 0) or (not os.path.exists(__cwd)):
		if (os.environ.has_key('cwd')):
		    __cwd = os.environ['cwd']
	    __cwd__ = __cwd
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    logging.warning('(%s) :: Cannot read --cwd=? option. Reason: %s' % (misc.funcName(),info_string))
	_cwd = __cwd__

	ts_last_email = -1
	is_getting_emails = lambda x:(x > -1)
	s_is_getting_emails = lambda x:'%s' % (x > -1)
	_num_messages = 0

	is_raw_email_message = lambda x:(str(x).find('Content-Type:') == -1) and (str(x).find('MIME-Version: 1.0') == -1)
	
	from vyperlogix.mail import mailServer
	print 'is_using_redirect is "%s".' % (is_using_redirect)
	if (is_using_redirect):
	    if (_redirect_hostname == 'gmail') and (len(_username) > 0) and (len(_password) > 0):
		#from vyperlogix.crypto import XTEAEncryption
		#username = XTEAEncryption._decryptode('396916F013B1C6001BF60ECDAE29BF0F02787AA8',XTEAEncryption.iv('smtpMailsink'))
		#password = XTEAEncryption._decryptode('3F7503FE00BF9957',XTEAEncryption.iv('smtpMailsink'))
		print '_username is "%s" and _password is "%s".' % (_username,_password)
		mailserver = mailServer.GMailServer(_username,_password)
	    else:
		mailserver = mailServer.GMailServer('','',server=_redirect_hostname,port=_redirect_port)
	    mailserver.debug = _isDebug
	    print '_redirect_hostname is "%s", mailserver is "%s" and _isDebug is "%s".' % (_redirect_hostname,str(mailserver),_isDebug)
	
	def callback(d,from_addrs,to_addrs,data):
	    global _num_messages
	    global ts_last_email
	
	    if (is_using_redirect):
		if (_isDebug):
		    _out = _utils.stringIO()
		    d.prettyPrint(fOut=_out)
		    SmtpMailsink.logMessage('d=%s' % (_out.getvalue()),__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.info)

		SmtpMailsink.logMessage('from_addrs=%s, to_addrs=%s' % (from_addrs,to_addrs),__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.info)
		try:
		    from vyperlogix.mail import html
		    _is_raw_email_message_ = is_raw_email_message(data)
		    _subj = ''
		    if (_is_raw_email_message_):
			lines = ListWrapper.ListWrapper(data.split('\n'))
    
			def fuzzyCompare(_item,s_search):
			    f = lambda _item,s_search:_item.lower().find(s_search.lower()) > -1
			    does_match = f(_item,s_search)
			    return does_match
			
			s_subj_target = 'Subject: '
			i_subj = lines.findFirstContaining(s_subj_target,callback=fuzzyCompare)
			if (i_subj > -1):
			    toks = lines[i_subj].split(s_subj_target)
			    _subj = toks[-1]
			data = '<BR/>'.join(lines)
			m_body = html.asHTMLOnlyEmail(to_addrs,from_addrs,data,data,_subj)
		    else:
			m_body = data
		    
		    try:
			info_string = '(%s) :: from_addrs=%s, to_addrs=%s' % (misc.funcName(),from_addrs,to_addrs)
			SmtpMailsink.logMessage(info_string,__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.error)
			mailserver._sendEmail(from_addrs,to_addrs,m_body)
		    except:
			exc_info = sys.exc_info()
			info_string = '\n'.join(traceback.format_exception(*exc_info))
			info_string = '(%s) :: Cannot redirect email from "%s" to "%s". Reason: %s' % (misc.funcName(),from_addrs,to_addrs,info_string)
			SmtpMailsink.logMessage(info_string,__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.error)
	
		    if (len(_bcc) > 0) and (to_addrs != _bcc):
			try:
			    mailserver._sendEmail(from_addrs,_bcc,m_body)
			except:
			    exc_info = sys.exc_info()
			    info_string = '\n'.join(traceback.format_exception(*exc_info))
			    info_string = '(%s) :: Cannot redirect email from "%s" to "%s". Reason: %s' % (misc.funcName(),from_addrs,_bcc,info_string)
			    SmtpMailsink.logMessage(info_string,__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.warning)
		    elif (_isDebug):
			SmtpMailsink.logMessage('No need to Bcc an email with Subject of "%s" to "%s" because Bcc is the same as To address.' % (_subj,to_addrs),__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.info)
		except:
		    exc_info = sys.exc_info()
		    info_string = '\n'.join(traceback.format_exception(*exc_info))
		    info_string = '(%s) :: Cannot redirect email from "%s" to "%s". Reason: %s' % (misc.funcName(),from_addrs,to_addrs,info_string)
		    SmtpMailsink.logMessage(info_string,__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.error)
	    
	    _num_messages += 1
	    ts_last_email = _utils.timeSeconds()
	    SmtpMailsink.logMessage('ts_last_email=%s, _num_messages=%s' % (ts_last_email,_num_messages),__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.info)
	
	_name = _utils.getProgramName()
	_log_path = _utils.safely_mkdir_logs(fpath=_cwd)
	_log_path = os.sep.join([_log_path,_utils.timeStampForFileName().split('_')[0]])
	_log_path = _utils.safely_mkdir(fpath=_log_path,dirname='')
	logFileName = os.sep.join([_log_path,'%s.log' % (_name)])
	
	_reports_path = _utils.safely_mkdir(fpath=_log_path,dirname='reports')

	sys.stderr = sys.stdout
    
	try:
	    _addr_info = socket.getaddrinfo(hostname,port)[0][-1]
	    _isListenerActive = sniffer.isListenerActive(_addr_info)
	    print 'About to Start SMTP Server as %s:%s, _isListenerActive=%s.' % (_addr_info[0],_addr_info[-1],_isListenerActive)
	    if (not _isListenerActive):
		_logging = logging.INFO
		standardLogging.standardLogging(logFileName,_level=_logging,console_level=logging.WARNING,isVerbose=True)
	
		smtpMailsink = SmtpMailsink.SmtpMailsink( host=_addr_info[0], port=_addr_info[-1], cwd=_cwd, callback=callback, author='Ray C Horn <raychorn@vyperlogix.com>', copyright=__copyright__ )
		smtpMailsink.start()
		print 'Started SMTP Server as %s' % smtpMailsink
    
		sys.stdout = Log(open(os.sep.join([_log_path,'stdout.txt']),'w'))
		sys.stderr = Log(open(os.sep.join([_log_path,'stderr.txt']),'w'))
    
		print >>sys.stdout, 'Logging to "%s" using level of "%s:.' % (logFileName,standardLogging.explainLogging(_logging))
		
		if (is_using_redirect):
		    retrySendmail(_reports_path,_retry_Q,mailserver) # start the retry loop as a background process...
		
		_debug_ = _isDebug
		ts_start = _utils.timeSeconds()
		while True:
		    if (_debug_):
			_is_getting_emails_ = s_is_getting_emails(ts_last_email)
			_timeout_ = _timeout[_is_getting_emails_]
			info_string = '(1) is_getting_emails is %s.' % (_is_getting_emails_)
			SmtpMailsink.logMessage(info_string,__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.info)
			if (_timeout_ > -1):
			    if (not is_getting_emails(ts_last_email)):
				info_string = '(2) e.t. is %s of %s.' % ((_utils.timeSeconds() - ts_start),_timeout_)
				SmtpMailsink.logMessage(info_string,__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.info)
				if ((_utils.timeSeconds() - ts_start) > _timeout_):
				    info_string = '(3) Stopping due to lack of activity.'
				    SmtpMailsink.logMessage(info_string,__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.info)
				    break
			    else:
				info_string = '(2.1) e.t. is %s of %s.' % ((_utils.timeSeconds() - ts_last_email),_timeout_)
				SmtpMailsink.logMessage(info_string,__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.info)
				if ((_utils.timeSeconds() - ts_last_email) > _timeout_):
				    info_string = '(3.1) Stopping due to lack of activity.'
				    SmtpMailsink.logMessage(info_string,__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.info)
				    break
			else:
			    _debug_ = False
			    info_string = '(+++) There is no timeout...  No reason to debug anything.'
			    SmtpMailsink.logMessage(info_string,__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.info)
		    time.sleep(1)
	    else:
		print >>sys.stdout, '%s is already running on this computer.  No need to do so again.' % _utils.getProgramName()
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    SmtpMailsink.logMessage(info_string,__name__,misc.funcName(),_logging=standardLogging.LoggingLevels.error)
	finally:
	    sys.stdout.close()
	    sys.stderr.close()
	    sys.exit( 1 )
