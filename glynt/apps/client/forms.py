from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm

from userena.forms import SignupFormOnlyEmail
from userena import settings as userena_settings
from django_countries.countries import COUNTRIES_PLUS
from models import UserSignup


class SignupForm(SignupFormOnlyEmail):
  """ The signup form overrides the Userena save method and hooks it up 
  to our own UserSignup model and process allowing us to expand on fields saved """
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
                                                  country=country,
                                                  state=state)

    return new_user

class AuthenticationForm(AuthenticationForm):
  #email = forms.EmailField(required=True)
  pass
