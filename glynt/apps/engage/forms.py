# -*- coding: utf-8 -*-
from django import forms
from postman.forms import WriteForm
from postman.fields import CommaSeparatedUserField


class EngageWriteMessageForm(WriteForm):
    recipients = CommaSeparatedUserField(label='Recipient', required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        """ get request object and user """
        self.request = kwargs.pop('request', None)
        self.user = self.request.user
        self.to = kwargs.pop('to', None)
        kwargs['sender'] = kwargs.pop('from', None)

        recipients = [self.to.username]

        super(EngageWriteMessageForm, self).__init__(*args, **kwargs)
        self.fields['recipients'].initial = recipients
