# -*- coding: utf-8 -*-
from django import forms
from django.core import exceptions
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

from parsley.decorators import parsleyfy

from glynt.apps.lawyer.services import EnsureLawyerService

from glynt.apps.company.services import EnsureCompanyService
from glynt.apps.customer.services import EnsureCustomerService

import logging
logger = logging.getLogger('django.request')


@parsleyfy
class ConfirmLoginDetailsForm(forms.ModelForm):
    """ Form shown to the use after logging in, assists in capturing the correct email
    """
    first_name = forms.CharField(max_length=24, widget=forms.TextInput(attrs={'placeholder': 'John'}))
    last_name = forms.CharField(max_length=24, widget=forms.TextInput(attrs={'placeholder': 'Doemann'}))
    company_name = forms.CharField(label="Company", help_text='', widget=forms.TextInput(attrs={'placeholder': 'Acme Inc'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'john.doemann@example.com'}))
    phone = forms.CharField(label="Phone number", widget=forms.TextInput(attrs={'data-type': 'phone', 'autocomplete': 'off'}))
    agree_tandc = forms.BooleanField(label='I agree to the <a target="_BLANK" href="{url}">Terms &amp; Conditions</a>', help_text='')

    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        """ get request object and user """
        self.request = kwargs.pop('request', None)
        self.user = self.request.user
        super(ConfirmLoginDetailsForm, self).__init__(*args, **kwargs)
        self.fields['agree_tandc'].label = self.fields['agree_tandc'].label.format(url=reverse_lazy('public:terms'))

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            lawyer_exists = User.objects.exclude(pk=self.user.pk).filter(email=email)
            if len(lawyer_exists) > 0:
                msg = 'Sorry but a user with that email already exists. Please contact Support.'
                logging.error(msg)
                raise exceptions.ValidationError(msg)
        except User.DoesNotExist:
            # ok this lawyer is valid
            pass
        return email

    def save(self, commit=True):
        user = self.user

        if commit is True:
            data = self.cleaned_data.copy()

            if self.user.profile.is_lawyer:
                lawyer_service = EnsureLawyerService(user=self.user, firm_name=data.get('company_name'), offices=[], form=self, **data)
                lawyer_service.process()

            elif self.user.profile.is_customer:
                customer_service = EnsureCustomerService(user=user, **data)
                customer = customer_service.process()

                company_service = EnsureCompanyService(name=data.pop('company_name'), customer=customer, **data)
                company_service.process()

        return user
