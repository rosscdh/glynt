# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson as json
from django.template.defaultfilters import slugify
from django.utils import safestring
from bootstrap.forms import BootstrapMixin, Fieldset

from django.contrib.localflavor.us.forms import USStateField, USZipCodeField
from django.contrib.localflavor.us.us_states import US_STATES as SHORT_US_STATES, USPS_CHOICES as SHORT_USPS_CHOICES
from django_countries import CountryFormField as CountryField

US_STATES = [(v,v) for k,v in SHORT_US_STATES]
USPS_CHOICES = [(v,v) for k,v in SHORT_USPS_CHOICES]


CUSTOM_VALID_FIELD_TYPES = ['CountryField', 'USStateField', 'USZipCodeField']
VALID_FIELD_TYPES = CUSTOM_VALID_FIELD_TYPES + ['BooleanField', 'CharField', 'ChoiceField', 'DateField', 'DateTimeField', 'DecimalField', 'EmailField', 'FloatField', 'ImageField', 'IntegerField', 'MultiValueField', 'MultipleChoiceField', 'SlugField', 'TimeField', 'URLField', ]

VALID_WIDGETS = ['TextInput', 'PasswordInput', 'HiddenInput', 'MultipleHiddenInput', 'FileInput', 'ClearableFileInput', 'DateInput', 'DateTimeInput', 'TimeInput', 'Textarea', 'CheckboxInput', 'Select', 'RadioSelect', 'SelectMultiple', 'CheckboxSelectMultiple', 'SplitDateTimeWidget', 'SelectDateWidget',]

import sys

def customFields(fieldTypeName):
  if fieldTypeName in CUSTOM_VALID_FIELD_TYPES:
    retr

