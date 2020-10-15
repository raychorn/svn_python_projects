if (__name__ == '__main__'):
    from pyamf.remoting.client import RemotingService

    gw = RemotingService('http://127.0.0.1:8888/gateway/')
    service = gw.getService('myservice')

    print service.echo('Hello World!')
