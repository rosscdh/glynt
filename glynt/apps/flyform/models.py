from django.db import models
from jsonfield import JSONField

from glynt.apps.document.models import Document


class FlyForm(models.Model):
    """ Flyform model used to store teh JSON representation of a form """
    body = JSONField(blank=False,null=False)
    defaults = JSONField(blank=True,null=True)

    def __unicode__(self):
      try:
        return u'FlyForm for %s' % (self.document.name,)
      except Document.DoesNotExist:
        return u'FlyForm for %s' % ('New Document',)

