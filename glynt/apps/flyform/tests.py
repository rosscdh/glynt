"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.utils import simplejson as json
from django.test import TestCase
from forms import BaseFlyForm


class BaseFlyFormTest(TestCase):
  def setUp(self):
    pass

  def test_basic_structure(self):
    """
    """
    json_form = {
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
    json_form_string = json.dumps(json_form)

    self.form = BaseFlyForm(json_form_string)

    self.assertEqual(1 + 1, 2)
