import os
import sys
import web

import re

import json
import urllib

from vyperlogix import github
from vyperlogix import paramiko

from vyperlogix import misc
from vyperlogix.lists import ConsumeableList
from vyperlogix.misc import ObjectTypeName

from vyperlogix.classes import SmartObject

import utils

import settings

import pyGitHubProxyMagic

from github import Github

settings.__data__.__proxy__ = SmartObject.SmartObject()

__github_client_id__ = 'd89bfe797d057ded5bcd'
__github_client_secret__ = 'dd0e228521ee0e09d666d5102c7cf5d16954b234'

__version__ = '1.0.1'

import logging
from logging import handlers

from vyperlogix.misc import _utils

LOG_FILENAME = './githubManagerServer.log'

class CannotUseGitException(Exception):
    pass

class CannotUseUnzipException(Exception):
    pass

class CommandFailedToInstall(Exception):
    pass

class TargetRepoNotAvailable(Exception):
    pass

class MyTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
    def __init__(self, filename, maxBytes=0, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False):
        handlers.TimedRotatingFileHandler.__init__(self, filename=filename, when=when, interval=interval, backupCount=backupCount, encoding=encoding, delay=delay, utc=utc)
        self.maxBytes = maxBytes

    def shouldRollover(self, record):
        response = handlers.TimedRotatingFileHandler.shouldRollover(self, record)
        if (response == 0):
            if self.stream is None:                 # delay was set...
                self.stream = self._open()
            if self.maxBytes > 0:                   # are we rolling over?
                msg = "%s\n" % self.format(record)
                try:
                    self.stream.seek(0, 2)  #due to non-posix-compliant Windows feature
                    if self.stream.tell() + len(msg) >= self.maxBytes:
                        return 1
                except:
                    pass
            return 0
        return response

logger = logging.getLogger('githubManagerServer')
handler = logging.FileHandler(LOG_FILENAME)
#handler = handlers.TimedRotatingFileHandler(LOG_FILENAME, when='d', interval=1, backupCount=30, encoding=None, delay=False, utc=False)
#handler = MyTimedRotatingFileHandler(LOG_FILENAME, maxBytes=1000000, when='d', backupCount=30)
#handler = handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1000000, backupCount=30, encoding=None, delay=False)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler) 
print 'Logging to "%s".' % (handler.baseFilename)

ch = logging.StreamHandler()
ch_format = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(ch_format)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

logging.getLogger().setLevel(logging.DEBUG)

from vyperlogix.webpy.session import Session
from vyperlogix.misc._utils import timeStampForFileName
from vyperlogix.misc._utils import formattedException

urls = (
    '/', 'Index',
    '/server/(.+)', 'GithubManagerServer',
    '/server', 'GithubManagerServer',
    '/setwindowsagentaddr', 'Nothing',
    '/setwindowsagentaddr/', 'Nothing',
)

### Templates
__fpath__ = os.path.dirname(__file__) if (os.path.isfile(__file__)) else __file__
if (os.getcwd().lower() != __fpath__):
    logger.info('Changing to directory "%s".' % (__fpath__))
    os.chdir(__fpath__)
render = web.template.render('templates', base='base')

web.template.Template.globals.update(dict(
    datestr = web.datestr,
    render = render
))

def notfound():
    return web.notfound("Sorry, the page you were looking for was not found.  This message may be seen whenever someone tries to issue a negative number as part of the REST URL Signature and this is just not allowed at this time.")

class Index:

    def GET(self):
        """ Show page """
        return render.index()

class Nothing:
    def POST(self):
	from utils import CustomJSONENcoder
        web.header('Content-Type', 'application/json')
        reasons = []
        url = web.ctx.home + web.ctx.path + web.ctx.query
        content = json.dumps(web.ctx.env,cls=CustomJSONENcoder)
        logger.info('%s --> %s %s' % (url,content,web.data()))
        content = json.dumps({'status':''.join(reasons)})
        return content

def get_all_pushable_files_from(fpath,__callback__=None):
    allfiles = _utils.get_allfiles_from(fpath,callback=__callback__,topdown=True,followlinks=True)
    allfiles = filter(os.path.isfile, allfiles)
    return allfiles

def log_all_from(items):
    for item in items:
        logger.info(item)

