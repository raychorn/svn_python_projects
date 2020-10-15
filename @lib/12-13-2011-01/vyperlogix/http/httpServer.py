# httpServer
#
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

import os
os.environ['TZ'] = 'UTC'
import time
if hasattr(time, 'tzset'):
    time.tzset()

import logging
import sys
import traceback
import tempfile

import BaseHTTPServer
import cgitb
import httplib
import cStringIO
import mimetools
import socket
import errno

from vyperlogix.hash import lists

MAX_URL_LENGTH = 2047

root_path = '/'
login_url = '/login'
_serve_address = '127.0.0.1'
port = 8080
_logging = None

def GetFullURL(server_name, server_port, relative_url):
    """Returns the full, original URL used to access the relative URL.

  Args:
    server_name: Name of the local host, or the value of the 'host' header
      from the request.
    server_port: Port on which the request was served (string or int).
    relative_url: Relative URL that was accessed, including query string.

  Returns:
    String containing the original URL.
  """
    if str(server_port) != '80':
        netloc = '%s:%s' % (server_name, server_port)
    else:
        netloc = server_name
    return 'http://%s%s' % (netloc, relative_url)

def RewriteResponse(httpServer, response_file):
    """Interprets server-side headers and adjusts the HTTP response accordingly.
  """
    headers = mimetools.Message(response_file)

    response_status = '%d Good to go' % httplib.OK

    location_value = headers.getheader('location')
    status_value = headers.getheader('status')

    if status_value:
        response_status = status_value
        del headers['status']
    elif location_value:
        response_status = '%d Redirecting' % httplib.FOUND

    if not 'Cache-Control' in headers:
        headers['Cache-Control'] = 'no-cache'

    status_parts = response_status.split(' ', 1)
    status_code, status_message = (status_parts + [''])[:2]
    try:
        status_code = int(status_code)
    except ValueError:
        status_code = 500
        body = 'Error: Invalid "status" header value returned.'
    else:
        body = response_file.read()
        if (len(body) == 0):
            body = response_file.getvalue()

    headers['content-length'] = str(len(body))

    header_list = []
    for header in headers.headers:
        header = header.rstrip('\n')
        header = header.rstrip('\r')
        header_list.append(header)

    header_data = '\r\n'.join(header_list) + '\r\n'
    return status_code, status_message, header_data, body

def dummy(*args):
    pass

