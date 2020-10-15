from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the home index.")

def detail(request, id):
    return HttpResponse("You're looking at id %s." % id)
