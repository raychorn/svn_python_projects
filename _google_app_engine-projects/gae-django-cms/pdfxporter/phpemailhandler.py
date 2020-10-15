### in phpemailhandler.py
import logging
import urllib
from wsgiref.handlers import CGIHandler
from google.appengine.api.taskqueue import TransientError, taskqueue
from users.g import send_php_email, __EMAIL_POST_ADDRESS__
def wsgi_app(env, res):
    results = ''
    try:
        token = '/'.join(env['PATH_INFO'].split('/')[-4:-1])
        info_string = '%s :: 1. (%s)' % (__name__,', '.join(['%s=%s'%(k,v) for k,v in env.iteritems()]))
        results += info_string + '\n\n'
        logging.warning(info_string)
        info_string = '%s :: 2. token=(%s)' % (__name__,token)
        results += info_string + '\n\n'
        logging.warning(info_string)
        
        tokens = env['wsgi.input'].getvalue().split('&')
	_parms = {}
	for token in tokens:
	    toks = token.split('=')
	    _parms[toks[0]] = urllib.unquote_plus(toks[-1])
        info_string = '%s :: 2.1 tokens=(%s)' % (__name__,str(tokens))
        logging.warning(info_string)

	results += send_php_email(__EMAIL_POST_ADDRESS__,parms=_parms)
    except Exception, e:
        logging.error('%s :: %s' % (__name__,e))
    
    res('200 OK',[('Content-Type','text/plain')])
    return ['%s :: ok\n\n%s' % ('phpemailhandler.py',results)]
def main():
    CGIHandler().run(wsgi_app)
    
if __name__ == '__main__':
    main()