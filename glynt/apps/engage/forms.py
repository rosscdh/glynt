# -*- coding: utf-8 -*-
from django import forms
from bootstrap.forms import BootstrapMixin

from postman.forms import WriteForm
from postman.fields import CommaSeparatedUserField
from postman.utils import WRAP_WIDTH

from parsley.decorators import parsleyfy

from services import EngageLawyerAsStartupService

import logging
logger = logging.getLogger('django.request')


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
    #
    # Part 1. May or may not show depending on wether or not the founder has completed their profile
    #
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First name', 'tabindex':'1'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last name','tabindex':'2'}))
    startup_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Acme Inc', 'tabindex':'3'}))
    already_incorporated = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'tabindex':'4'}))
    already_raised_capital = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'tabindex':'5'}))
    process_raising_capital = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'tabindex':'6'}))
    incubator_or_accelerator_name  = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Incubator or accelerator name', 'tabindex':'7'}))

    #
    # Part 2. Always Shows, but may prepopulate with previous requests data
    #
    engage_for_general = forms.BooleanField(required=False, label='', initial=True, widget=forms.HiddenInput(attrs={'data-target':'li#engage_for_general'}))
    engage_for_incorporation = forms.BooleanField(required=False, label='', widget=forms.HiddenInput(attrs={'data-target':'li#engage_for_incorporation'}))
    engage_for_ip = forms.BooleanField(required=False, label='', widget=forms.HiddenInput(attrs={'data-target':'li#engage_for_ip'}))
    engage_for_employment = forms.BooleanField(required=False, label='', widget=forms.HiddenInput(attrs={'data-target':'li#engage_for_employment'}))
    engage_for_cofounders = forms.BooleanField(required=False, label='', widget=forms.HiddenInput(attrs={'data-target':'li#engage_for_cofounders'}))
    engage_for_fundraise = forms.BooleanField(required=False, label='', widget=forms.HiddenInput(attrs={'data-target':'li#engage_for_fundraise'}))

    engagement_statement = forms.CharField(label='Your Requirements', help_text='', required=True, widget=forms.Textarea(attrs={'placeholder':'Your requirements', 'class': 'input-xlarge', 'tabindex':'1'}))

    def __init__(self, *args, **kwargs):
        """ Setup whether or not to show the Part1 aspect of the form """
        self.request = kwargs.pop('request', None)
        self.user = self.request.user
        self.lawyer = kwargs.pop('lawyer', None)

        initial_bunch = kwargs.get('initial')

        super(EngageStartupLawyerForm, self).__init__(*args, **kwargs)

        if initial_bunch.is_valid():
            # the lawyer has already completed their profile
            # so hide the fields
            self.fields['first_name'].widget = forms.HiddenInput()
            self.fields['last_name'].widget = forms.HiddenInput()
            self.fields['startup_name'].widget = forms.HiddenInput()
            self.fields['already_incorporated'].widget = forms.HiddenInput()
            self.fields['already_raised_capital'].widget = forms.HiddenInput()
            self.fields['process_raising_capital'].widget = forms.HiddenInput()
            self.fields['incubator_or_accelerator_name'].widget = forms.HiddenInput()


    def save(self, commit=True):
        logger.info('Starting EngageStartupLawyerForm save')
        data = self.cleaned_data

        engage_service = EngageLawyerAsStartupService(user=self.user, lawyer=self.lawyer, startup_name=data.pop('startup_name'), **data)
        engagement = engage_service.process()

        return engagement