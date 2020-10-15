from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.conf import settings

from django.shortcuts import render_to_response
from django.views.decorators.csrf import requires_csrf_token

from django.template import RequestContext

import os
import re

from django.contrib.auth.models import AnonymousUser

from models import Candidate, Cities

from vyperlogix import misc

get_user = lambda r:r.session.get('__user__', AnonymousUser) if (r and isinstance(r.session,dict)) else AnonymousUser

def __callback__(request,url,data):
    __user__ = get_user(request)
    
    normalize_doc_name = lambda name:''.join([ch if ( ((ch.lower() >= 'a') and (ch.lower() <= 'z')) or ((ch >= '0') and (ch <= '9')) ) else '-' for ch in os.path.splitext(name)[0]])

    try:
	data['IS_NOT_LOGGED_IN'] = True if (not __user__) else not __user__.is_authenticated
    except:
	data['IS_NOT_LOGGED_IN'] = True
    try:
	data['IS_LOGGED_IN'] = not data['IS_NOT_LOGGED_IN']
    except:
	data['IS_LOGGED_IN'] = False
    
    #data['document_action'] = '/documents/'
    #data['document_form'] = DocumentForm()
    #documents = Document.objects.filter(user_id=__user__.id)
    #d = dict([(doc.docfile.name,doc.id) for doc in documents])
    #json = simplejson.dumps(documents,cls=ComplexEncoder)
    #__documents__ = simplejson.loads(json)
    #num_docs = 0
    #document = None
    #for document in __documents__:
	#document['docfile']['fname'] = document['docfile']['name'].replace(os.sep,'/').split('/')[-1]
	#document['docfile']['name'] = normalize_doc_name(os.path.splitext(document['docfile']['fname'])[0])
	#document['id'] = d.get(document['docfile']['name'],-1)
	#ext = os.path.splitext(document['docfile']['fname'])[-1]
	#if (str(ext).lower().find('.doc') > -1):
	    #document = document['docfile']
	    #num_docs += 1
    #data['documents'] = __documents__
    #data['document'] = document
    #data['num_documents'] = len(data['documents'])
    #data['num_docs'] = num_docs
    #data['has_full_load'] = (num_docs == 1)
    #data['documents'] = __documents__
    
    candidates = []
    data['really_has_candidates'] = False
    data['candidates'] = [{}]
    candidates_count = 0
    if (__user__ is not AnonymousUser):
	candidates = Candidate.objects.filter(user=__user__)
	candidates_count = candidates.count()
	data['really_has_candidates'] = candidates_count > 0
	data['candidates'] = [(candidate.asDict().get('candidate',{})) for candidate in candidates] if (candidates_count > 0) else [(Candidate().asDict().get('candidate',{}))]
    data['has_candidates'] = True
    #data['candidate_form'] = CandidateForm()
    data['candidate_action'] = '/candidates/'
    
    myCountry = 'US' if (candidates_count == 0) else candidates[0].city.country
    countries = Cities.objects.order_by('country') #.values_list('country').distinct()
    #if (countries.count() == 0):
	#from django.utils import simplejson
	#from citiesdata import data
	#for item in data:
	    #pass
    assert countries.count()>0, 'Whats up with this query ?  Got no data ?'
    __countries__ = [c[0] if (misc.isIterable(c)) else c for c in countries]
    if (myCountry):
	data['countries'] = [{'abbrev':c,'selected':'' if (c != myCountry) else ' selected'} for c in __countries__]
    else:
	wrapper = ListWrapper(__countries__)
	i = wrapper.findFirstMatching('US')
	if (i > 0):
	    myCountry = __countries__[i]
	    del __countries__[i]
	    __countries__.insert(0,{'abbrev':myCountry,'selected':' selected'})
	data['countries'] = __countries__[0:1]+[{'abbrev':c,'selected':''} for c in __countries__[1:]]
    
    myState = None if (candidates.count() == 0) else candidates[0].city.region
    if (myCountry):
	states = Cities.objects.filter(country=myCountry).order_by('region').values_list('region').distinct()
    else:
	states = Cities.objects.order_by('region').values_list('region').distinct()
    __states__ = [s[0] if (misc.isIterable(s)) else s for s in states]
    data['states'] = [{'abbrev':s,'selected':'' if (s != myState) else ' selected'} for s in __states__]

@requires_csrf_token
def default(request):
    __url__ = request.META.get('PATH_INFO','/')
    __data__ = {"url": __url__}
    __callback__(request, __url__, __data__)
    return render_to_response('jobs.html', __data__, content_type="text/html", context_instance=RequestContext(request))
