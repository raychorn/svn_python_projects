from wsgiref import simple_server

__version__ = "0.1"

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

class WSGILoggingRequestHandler(simple_server.WSGIRequestHandler):

    server_version = "WSGILoggingServer/" + __version__

    def __init__(self, request, client_address, server, _logging=None):
	self.__logging__ = _logging
	simple_server.WSGIRequestHandler.__init__(self, request, client_address, server)

    def log_message(self, format, *args):
        """Log an arbitrary message.

        This is used by all other logging functions.  Override
        it if you have specific logging wishes.

        The first argument, FORMAT, is a format string for the
        message to be logged.  If the format string contains
        any % escapes requiring parameters, they should be
        specified as subsequent arguments (it's just like
        printf!).

        The client host and current date/time are prefixed to
        every message.

        """

	try:
	    self.logging("%s - - [%s] %s\n" %
			     (self.address_string(),
			      self.log_date_time_string(),
			      format%args))
	except:
	    simple_server.WSGIRequestHandler.log_message(self, format, *args)

    def logging():
        doc = "logging"
        def fget(self):
            return self.__logging__
        def fset(self, logging):
            self.__logging__ = logging
        return locals()
    logging = property(**logging())

