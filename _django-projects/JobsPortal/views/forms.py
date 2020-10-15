from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a Microsoft Word doc file',
        help_text='(must be of type doc or docx).',
        max_length = 50
    )

class CandidateForm(forms.Form):
    fullname = forms.CharField(
        label='Enter your Full Name',
        help_text='',
        max_length = 32
    )
    phone = forms.CharField(
        label='Enter your telephone number',
        help_text='',
        max_length = 16
    )
    city = forms.CharField(
        label='Enter your current city name',
        help_text='',
        max_length = 32
    )
    state = forms.CharField(
        label='Enter your current state',
        help_text='',
        max_length = 5
    )
    zipcode = forms.CharField(
        label='Enter your current zipcode',
        help_text='',
        max_length = 16
    )
    country = forms.CharField(
        label='Enter your current country',
        help_text='',
        max_length = 2
    )
    relocateable = forms.BooleanField(
        label='Choose yes or no',
        help_text=''
    )
