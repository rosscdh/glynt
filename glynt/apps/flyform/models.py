from django.db import models
from jsonfield import JSONField


class FlyForm(models.Model):
    """ Flyform model used to store teh JSON representation of a form """
    body = JSONField(blank=False,null=False)

    def __unicode__(self):
      return u'FlyForm for %s' % (self.document.name,)

