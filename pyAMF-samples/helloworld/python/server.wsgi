# Copyright (c) 2007-2008 The PyAMF Project.
# See LICENSE for details.

import sys

from pyamf.remoting.gateway.wsgi import WSGIGateway
import server

application = WSGIGateway(server.services)
