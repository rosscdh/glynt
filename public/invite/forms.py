# -*- coding: UTF-8 -*-
from django import forms
from django.conf import settings
from django.contrib.auth.models import User

from bootstrap.forms import BootstrapMixin

import logging
logger = logging.getLogger('django.request')


class InviteEmailForm(BootstrapMixin, forms.Form):
    invite_type = forms.CharField(widget=forms.HiddenInput)
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder':'their.name@example.com'}))
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'John Doe'}))

    def clean_email(self):
        email = self.cleaned_data.get('email', None)

    def save(self, commit=True):
        logger.info('Inviting a User')
        invite_service = InviteUserService(inviting_user=self.request.user, email_to_invite=firm_name, **self.cleaned_data)
        invite_service.process()