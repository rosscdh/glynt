# -*- coding: UTF-8 -*-
from django import forms
from django.core import exceptions

from bootstrap.forms import BootstrapMixin
from glynt.apps.lawyer.models import Lawyer


class LawyerSignupForm(BootstrapMixin, forms.Form):
    title = forms.CharField()
    first_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'John'}))
    last_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Sonsini'}))
    email = forms.EmailField(help_text="Your Email", widget=forms.TextInput(attrs={'placeholder':'john@lawpal.com'}))
    firm = forms.CharField()
    position = forms.ChoiceField(choices=Lawyer.LAWYER_ROLES.get_choices(), initial=Lawyer.LAWYER_ROLES.associate, label="Position", help_text="")
    years_practiced = forms.IntegerField(label="Years Practicing", widget=forms.TextInput(attrs={'class':'input-mini'}))
    profile_photo = forms.ImageField()
    practice_location_1 = forms.CharField(label="Primary Location", widget=forms.TextInput(attrs={'class':'input-large','placeholder':'San Francisco, CA','title':'The primary city you operate from'}))
    practice_location_2 = forms.CharField(label="Secondary Location", widget=forms.TextInput(attrs={'class':'input-large','placeholder':'London, UK','title':'Optional. The secondary city you operate from.'}))
    profile_summary = forms.CharField(label="Short description", widget=forms.TextInput(attrs={'class':'input-xxlarge','placeholder':'e.g. Partner at WDJ advising technology companies in Europe','title':'Keep it short, and make it personal.'}))
    profile_bio = forms.CharField(widget=forms.Textarea(attrs={'class':'input-xxlarge','placeholder':'A bit more about you.','title':'A bit longer, but still make it personal.'}))
    phone = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'+44 207 7778 2020', 'title':'Shows on your profile. Include country code.'}))
    angelist_url = forms.URLField()
    linkedin_url = forms.URLField()
    facebook_url = forms.URLField()
    twitter_url = forms.URLField()
    startups_advised = forms.CharField(label="Startups Advised", help_text='This helps us match you with similar startups', widget=forms.Textarea(attrs={'data-provide':'', 'data-items':4, 'data-source':''}))
    approx_tx_vol_incorp_setup = forms.CharField() # list of lists :[[2010,2011,2012]]
    approx_tx_vol_seed_financing = forms.CharField() # list of lists :[[2010,2011,2012]]
    approx_tx_vol_series_a = forms.CharField() # list of lists :[[2010,2011,2012]]
    agree_tandc = forms.BooleanField()

    def clean_email(self):
        email = self.cleaned_data['email']
        # Nasty
        for l in tmpLawyerFirm.objects.all():
            if l.email == email:
                raise exceptions.ValidationError('Sorry but a Lawyer with that email already exists (id: %s)' % (l.pk) )

    def clean_firm(self):
        pass
    def clean_practice_location_1(self):
        pass
    def clean_practice_location_2(self):
        pass
    def firm_locations(self):
        pass

    def save(self, commit=True):
        lawerfirm = tmpLawyerFirm(data=self.cleaned_data)
        return lawerfirm.save()

