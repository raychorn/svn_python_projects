from django.template import Context
from vyperlogix.html import myOOHTML as oohtml

from vyperlogix import misc

def render_list_as_table(aList=[]):
    rows = []
    h = oohtml.Html()
    for item in aList:
	rows.append(item)
    h.html_simple_table([[row] if (not isinstance(row,list)) else row for row in rows],width='100%')
    return h.toHtml()
    
def _form_for_model(form, request=None, callback=None, context={}):
    if (callable(callback)):
	callback(form,request=request)
    html = form.as_html(context=context,request=request)
    html = render_list_as_table(aList=[html])
    return html

def form_as_html(form, request=None, callback=None, context={}):
    from vyperlogix.django.forms import templates

    form_html = _form_for_model(form, request=request, callback=callback, context=context)
    form_template = templates.template_for_form(form_html)
    if (request is not None):
	for name,value in request.POST.iteritems():
	    context["VALUE_%s" % (name.upper())] = value[0] if (misc.isList(value)) else value
    form_content = form_template.render(Context(context))
    return form_content

