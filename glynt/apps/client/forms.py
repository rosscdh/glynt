from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.template.defaultfilters import slugify

from bootstrap.forms import BootstrapMixin, Fieldset

from userena.forms import SignupFormOnlyEmail
from userena import settings as userena_settings
from userena import signals as userena_signals
from django_countries.countries import COUNTRIES_PLUS

ACCEPTED_COUNTRIES = ('GB',)

COUNTRIES_PLUS = [(i,c) for i,c in COUNTRIES_PLUS if i in ACCEPTED_COUNTRIES]

from models import UserSignup


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

    def save(self):
        """ Creates a new user and account. Returns the newly created user. """
        username, email, password, first_name, last_name, country, state = (self.cleaned_data['username'] if 'username' in self.cleaned_data else self.generate_username_from_email(self.cleaned_data['email']),
                                      self.cleaned_data['email'],
                                      self.cleaned_data['password1'],
                                      self.cleaned_data['first_name'],
                                      self.cleaned_data['last_name'],
                                      self.cleaned_data['country'],
                                      self.cleaned_data['state'])

        user = UserSignup.objects.create_user(username,
                                                      email,
                                                      password,
                                                      not userena_settings.USERENA_ACTIVATION_REQUIRED,
                                                      userena_settings.USERENA_ACTIVATION_REQUIRED,
                                                      first_name=first_name,
                                                      last_name=last_name,
                                                      country=country,
                                                      state=state)
        # Send the signup complete signal
        userena_signals.signup_complete.send(sender=None,
                                             user=user)

        return user


class AuthenticationForm(BootstrapMixin, AuthenticationForm):
    username = forms.CharField(label=_("Email or Username"), max_length=30, widget=forms.TextInput(attrs={'placeholder': 'username@example.com'}))
    password = forms.CharField(label=_("Password"), max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    class Meta:
        layout = (
          Fieldset("Please Login", "username", "password"),
        )
