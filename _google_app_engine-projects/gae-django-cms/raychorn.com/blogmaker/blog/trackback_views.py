''' Copyright (c) 2006-2007, PreFab Software Inc. '''


import logging
from itertools import count

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from blogmaker.blog.models import Entry, TrackbackStatus

def postTrackbacks(request, slug):
    ''' This view helps to post trackbacks for our entries '''
    entry = get_object_or_404(Entry, slug=slug)
    if request.method == 'POST':
        # Attempt the requested trackbacks
        for ix in count():
            try:
                tbId = request.POST['id%s' % ix]
            except KeyError:
                break
            
            checked = request.POST.get('link%s' % ix)
            if checked:
                try:
                    tb = TrackbackStatus.objects.get(id=int(tbId))
                    tb.attempt()
                except:
                    logging.error('Trackback attempt failed for id=%s' % tbId, exc_info=True)
    
    # Always return the same form to show status and allow retries
    context = dict(entry=entry, title='Post trackbacks for "%s"'%entry.headline)
    return render_to_response('blog/post_trackback_form.html', 
        context, context_instance=RequestContext(request))