class BaseFlyForm(forms.Form, BootstrapMixin):
  """ This form is the basis for the self generating form representations
  it requires that a valid json_object be passed in which adheres to the following schema
  schema = {
    "type" : "step",
    "properties" : {
      "step_title" : {"type" : "string"},
      hide_from = forms.CharField(),
      hide_to = forms.CharField(),
      iteration_title = forms.CharField(),
    },
    "fields": [
        "field" : {"type" : "number"},
        "widget" : {"type" : "string"},
        "name" : {"type" : "string"},
        "label" : {"type" : "string"},
        "required" : {"type" : "boolean"},
        "help_text" : {"type" : "string"},
        "placeholder" : {"type" : "string"},
        "class" : {"type" : "string"},
        "data-hb-name" : {"type" : "string"},
        "data-show_when":"customer_country == 'United States'",
        "data-hide_when":"function(){ customer_country == 'Germany' }"
      ]
  }
  """
  class Meta:
    layout = ()

  def __init__(self, step_num=None, json_form=None, data=None, files=None, auto_id='id_%s', prefix=None,
               initial=None, error_class=ErrorList, label_suffix=':',
               empty_permitted=False):

    super(BaseFlyForm, self).__init__(data, files, auto_id, prefix,
                            initial, error_class, label_suffix,
                            empty_permitted)

    self.step_num = step_num if step_num > 0 else 1

    if json_form is not None:
      self.setup_form(json_form)

    self.bootstrap_layout()

  def bootstrap_layout(self):
    step_title = "Step %d" % (self.step_num,)
    layout_keys = [step_title] + self.fields.keys()
    self.Meta.layout = self.Meta.layout + ( Fieldset(*layout_keys), )

  def setup_form(self, json_form):
    """ Main form setup method used to generate the base form fields """
    schema = json_form if isinstance(json_form, dict) else json.loads(json_form)
    #@TODO
    #self.validate_schema(schema)
    self.setup_step_title(schema)
    self.setup_fields(schema['fields'])

  def slugify(self, text):
    """ Modified slugify replaced - with _ """
    return '%s' %(slugify(text).replace('-','_'),)

  def string_attribs(self, attribs):
    """ convert flat dict into string version """
    attribs_as_s = ''
    for k,v in attribs.iteritems():
      if v:
        attribs_as_s += "'%s': '%s'," % (k, v, )
    # remove last , and return
    if attribs_as_s != '':
      return '[{%s}]' % (attribs_as_s[0:-1], )
    else:
      return None

  def setup_step_title(self, step_schema):
    """ Setup the step info field """
    loop_step_attrs = None
    # setup step title
    step_attrs = {
      'data-step-title': step_schema['properties']['step_title'],
    }

    if step_schema['type'] == 'loop-step':
      step_attrs['data-glynt-loop_step'] = self.define_loopstep_attribs(step_schema)

    self.fields['step_title'] = forms.CharField(max_length=128, required=False, widget=forms.HiddenInput(attrs=step_attrs))

  def define_loopstep_attribs(self, step_schema):
    """ Make the appropriate changes should a loop-step present itself """
    step_schema['properties']['iteration_title'] = step_schema['properties']['iteration_title'] if 'iteration_title' in step_schema['properties'] and step_schema['properties']['iteration_title'] else step_schema['properties']['step_title']
    loop_step_attrs = {
      "iteration_title": step_schema['properties']['iteration_title'],
      "hide_from": self.slugify(step_schema['properties']['hide_from']),
    }
    return safestring.mark_safe(self.string_attribs(loop_step_attrs))

  def setup_fields(self, schema_fields):
    if len(schema_fields) > 0:
      for field in schema_fields:
        f = getattr(forms.fields, field['field'], None) if field['field'] else None

        # Is custom imported field
        if f is None:
          f = getattr(sys.modules[__name__], field['field'], None)

        if f:
          field_instance = f()
          field_instance.label = field['label'] if field['label'] else field['name']
          field_instance.name = self.slugify(field['name']) if field['name'] else self.slugify(field_instance.label)
          field_instance.help_text = field['help_text'] if field['help_text'] else None
          field_instance.required = True if field['required'] in ['true',True,'1', 1] else False
          if 'initial' in field:
            field_instance.initial = field['initial']

          if hasattr(f, 'choices') and 'choices' in field:
            # Add log here as sometimes choices may be present but not specified
            field_instance.choices = self.valid_choice_options(field['choices'])

          widget = self.setup_field_widget(field_instance, field)
          if widget:
            field_instance.widget = widget

          # Append the field
          self.fields[field_instance.name] = field_instance

  def valid_choice_options(self, choices):
    """ Converts JSON fomrat tuple into python tuple 
    expects JSON format tuple in form:
    [[k,v],[k,v]]
    Also accepts String which must equate to a locally availabel variable
    """
    if type(choices) in [unicode, str]:
      local_choice = getattr(sys.modules[__name__], choices, None)
      if local_choice is not None:
        return local_choice
    elif type(choices) is list:
      return tuple(tuple(c) for c in choices)
    else:
      return tuple()

  def setup_field_widget(self, field_instance, field_dict):
    w = getattr(forms.widgets, field_dict['widget'], None) if field_dict['widget'] else None
    if w:
      widget = w()
    else:
      widget = field_instance.widget

    widget.attrs = {
      'class': field_dict['class'],
      'placeholder': field_dict['placeholder'],
      'data-hb-name': field_dict['data-hb-name'] if field_dict['data-hb-name'] else field_instance.name,
    }

    if 'data-show_when' in field_dict:
      widget.attrs['data-show_when'] = safestring.mark_safe(field_dict['data-show_when'])
    if 'data-hide_when' in field_dict:
      widget.attrs['data-hide_when'] = safestring.mark_safe(field_dict['data-hide_when'])

    # Handle loop step loop length fields, required to make the loop function
    if 'data-glynt-loop_length' in field_dict:
      widget.attrs['data-glynt-loop_length'] = len(field_instance.choices) if hasattr(field_instance, 'choices') else ''


    return widget



class TmpStepCreator(forms.Form):
  updater_class = forms.CharField(initial='md-updater', widget=forms.widgets.HiddenInput())
  #data-hb-name = forms.CharField()
  name = forms.CharField(label='slugify version of label', help_text='a slugified version of the label used as template variables', required=True, widget=forms.widgets.HiddenInput())
  label = forms.CharField(label='Field Name', help_text='This name becomes the variable name for use in the doc.. i.e. First Name becomes first_name', required=False)
  help_text = forms.CharField(label='Help', help_text='This is the extended help text, that is abde available via a tooltip', required=False)
  placeholder = forms.CharField(label='Placeholder', help_text='A prompt for the value that the field expects i.e. if the field is Email then the prompt would be your_name@example.com', required=False)
  required = forms.BooleanField(label='Is Required', help_text='Is this a required value; can the user progress without filling it in', initial=True)
  field_type = forms.ChoiceField(label='Type of Field', help_text='What kind of data does this field expect?', choices=tuple((i,i) for i in sorted(VALID_FIELD_TYPES)), initial='CharField')
  widget = forms.ChoiceField(label='Widget', help_text='How should the value this Field be captured? i.e. SelectBox for a dropdown or TextArea for lots of text or other', choices=tuple((i,i) for i in sorted([""] + VALID_WIDGETS)), initial='TextInput')




