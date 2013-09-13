# -*- coding: UTF-8 -*-
from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from django.core import exceptions
from django.core.cache import cache
from glynt.cache_utils_1_5 import make_template_fragment_key

from cicu.models import UploadedFile
from cicu.widgets import CicuUploaderInput

from glynt.apps.lawyer.models import Lawyer

from glynt.apps.lawyer.services import EnsureLawyerService

from parsley.decorators import parsleyfy

from glynt.apps.utils import API_URLS

import logging
logger = logging.getLogger('django.request')


@parsleyfy
class LawyerProfileSetupForm(forms.Form):

    ROLES = [display_name for name,display_name in Lawyer.LAWYER_ROLES.get_choices()]

    title = forms.CharField(required=False)

    first_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder': 'John', 'tabindex': '1'}))
    last_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder': 'Sonsini', 'tabindex': '2'}))

    firm_name = forms.CharField(widget=forms.TextInput(attrs={'tabindex': '3' }))

    phone = forms.CharField(help_text="", widget=forms.TextInput(attrs={'data-trigger': 'change', 'placeholder': '+1 415 225 6464', 'title': 'Shows on your profile. Include country code.', 'tabindex': '4'}))

    position = forms.ChoiceField(choices=Lawyer.LAWYER_ROLES.get_choices(), label="Position")
    years_practiced = forms.IntegerField(label="Years Practicing", initial="3", widget=forms.TextInput(attrs={'data-trigger': 'change', 'class': 'input-mini', 'tabindex': '6'}))

    bar_membership_input = forms.CharField(required=False, label="Bar Location", help_text='Enter the location of your bar memberships.', widget=forms.TextInput(attrs={'class': 'input-large', 'placeholder': 'California', 'title': 'The state you are licensed in', 'tabindex': '7'}))
    bar_membership = forms.CharField(required=False, widget=forms.HiddenInput)

    practice_location_1 = forms.CharField(label="Primary Location", widget=forms.TextInput(attrs={'class': 'input-large', 'placeholder': 'San Francisco, California', 'title': 'The primary city you operate from', 'tabindex': '8'}))
    practice_location_2 = forms.CharField(required=False, label="Secondary Location", widget=forms.TextInput(attrs={'class': 'input-large', 'placeholder': 'London, England', 'title': 'Optional. The secondary city you operate from.', 'tabindex': '9'}))

    summary = forms.CharField(label="Short description", widget=forms.TextInput(attrs={'data-trigger': 'change', 'data-rangelength': '[0,1024]', 'class': 'input-xxlarge', 'placeholder': 'e.g. Partner at Orrick advising technology companies in Europe', 'title': 'Keep it short, and make it personal.'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'data-trigger': 'change', 'class': 'input-xxlarge', 'data-rangelength': '[0,4024]', 'placeholder': 'A bit more about you.', 'title': 'A bit longer, but still make it personal.'}))
    if_i_wasnt_a_lawyer = forms.CharField(label="If I wasn't a lawyer", required=False, widget=forms.TextInput(attrs={'data-trigger': 'change', 'class': 'input-xxlarge', 'placeholder': 'e.g. Astronaut and part-time Pastry Chef', 'title': 'If I wasn\'t a lawyer, I would be a...'}))

    photo = forms.ImageField(required=False, label="Main Photo", help_text="Please add a good quality photo to your profile. It really helps.", widget=CicuUploaderInput(attrs={'data-trigger': 'change', 'data-required': 'false'}, options={
                'ratioWidth': '110',       #fix-width ratio, default 0
                'ratioHeight': '110',       #fix-height ratio , default 0
                'sizeWarning': 'False',    #if True the crop selection have to respect minimal ratio size defined above. Default 'False'
                'modalButtonLabel': 'Upload photo',
                'onReady': 'preparePhotoPreview',
                'onCrop': 'photoCrop'
            }))
    
    hidden_photo = forms.CharField(required=False, widget=forms.HiddenInput) # transports the id

    twitter = forms.CharField(required=False, label="twitter.com/", help_text="", widget=forms.TextInput(attrs={}))

    websites_input = forms.URLField(required=False, label="Website Address", help_text='Enter the domain name of your public website, if you have one.', widget=forms.TextInput(attrs={}))
    websites = forms.CharField(required=False, widget=forms.HiddenInput)

    companies_advised_input = forms.URLField(required=False, label="Companies Advised", help_text='Enter the domain name of any companies you have advised and press "Add". It must be public knowledge that you have advised them.', widget=forms.TextInput(attrs={'placeholder': 'e.g. Instagram.com'}))
    companies_advised = forms.CharField(required=False, widget=forms.HiddenInput)

    volume_incorp_setup = forms.CharField(required=False, widget=forms.HiddenInput) # list of lists :[[2010,2011,2012]]
    volume_seed_financing = forms.CharField(required=False, widget=forms.HiddenInput) # list of lists :[[2010,2011,2012]]
    volume_series_a = forms.CharField(required=False, widget=forms.HiddenInput) # list of lists :[[2010,2011,2012]]
    volume_ip = forms.CharField(required=False, widget=forms.HiddenInput) # list of lists :[[2010,2011,2012]]
    volume_other = forms.CharField(required=False, widget=forms.HiddenInput) # list of lists :[[2010,2011,2012]]

    volume_by_year = forms.CharField(required=False, widget=forms.HiddenInput)

    seed_financing_amount_min = forms.IntegerField(required=False, initial=0, label="Seed Financing Min", widget=forms.TextInput(attrs={'data-trigger': 'change', 'class': 'input-mini', 'title': 'Seed financing minimum e.g. 500'}))
    seed_financing_amount_max = forms.IntegerField(required=False, initial=0, label="Seed Financing Max", widget=forms.TextInput(attrs={'data-trigger': 'change', 'data-morethanorequal': '#id_seed_financing_amount_min', 'data-morethanorequal-message': 'This value should be more than the "Seed Financing" min.', 'class': 'input-mini', 'title': 'Seed financing maximum e.g. 50000'}))
    seed_fee_cap_available = forms.BooleanField(required=False, label='Fee cap available for this transaction?', widget=forms.CheckboxInput)
    seed_deferred_fees_available = forms.BooleanField(required=False, label='Deferred fees available for this transaction?', widget=forms.CheckboxInput)
    seed_fixed_fees_available = forms.BooleanField(required=False, label='Fixed fees available for this transaction?', widget=forms.CheckboxInput)

    incorporation_min = forms.IntegerField(required=False, initial=0, label="Incorporation Min", widget=forms.TextInput(attrs={'data-trigger': 'change', 'class': 'input-mini', 'title': 'Incorporation minimum e.g. 500'}))
    incorporation_max = forms.IntegerField(required=False, initial=0, label="Incorporation Max", widget=forms.TextInput(attrs={'data-trigger': 'change', 'data-morethanorequal': '#id_incorporation_min', 'data-morethanorequal-message': 'This value should be more than the "Incorporation" min.', 'class': 'input-mini', 'title': 'Incorporation maximum e.g. 50000'}))
    inc_fee_cap_available = forms.BooleanField(required=False, label='Fee cap available for this transaction?', widget=forms.CheckboxInput)
    inc_deferred_fees_available = forms.BooleanField(required=False, label='Deferred fees available for this transaction?', widget=forms.CheckboxInput)
    inc_fixed_fees_available = forms.BooleanField(required=False, label='Fixed fees available for this transaction?', widget=forms.CheckboxInput)

    optional_funding = forms.CharField(required=False, help_text="", widget=forms.TextInput(attrs={'placeholder': 'Package name', 'class': 'inline-form-element'}))
    optional_min = forms.IntegerField(required=False, initial=0, label="Optional Min", widget=forms.TextInput(attrs={'data-trigger': 'change', 'class': 'input-mini', 'title': 'minimum e.g. 500'}))
    optional_max = forms.IntegerField(required=False, initial=0, label="Optional Max", widget=forms.TextInput(attrs={'data-trigger': 'change', 'data-morethanorequal': '#id_optional_min', 'class': 'input-mini', 'title': 'maximum e.g. 50000'}))
    optional_fee_cap_available = forms.BooleanField(required=False, label='Fee cap available for this transaction?', widget=forms.CheckboxInput)
    optional_deferred_fees_available = forms.BooleanField(required=False, label='Deferred fees available for this transaction?', widget=forms.CheckboxInput)
    optional_fixed_fees_available = forms.BooleanField(required=False, label='Fixed fees available for this transaction?', widget=forms.CheckboxInput)

    optional_funding2 = forms.CharField(required=False, help_text="", widget=forms.TextInput(attrs={'placeholder': 'Package name', 'class': 'inline-form-element'}))
    optional_min2 = forms.IntegerField(required=False, initial=0, label="Optional Min", widget=forms.TextInput(attrs={'data-trigger': 'change', 'class': 'input-mini', 'title': 'minimum e.g. 500'}))
    optional_max2 = forms.IntegerField(required=False, initial=0, label="Optional Max", widget=forms.TextInput(attrs={'data-trigger': 'change', 'data-morethanorequal': '#id_optional_min2', 'data-morethanorequal-message': 'This value should be more than the min.', 'class': 'input-mini', 'title': 'maximum e.g. 50000'}))
    optional_fee_cap_available2 = forms.BooleanField(required=False, label='Fee cap available for this transaction?', widget=forms.CheckboxInput)
    optional_deferred_fees_available2 = forms.BooleanField(required=False, label='Deferred fees available for this transaction?', widget=forms.CheckboxInput)
    optional_fixed_fees_available2 = forms.BooleanField(required=False, label='Fixed fees available for this transaction?', widget=forms.CheckboxInput)

    optional_funding3 = forms.CharField(required=False, help_text="", widget=forms.TextInput(attrs={'placeholder': 'Package name', 'class': 'inline-form-element'}))
    optional_min3 = forms.IntegerField(required=False, initial=0, label="Optional Min", widget=forms.TextInput(attrs={'data-trigger': 'change', 'class': 'input-mini', 'title': 'minimum e.g. 500'}))
    optional_max3 = forms.IntegerField(required=False, initial=0, label="Optional Max", widget=forms.TextInput(attrs={'data-trigger': 'change', 'data-morethanorequal': '#id_optional_min3', 'data-morethanorequal-message': 'This value should be more than the min.', 'class': 'input-mini', 'title': 'maximum e.g. 50000'}))
    optional_fee_cap_available3 = forms.BooleanField(required=False, label='Fee cap available for this transaction?', widget=forms.CheckboxInput)
    optional_deferred_fees_available3 = forms.BooleanField(required=False, label='Deferred fees available for this transaction?', widget=forms.CheckboxInput)
    optional_fixed_fees_available3 = forms.BooleanField(required=False, label='Fixed fees available for this transaction?', widget=forms.CheckboxInput)

    agree_tandc = forms.BooleanField(label='', widget=forms.CheckboxInput)

    def __init__(self, *args, **kwargs):
        """ get request object and user """
        self.request = kwargs.pop('request', None)
        self.user = self.request.user
        self.data_source_urls = API_URLS
        super(LawyerProfileSetupForm, self).__init__(*args, **kwargs)
        self.inject_email_pass_objects()

    def inject_email_pass_objects(self):
        """ If the user has not yet defined a password
        I.e they are new, then show the email and password elements
        """
        if self.user.password == '!':
            self.fields['email'] = forms.EmailField(label="Firm email", help_text="", widget=forms.TextInput(attrs={'data-trigger': 'change', 'placeholder': 'john@lawpal.com'}))
            self.fields['password'] = forms.CharField(label="Password", help_text="", widget=forms.PasswordInput(attrs={'data-trigger': 'change'}))
            self.fields['password_confirm'] = forms.CharField(label="Confirm password", help_text="", widget=forms.PasswordInput(attrs={'data-trigger': 'change', 'minLength': '5', 'data-equalto': '#id_password'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.exclude(pk=self.user.pk).get(email=email)
            msg = 'Sorry but a User with that email already exists (id: %s)' % (self.user.pk)
            logging.error(msg)
            raise exceptions.ValidationError(msg)
        except User.DoesNotExist:
            # ok this lawyer is valid
            pass
        return email

    def clean_hidden_photo(self):
        hidden_photo = self.cleaned_data.get('hidden_photo', None)
        return int(hidden_photo) if hidden_photo else None

    def clean(self):
        cleaned_data = super(LawyerProfileSetupForm, self).clean()
        msg = 'Sorry but the minimum amount needs to be lower than the maximum'
        min_max_li = [('seed_financing_amount_min', 'seed_financing_amount_max'), ('incorporation_min', 'incorporation_max'), ('optional_min', 'optional_max'), ('optional_min2', 'optional_max2'), ('optional_min3', 'optional_max3')]

        for min, max in min_max_li:
            min = cleaned_data.get(min)
            max = cleaned_data.get(max)

            if min > max:
                logging.error(msg)
                raise exceptions.ValidationError(msg)

        return cleaned_data

    def delete_cookie(self, cookie_name):
        if self.request.COOKIES.get(cookie_name, None) is not None:
            del(self.request.COOKIES[cookie_name])

    def delete_cookies(self):
        """ Remove the lawyer_profile cookie set when photo is uploaded """
        self.delete_cookie('lawyer_profile_photo-%d' % self.user.pk)
        # startup list
        self.delete_cookie('company_list-%d' % self.user.pk)
        # websites list
        self.delete_cookie('website_list-%d' % self.user.pk)
        # bar_membership list
        self.delete_cookie('bar_membership-%d' % self.user.pk)
        

    def save(self, commit=True):
        logger.info('Ensuring the LawyerProfile Exists')

        data = self.cleaned_data

        firm_name = data.pop('firm_name')

        # @TODO should be in the clean_photo method
        hidden_photo = self.cleaned_data.get('hidden_photo', None)
        if type(hidden_photo) is int:
            try:
                data['photo'] = UploadedFile.objects.get(pk=hidden_photo)
            except UploadedFile.DoesNotExist:
                data['photo'] = None


        offices = []
        # dont pop these as we need them for local storage in lawyer
        offices.append(data.get('practice_location_1', None))
        offices.append(data.get('practice_location_2', None))

        lawyer_service = EnsureLawyerService(user=self.user, firm_name=firm_name, offices=offices, form=self, **data)
        lawyer_service.process()

        self.delete_cookies()
        # clear the nav cache for the user
        cache.delete(make_template_fragment_key("user", ["mugshot", self.request.user.pk]))

        logger.info('Complete: Ensuring the LawyerProfile Exists')


@parsleyfy
class LawyerSearchForm(forms.Form):
    q = forms.CharField(label='', help_text='', required=False, widget=forms.TextInput(attrs={'placeholder': 'Anywhere', 'tabindex': '1', 'class': 'input-xlarge typeahead', 'autocomplete': 'off', 'data-provide': 'ajax', 'minLength': '2', 'data-items': 5, 'data-source': API_URLS.get('locations'), 'data-filter': 'name__istartswith', 'tabindex': '2', 'data-toggle': 'tooltip', 'title': 'Enter a Location or just leave it blank'}))

    def __init__(self, *args, **kwargs):
        """ get request object and user """
        self.api_urls = API_URLS
        self.request = kwargs.pop('request', None)
        self.user = self.request.user
        super(LawyerSearchForm, self).__init__(*args, **kwargs)


class LawyerProfileIsCompleteValidator(forms.Form):
    """ is used by the profile_complete template tag 
    to evaluate the completeness of a lawyers profile """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    firm_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    position = forms.CharField(required=True)
    years_practiced = forms.IntegerField(required=True)
    practice_location_1 = forms.CharField(required=True)
    fee_packages = forms.CharField(required=True)
    summary = forms.CharField(required=True)
