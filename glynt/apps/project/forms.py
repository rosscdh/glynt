# -*- coding: UTF-8 -*-
from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper

from public.forms import ContactForm


class ContactUsForm(ContactForm):
    """
    Form to handle contacting us when we don't offer the service required
    """


class CreateProjectForm(forms.Form):
    transaction_type = forms.CharField(widget=forms.HiddenInput)
