# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from bootstrap.forms import BootstrapForm, BootstrapMixin, Fieldset

from glynt.apps.document.models import ClientCreatedDocument
from glynt.apps.flyform.forms import VALID_FIELD_TYPES, VALID_WIDGETS

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

