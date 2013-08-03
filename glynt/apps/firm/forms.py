# -*- coding: UTF-8 -*-
from django import forms

from bootstrap.forms import BootstrapMixin
#from models import tmpLawyerFirm


class CreateLawyerFirmForm(BootstrapMixin, forms.Form):
    title = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    firm = forms.CharField()
    city_location = forms.CharField()
    phone = forms.CharField()
    angelist_url = forms.URLField()
    linkedin_url = forms.URLField()
    facebook_url = forms.URLField()
    twitter_url = forms.URLField()
    list_of_start_ups = forms.CharField(help_text='Comma Separated names', widget=forms.Textarea)
