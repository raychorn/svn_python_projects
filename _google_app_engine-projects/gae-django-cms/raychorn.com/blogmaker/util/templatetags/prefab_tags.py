''' Copyright (c) 2006-2007, PreFab Software Inc. '''

from django import template
from django.conf import settings

from blogmaker.util import expand_shortcuts

register = template.Library()

register.filter('expand_shortcuts', template.defaultfilters.stringfilter(expand_shortcuts))

@register.simple_tag
def setting(name):
    return getattr(settings, name)
    
    
@register.tag
def getsetting(parser, token):
    ''' Access a setting and assign a variable in the template
        Usage: {% getsetting setting as var %}
    '''
    args = token.split_contents()
    if len(args) != 4:
        raise template.TemplateSyntaxError, "%r tag requires two or four arguments" % args[0]
    
    return GetSettingNode(args[1], args[3])

class GetSettingNode(template.Node):
    def __init__(self, setting, var):
        self.setting = setting
        self.var = var
        
    def render(self, context):
        value = getattr(settings, self.setting)
        context[self.var] = value
        return ''
