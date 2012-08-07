# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson as json


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

    self.setup_form(json_form)

  def setup_form(self, json_form):
    schema = json.loads(json_form)
    print schema['properties']['step_title']
    # setup step title
    # step_title = forms.CharField(max_length=100,required=False,widget=forms.HiddenInput(attrs={'data-step-title':'About the company'}))
    self.fields['step_title'] = forms.CharField(max_length=100,required=False,widget=forms.HiddenInput(attrs={'data-step-title':schema['properties']['step_title']}))
