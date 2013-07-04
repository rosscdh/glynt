# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core import exceptions

from django.contrib.auth.models import User

from parsley.decorators import parsleyfy
from bootstrap.forms import BootstrapMixin

from django_countries.countries import COUNTRIES_PLUS

from glynt.apps.lawyer.services import EnsureLawyerService

from glynt.apps.company.services import EnsureCompanyService
from glynt.apps.customer.services import EnsureCustomerService

ACCEPTED_COUNTRIES = ('GB',)

COUNTRIES_PLUS = [(i, c) for i, c in COUNTRIES_PLUS if i in ACCEPTED_COUNTRIES]

import logging
logger = logging.getLogger('django.request')


class ChangePasswordMixinBase(object):
    """ Mixin used to ensure passwords match """
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise exceptions.ValidationError(_('Passwords do not match'))

        return password


class ChangePasswordMixinModelForm(ChangePasswordMixinBase, forms.ModelForm):
    pass


class ChangePasswordMixin(ChangePasswordMixinBase, forms.Form):
    pass


class ConfirmChangePasswordMixinBase(object):
    """ Mixin used to ensure that the current_password was entered properly """
    current_password = forms.CharField(widget=forms.PasswordInput)

    def clean_current_password(self):
        if not self.user:
            raise exceptions.ValidationError(_('No User was provided for this form'))

        current_password = self.cleaned_data.get('current_password')

        if not self.user.check_password(current_password):
            raise exceptions.ValidationError(_('The Password entered as "%s" is not correct' % (self.fields['current_password'].label,)))

        return current_password


class ConfirmChangePasswordMixinModelForm(ConfirmChangePasswordMixinBase, forms.ModelForm):
    pass


class ConfirmChangePasswordMixin(ConfirmChangePasswordMixinBase, forms.Form):
    pass


@parsleyfy
class ConfirmLoginDetailsForm(BootstrapMixin, ConfirmChangePasswordMixinModelForm, forms.ModelForm):
    """ Shown to the user when they login using linked in
    Is the first form they see after signing in
    """
    first_name = forms.CharField(max_length=24, widget=forms.TextInput(attrs={'placeholder': 'John', 'tabindex': '1'}))
    last_name = forms.CharField(max_length=24, widget=forms.TextInput(attrs={'placeholder': 'Doemann', 'tabindex': '2'}))
    company = forms.CharField(label="Company Name", help_text='', widget=forms.TextInput(attrs={'placeholder': 'Acme Inc', 'tabindex': '3'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'john.doemann@example.com', 'tabindex': '4'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'tabindex': '5'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'tabindex': '6'}))
    agree_tandc = forms.BooleanField(label='', help_text='I agree to the Terms &amp; Conditions', widget=forms.CheckboxInput(attrs={'tabindex': '7'}))

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
        user = super(ConfirmLoginDetailsForm, self).save(commit=False)
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
