''' 
Copyright (c) 2006-2007, PreFab Software Inc.

Copyright (c) 2006, Andrew Gwozdziewycz <apgwoz@gmail.com>
All rights reserved.
'''


import calendar, datetime, time

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader
from django.views.generic.date_based import archive_day

from blogmaker.blog.models import Tag, Entry
import blogmaker.comments.views

def view_tagged_items(request, tag):
    ''' View all blog entries for a given tag '''
    
    current_tag = get_object_or_404(Tag, tag=tag)
    entries = current_tag.entry_set.current_active().select_related()
    
    t = loader.get_template('blog/tag_index.html')
    c = RequestContext(request, {'object_list': entries, 'tag': tag})
    return HttpResponse(t.render(c))


def view_tags(request):
    ''' View two lists of tags, one by popularity, one alphabetical '''
    
    entries = Entry.objects.current_active()
    all_tags = Tag.objects.all()
    popular_tags = []
    alpha_tags = []
    for tag in all_tags:
        entry_count = entries.filter(tags__exact=tag).count()
        if entry_count > 0:
            tag = str(tag)
            popular_tags.append( (entry_count, tag) )
            popular_tags.sort(reverse=True)
            alpha_tags.append( (tag, entry_count) )
            alpha_tags.sort(key=lambda x: x[0].lower())
            
    t = loader.get_template('blog/tag_list.html')
    c = RequestContext(request, {'alpha_list': alpha_tags, 'popular_list': popular_tags, 'taglist': all_tags})
    return HttpResponse(t.render(c))


def view_user_items(request, user):
    ''' View all items by a specific user '''
    
    user = get_object_or_404(User, username=user)
    entries = Entry.objects.current_active().filter(user__exact=user)
    
    t = loader.get_template('blog/user_index.html')
    c = RequestContext(request, {'object_list': entries, 'postedby': user, 'userposts': entries})
    return HttpResponse(t.render(c))

    
def search(request):
    ''' Search entries for term (in body and headline) '''
    
    if not request.POST:
        search = 'Search'
        search_terms = []
        searched = []
        t = loader.get_template('blog/search.html')
    else:
        search = []
        search_terms = request.POST['query'].split(' ')
        if search_terms == ['']:
            search_terms = ['']
            searched = []
        else:
            entries = Entry.objects.current_active()
            searched = []
            for term in search_terms:
                term = term.lower()
                for entry in entries:
                    if (term in entry.headline.lower() or term in entry.body.lower()) and entry not in searched:
                        searched.append(entry)
        t = loader.get_template('blog/search_results.html')
    c = RequestContext(request, {'object_list':searched, 'query': search_terms, 'search': search})
    return HttpResponse(t.render(c))


def extras_day(request, year, month, day, queryset, date_field,
        month_format='%m', day_format='%d'):
    ''' Add a list of days and if and type of entries contained,
    then send to generic archive_day view '''
    
    number = calendar.mdays[datetime.date(*time.strptime(year+month+day, '%Y'+month_format+day_format)[:3]).month]
    days = range(1,number+1,1)
    day_values = []
    for d in days:
        current_day = int(day)
        day_posts = Entry.objects.current_active().filter(pub_date__day=d, pub_date__month=int(month), pub_date__year=int(year))
        if not day_posts:
            value = 'no'
        elif d == current_day:
            value = 'current'
        else:
            value = 'yes'
        day_values.append(value)
    extras = {'days': day_values}
    return archive_day(request, year, month, day, queryset, date_field,
        month_format='%m', day_format='%d', extra_context = extras)


def trackback(request, slug):
    ''' This is the view that receives external trackback requests '''
    blog = get_object_or_404(Entry, slug=slug)
    content_type = ContentType.objects.get(app_label__exact='blog', model__exact='entry')
    return blogmaker.comments.views.trackback(request, content_type.id, blog.id, blog.get_absolute_url())
