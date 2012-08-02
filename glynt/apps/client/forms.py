from django import forms
from django.utils.translation import ugettext_lazy as _

from userena.forms import SignupFormOnlyEmail
from userena import settings as userena_settings
from django_countries.countries import COUNTRIES_PLUS
from models import UserSignup


class SignupForm(SignupFormOnlyEmail):
  country = forms.ChoiceField(choices=COUNTRIES_PLUS, initial='US')
  state = forms.CharField(max_length=128)

  def __generate_username_from_email(self, email):
    """ @TODO very rough make nicer """
    tmp = email.replace('@','_')
    tmp = tmp.replace('.','_')
    tmp = tmp.replace('+','_')
    username = tmp.replace('-','_')

    return '%s' % (username)

  def save(self):
    """ Creates a new user and account. Returns the newly created user. """
    username, email, password, country, state = (self.cleaned_data['username'] if 'username' in self.cleaned_data else self.__generate_username_from_email(self.cleaned_data['email']),
                                  self.cleaned_data['email'],
                                  self.cleaned_data['password1'],
                                  self.cleaned_data['country'],
                                  self.cleaned_data['state'])

    new_user = UserSignup.objects.create_user(username,
                                                  email,
                                                  password,
                                                  not userena_settings.USERENA_ACTIVATION_REQUIRED,
                                                  userena_settings.USERENA_ACTIVATION_REQUIRED,
                                                  country,
                                                  state)

    return new_user