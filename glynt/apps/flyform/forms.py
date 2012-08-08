# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson as json
from django.template.defaultfilters import slugify
from django.utils import safestring


VALID_FIELD_TYPES = ['BooleanField', 'CharField', 'ChoiceField', 'DateField', 'DateTimeField', 'DecimalField', 'EmailField', 'FloatField', 'ImageField', 'IntegerField', 'MultiValueField', 'MultipleChoiceField', 'SlugField', 'TimeField', 'URLField', ]


class BaseFlyForm(forms.Form):
  """ This form is the basis for the self generating form representations
  it requires that a valid json_object be passed in which adheres to the following schema
  schema = {
    "type" : "step",
    "properties" : {
      "step_title" : {"type" : "string"},
      "hide_from": "",
      "hide_to": "",
      "iteration_title": "",
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
        "data-hb-name" : {"type" : "string"}
      ]
  }
  """
  def __init__(self, json_form=None, data=None, files=None, auto_id='id_%s', prefix=None,
               initial=None, error_class=ErrorList, label_suffix=':',
               empty_permitted=False):

    super(BaseFlyForm, self).__init__(data, files, auto_id, prefix,
                            initial, error_class, label_suffix,
                            empty_permitted)

    if json_form is not None:
      self.setup_form(json_form)

  def setup_form(self, json_form):
    """ Main form setup method used to generate the base form fields """
    schema = json.loads(json_form)
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
        attribs_as_s += '"%s": "%s",' % (k, v, )
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
      'iteration_title': step_schema['properties']['iteration_title'],
      'hide_from': self.slugify(step_schema['properties']['hide_from']),
    }
    return safestring.mark_safe(self.string_attribs(loop_step_attrs).replace('""', "'"))

  def setup_fields(self, schema_fields):
    if len(schema_fields) > 0:
      for field in schema_fields:
        f = getattr(forms.fields, field['field'], None) if field['field'] else None
        if f:
          field_instance = f()
          field_instance.name = self.slugify(field['name'])
          field_instance.label = field['label'] if field['label'] else field['name']
          field_instance.help_text = field['help_text'] if field['help_text'] else None
          field_instance.required = True if field['required'] in ['true',True,'1', 1] else False

          widget = self.setup_field_widget(field_instance, field)
          if widget:
            field_instance.widget = widget

          # Append the field
          self.fields[field_instance.name] = field_instance

  def setup_field_widget(self, field_instance, field_dict):
    w = getattr(forms.widgets, field_dict['widget'], None) if field_dict['widget'] else None
    if w:
      widget = w()
      widget.attrs = {
        'class': field_dict['class'],
        'placeholder': field_dict['placeholder'],
        'data-hb-name': field_dict['data-hb-name'] if field_dict['data-hb-name'] else field_instance.name,
      }
      return widget
    return None

