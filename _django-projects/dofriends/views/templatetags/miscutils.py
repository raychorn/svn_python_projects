from django import template
from django.template import Library, Node, TemplateSyntaxError, \
    resolve_variable, VariableDoesNotExist
from django.conf import settings

register = Library()

class MiscUtils(template.Node):
    def __init__(self, format_string, var_name):
        self.format_string = format_string
        self.var_name = var_name
    def render(self, context):
        from vyperlogix.misc import _utils
        try:
            context[self.var_name] = eval('_utils.%s' % self.format_string)
        except:
            pass
        return ''

import re
@register.tag(name="misc_utils")
def do_current_time(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    format_string, var_name = m.groups()
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return MiscUtils(format_string[1:-1], var_name)