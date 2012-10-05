# -*- coding: utf-8 -*-
from django import forms
from bootstrap.forms import BootstrapMixin, Fieldset

from glynt.apps.document.models import ClientCreatedDocument

import datetime

DATE_FORMAT = "%a, %d %b %Y"
def _get_date_today():
  return datetime.date.today().strftime(DATE_FORMAT)


class ClientCreatedDocumentForm(forms.ModelForm):
  id = forms.IntegerField(required=False, widget=forms.HiddenInput)
  name = forms.CharField(label='', required=True, max_length=128, widget=forms.HiddenInput)

  class Meta:
    model = ClientCreatedDocument
    fields = ('id', 'name')


class CreateStepForm(forms.Form, BootstrapMixin):
    """ The template form used to help the authoring tool """
    STEP_TYPES = (
        ('step', 'Normal Step'),
        ('loop-step', 'Loop Step')
    )
    step_type = forms.ChoiceField(choices=STEP_TYPES)
    step_type = forms.ChoiceField(choices=STEP_TYPES)

    class Meta:
        layout = (
            Fieldset("Login Details", "email", "password1", "password2"),
        )


class CreateStepFieldForm(forms.Form, BootstrapMixin):
    """ The template form used to help the authoring tool """

    class Meta:
        layout = (
            Fieldset("Login Details", "email", "password1", "password2"),
        )