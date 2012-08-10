from django.db import models


class DocumentManager(models.Manager):
  """ Default handler of Document objects """
  pass


class PublicDocumentManager(DocumentManager):
  """ Manager for documents that are public """
  def get_query_set(self):
      return super(PublicDocumentManager, self).get_query_set().filter(is_public=True)

class PrivateDocumentManager(DocumentManager):
  """ Manager for documents that are public """
  def get_query_set(self):
      return super(PrivateDocumentManager, self).get_query_set().filter(is_public=False)
  