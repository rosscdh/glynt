# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson as json
from django.utils import safestring
from django.template.defaultfilters import slugify
from bootstrap.forms import BootstrapMixin, Fieldset

from django.contrib.localflavor.us.forms import USStateField, USZipCodeField
from django.contrib.localflavor.us.us_states import US_STATES as SHORT_US_STATES, USPS_CHOICES as SHORT_USPS_CHOICES
from django_countries import CountryFormField as CountryField

US_STATES = [(v,v) for k,v in SHORT_US_STATES]
USPS_CHOICES = [(v,v) for k,v in SHORT_USPS_CHOICES]

# Custom Fields
USStatesField = forms.ChoiceField(choices=US_STATES)
USStatesUPSField = forms.ChoiceField(choices=USPS_CHOICES)


CUSTOM_VALID_FIELD_TYPES = ['CountryField', 'USStatesField', 'USStatesUPSField']
VALID_FIELD_TYPES = CUSTOM_VALID_FIELD_TYPES + ['BooleanField', 'CharField', 'ChoiceField', 'DateField', 'DateTimeField', 'DecimalField', 'EmailField', 'FloatField', 'ImageField', 'IntegerField', 'MultiValueField', 'MultipleChoiceField', 'SlugField', 'TimeField', 'URLField', ]


VALID_WIDGETS_CUSTOM = ['SocialContactWidget', 'InviteeWidget']
VALID_WIDGETS = ['TextInput', 'PasswordInput', 'HiddenInput', 'MultipleHiddenInput', 'FileInput', 'ClearableFileInput', 'DateInput', 'DateTimeInput', 'TimeInput', 'Textarea', 'CheckboxInput', 'Select', 'RadioSelect', 'SelectMultiple', 'CheckboxSelectMultiple', 'SplitDateTimeWidget', 'SelectDateWidget'] + VALID_WIDGETS_CUSTOM


# Custom Widgets
forms.widgets.InviteeWidget = forms.TextInput(attrs={"class": "md-updater is_invitee"})
forms.widgets.SocialContactWidget = forms.TextInput(attrs={"class": "md-updater contact-list"})



import sys
import re
import copy


def customFields(fieldTypeName):
  if fieldTypeName in CUSTOM_VALID_FIELD_TYPES:
    retr


class LoopStepCleanFieldsMixin(object):
    """ need to handle loop-step forms slightly differently
    as they are repitions of a single form, similar to django formsets
    https://docs.djangoproject.com/en/dev/topics/forms/formsets/ """
    def is_valid_loopstep_count(self, value):
        value_type = type(value)
        if (value_type is int or value.isdigit()) and int(value) > 0:
            return True
        if value_type is bool and value in [True]:
            return True
        if value_type is str and value.lowercase() in ['yes', 'y', '1', 'true']:
            return True
        return False

    def process_loopstep(self):
        steps = {}

        for k, v in self.data.iteritems():
            match = re.findall(r'(.+)_(\d+)$', k)

            if len(match) >= 1:
                key,index = match[0]
                index = int(index)
                if index not in steps:
                    steps[index] = {}
                steps[index][key] = v

        self.validate_loopstep(steps)
        #assert False

    def validate_loopstep(self, steps):
        original_data = self.data.copy()
        for k, data in steps.iteritems():
            form = copy.deepcopy(self)
            original_data.update(data)
            form.__init__(None, self.schema, original_data)
            form.form_type = 'step'
            #form.data.update(data)
            if not form.is_valid():
                self._errors[k] = form._errors


class StepHiddenFieldsMixin(object):
    """ uses the step.hidden_fields field which is populated by javascript
    with a list of fields in the step that are not visible, and thus should not be validated """
    def process_hidden_fields(self):
        try:
            hidden_fields = json.loads(self.data['hidden_fields'])
        except ValueError:
            hidden_fields = []

        for f in hidden_fields:
            if f in self.fields:
                # init any calls on the is_required false
                self.fields[f].is_required = False
                # delete the field form the form
                del(self.fields[f])


