# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from bootstrap.forms import BootstrapForm, Fieldset


import datetime


DATE_FORMAT = "%a, %d %b %Y"
def _get_date_today():
  return datetime.date.today().strftime(DATE_FORMAT)


class CreateStepForm(BootstrapForm):
    """ The template form used to help the authoring tool """
    STEP_TYPES = (
        ('step', 'Normal Step'),
        ('loop-step', 'Loop Step')
    )

    type = forms.ChoiceField(choices=STEP_TYPES, initial='step')
    hide_from = forms.CharField(max_length=32, widget=forms.Select)
    step_title = forms.CharField(max_length=32, initial=_('Step No. 1'))
    iteration_title = forms.CharField(max_length=32)

    class Meta:
        layout = (
            Fieldset("Step Details", "step_title", "type", "hide_from", "iteration_title", ),
        )


class CreateStepFieldForm(BootstrapForm):
    """ The template form used to help the authoring tool """
    # Overrides
    VALID_FIELD_TYPES = ['ChoiceField', 'CharField', 'IntegerField', 'DecimalField', 'DateFieldField', 'USStatesField', 'CountryField']
    VALID_WIDGETS = ['SocialContactWidget', 'InviteeWidget', 'TextInput', 'Textarea', 'Select', 'RadioSelect', 'SelectMultiple']
    FIELDS = [(v, v) for v in sorted(VALID_FIELD_TYPES)]
    WIDGETS = [('', 'Default')] + [(v, v) for v in sorted(VALID_WIDGETS)]

    label = forms.CharField(label=_('Question'))
    name = forms.CharField(label=_('Doc. Variable'), help_text=_('The Variable to use in the document'))
    placeholder = forms.CharField(help_text=_('A Hint which is not submittable'))
    help_text = forms.CharField()
    initial = forms.CharField(label=_('Inital Value'), help_text=_('The initial submittable Value of this field - not required'))
    required = forms.ChoiceField(choices=(('true',_('Yes')), ('false',_('No'))), initial='false', required=False)
    field = forms.ChoiceField(choices=FIELDS, initial='CharField')
    widget = forms.ChoiceField(choices=WIDGETS, initial='')
    choices = forms.CharField(widget=forms.Textarea, help_text=_('In the form [["a","Alpha"], [1,"One"], [1,1]]'))
    css_class = forms.CharField(initial='md-updater', help_text=_('*md-updater, contact-list'))

    class Meta:
        layout = (
            Fieldset("Question", "label", "name", "placeholder", "help_text", "initial", "required", "field", "widget", "choices", "css_class"),
        )


class DocumentForm(BootstrapForm):
    body = forms.ChoiceField(widget=forms.widgets.Textarea(attrs={'class':'span6'}))


class DocumentMetaForm(BootstrapForm):
    """ The template form used to help the authoring tool document meta """
    can_add_invite = forms.ChoiceField(label=_('Allow 3rd parties to sign'), choices=(('true','Yes'),('false','No')), initial='false', help_text=_('Can the user invite extra People to sign?'))

    class Meta:
        layout = (
            Fieldset("Document Meta", "can_add_invite", ),
        )