class HTTPServer:
    def __init__(self,root_path,login_url,ip,port,logging,callback=dummy):
        """Initializer.
    """
        self.__root_path__ = root_path
        self.__login_url__ = login_url
        self.__ip__ = ip
        self.__port__ = port
        self.__logging__ = logging
        self.__python_path_list__ = sys.path
        self.__require_indexes__ = False
        self.__handler_class__ = None
        self.__callback__ = callback

        self.__http_server__ = self.CreateServer()

        self.logging.info('Running on port %d: http://%s:%d', self.port, self.ip, self.port)
        try:
            try:
                self.http_server.serve_forever()
            except KeyboardInterrupt:
                self.logging.info('Server interrupted by user, terminating')
            except:
                exc_info = sys.exc_info()
                info_string = '\n'.join(traceback.format_exception(*exc_info))
                self.logging.error('Error encountered:\n%s\nNow terminating.', info_string)
                return 1
        finally:
            self.http_server.server_close()
        return 0

    def CreateRequestHandler(self,root_path):
        """Creates a new BaseHTTPRequestHandler sub-class for use with the Python
    BaseHTTPServer module's HTTP server.

    Python's built-in HTTP server does not support passing context information
    along to instances of its request handlers. This function gets around that
    by creating a sub-class of the handler in a closure that has access to
    this context information.

    Args:
      root_path: Path to the root of the application running on the server.
      require_indexes: True if index.yaml is read-only gospel; default False.

    Returns:
      Sub-class of BaseHTTPRequestHandler.
    """
        httpServer = self

        class DevAppServerRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
            """Dispatches URLs using patterns from a URLMatcher, which is created by
      loading an application's configuration file. Executes CGI scripts in the
      local process so the scripts can use mock versions of APIs.

      HTTP requests that correctly specify a user info cookie (dev_appserver_login.COOKIE_NAME) 
      will have the 'USER_EMAIL' environment variable set accordingly. If the user is also an admin, the
      'USER_IS_ADMIN' variable will exist and be set to '1'. If the user is not logged in, 
      'USER_EMAIL' will be set to the empty string.
      """
            server_version = 'PythonServer/1.0'

            def __init__(self, *args, **kwargs):
                """Initializer.

        Args:
          args, kwargs: Positional and keyword arguments passed to the constructor
            of the super class.
        """
                BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

            def do_GET(self):
                """Handle GET requests."""
                self._HandleRequest()

            def do_POST(self):
                """Handles POST requests."""
                self._HandleRequest()

            def do_PUT(self):
                """Handle PUT requests."""
                self._HandleRequest()

            def do_HEAD(self):
                """Handle HEAD requests."""
                self._HandleRequest()

            def do_OPTIONS(self):
                """Handles OPTIONS requests."""
                self._HandleRequest()

            def do_DELETE(self):
                """Handle DELETE requests."""
                self._HandleRequest()

            def do_TRACE(self):
                """Handles TRACE requests."""
                self._HandleRequest()

            def _HandleRequest(self):
                """Handles any type of request and prints exceptions if they occur."""
                server_name = self.headers.get('host') or self.server.server_name
                server_name = server_name.split(':', 1)[0]

                env_dict = lists.HashedLists2()
                env_dict['REQUEST_METHOD'] = self.command
                env_dict['REMOTE_ADDR'] = self.client_address[0]
                env_dict['SERVER_SOFTWARE'] = self.server_version
                env_dict['SERVER_NAME'] = server_name
                env_dict['SERVER_PROTOCOL'] = self.protocol_version
                env_dict['SERVER_PORT'] = str(self.server.server_port)

                full_url = GetFullURL(server_name, self.server.server_port, self.path)
                if len(full_url) > MAX_URL_LENGTH:
                    msg = 'Requested URI too long: %s' % full_url
                    httpServer.logging.error(msg)
                    self.send_response(httplib.REQUEST_URI_TOO_LONG, msg)
                    return

                tbhandler = cgitb.Hook(file=self.wfile).handle
                try:
                    infile = cStringIO.StringIO(self.rfile.read(int(self.headers.get('content-length', 0))))
                    outfile = cStringIO.StringIO()
                    try:
                        import types
                        import urllib
                        if (callable(httpServer.callback)):
                            # In this model the callback handles the mapping of URL path to process and emits HTML as-needed to outfile.
                            # The callback is free to use whatever Framework may be desired to render the HTML or XML.
                            try:
                                env_dict['FORM'] = lists.HashedLists2()
                                for f in infile.getvalue().split('&'):
                                    toks = [urllib.unquote_plus(t.strip()) for t in f.split('=')]
                                    if (len(toks) > 1): #  and (len(toks[0]) > 0) and (len(toks[-1]) > 0)
                                        env_dict['FORM'][toks[0]] = toks[-1]
                                httpServer.callback(self, self.path, self.headers, outfile, env_dict)
                            except:
                                exc_info = sys.exc_info()
                                info_string = '\n'.join(traceback.format_exception(*exc_info))
                                httpServer.logging.error(info_string)
                        else:
                            httpServer.logging.info('Dispatch :: path=[%s], headers=[%s], env_dict=[%s]' % (self.path,self.headers,env_dict))
                    except:
                        exc_info = sys.exc_info()
                        info_string = '\n'.join(traceback.format_exception(*exc_info))
                        httpServer.logging.error(info_string)
                    outfile.flush()
                    outfile.seek(0)
                    status_code, status_message, header_data, body = RewriteResponse(httpServer,outfile)
                    pass

                except:
                    msg = 'Exception encountered handling request'
                    httpServer.logging.exception(msg)
                    self.send_response(httplib.INTERNAL_SERVER_ERROR, msg)
                    tbhandler()
                else:
                    try:
                        self.send_response(status_code, status_message)
                        httpServer.logging.info('status_code=[%s], status_message=[%s]' % (status_code,status_message))
                        self.wfile.write(header_data)
                        httpServer.logging.info('header_data=[%s]' % (header_data))
                        self.wfile.write('\r\n')
                        if self.command != 'HEAD':
                            self.wfile.write(body)
                        elif body:
                            httpServer.logging.warning('Dropping unexpected body in response to HEAD request')
                    except (IOError, OSError), e:
                        exc_info = sys.exc_info()
                        info_string = '\n'.join(traceback.format_exception(*exc_info))
                        httpServer.logging.error(info_string)
                        if e.errno != errno.EPIPE:
                            raise e
                    except socket.error, e:
                        exc_info = sys.exc_info()
                        info_string = '\n'.join(traceback.format_exception(*exc_info))
                        httpServer.logging.error(info_string)
                        if len(e.args) >= 1 and e.args[0] != errno.EPIPE:
                            raise e

            def log_error(self, format, *args):
                """Redirect error messages through the logging module."""
                httpServer.logging.error(format, *args)

            def log_message(self, format, *args):
                """Redirect log messages through the logging module."""
                httpServer.logging.info(format, *args)

        return DevAppServerRequestHandler

    def CreateServer(self):
        """Creates an new HTTPServer for an application.
    """
        absolute_root_path = os.path.abspath(root_path)

        self.handler_class = self.CreateRequestHandler(absolute_root_path)

        if (absolute_root_path not in self.python_path_list):
            self.python_path_list.insert(0, absolute_root_path)

        return BaseHTTPServer.HTTPServer((self.ip, self.port), self.handler_class)

    def http_server():
        doc = "http_server"
        def fget(self):
            return self.__http_server__
        return locals()
    http_server = property(**http_server())

    def callback():
        doc = "callback"
        def fget(self):
            return self.__callback__
        def fset(self,callback):
            self.__callback__ = callback
        return locals()
    callback = property(**callback())

    def python_path_list():
        doc = "python_path_list"
        def fget(self):
            return self.__python_path_list__
        def fset(self,python_path_list):
            self.__python_path_list__ = python_path_list
        return locals()
    python_path_list = property(**python_path_list())

    def handler_class():
        doc = "handler_class"
        def fget(self):
            return self.__handler_class__
        def fset(self,handler_class):
            self.__handler_class__ = handler_class
        return locals()
    handler_class = property(**handler_class())

    def require_indexes():
        doc = "require_indexes"
        def fget(self):
            return self.__require_indexes__
        def fset(self,require_indexes):
            self.__require_indexes__ = require_indexes
        return locals()
    require_indexes = property(**require_indexes())

    def root_path():
        doc = "root_path"
        def fget(self):
            return self.__root_path__
        def fset(self,root_path):
            self.__root_path__ = root_path
        return locals()
    root_path = property(**root_path())

    def login_url():
        doc = "login_url"
        def fget(self):
            return self.__login_url__
        def fset(self,login_url):
            self.__login_url__ = login_url
        return locals()
    login_url = property(**login_url())

    def ip():
        doc = "ip"
        def fget(self):
            return self.__ip__
        def fset(self,ip):
            self.__ip__ = ip
        return locals()
    ip = property(**ip())

    def port():
        doc = "port"
        def fget(self):
            return self.__port__
        def fset(self,port):
            self.__port__ = port
        return locals()
    port = property(**port())

    def logging():
        doc = "logging"
        def fget(self):
            return self.__logging__
        def fset(self,logging):
            self.__logging__ = logging
        return locals()
    logging = property(**logging())

def dictFromHeaders(headers):
    d_headers = lists.HashedLists2()
    for h in str(headers).split('\n'):
        toks = [t.strip() for t in h.split(':')]
        d_headers[toks[0]] = toks[-1]
    return d_headers
