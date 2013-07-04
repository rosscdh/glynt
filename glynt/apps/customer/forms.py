# -*- coding: UTF-8 -*-
from django import forms
from bootstrap.forms import BootstrapMixin

from cicu.models import UploadedFile
from cicu.widgets import CicuUploderInput

from parsley.decorators import parsleyfy

from glynt.apps.client.forms import ChangePasswordMixin, ConfirmChangePasswordMixin

from glynt.apps.firm.services import EnsureFirmService
from glynt.apps.company.services import EnsureCompanyService
from glynt.apps.customer.services import EnsureCustomerService

import logging
logger = logging.getLogger('django.request')


@parsleyfy
class CustomerProfileSetupForm(BootstrapMixin, ChangePasswordMixin, ConfirmChangePasswordMixin, forms.Form):
    """ Form to allow companies to enter basic information about
    their setups
    """
    # django user ifo used to populate customer object
    first_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder': 'First name', 'tabindex': '1'}))
    last_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder': 'Last name', 'tabindex': '2'}))
    email = forms.EmailField(help_text="", widget=forms.TextInput(attrs={'placeholder': 'first.name@example.com', 'tabindex': '3'}))
    phone = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder': 'Contact Phone', 'tabindex': '4'}))

    photo = forms.ImageField(required=False, label="Main Photo", help_text="Please add a good quality photo to your profile. It really helps.", widget=CicuUploderInput(attrs={'data-trigger': 'change', 'data-required': 'false'}, options={
                'ratioWidth': '110',       # fix-width ratio, default 0
                'ratioHeight': '110',      # fix-height ratio , default 0
                'sizeWarning': 'False',    # if True the crop selection have to respect minimal ratio size defined above. Default 'False'
                'modalButtonLabel': 'Upload photo',
                'onReady': 'preparePhotoPreview',
                'onCrop': 'photoCrop'
            }))

    hidden_photo = forms.CharField(required=False, widget=forms.HiddenInput) # transports the id

    # company
    company_name = forms.CharField(label="Company Name", help_text="", widget=forms.TextInput(attrs={'placeholder': 'Acme Inc', 'tabindex': '5'}))
    website = forms.URLField(label="URL", help_text="", widget=forms.TextInput(attrs={'placeholder': 'http://acmeco.com', 'class': 'input-large', 'tabindex': '8'}))
    twitter = forms.CharField(required=False, label="Twitter", help_text="", widget=forms.TextInput(attrs={'tabindex': '6'}))
    summary = forms.CharField(label="Summary", widget=forms.Textarea(attrs={'placeholder': 'A brief description of your startup', 'tabindex': '7', 'class': 'input-large', 'data-rangelength': '[0,1024]', 'rows': '2'}))


    agree_tandc = forms.BooleanField(label='', widget=forms.CheckboxInput(attrs={'tabindex': '13'}))

    def __init__(self, *args, **kwargs):
        """ get request object and user """
        self.request = kwargs.pop('request', None)
        self.user = self.request.user
        super(CustomerProfileSetupForm, self).__init__(*args, **kwargs)

    def clean_hidden_photo(self):
        hidden_photo = self.cleaned_data.get('hidden_photo', None)
        return int(hidden_photo) if hidden_photo else None

    def save(self, commit=True):
        data = self.cleaned_data

        #self.user
        logger.info('CustomerProfileSetupForm Starting')

        # @TODO should be in the clean_photo method
        hidden_photo = self.cleaned_data.get('hidden_photo', None)
        if type(hidden_photo) is int:
            try:
                data['photo'] = UploadedFile.objects.get(pk=hidden_photo)
            except UploadedFile.DoesNotExist:
                data['photo'] = None

        customer_service = EnsureCustomerService(user=self.user, **data)
        customer = customer_service.process()

        if self.user.profile.is_customer:
            company_service = EnsureCompanyService(name=data.get('company_name'), customer=customer, **data)
            company_service.process()
