''' Copyright (c) 2006-2007, PreFab Software Inc. '''


''' Blogmaker views for use from the admin site. 
    These views should be mapped to the same domain as /admin/blogmaker/.
'''

from django.contrib.auth.decorators import login_required
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404

from blogmaker.blog.models import Entry

@login_required
def entryRedirect(request, id):
    ''' Cross-site access to the public page for a blog '''
    entry = get_object_or_404(Entry, id=id)
    return HttpResponsePermanentRedirect(entry.get_absolute_url())

@login_required
def trackbacksRedirect(request, id):
    ''' Cross-site access to the postTrackbacks page for a blog '''
    entry = get_object_or_404(Entry, id=id)
    return HttpResponsePermanentRedirect(entry.get_absolute_url() + 'postTrackbacks/')
