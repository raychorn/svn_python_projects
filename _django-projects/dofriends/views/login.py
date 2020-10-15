from django.utils.translation import gettext_lazy as _, gettext
try:
    from django import forms
    _Form = forms.Form
except AttributeError:
    from django import newforms as forms
    _Form = forms.Form

class LoginForm(_Form):
    username = forms.CharField(label=_('username'))
    password = forms.CharField(label=_('Password'),widget=forms.PasswordInput(render_value=False),max_length=100)
    user = None   # allow access to user object     
    def clean(self):
        # only do further checks if the rest was valid
        if self._errors: return

        from django.contrib.auth import login, authenticate
        user = authenticate(username=self.data['username'],
                            password=self.data['password'])
        if user is not None:
            if user.is_active:
                self.user = user                    
            else:
                raise forms.ValidationError(gettext(
                    'This account is currently inactive. Please contact '
                    'the administrator if you believe this to be in error.'))
        else:
            raise forms.ValidationError(gettext(
                'The username and password you specified are not valid.'))
        return self.cleaned_data
    
    def login(self, request):
        from django.contrib.auth import login
        if self.is_valid():
            login(request, self.user)
            return True
        return False
    
class ForgotPasswordForm(_Form):
    username = forms.CharField(label=_('username'))
    user = None   # allow access to user object     
    def clean(self):
        # only do further checks if the rest was valid
        if self._errors: return

        from django.contrib.auth import login, authenticate
        user = authenticate(username=self.data['username'],
                            password=self.data['password'])
        if user is not None:
            if user.is_active:
                self.user = user                    
            else:
                raise forms.ValidationError(gettext(
                    'This account is currently inactive. Please contact '
                    'the administrator if you believe this to be in error.'))
        else:
            raise forms.ValidationError(gettext(
                'The username and password you specified are not valid.'))
        return self.cleaned_data
    
    def login(self, request):
        from django.contrib.auth import login
        if self.is_valid():
            login(request, self.user)
            return True
        return False
    
def login(request,template='login.html',onAction='',onSuccess=''):
    from django.template import loader
    from vyperlogix.django import django_utils

    form = None

    _error_msg = ''
    if (request.method.lower() == 'POST'.lower()):
        post_data = request.POST.copy()
        form = LoginForm(post_data)
        if (form.is_valid()):
            success = form.login(request)
            if (success is not None) and (onSuccess not in ['',None]):
                _error_msg = success
            else:
                return http.HttpResponseRedirect(onSuccess)
        else:
            _error_msg = 'WARNING: Cannot login due to a technical problem.  Please try back a bit later in the day.'
    else:
        form = LoginForm() if (onAction.find('forgot-password') == -1) else ForgotPasswordForm()
    if ((request.META.has_key('HTTP_HOST')) and ( (django_utils.isProduction(django_utils._cname)) or (django_utils.isStaging(django_utils._cname)) ) ):
        onAction = 'https://%s%s' % (request.META['HTTP_HOST'],onAction)
    return loader.render_to_string(template, {'form':form, 'FORM_ACTION':onAction, 'ERROR_MESSAGE':_error_msg})
