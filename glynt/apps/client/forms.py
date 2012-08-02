from django import forms
from django.utils.translation import ugettext_lazy as _

from userena.forms import SignupFormOnlyEmail


class SignupForm(SignupFormOnlyEmail):
    country = forms.CharField(max_length=128)
    state = forms.CharField(max_length=128)