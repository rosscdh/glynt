# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.utils import simplejson as json
from django.test import TestCase
from django.forms import fields
from django.forms import widgets

from forms import BaseFlyForm, VALID_FIELD_TYPES

import inspect
import re
import copy


class BaseFlyFormTest(TestCase):
  def setUp(self):
    self.base_json = {
                      "type": "step",
                      "properties": {
                        "step_title": "Step No. 1",
                        "hide_from": "",
                        "hide_to": "",
                        "iteration_title": "",
                      },
                      "fields": [
                          {"field": "CharField",
                          "widget": "TextInput",
                          "name": "Test Field",
                          "label": "Test",
                          "required": "true",
                          "help_text": "My Test Field",
                          "placeholder": "tester",
                          "class": "md-updater",
                          "data-hb-name": "test_field"}
                      ]
                    }

  def test_flyform_slugify(self):
    form = BaseFlyForm()
    self.assertEqual(form.slugify('test 123'), 'test_123')
    self.assertEqual(form.slugify('test-123'), 'test_123')
    self.assertEqual(form.slugify('test_123'), 'test_123')
    self.assertEqual(form.slugify(' test 123 '), 'test_123')
    self.assertEqual(form.slugify('test *** 123'), 'test_123')
    self.assertEqual(form.slugify('test üöä 123'), u'test_uoa_123')

  def test_string_attribs(self):
    form = BaseFlyForm(json.dumps(self.base_json))
    result = form.string_attribs({'my_key': 'my_value'})
    self.assertEqual(result, '[{"my_key": "my_value"}]')

    result = form.string_attribs({'my_key': 'my_value', 'my_key2': 'my_value2'})
    self.assertEqual(result, '[{"my_key2": "my_value2","my_key": "my_value"}]')

  def test_basic_step_form(self):
    form = BaseFlyForm(json.dumps(self.base_json))
    self.assertEqual(type(form.fields['test_field']), fields.CharField)
    self.assertEqual(type(form.fields['test_field'].widget), widgets.TextInput)
    self.assertEqual(form.as_ul(), '<li><label for="id_test_field">Test:</label> <input name="test_field" id="id_test_field" placeholder="tester" type="text" class="md-updater" data-hb-name="test_field" /> <span class="helptext">My Test Field</span><input id="id_step_title" type="hidden" data-step-title="Step No. 1" name="step_title" /></li>')

  def test_setup_step_title(self):
    form = BaseFlyForm(json.dumps(self.base_json))
    self.assertEqual(type(form.fields['step_title'].widget), widgets.HiddenInput)
    self.assertEqual(form.fields['step_title'].widget.attrs, {'data-step-title': u'Step No. 1'})

  def test_define_loopstep_attribs(self):
    loop_step = self.base_json
    loop_step['properties']['type'] = 'loop-step'
    loop_step['properties']['hide_from'] = 'Test Field'
    form = BaseFlyForm(json.dumps(loop_step))
    self.assertEqual(form.define_loopstep_attribs(loop_step), '[{"iteration_title": "Step No. 1","hide_from": "test_field"}]')

  def test_basic_loopstep(self):
    json_form = {
      "type": "loop-step",
      "properties": {
        "step_title": "Step No. 1",
        "hide_from": "Test Field",
        "hide_to": "",
        "iteration_title": "",
      },
      "fields": [
          {"field": "CharField",
          "widget": "TextInput",
          "name": "Test Field",
          "label": "Test",
          "required": "true",
          "help_text": "My Test Field",
          "placeholder": "tester",
          "class": "md-updater",
          "data-hb-name": "test_field"}
      ]
    }
    json_form_string = json.dumps(json_form)
    form = BaseFlyForm(json_form_string)

    self.assertEqual(type(form.fields['test_field']), fields.CharField)
    self.assertEqual(type(form.fields['test_field'].widget), widgets.TextInput)
    self.assertEqual(form.as_ul(), '<li><label for="id_test_field">Test:</label> <input name="test_field" id="id_test_field" placeholder="tester" type="text" class="md-updater" data-hb-name="test_field" /> <span class="helptext">My Test Field</span><input id="id_step_title" type="hidden" data-step-title="Step No. 1" name="step_title" data-glynt-loop_step="[{"iteration_title": "Step No. 1","hide_from": "test_field"}]" /></li>')

  def test_basic_fields(self):
    multi_field = self.base_json
    multi_field['properties']['step_title'] = 'Multiple Step Test Form'
    for name in VALID_FIELD_TYPES:
      field = multi_field['fields'][0].copy()
      field['field'] = name
      field['name'] = '%s Field' % (name.replace('Field',''),)
      field['placeholder'] = 'input for type %s' % (name,)
      field['widget'] = ''
      field['label'] = ''
      field['help_text'] = 'Help for my %s Field' % (name.replace('Field',''),)
      multi_field['fields'].append(field)

    del(multi_field['fields'][0])
    form = BaseFlyForm(json.dumps(multi_field))

  def test_multi_step_form(self):
    steps = []
    step_set = self.base_json.copy()
    for index, name in enumerate(VALID_FIELD_TYPES):
      step = step_set.copy()
      step['properties']['step_title'] = 'Multiple Field Type Test Step %d' % (index+1,)

      field = step_set['fields'][0].copy()
      field['field'] = name
      field['name'] = '%s Field' % (name.replace('Field',''),)
      field['placeholder'] = 'input for type %s' % (name,)
      field['widget'] = ''
      field['label'] = ''
      field['help_text'] = 'Help for my %s Field' % (name.replace('Field',''),)

      step['fields'].append(field)
      del(step['fields'][0])
      steps.append(copy.deepcopy(step))

    for s in steps:
      form = BaseFlyForm(json.dumps(s))
      print form.as_ul()

