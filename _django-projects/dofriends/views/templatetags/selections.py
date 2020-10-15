from django import template
from django.template import Library, Node, TemplateSyntaxError, \
    resolve_variable, VariableDoesNotExist
from django.conf import settings

register = Library()

class SelectionUtils(template.Node):
    def __init__(self, data, default, value_id, text_id, var_name):
        self.data = data
        self.default = default
        self.value_id = value_id
        self.text_id = text_id
        self.var_name = var_name
    def render(self, context):
        from vyperlogix.html import myOOHTML as oohtml
        try:
            context[self.var_name] = oohtml.render_select_content(data,id=self.var_name,name=self.var_name,value_id=self.value_id,text_id=self.text_id,selected=default[self.value_id])
        except:
            pass
        return ''

import re
@register.tag(name="selections")
def do_selections(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    blob, var_name = m.groups()
    data, default, value_id, text_id = blob.split(',')
    return SelectionUtils(data, default, value_id, text_id, var_name)