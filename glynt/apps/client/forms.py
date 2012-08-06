from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.template.defaultfilters import slugify

from userena.forms import SignupFormOnlyEmail
from userena import settings as userena_settings
from django_countries.countries import COUNTRIES_PLUS
from models import UserSignup


class SignupForm(SignupFormOnlyEmail):
  """ The signup form overrides the Userena save method and hooks it up 
  to our own UserSignup model and process allowing us to expand on fields saved """
  first_name = forms.CharField(max_length=24)
  last_name = forms.CharField(max_length=24)
  country = forms.ChoiceField(choices=COUNTRIES_PLUS, initial='US')
  state = forms.CharField(max_length=128)

  def __generate_username_from_email(self, email):
    username = slugify(email)

    return '%s' % (username[0:30])

  def save(self):
    """ Creates a new user and account. Returns the newly created user. """
    username, email, password, first_name, last_name, country, state = (self.cleaned_data['username'] if 'username' in self.cleaned_data else self.__generate_username_from_email(self.cleaned_data['email']),
                                  self.cleaned_data['email'],
                                  self.cleaned_data['password1'],
                                  self.cleaned_data['first_name'],
                                  self.cleaned_data['last_name'],
                                  self.cleaned_data['country'],
                                  self.cleaned_data['state'])

    new_user = UserSignup.objects.create_user(username,
                                                  email,
                                                  password,
                                                  not userena_settings.USERENA_ACTIVATION_REQUIRED,
                                                  userena_settings.USERENA_ACTIVATION_REQUIRED,
                                                  first_name=first_name,
                                                  last_name=last_name,
                                                  country=country,
                                                  state=state)

    return new_user

class AuthenticationForm(AuthenticationForm):
  username = forms.CharField(label=_("Email or Username"), max_length=30, widget=forms.TextInput(attrs={'placeholder': _('username@example.com')}))
  pass
