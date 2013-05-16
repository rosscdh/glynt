# -*- coding: UTF-8 -*-
from django.db import models


class DocumentTemplateManager(models.Manager):
    """ Default handler of Document objects """
    def by_acronym(self):
        return self.get_query_set().values('pk', 'slug','name','summary','acronym').distinct()

    def by_user(self, user):
        return self.get_query_set().filter(owner=user)


class PublicDocumentTemplateManager(DocumentTemplateManager):
    """ Manager for documents that are public """
    def get_query_set(self):
        return super(PublicDocumentTemplateManager, self).get_query_set().filter(doc_status=1, is_public=True)


class PrivateDocumentTemplateManager(DocumentTemplateManager):
    """ Manager for documents that are public """
    def get_query_set(self):
        return super(PrivateDocumentTemplateManager, self).get_query_set().filter(doc_status=1, is_public=False)


class ClientCreatedDocumentManager(models.Manager):
    """ Default handler of clientdocuments objects """
    def get_query_set(self):
        """ Always select the owner and sourcedocument as default """
        return super(ClientCreatedDocumentManager, self).get_query_set() \
                            .select_related('owner', 'source_document') \
                            .filter(is_deleted=False)

    def by_user(self, user):
        return self.get_query_set().select_related('owner', 'source_document').filter(owner=user)


class PublicClientCreatedDocumentManager(ClientCreatedDocumentManager):
    """ Default handler of clientdocuments objects """
    pass


class DeletedClientCreatedDocumentManager(models.Manager):
    """ Manager for clientdocuments that are deleted """
    def get_query_set(self):
        return super(DeletedClientCreatedDocumentManager, self).get_query_set().filter(is_deleted=True)