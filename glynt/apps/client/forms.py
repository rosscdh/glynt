# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.template.defaultfilters import slugify
from django.core import exceptions

from django.contrib.auth.models import User

from parsley.decorators import parsleyfy
from bootstrap.forms import BootstrapMixin, Fieldset

from userena.forms import SignupFormOnlyEmail
from django_countries.countries import COUNTRIES_PLUS

from glynt.apps.company.services import EnsureCompanyService
from glynt.apps.customer.services import EnsureCustomerService

ACCEPTED_COUNTRIES = ('GB',)

COUNTRIES_PLUS = [(i, c) for i, c in COUNTRIES_PLUS if i in ACCEPTED_COUNTRIES]

import logging
logger = logging.getLogger('django.request')


@parsleyfy
class ConfirmLoginDetailsForm(forms.ModelForm):
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

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise exceptions.ValidationError(_('Passwords do not match'))

        return password

    def save(self, commit=True):
        user = super(ConfirmLoginDetailsForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save(update_fields=['password'])

            data = self.cleaned_data.copy()
            data.pop('password')
            data.pop('confirm_password')

            customer_service = EnsureCustomerService(user=user, **data)
            customer = customer_service.process()

            comapny_service = EnsureCompanyService(name=data.pop('company'), customer=user.customer_profile, **data)
            comapny_service.process()
        return user


class SignupForm(BootstrapMixin, SignupFormOnlyEmail):
    """ The signup form overrides the Userena save method and hooks it up
    to our own UserSignup model and process allowing us to expand on fields saved """
    first_name = forms.CharField(max_length=24)
    last_name = forms.CharField(max_length=24)
    country = forms.ChoiceField(choices=COUNTRIES_PLUS, initial='GB')
    state = forms.CharField(max_length=128)

    class Meta:
        layout = (
            Fieldset("Login Details", "email", "password1", "password2"),
            Fieldset("Your Account Details", "first_name", "last_name", "country", "state")
        )

    def generate_username_from_email(self, email):
        username = slugify(email)

        return '%s' % (username[0:30])


class AuthenticationForm(BootstrapMixin, AuthenticationForm):
    username = forms.CharField(label=_("Email or Username"), max_length=30, widget=forms.TextInput(attrs={'placeholder': 'username@example.com'}))
    password = forms.CharField(label=_("Password"), max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'password'}))

    class Meta:
        layout = (
            Fieldset("Please Login", "username", "password"),
        )