class GithubManagerServer:

    __PUSH_COMMAND__ = 'push'

    def GET(self, args):
        '''
        /server/push/pathname/githubuser/githubpassword/repo-name/ip-address/port/username

        http://127.0.0.1:9999/server/
        '''
        reasons = []
        exceptions = []
        status = {}
        web.header('Content-Type', 'application/json')
        toks = ConsumeableList(args.split('/'))
	
	options = settings.__data__.options
	__username__ = settings.__data__.__username__
	__password__ = settings.__data__.__password__
	__githubproxy__ = settings.__data__.__githubproxy__
	
	if (__username__) and (len(__username__) > 0) and (__password__) and (len(__password__) > 0) and (__githubproxy__) and (len(__githubproxy__) > 0):
	    __github__ = pyGitHubProxyMagic.GitHubProxyServer(__username__,__password__, __githubproxy__)
	else:
	    raise ValueError('ERROR: Invalid githubproxy="%s" or username="%s" or password="%s", due to missing or invalid information (--githubproxy=127.0.0.1:9909, --username=something, --password=something).' % (__githubproxy__,__username__,__password__))

        try:
            __cmd__ = toks[0]
            if (__cmd__ == GithubManagerServer.__PUSH_COMMAND__):
                logger.info('BEGIN PUSH.')
                __pathname__ = toks[0]
		if (not os.path.exists(__pathname__)):
		    __pathname__ = __pathname__ if (os.path.isdir(__pathname__)) else os.path.dirname(__pathname__)
		    tokens = __pathname__.replace(os.sep,'/').split('/')
		    while (len(tokens) > 0):
			token = tokens.pop()
			if (not str(token).isdigit()):
			    __pathname__ = '/'.join(tokens)
			    break
		assert(os.path.exists(__pathname__))
		if (os.path.isfile(__pathname__)):
		    __pathname__ = os.path.dirname(__pathname__)
                if (os.path.isdir(__pathname__)):
		    __callback__ = lambda top,dirs,f:True if (str(f).lower().endswith('.zip') or (str(f).lower() == 'id_rsa')) else False
                    __files__ = get_all_pushable_files_from(__pathname__,__callback__=__callback__)
                else:
                    __files__ = [__pathname__]
		__zips__ = [f for f in __files__ if (os.path.splitext(os.path.basename(f))[-1].lower() == '.zip')]
		__id_rsas__ = [f for f in __files__ if (os.path.basename(f).lower() == 'id_rsa')]
		assert(len(__zips__) == 1)
		assert(len(__id_rsas__) == 1)
		assert(len(__zips__) == len(__id_rsas__))
                __githubuser__ = toks[0]
                __githubpassword__ = toks[0]
                __repo_name__ = toks[0]
                __ip__ = str(toks[0]).lower()
                __port__ = toks[0]
                __username__ = toks[0]
		assert(str(__username__).lower() != 'root')
		__is_localhost__ = (__ip__ in ['127.0.0.1','localhost'])
                assert(len(toks) == 0)
		logger.info('__githubuser__=%s' % (__githubuser__))
		logger.info('__githubpassword__=%s' % (__githubpassword__))
		logger.info('__repo_name__=%s' % (__repo_name__))
		logger.info('__ip__=%s' % (__ip__))
		logger.info('__port__=%s' % (__port__))
		logger.info('__username__=%s' % (__username__))
		__github__.username = __githubuser__
		__github__.password = __githubpassword__
		__github__.client_id = __github_client_id__
		__github__.client_secret = __github_client_secret__
		uid = __github__.github.get.user().user__id
		assert(str(uid).isdigit())
		__email__ = __github__.github.get.user().user__email
		assert(len(__email__) > 0)
		__repos__ = __github__.github.get.user.repos().repos
		assert(len(__repos__.repos) > 0)
		__available__ = __github__.github.get.user.repos.available().available
                if (_utils.isUsingLinux):
                    pass
                elif (_utils.isUsingWindows):
                    if (_utils.isBeingDebugged):
                        __reason__ = None
                        try:
                            sftp = paramiko.ParamikoSFTP(__ip__,int(__port__),'root',callback=None,auto_close=False,logPath=None)
                            
                            __command__ = '/root/bin/zip2github.sh'
                            __remote__ = __command__
			    __Local__ = os.path.abspath('./%s' % (os.path.basename(__command__)))

			    __sftp__ = sftp.getSFTPClient
                            
                            cmd = 'ls -la %s' % (__command__)
                            __re__ = re.compile(r".*\sNo.*\ssuch.*\sfile.*\sor.*\sdirectory.*", re.MULTILINE)
                            try:
                                responses = utils.handle_command(sftp,cmd,regex=__re__,log_all_callback=log_all_from)
                            except utils.RegexMatches:
                                __reason__ = 'INSTALLED'
                                __sftp__.mkdir(os.path.dirname(__command__))
                                response = __sftp__.put(__Local__, __remote__)
                                
                                cmd = 'chmod +x %s' % (__command__)
                                responses = utils.handle_command(sftp,cmd,log_all_callback=log_all_from)
    
                            __re__ = re.compile(r"(?P<mode>[0-9]{3})\s(?P<fpath>(/)?([^/\0]+(/)?)+)", re.MULTILINE)
                            cmd = 'stat -c "%%a %%n" %s' % (__command__)
                            try:
				sftp = paramiko.ParamikoSFTP(__ip__,int(__port__),'root',callback=None,auto_close=False,logPath=None)
                                responses, matches = utils.handle_command(sftp,cmd,regex=__re__,log_all_callback=log_all_from,return_matches=True)
                            except:
                                logger.exception('Cannot continue because "%s" cannot be found on the target computer "%s:%s".' % (__remote__,__ip__,__port__))
                            _matches = [m for m in matches if (m)]
                            match = _matches[0] if (len(_matches) > 0) else None
                            if (match):
                                d_match = match.groupdict()
                                __mode__ = d_match.get('mode','000')
                                if (__mode__.find('755') == -1):
                                    raise CommandFailedToInstall()
                                else:
                                    __reason__ = 'VERIFIED' if (not __reason__) else __reason__
                                    reasons.append('COMMAND %s !!!' % (__reason__))
				    
			    __normalized_repo_name__ = github.normalize_repo_name(__repo_name__)
			    if (len(__available__.available) == 0):
				if (__normalized_repo_name__ in [r._name for r in __repos__.repos]):
				    raise TargetRepoNotAvailable('The repo ("%s") cannot be used because it already has content.' % (__repo_name__))
				else:
				    __github__.github.user.repos.create(__repo_name__)
			    else:
				if (__normalized_repo_name__ not in [r.repo__name for r in __available__.available]):
				    raise TargetRepoNotAvailable('The repo ("%s") cannot be used because it cannot be found in the available repos.' % (__repo_name__))
			    
			    __remotes__ = []
			    __sftp__ = sftp.getSFTPClient
			    for f in __files__:
				try:
				    __r__ = f
				    __r__ = __fp__ = '/root/%s' % (os.path.basename(__r__))
				    sf = __sftp__.stat(__fp__)
				    __fp__ = '/'.join([f for f in __fp__.split('/') if (len(f) > 0)][0:-1])
				    __remotes__.append(__r__)
				except IOError:
				    def __callback__(size, file_size):
					print '%4.2f %%' % ((size/file_size)*100.0)
				    __r__ = '%s' % (os.path.basename(f))
				    __sftp__.put(f, './%s' % (__r__), callback=__callback__)

			    def get_remotes_from(remotes):
				i = 1
				results = []
				for r in remotes:
				    results.append('-f%s="%s"' % (i,r))
				    i += 1
				return results
			    
			    cmd = '%s -u=%s -e="%s" -d="/%s" %s -g="git@github.com:%s/%s"' % (__command__,__username__,__email__,__fp__,' '.join(get_remotes_from(__remotes__)),__githubuser__,__normalized_repo_name__)
			    print cmd
			    print
                                    
                            # check to make sure the repo exists and is empty...
                            # then run the command...
    
                            #utils.handle_noninteractive_actions(sftp,'git',log_all_callback=log_all_from,logger=logger,exception=CannotUseGitException)
                            #utils.handle_noninteractive_actions(sftp,'unzip',log_all_callback=log_all_from,logger=logger,exception=CannotUseUnzipException)
    
                            sftp.close()
                        except CannotUseUnzipException, ex:
                            logger.exception('Failed to install unzip or it cannot be used.')
                            __exception__ = _utils.formattedException(details=ex)
                            exceptions.append(__exception__)
                        except CannotUseGitException, ex:
                            logger.exception('Failed to install git or it cannot be used.')
                            __exception__ = _utils.formattedException(details=ex)
                            exceptions.append(__exception__)
                        except CommandFailedToInstall, ex:
                            logger.exception('Failed to install "%s" or it cannot be used.' % (__command__))
                            __exception__ = _utils.formattedException(details=ex)
                            exceptions.append(__exception__)
			except TargetRepoNotAvailable, ex:
			    logger.exception('Failed to properly specify a target repo.')
			    __exception__ = _utils.formattedException(details=ex)
			    exceptions.append(__exception__)
                        except ValueError, ex:
                            logger.exception('Failed to install something or it cannot be used because the exception could not be raised due to a programming error.')
                            __exception__ = _utils.formattedException(details=ex)
                            exceptions.append(__exception__)
                        except Exception, ex:
                            logger.exception('Failed to handle the ip address, port and username correctly during development.')
                            __exception__ = _utils.formattedException(details=ex)
                            exceptions.append(__exception__)
                    else:
                        logger.warning('CANNOT PROCEED WITHOUT LINUX.')
                    logger.info('Not designed to work with Windows at this time since this part of the system was designed to work with Linux...')
		logger.info('END PUSH !!!')
            else:
                logger.warning('UNDEFINED COMMAND.')
                reasons.append('UNDEFINED COMMAND.')
        except Exception, ex:
            __exception__ = _utils.formattedException(details=ex)
            exceptions.append(__exception__)

        i = 0
        for exception in exceptions:
            status['exception_%s' % (i)] = exception
            i += 1
        
        status['status'] = ''.join(reasons)
        content = json.dumps(status)
        return content

    def POST(self):
        web.header('Content-Type', 'application/json')
        reasons = []
        data = json.loads(web.data())
        content = json.dumps({'status':reasons})
        return content

