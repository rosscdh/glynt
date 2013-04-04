# -*- coding: UTF-8 -*-
from django import forms
from django.conf import settings
from django.contrib.auth.models import User

from bootstrap.forms import BootstrapMixin

from tasks import send_invite_email

import logging
logger = logging.getLogger('django.request')


class InviteEmailForm(BootstrapMixin, forms.Form):
    invite_type = forms.CharField(initial='lawyer', widget=forms.HiddenInput)
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'name':'email[]', 'placeholder':'their.name@example.com', 'data-type':'email', 'data-trigger':'change'}))
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'name':'name[]', 'placeholder':'John Doe', 'data-required':'true', 'data-required':'true', 'data-trigger':'change'}))

    def clean_email(self):
        """ check invitee has not opted-out
        and is not already a user """
        email = self.cleaned_data.get('email', None)

    @property
    def invitee(self):
        return (self.cleaned_data.get('email'), self.cleaned_data.get('name'),)

    def save(self, user, commit=True):
        logger.info('Inviting a User')
        send_invite_email(from_user=user, to_object=self.invitee, subject='Invitation to join Lawpal.com')