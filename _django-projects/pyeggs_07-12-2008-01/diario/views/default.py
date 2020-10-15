from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

def default(request):
    t = get_template('flatfiles/index.html')
    html = t.render(Context({'content-main':''}))
    return HttpResponse(html)