app = web.application(urls, globals())
app.notfound = notfound

if __name__ == '__main__':
    '''
    python githubManagerServer.py 127.0.0.1:9999

    python githubManagerServer.py --proxy=127.0.0.1:8888 127.0.0.1:9999
    '''
    import re
    regexes = []
    regexes.append(re.compile(r"(-|--)(?P<option>\w*)=(?P<value>%s)"%(_utils.__regex_valid_ip_and_port__), re.MULTILINE))
    regexes.append(re.compile(r"(-|--)(?P<option>\w*)=(?P<value>(([a-zA-Z])[a-zA-Z_-]*[\w_-]*[\S]$|^([a-zA-Z])[0-9_-]*[\S]$|^[a-zA-Z]*[\S]))", re.MULTILINE))
    regexes.append(re.compile(r"(-|--)(?P<option>\w*)=(?P<value>((http|https)://%s))"%(_utils.__regex_valid_ip_and_port__), re.MULTILINE))
    options = {}
    args = [arg for arg in sys.argv]
    i = 0
    for arg in sys.argv:
	for _re_ in regexes:
	    matches = _re_.match(arg)
	    if (matches):
		opts = matches.groupdict()
		if (opts.has_key('option')):
		    if (opts.has_key('value')):
			options[opts['option']] = opts['value']
		del args[i]
		i -= 1
		break
        i += 1
    sys.argv = args
    has_binding = any([_utils.is_valid_ip_and_port(arg) for arg in args])
    if (not has_binding):
        sys.argv.append('127.0.0.1:9999')
    if (options.has_key('proxy')) or (options.has_key('p')):
	__proxy__ = settings.__data__.__proxy__
	__proxy__.proxy = options['proxy'].split(':') if (options.has_key('proxy')) else options['p'].split(':') if (options.has_key('p')) else []
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
    elif (options.has_key('githubproxy')) or (options.has_key('g')):
	__githubproxy__ = options['githubproxy'] if (options.has_key('githubproxy')) else options['g'] if (options.has_key('q')) else []
	toks = __githubproxy__.split('://')
	if (len(toks) == 2):
	    if (toks[0] not in ['http', 'https']):
		toks[0] = 'http'
	elif (len(toks) == 1):
	    toks.insert(0,'http')
	else:
	    raise AttributeError('ERROR: githubproxy (%s) is not a valid value.' % (__githubproxy__))
	__githubproxy__ = '://'.join(toks)
	settings.__data__.__githubproxy__ = __githubproxy__
	assert(options.has_key('username') or options.has_key('u'))
	assert(options.has_key('password') or options.has_key('p'))
	__username__ = options['username'] if (options.has_key('username')) else options['u']
	__password__ = options['password'] if (options.has_key('password')) else options['p']
	settings.__data__.__username__ = __username__
	settings.__data__.__password__ = __password__

    settings.__data__.options = options
    
    def __init__():
        logger.info('githubManagerServer %s started !!!' % (__version__))
        app.run()

    __init__() 

