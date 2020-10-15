from django.http import HttpResponse

def default(request):
    html = "<html><body>Default page.</body></html>"
    return HttpResponse(html)
