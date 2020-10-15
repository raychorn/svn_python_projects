from pyamf.remoting.gateway.django import DjangoGateway

def echo(request):
    return request.raw_post_data

services = {
    'myservice.echo': echo
    # could include other functions as well
}

echoGateway = DjangoGateway(services)