class BaseFlyForm(forms.Form, LoopStepCleanFieldsMixin, StepHiddenFieldsMixin, BootstrapMixin):
  """ This form is the basis for the self generating form representations
  the base structure is
  {
    "meta": {
        "can_add_invite": True|False
    },
    "steps": []
  }
  the steps propery requires that a valid json_object be passed in which adheres to the following schema
  schema = {
    "type" : "step", # step, loop-step
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
        "class" : {"type" : "string"}, # *md-updater, contact-list
        "data-hb-name" : {"type" : "string"},
        "choices": [['a','a'], [1,1]],
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

  def _clean_fields(self):
    if self.form_type == 'loop-step':
        hide_from_name = self.schema['properties']['hide_from']
        hide_from_value = self.data[hide_from_name]
        if self.is_valid_loopstep_count(hide_from_value):
            # custom validation based on many of same value
            self.process_loopstep()
    else:
        self.process_hidden_fields()
        super(BaseFlyForm, self)._clean_fields()

  def bootstrap_layout(self):
    step_title = "Step %d" % (self.step_num,)
    layout_keys = [step_title] + self.fields.keys()
    self.Meta.layout = self.Meta.layout + ( Fieldset(*layout_keys), )

  def setup_form(self, json_form):
    """ Main form setup method used to generate the base form fields """
    self.schema = json_form if isinstance(json_form, dict) else json.loads(json_form)
    #@TODO
    #self.validate_schema(schema)
    self.setup_step_title(self.schema)
    self.form_type = self.schema['type']
    self.setup_fields(self.schema['fields'])

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
    step_title_attrs = {
      'data-step-title': step_schema['properties']['step_title'],
    }

    if step_schema['type'] == 'loop-step':
      step_title_attrs['data-glynt-loop_step'] = self.define_loopstep_attribs(step_schema)

    self.fields['step_title'] = forms.CharField(max_length=128, required=False, widget=forms.HiddenInput(attrs=step_title_attrs))

    # hidden field that stores set of fields not visible to the user; and this should not be validated
    self.fields['hidden_fields'] = forms.CharField(required=False, widget=forms.HiddenInput)

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
          if callable(f):
              field_instance = f()
          else:
              field_instance = f

          field_instance.label = field['label'] if field['label'] else field['name']
          field_instance.name = self.slugify(field['name']) if field['name'] else self.slugify(field_instance.label)
          field_instance.help_text = field['help_text'] if field['help_text'] else None
          field_instance.required = True if field['required'] in ['true','True',True,'1', 1] else False

          widget = self.setup_field_widget(field_instance, field)
          if widget:
            field_instance.widget = widget

          if hasattr(f, 'choices') and 'choices' in field and type(field['choices']) is list:
            # Add log here as sometimes choices may be present but not specified
            field_instance.choices = self.valid_choice_options(field['choices'])

          if 'initial' in field:
            field_instance.initial = field['initial']

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
    if 'widget' in field_dict and field_dict['widget'] in VALID_WIDGETS_CUSTOM:
        widget = getattr(forms.widgets, field_dict['widget'], None)
    else:
        w = getattr(forms.widgets, field_dict['widget'], None) if 'widget' in field_dict else None
        if callable(w):
          widget = w()
        else:
          widget = field_instance.widget

    widget.attrs.update({
      'placeholder': field_dict['placeholder'],
      'data-hb-name': field_dict['data-hb-name'] if field_dict['data-hb-name'] else field_instance.name,
    })
    if 'class' in widget.attrs:
        # join with custom widget attrs
        widget.attrs['class'] = ' '.join(widget.attrs['class'].split(' ') + field_dict['class'].split(' '))
    else:
        widget.attrs['class'] = field_dict['class']

    if 'data-show_when' in field_dict:
      widget.attrs['data-show_when'] = safestring.mark_safe(field_dict['data-show_when'])
    if 'data-hide_when' in field_dict:
      widget.attrs['data-hide_when'] = safestring.mark_safe(field_dict['data-hide_when'])

    # Handle loop step loop length fields, required to make the loop function
    if 'data-glynt-loop_length' in field_dict:
      widget.attrs['data-glynt-loop_length'] = len(field_instance.choices) if hasattr(field_instance, 'choices') else ''


    return widget

