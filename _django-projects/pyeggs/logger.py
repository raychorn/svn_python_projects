from datetime import datetime
from vyperlogix.misc import _utils

class LoggingMiddleware():
    def log_request(self, request, response, extra_info=''):
        return '%s:%s - - [%s] "%s %s %s" %d %d "%s" "%s"%s' % (request.environ['REMOTE_ADDR'],request.environ['REMOTE_PORT'],_utils.timeStampApache(),request.environ['REQUEST_METHOD'],request.environ['PATH_INFO'],request.environ['SERVER_PROTOCOL'],response.status_code,len(response.content),request.environ['HTTP_HOST'],request.environ['HTTP_USER_AGENT'],extra_info if (len(extra_info) == 0) else ' "%s"' % (extra_info))
    
    def process_request(self, request):
        request.log_func = self.log_request

    def process_response(self, request, response):
        try:
            if (callable(request.log_func)):
                print request.log_func(request,response)
        except:
            pass
        return response

    def process_exception(self, request, exception):
        import traceback
        try:
            if (callable(request.log_func)):
                from vyperlogix.classes.SmartObject import SmartObject
                response = SmartObject()
                response.status_code = 500
                response.content = exception.message
                print request.log_func(request,response, extra_info=','.join(traceback.format_exc().split('\n')))
        except:
            pass

        return None