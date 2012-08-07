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
from forms import BaseFlyForm


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
    json_form = self.base_json
    json_form_string = json.dumps(json_form)
    form = BaseFlyForm(json_form_string)

    self.assertEqual(type(form.fields['test_field']), fields.CharField)
    self.assertEqual(type(form.fields['test_field'].widget), widgets.TextInput)
    self.assertEqual(form.as_ul(), '<li><label for="id_test_field">Test:</label> <input id="id_test_field" type="text" class="md-updater" name="test_field" data-hb-name="test_field" /> <span class="helptext">My Test Field</span><input id="id_step_title" type="hidden" data-step-title="Step No. 1" name="step_title" /></li>')

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
    self.assertEqual(form.as_ul(), '<li><label for="id_test_field">Test:</label> <input id="id_test_field" type="text" class="md-updater" name="test_field" data-hb-name="test_field" /> <span class="helptext">My Test Field</span><input id="id_step_title" type="hidden" data-step-title="Step No. 1" name="step_title" data-glynt-loop_step="[{hide_from:test_field,iteration_title:Step No. 1}]" /></li>')
