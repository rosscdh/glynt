from django.db import models


class DocumentManager(models.Manager):
  """ Default handler of Document objects """
  def by_user(self, user):
    return self.get_query_set().filter(owner=user)

class PublicDocumentManager(DocumentManager):
  """ Manager for documents that are public """
  def get_query_set(self):
      return super(PublicDocumentManager, self).get_query_set().filter(is_public=True)


class PrivateDocumentManager(DocumentManager):
  """ Manager for documents that are public """
  def get_query_set(self):
      return super(PrivateDocumentManager, self).get_query_set().filter(is_public=False)


class ClientCreatedDocumentManager(models.Manager):
  """ Default handler of clientdocuments objects """
  def by_user(self, user):
    return self.get_query_set().select_related('owner', 'source_document').filter(owner=user)


class PublicClientCreatedDocumentManager(ClientCreatedDocumentManager):
  """ Default handler of clientdocuments objects """
  def get_query_set(self):
      return super(PublicClientCreatedDocumentManager, self).get_query_set().filter(is_deleted=False)

class DeletedClientCreatedDocumentManager(ClientCreatedDocumentManager):
  """ Manager for clientdocuments that are deleted """
  def get_query_set(self):
      return super(DeletedClientCreatedDocumentManager, self).get_query_set().filter(is_deleted=True)


