# -*- coding: UTF-8 -*-
from django import forms
from django.core import exceptions

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

    def clean_email(self):
        email = self.cleaned_data['email']
        # # Nasty
        # for l in tmpLawyerFirm.objects.all():
        #     if l.email == email:
        #         raise exceptions.ValidationError('Sorry but a Lawyer with that email already exists (id: %s)' % (l.pk) )

    def save(self, commit=True):
        # lawerfirm = tmpLawyerFirm(data=self.cleaned_data)
        pass
        # return lawerfirm.save()