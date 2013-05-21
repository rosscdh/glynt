# -*- coding: UTF-8 -*-
from django import forms
from bootstrap.forms import BootstrapMixin

from parsley.decorators import parsleyfy

from models import Startup, Founder

from services import EnsureFounderService, EnsureStartupService

import logging
logger = logging.getLogger('django.request')


@parsleyfy
class StartupProfileSetupForm(BootstrapMixin, forms.Form):
    """ Form to allow startups to enter basic information about 
    their setups
    """
    # django user ifo used to populate founder object
    first_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'First name', 'tabindex':'1'}))
    last_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Last name','tabindex':'2'}))

    # startup
    startup_name = forms.CharField(label="Startup Name", help_text="", widget=forms.TextInput(attrs={'placeholder':'Acme Inc', 'tabindex':'3'}))
    twitter = forms.CharField(required=False, label="Twitter", help_text="", widget=forms.TextInput(attrs={'tabindex':'6'}))
    summary = forms.CharField(label="Summary", widget=forms.Textarea(attrs={'placeholder':'A brief description of your startup', 'tabindex':'4', 'class':'input-large', 'data-rangelength':'[0,1024]', 'rows':'2'}))
    url = forms.URLField(label="URL", help_text="", widget=forms.TextInput(attrs={'placeholder':'http://acmeco.com', 'class':'input-large', 'tabindex':'4'}))

    # capital details
    already_raised_capital = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'tabindex':'7'}))
    process_raising_capital = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'tabindex':'8'}))
    incubator_or_accelerator_name  = forms.CharField(required=False, label='', help_text="", widget=forms.TextInput(attrs={'placeholder':'Incubator or accelerator name'}))

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

        founder_service = EnsureFounderService(founder_user=self.user, **data)
        founder = founder_service.process()

        startup_service = EnsureStartupService(name=data.get('startup_name'), founder=founder, **data)
        startup = startup_service.process()
