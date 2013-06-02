# -*- coding: utf-8 -*-
from django import forms
from bootstrap.forms import BootstrapMixin

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


@parsleyfy
class EngageStartupLawyerForm(BootstrapMixin, forms.Form):
    first_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'First name', 'tabindex':'1'}))
    last_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Last name','tabindex':'2'}))
    startup_name = forms.CharField(label="Startup Name", help_text="", widget=forms.TextInput(attrs={'placeholder':'Acme Inc', 'tabindex':'3'}))
    already_incorporated = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'tabindex':'4'}))
    already_raised_capital = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'tabindex':'5'}))
    process_raising_capital = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'tabindex':'6'}))
    incubator_or_accelerator_name  = forms.CharField(required=False, label='', help_text="", widget=forms.TextInput(attrs={'placeholder':'Incubator or accelerator name', 'tabindex':'7'}))

    need_incorporation = forms.BooleanField(required=False, label='', widget=forms.HiddenInput(attrs={'tabindex':'8'}))
