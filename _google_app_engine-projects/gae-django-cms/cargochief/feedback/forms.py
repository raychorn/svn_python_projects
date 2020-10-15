# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext as __
from feedback.models import Feedback
from ragendja.auth.models import UserTraits
from ragendja.forms import FormWithSets, FormSetField

import datetime

from django.conf import settings

attrs_dict = { 'class': 'required' }

class FeedbackForm(forms.Form):
    """
    Form for providing feedback.
    """
    subject = forms.CharField(widget=forms.TextInput(attrs=attrs_dict),label=_(u'Subject'))
    message = forms.CharField(widget=forms.Textarea(attrs=attrs_dict),label=_(u'Message'))
    
    def save(self, domain_override="", user=None):
        """
        Saves the message in the database...
        """
        results = {'bool':False}
        if (self.cleaned_data.has_key('message') and self.cleaned_data.has_key('subject') and (len(self.cleaned_data['subject']) > 0) and (len(self.cleaned_data['message']) > 0)):
            aFeedback = Feedback(subject=self.cleaned_data['subject'],message=self.cleaned_data['message'],user=user)
            aFeedback.save()
            results['bool'] = True
            expiration_date = datetime.timedelta(days=settings.ACCOUNT_FEEDBACK_DAYS)
            feedbacks = [aFeedback for aFeedback in Feedback.all() if (aFeedback.timestamp + expiration_date <= datetime.datetime.now())]
            for aFeedback in feedbacks:
                aFeedback.delete()
        else:
            raise forms.ValidationError(_(u'You must enter a subject and message together.'))
        return results

