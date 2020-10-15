### in emailhandler.py
import logging
from wsgiref.handlers import CGIHandler
from google.appengine.api.taskqueue import TransientError, taskqueue
def wsgi_app(env, res):
    results = ''
    try:
        token = '/'.join(env['PATH_INFO'].split('/')[-4:-1])
        info_string = '%s :: 1. (%s)' % (__name__,', '.join(['%s=%s'%(k,v) for k,v in env.iteritems()]))
        results += info_string + '\n\n'
        #logging.debug(info_string)
        info_string = '%s :: 2. token=(%s)' % (__name__,token)
        results += info_string + '\n\n'
        #logging.debug(info_string)
    
        url = 'https://%s/email/task/%s/' % (env['HTTP_HOST'],token)
    
        info_string = '%s :: 3. url=(%s)' % (__name__,url)
        results += info_string + '\n\n'
    
        import urllib2
        response = urllib2.urlopen(url)
        html = response.read()
    
        results += html
    except Exception, e:
        logging.error('%s :: %s' % (__name__,e))
    
    res('200 OK',[('Content-Type','text/plain')])
    return ['%s :: ok\n\n%s' % ('emailhandler.py',results)]
def main():
    CGIHandler().run(wsgi_app)
    
if __name__ == '__main__':
    main()