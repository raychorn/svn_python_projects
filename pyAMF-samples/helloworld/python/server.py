# Copyright (c) 2007-2008 The PyAMF Project.
# See LICENSE for details.

"""
Hello world example server.

@see: U{HelloWorld<http://pyamf.org/wiki/HelloWorld>} wiki page.
@author: U{Nick Joyce<mailto:nick@boxdesign.co.uk>}
@since: 0.1.0
"""

def echo(data):
    """
    Just return data back to the client.
    """
    return data

services = {
    'echo': echo,
    'echo.echo': echo
}

if __name__ == '__main__':
    from pyamf.remoting.gateway.wsgi import WSGIGateway
    from wsgiref import simple_server

    gw = WSGIGateway(services)

    httpd = simple_server.WSGIServer(
        ('localhost', 8000),
        simple_server.WSGIRequestHandler,
    )

    httpd.set_app(gw)

    print "Running Hello World AMF gateway on http://localhost:8000"

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

