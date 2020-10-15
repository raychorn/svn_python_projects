from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

try:
    from django import forms
    _Form = forms.Form
except AttributeError:
    from django import newforms as forms
    _Form = forms.Form

from vyperlogix.django import django_utils

class UploadFileForm(_Form):
    title = forms.CharField(max_length=50)
    image  = _Form.ImageField()
    
def handle_uploaded_file(aFile):
    pass

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    t_form = get_template('_upload_image.html')
    c_form = Context({'form': form})
    content_form = t_form.render(c_form)
    return content_form
