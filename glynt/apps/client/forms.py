# -*- coding: utf-8 -*-
from django import forms
from django.core import exceptions

from django.contrib.auth.models import User

from parsley.decorators import parsleyfy

from glynt.mixins import ModelFormChangePasswordMixin
from glynt.apps.lawyer.services import EnsureLawyerService

from glynt.apps.company.services import EnsureCompanyService
from glynt.apps.customer.services import EnsureCustomerService

import logging
logger = logging.getLogger('django.request')


@parsleyfy
class ConfirmLoginDetailsForm(ModelFormChangePasswordMixin, forms.ModelForm):
    """ Form shown to the use after logging in, assists in capturing the correct email
    and setting a user password
    """
    first_name = forms.CharField(max_length=24, widget=forms.TextInput(attrs={'tabindex': '1', 'placeholder': 'John'}))
    last_name = forms.CharField(max_length=24, widget=forms.TextInput(attrs={'tabindex': '2', 'placeholder': 'Doemann'}))
    company = forms.CharField(label="Company", help_text='', widget=forms.TextInput(attrs={'tabindex': '3', 'placeholder': 'Acme Inc'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'tabindex': '4', 'placeholder': 'john.doemann@example.com'}))
    telephone = forms.CharField(label="Phone number", widget=forms.TextInput(attrs={'tabindex': '5', 'data-type': 'phone', 'autocomplete': 'off'}))
    agree_tandc = forms.BooleanField(label='I agree to the Terms &amp; Conditions', help_text='')

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        """ get request object and user """
        self.request = kwargs.pop('request', None)
        self.user = self.request.user
        super(ConfirmLoginDetailsForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            lawyer_exists = User.objects.exclude(pk=self.user.pk).filter(email=email)
            if len(lawyer_exists) > 0:
                msg = 'Sorry but a User with that email already exists (email: %s)' % (email)
                logging.error(msg)
                raise exceptions.ValidationError(msg)
        except User.DoesNotExist:
            # ok this lawyer is valid
            pass
        return email

    def save(self, commit=True):
        user = self.user
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save(update_fields=['password'])

            data = self.cleaned_data.copy()
            data.pop('password')
            data.pop('confirm_password')

            if self.user.profile.is_lawyer:
                lawyer_service = EnsureLawyerService(user=self.user, firm_name=data.get('company_name'), offices=[], form=self, **data)
                lawyer_service.process()

            if self.user.profile.is_customer:
                customer_service = EnsureCustomerService(user=user, **data)
                customer = customer_service.process()
                company_service = EnsureCompanyService(name=data.pop('company'), customer=customer, **data)
                company_service.process()

        return user
