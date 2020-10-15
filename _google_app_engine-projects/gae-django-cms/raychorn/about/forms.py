# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext as __
from feedback.models import Feedback
from ragendja.auth.models import UserTraits
from ragendja.forms import FormWithSets, FormSetField

from django.conf import settings

