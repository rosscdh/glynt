# -*- coding: utf-8 -*-
from django import forms
from postman.forms import WriteForm
from postman.fields import CommaSeparatedUserField
from postman.utils import WRAP_WIDTH

from parsley.decorators import parsleyfy


@parsleyfy
class EngageWriteMessageForm(WriteForm):
    recipients = CommaSeparatedUserField(label='Recipient', required=True, widget=forms.HiddenInput)
    body = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': WRAP_WIDTH, 'rows': 12}))

    def __init__(self, *args, **kwargs):
        """ get request object and user """
        self.request = kwargs.pop('request', None)
        self.user = self.request.user
        self.to = kwargs.pop('to', None)
        kwargs['sender'] = kwargs.pop('from', None)

        kwargs['initial'].update({
            'sender': kwargs['sender'],
            'recipients': self.to.username,
        })

        super(EngageWriteMessageForm, self).__init__(*args, **kwargs)
