''' 
Copyright (c) 2006-2007, PreFab Software Inc.

Copyright (c) 2006, Andrew Gwozdziewycz <apgwoz@gmail.com>
All rights reserved.
'''


import datetime

from django import template 
from django.template import resolve_variable
from django.conf import settings

from blogmaker.blog.models import Entry, Tag


register = template.Library()

    
@register.tag('get_yearly_archive')
def do_archive_year(parser, token):
    ''' get_yearly_archive as archive_list '''
    
    bits = token.contents.split()
    if len(bits) == 3 and bits[1] == 'as':
        return YearArchiveNode(bits[2])
    else:
        return template.TemplateSyntaxError

class YearArchiveNode(template.Node):
    def __init__(self, context_variable):
        self.context_variable = context_variable

    def render(self, context):
        date_list = Entry.objects.current_active().dates('pub_date', 'month', order='DESC')
        context[self.context_variable] = date_list
        return ''


@register.tag('get_recent_posts')
def do_recent_posts(parser, token):
    ''' get_recent_posts 5 as post_list object.id '''
    
    bits = token.contents.split()
    if len(bits) == 5 and bits[2] == 'as':
        return RecentPostsNode(bits[3], int(bits[1]), bits[4])
    elif len(bits) == 4 and bits[2] == 'as':
        return RecentPostsNode(bits[3], int(bits[1]), 0)
    else:
        return template.TemplateSyntaxError

class RecentPostsNode(template.Node):
    def __init__(self, context_variable, count, ident):
        self.context_variable = context_variable
        self.count = count
	self.ident = ident
    def render(self, context):
	if self.ident > 0:
            current_ident = resolve_variable(self.ident, context)
	else:
	    current_ident = 0
        post_list = Entry.objects.current_active().extra(select={'current_post': "id=%s"}, params=[current_ident]).order_by('-pub_date')[:self.count]
        context[self.context_variable] = post_list
        return ''


@register.tag('get_popular_tags')
def do_popular_tags(parser, token):
    ''' get_popular_tags 5 as popular_tags '''
    
    bits = token.contents.split() 
    if len(bits) == 4 and bits[2] == 'as':
    	return PopularTagsNode(int(bits[1]), bits[3])
    
class PopularTagsNode(template.Node):
    def __init__(self, num, varname):
	self.num = num
        self.varname = varname
    def render(self, context):
	tags = Tag.objects.all()
	popular_tags = []
	for tag in tags:
	    entry_count = Entry.objects.current_active().filter(tags__exact=tag).count()
	    if entry_count > 0:
		tag = str(tag)
	        popular_tags.append( (entry_count, tag) )
	popular_tags.sort(reverse=True)
	context[self.varname] = popular_tags[:self.num]
	return ''


@register.tag('get_next')
def do_next_post(parser, token):
    ''' get_next object.id next_post '''
    
    bits = token.contents.split()
    if len(bits) == 3:
        return NextPostNode(bits[1], bits[2])
    else:
        return template.TemplateSyntaxError

class NextPostNode(template.Node):
    def __init__(self, ident, context_variable):
        self.context_variable = context_variable
	self.ident = ident
    def render(self, context):
	current_ident = resolve_variable(self.ident, context)
	current_entry = Entry.objects.get(id__exact=current_ident)
	try:
	    next_post = current_entry.get_next_by_pub_date(pub_date__lte=datetime.datetime.now())
	    while next_post.active == False:
		next_post = next_post.get_next_by_pub_date(pub_date__lte=datetime.datetime.now())
	except Entry.DoesNotExist:
	    next_post = []
        context[self.context_variable] = next_post
        return ''

    
@register.tag('get_previous')
def do_previous_post(parser, token):
    ''' get_previous object.id previous_post '''
    
    bits = token.contents.split()
    if len(bits) == 3:
        return PreviousPostNode(bits[1], bits[2])
    else:
        return template.TemplateSyntaxError

class PreviousPostNode(template.Node):
    def __init__(self, ident, context_variable):
        self.context_variable = context_variable
	self.ident = ident
    def render(self, context):
	current_ident = resolve_variable(self.ident, context)
	current_entry = Entry.objects.get(id__exact=current_ident)
	try:
	    previous_post = current_entry.get_previous_by_pub_date(pub_date__lte=datetime.datetime.now())
	    while previous_post.active == False:
		previous_post = previous_post.get_previous_by_pub_date(pub_date__lte=datetime.datetime.now())
	except Entry.DoesNotExist:
	    previous_post = []
        context[self.context_variable] = previous_post
        return ''
        
@register.simple_tag
def BLOG_ROOT():
    return settings.BLOG_ROOT
        
@register.simple_tag
def SITE_ROOT():
    return settings.SITE_ROOT



