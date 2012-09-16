from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson as json
from jsonfield import JSONField
from glynt.apps.document.models import ClientCreatedDocument


class DocumentSignature(models.Model):
  """ Model to store a users signature of a document
  signatures are stored as JSON value 
  http://thomasjbradley.ca/lab/signature-pad/#database
  """
  document = models.ForeignKey(ClientCreatedDocument)
  key_hash = models.CharField(blank=False, max_length=32, unique=True)
  hash_data = models.CharField(blank=False, max_length=255)
  user = models.ForeignKey(User, blank=True, null=True)
  signature = JSONField(blank=True, null=True)
  meta_data = JSONField(blank=True, null=True)
  is_signed = models.BooleanField(default=False)
  date_invited = models.DateTimeField(auto_now=False, auto_now_add=True)
  date_signed = models.DateTimeField(blank=True, null=True, auto_now=False, auto_now_add=False)

  def __unicode__(self):
    return u'%s - %s (%s)' % (self.key_hash, self.meta_data['to_name'], self.meta_data['to_email'])

  def signature_as_string(self):
    return json.dumps(self.signature)

  def signee_name(self):
    return u'%s' % (self.meta_data['to_name'],)

  def signee_email(self):
    return u'%s' % (self.meta_data['to_email'],)

# import signals here as they need to be initialized with the models
from glynt.apps.sign.signals import *