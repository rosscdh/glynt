# -*- coding: UTF-8 -*-
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core import exceptions

from bootstrap.forms import BootstrapMixin
from cicu.widgets import CicuUploderInput

from glynt.apps.lawyer.models import Lawyer

from glynt.apps.lawyer.services import EnsureLawyerService

import logging
logger = logging.getLogger('django.request')

import pdb

API_URLS = {
    'firms': '/api/v1/firm/?format=json&limit=1000',
    'offices': '/api/v1/office/?format=json&limit=1000',
}


class LawyerProfileSetupForm(BootstrapMixin, forms.Form):
    title = forms.CharField(required=False)

    first_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'John'}))
    last_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Sonsini'}))
    email = forms.EmailField(help_text="Your Email", widget=forms.TextInput(attrs={'placeholder':'john@lawpal.com'}))

    firm_name = forms.CharField( widget=forms.TextInput(attrs={'class':'typeahead','autocomplete':'off','data-provide':'', 'data-items':4, 'data-source': 'firms'}))

    phone = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'+44 207 7778 2020', 'title':'Shows on your profile. Include country code.'}))
    position = forms.ChoiceField(choices=Lawyer.LAWYER_ROLES.get_choices(), initial=Lawyer.LAWYER_ROLES.associate, label="Position", help_text="")
    years_practiced = forms.IntegerField(label="Years Practicing", initial="3", widget=forms.TextInput(attrs={'class':'input-mini'}))

    practice_location_1 = forms.CharField(label="Primary Location", widget=forms.TextInput(attrs={'class':'input-large','placeholder':'San Francisco, CA','title':'The primary city you operate from','class':'typeahead','autocomplete':'off','data-provide':'', 'data-items':4, 'data-source':'offices'}))
    practice_location_2 = forms.CharField(required=False, label="Secondary Location", widget=forms.TextInput(attrs={'class':'input-large','placeholder':'London, UK','title':'Optional. The secondary city you operate from.','class':'typeahead','autocomplete':'off','data-provide':'', 'data-items':4, 'data-source':'offices'}))

    summary = forms.CharField(label="Short description", widget=forms.TextInput(attrs={'class':'input-xxlarge','placeholder':'e.g. Partner at WDJ advising technology companies in Europe','title':'Keep it short, and make it personal.'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'input-xxlarge','placeholder':'A bit more about you.','title':'A bit longer, but still make it personal.'}))

    photo = forms.ImageField(required=False, label="Main Photo", help_text="Please add a good quality photo to your profile. It really helps.", widget=CicuUploderInput(options={
                'ratioWidth': '110',       #fix-width ratio, default 0
                'ratioHeight':'110',       #fix-height ratio , default 0
                'sizeWarning': 'False',    #if True the crop selection have to respect minimal ratio size defined above. Default 'False'
                'modalButtonLabel': 'Upload photo',
                'onCrop': 'photoUploadComplete',
            }))

    startups_advised = forms.CharField(required=False, label="Startups Advised", help_text='This helps us match you with similar startups', widget=forms.TextInput(attrs={'title':'e.g. instagram.com','class':'typeahead','autocomplete':'off','data-provide':'', 'data-items':4, 'data-source':''}))

    volume_incorp_setup = forms.CharField(required=False, widget=forms.HiddenInput) # list of lists :[[2010,2011,2012]]
    volume_seed_financing = forms.CharField(required=False, widget=forms.HiddenInput) # list of lists :[[2010,2011,2012]]
    volume_series_a = forms.CharField(required=False, widget=forms.HiddenInput) # list of lists :[[2010,2011,2012]]

    agree_tandc = forms.BooleanField(widget=forms.CheckboxInput)

    def __init__(self, *args, **kwargs):
        """ get request object and user """
        self.request = kwargs.pop('request', None)
        self.user = self.request.user
        self.data_source_urls = API_URLS
        super(LawyerProfileSetupForm, self).__init__(*args, **kwargs)


    def clean_email(self):
        email = self.cleaned_data['email']
        # Nasty
        try:
            lawyer_exists = User.objects.exclude(pk=self.user.pk).get(email=email)
            msg = 'Sorry but a Lawyer with that email already exists (id: %s)' % (lawyer.pk)
            logging.error(msg)
            raise exceptions.ValidationError(msg)
        except User.DoesNotExist:
            # ok this lawyer is valid
            pass
        return email

    def clean_photo(self):
        photo = self.cleaned_data.get('photo', None)
        return photo

    def save(self, commit=True):
        logger.info('Ensuring the LawyerProfile Exists')

        data = self.cleaned_data

        firm_name = data.pop('firm_name')

        offices = []
        # dont pop these as we need them for local storage in lawyer
        offices.append(data.get('practice_location_1', None))
        offices.append(data.get('practice_location_2', None))
        pdb.set_trace()
        lawyer_service = EnsureLawyerService(user=self.user, firm_name=firm_name, offices=offices, **data)
        lawyer_service.process()

        logger.info('Complete: Ensuring the LawyerProfile Exists')


