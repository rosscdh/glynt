from django.db import models
from jsonfield import JSONField
from django.utils import simplejson as json

from glynt.apps.document.models import Document
from glynt.apps.flyform.forms import BaseFlyForm


class FlyForm(models.Model):
    """ Flyform model used to store teh JSON representation of a form """
    body = JSONField(blank=False,null=False)
    defaults = JSONField(blank=True,null=True)

    def __unicode__(self):
      try:
        return u'FlyForm for %s' % (self.document.name,)
      except Document.DoesNotExist:
        return u'FlyForm for %s' % ('New Document',)

    @property
    def flyform_meta(self):
        """ Return the Meta component of new forms otherwise its an old form"""
        return self.body["meta"] if type(self.body) is dict and "meta" in self.body else {}

    @property
    def flyform_steps(self):
        """ Return the Form component of new forms otherwise its an old form"""
        return self.body["steps"] if type(self.body) is dict and "steps" in self.body else self.body

    def flyformset(self):
      """ return a list of FlyForms based on the models steps """
      return [BaseFlyForm(step_num, json.dumps(step)) for step_num, step in enumerate(self.flyform_steps)]

