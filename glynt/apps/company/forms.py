# -*- coding: UTF-8 -*-
from django import forms
from django.utils.safestring import mark_safe
from bootstrap.forms import BootstrapMixin

from cicu.models import UploadedFile
from cicu.widgets import CicuUploderInput

from parsley.decorators import parsleyfy

from models import Company, Founder

from services import EnsureFounderService, EnsureCompanyService

import logging
logger = logging.getLogger('django.request')


@parsleyfy
class CompanyProfileSetupForm(BootstrapMixin, forms.Form):
    """ Form to allow companies to enter basic information about 
    their setups
    """
    # django user ifo used to populate founder object
    first_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'First name', 'tabindex':'1'}))
    last_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Last name','tabindex':'2'}))

    photo = forms.ImageField(required=False, label="Main Photo", help_text="Please add a good quality photo to your profile. It really helps.", widget=CicuUploderInput(attrs={'data-trigger':'change','data-required': 'false'}, options={
                'ratioWidth': '110',       #fix-width ratio, default 0
                'ratioHeight':'110',       #fix-height ratio , default 0
                'sizeWarning': 'False',    #if True the crop selection have to respect minimal ratio size defined above. Default 'False'
                'modalButtonLabel': 'Upload photo',
                'onReady': 'preparePhotoPreview',
                'onCrop': 'photoCrop'
            }))
    
    hidden_photo = forms.CharField(required=False, widget=forms.HiddenInput) # transports the id

    # startup
    startup_name = forms.CharField(label="Company Name", help_text="", widget=forms.TextInput(attrs={'placeholder':'Acme Inc', 'tabindex':'3'}))
    twitter = forms.CharField(required=False, label="Twitter", help_text="", widget=forms.TextInput(attrs={'tabindex':'6'}))
    summary = forms.CharField(label="Summary", widget=forms.Textarea(attrs={'placeholder':'A brief description of your startup', 'tabindex':'4', 'class':'input-large', 'data-rangelength':'[0,1024]', 'rows':'2'}))
    website = forms.URLField(label="URL", help_text="", widget=forms.TextInput(attrs={'placeholder':'http://acmeco.com', 'class':'input-large', 'tabindex':'4'}))

    # capital details
    already_incorporated = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'tabindex':'7'}))
    already_raised_capital = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'tabindex':'8'}))
    process_raising_capital = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'tabindex':'9'}))
    incubator_or_accelerator_name  = forms.CharField(required=False, label='', help_text="", widget=forms.TextInput(attrs={'placeholder':'Incubator or accelerator name', 'tabindex':'10'}))

    agree_tandc = forms.BooleanField(label='', widget=forms.CheckboxInput(attrs={'tabindex':'11'}))

    def __init__(self, *args, **kwargs):
        """ get request object and user """
        self.request = kwargs.pop('request', None)
        self.user = self.request.user
        super(CompanyProfileSetupForm, self).__init__(*args, **kwargs)

    def clean_hidden_photo(self):
        hidden_photo = self.cleaned_data.get('hidden_photo', None)
        return int(hidden_photo) if hidden_photo else None

    def save(self, commit=True):
        data = self.cleaned_data

        #self.user
        logger.info('CompanyProfileSetupForm Starting')

        # @TODO should be in the clean_photo method
        hidden_photo = self.cleaned_data.get('hidden_photo', None)
        if type(hidden_photo) is int:
            try:
                data['photo'] = UploadedFile.objects.get(pk=hidden_photo)
            except UploadedFile.DoesNotExist:
                data['photo'] = None

        founder_service = EnsureFounderService(user=self.user, **data)
        founder = founder_service.process()

        startup_service = EnsureCompanyService(name=data.get('startup_name'), founder=founder, **data)
        startup = startup_service.process()


class CompanyProfileIsCompleteValidator(forms.Form):
    """ is used by the profile_complete template tag 
    to evaluate the completeness of a companies profile """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    startup_name = forms.CharField(required=True)