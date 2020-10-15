# Copyright (c) 2007-2008 The PyAMF Project.
# See LICENSE for details.

"""
Hello world example client.

@see: U{HelloWorld<http://pyamf.org/wiki/HelloWorld>} wiki page.
@author: U{Nick Joyce<mailto:nick@boxdesign.co.uk>}
@since: 0.1.0
"""

from pyamf.remoting.client import RemotingService

gateway = RemotingService('http://demo.pyamf.org/gateway/helloworld')

echo_service = gateway.getService('echo.echo')

print echo_service('Hello world!')
