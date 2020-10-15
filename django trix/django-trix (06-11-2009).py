# See also: http://blog.vyperlogix.com/?p=560
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.conf import settings
from django.db.models import Q

from vyperlogix.django import django_utils # this comes from the VyperLogix Library that can be found at http://www.pypi.info or http://www.vyperlogix.com and is documented at http://library.vyperlogix.com

def default(request):
    url_toks = django_utils.get_from_session(request,'url_toks',None) # try to grab the tokens from the last redirection.
    if (url_toks is not None):
        # handle the request here...
        if (url_toks == ['one', 'two', 'three']):
            pass # this is the real handler here...
        del request.session['url_toks'] # make sure we do not go into a loop.
        return HttpResponse() # put your response here...
    url_toks = [item for item in django_utils.parse_url_parms(request) if (len(item) > 0)]
    params = _utils.get_dict_as_pairs(url_toks)
    
    if (url_toks == ['one', 'two', 'three']):
        request.session['url_toks'] = url_toks
        HttpResponseRedirect('/') # redirect to perform the real handler...