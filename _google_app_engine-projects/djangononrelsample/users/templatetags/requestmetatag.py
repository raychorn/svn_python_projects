from django.template import resolve_variable 
from django import template 
from django.template import Library, Node 
register = template.Library() 

class AlertNode(Node): 
    def __init__(self, request): 
        self.request = request 
    def render(self, context): 
        request = resolve_variable(self.request, context) 
        # Do something with the session 
        var = request.session.get('js_alert', None) 
        if var: 
            del request.session['js_alert'] 
            return str('<script type="text/javascript">alert("%s");</script>' % var) 
        else: 
            return '' 

@register.tag(name="get_request_meta") 
def get_request_meta(parser, token): 
    toks = token.split_contents() 
    try: 
        if (len(toks) == 2):
            tag_name, request = toks 
        elif (len(toks) == 4):
            tag_name, request, _as, varname = toks 
        else:
            raise template.TemplateSyntaxError, "%r tag requires either one argument which is the request or the clause 'as varname'." % token.contents[0] 
    except ValueError: 
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents[0] 
    return AlertNode(request) 
