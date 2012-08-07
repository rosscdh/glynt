# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson as json
from django.template.defaultfilters import slugify


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

  def slugify(self, text):
    return '%s' %(slugify(text).replace('-','_'),)

  def setup_form(self, json_form):
    schema = json.loads(json_form)

    # setup step title
    step_attrs = {
      'data-step-title': schema['properties']['step_title'],
    }

    loop_step_attrs = None
    if schema['type'] == 'loop-step':
      schema['properties']['iteration_title'] = schema['properties']['iteration_title'] if 'iteration_title' in schema['properties'] and len(schema['properties']['iteration_title']) > 0 else schema['properties']['step_title']
      ## @TODO make this a string
      loop_step_attrs = {
        'iteration_title': schema['properties']['iteration_title'] if schema['properties']['iteration_title'] else '',
        'hide_from': self.slugify(schema['properties']['hide_from']) if schema['properties']['hide_from'] else '',
      }
      loop_step_attrs = '[%s]' %(json.dumps(loop_step_attrs),)
      step_attrs['data-glynt-loop_step'] = loop_step_attrs

    self.fields['step_title'] = forms.CharField(max_length=100,required=False,widget=forms.HiddenInput(attrs=step_attrs))

    if len(schema['fields']) > 0:
      for f in schema['fields']:
        if hasattr(forms.fields, f['field']):
          new_field = getattr(forms.fields, f['field'])
          fld = new_field()
          fld.name = self.slugify(f['name'])
          fld.label = f['label']
          fld.help_text = f['help_text'] if len(f['help_text']) > 0 else None
          fld.required = bool(f['required']) if f['required'] in ['true',True,'false','False'] else False
          if hasattr(forms.fields, f['widget']):
            new_widget = getattr(forms.fields, f['widget'])
            fld.widget = new_widget()
            widget_attrs = {
              'class': f['class'],
              'data-hb-name': f['data-hb-name'] if f['data-hb-name'] else fld.name,
            }
            fld.widget.attrs = widget_attrs
        self.fields[fld.name] = fld

