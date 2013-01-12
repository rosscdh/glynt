from django.db import models
from jsonfield import JSONField
from django.utils import simplejson as json
from django.template import loader

from glynt.apps.document.models import DocumentTemplate
from glynt.apps.flyform.forms import BaseFlyForm


class FlyForm(models.Model):
    """ Flyform model used to store teh JSON representation of a form """
    document = models.ForeignKey(DocumentTemplate, blank=True, null=True)
    body = JSONField(blank=False, null=False)
    defaults = JSONField(blank=True, null=True)

    def __unicode__(self):
      if self.document is not None:
        return u'FlyForm for %s' % (self.document.name,)
      else:
        return u'Unbound FlyForm, has no document'

    @property
    def flyform_meta(self):
        """ Return the Meta component of new forms otherwise its an old form"""
        return self.body["meta"] if type(self.body) is dict and "meta" in self.body else {}

    @property
    def flyform_steps(self):
        """ Return the Form component of new forms otherwise its an old form"""
        return self.body["steps"] if type(self.body) is dict and "steps" in self.body else self.body

    @property
    def flyform_fields(self):
        field_names = []
        for step in self.flyform_steps:
            for field in step['fields']:
                field_names.append(field['name'])
        return field_names

    @property
    def signature_template(self):
        template_file = self.flyform_meta['templates']['signature'] if 'templates' in self.flyform_meta and 'signature' in self.flyform_meta['templates'] else 'sign/partials/signature_template.html'
        return loader.get_template(template_file)

    def flyform_fields_as_json(self):
        return json.dumps(self.flyform_fields)

    def flyformset(self):
      """ return a list of FlyForms based on the models steps """
      return [BaseFlyForm(step_num, json.dumps(step)) for step_num, step in enumerate(self.flyform_steps)]

