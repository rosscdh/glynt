# -*- coding: utf-8 -*-
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


class CreateStepForm(BootstrapForm):
    """ The template form used to help the authoring tool """
    STEP_TYPES = (
        ('step', 'Normal Step'),
        ('loop-step', 'Loop Step')
    )
    class Meta:
        layout = (
            Fieldset("Step Details", "type", "step_title", "hide_from",),
        )
    type = forms.ChoiceField(choices=STEP_TYPES, initial='step')
    step_title = forms.CharField(max_length=32)
    hide_from = forms.CharField(max_length=32, widget=forms.Select)


class CreateStepFieldForm(BootstrapForm):
    """ The template form used to help the authoring tool """
    FIELDS = [(v, v) for v in sorted(VALID_FIELD_TYPES)]
    WIDGETS = [(v, v) for v in sorted(VALID_WIDGETS)]
    class Meta:
        layout = (
            Fieldset("Basic", "label", "placeholder", "help_text", "required",),
            Fieldset("Extra", "field", "widget", "css_class",),
        )
    label = forms.CharField()
    placeholder = forms.CharField()
    help_text = forms.CharField()
    required = forms.BooleanField()
    field = forms.ChoiceField(choices=FIELDS, initial='CharField')
    widget = forms.ChoiceField(choices=WIDGETS, initial='TextInput')
    css_class = forms.CharField(initial='md-updater')
