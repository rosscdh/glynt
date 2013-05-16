# -*- coding: UTF-8 -*-
from django import forms
from bootstrap.forms import BootstrapMixin

from parsley.decorators import parsleyfy
from models import Startup, Founder

from services import EnsureStartupService

import logging
logger = logging.getLogger('django.request')


@parsleyfy
class StartupProfileSetupForm(BootstrapMixin, forms.Form):
    """ Form to allow startups to enter basic information about 
    their setups
    """
    first_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'First name', 'tabindex':'1'}))
    last_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Last name','tabindex':'2'}))
    startup_name = forms.CharField(label="Acme Inc", help_text="", widget=forms.TextInput(attrs={'placeholder':'Startup Name', 'tabindex':'6'}))
    already_raised_capital = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'tabindex':'7'}))
    process_raising_capital = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'tabindex':'8'}))
    incubator_or_accelerator = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={'class':'incubator', 'tabindex':'9'}))
    agree_tandc = forms.BooleanField(label='', widget=forms.CheckboxInput(attrs={'tabindex':'10'}))

    def __init__(self, *args, **kwargs):
        """ get request object and user """
        self.request = kwargs.pop('request', None)
        self.user = self.request.user
        super(StartupProfileSetupForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        data = self.cleaned_data

        #self.user
        logger.info('StartupProfileSetupForm Starting')

        founder_service = EnsureFounderService(founder_user=self.user)
        founder = founder_service.process()

        startup_service = EnsureStartupService(founder=founder, **data)
        startup = startup_service.process()
