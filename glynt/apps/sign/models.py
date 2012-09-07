from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField
from glynt.apps.document.models import ClientCreatedDocument


class DocumentSignature(models.Model):
  """ Model to store a users signature of a document
  signatures are stored as JSON value 
  http://thomasjbradley.ca/lab/signature-pad/#database
  """
  document = models.ForeignKey(ClientCreatedDocument)
  user = models.ForeignKey(User)
  signature = JSONField(blank=True, null=True)
  is_signed = models.BooleanField(default=False)
  date_signed = models.DateTimeField(auto_now=False, auto_now_add=True)