from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.template.defaultfilters import slugify
from django.core import exceptions

from django.contrib.auth.models import User

from parsley.decorators import parsleyfy
from bootstrap.forms import BootstrapMixin, Fieldset

from userena.forms import SignupFormOnlyEmail
from userena import settings as userena_settings
from userena import signals as userena_signals
from django_countries.countries import COUNTRIES_PLUS

ACCEPTED_COUNTRIES = ('GB',)

COUNTRIES_PLUS = [(i,c) for i,c in COUNTRIES_PLUS if i in ACCEPTED_COUNTRIES]


@parsleyfy
class ConfirmLoginDetailsForm(forms.ModelForm):
    """ Shown to the user when they login using linked in 
    Is the first form they see after signing in
    """
    username = forms.CharField(widget=forms.HiddenInput)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise exceptions.ValidationError(_('Passwords do not match'))
        return password

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
