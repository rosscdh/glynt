# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.utils.encoding import smart_unicode

from tidylib import tidy_document


class HtmlValidatorService(object):
    """ Service used to validate HTML being added to the system 
    Used primarily with document template additions
    """
    def __init__(self, ident, html, **kwargs):
        self.preprocessors = kwargs.pop('preprocessors') if 'preprocessors' in kwargs else []
        self.ident = ident
        self.html = self.preprocess(html)
        self.errors = None
        self.document = None
        self.valid_doc_path = None
        self.error_msg = None

    def preprocess(self, html):
        for c in self.preprocessors:
            instance = c(source_html=html)
            html = instance.render({})
        return html

    def save_valid_doc(self):
        version_location_msg = None
        self.valid_doc_path = os.path.join(settings.SITE_ROOT, '%s_valid.html' % self.ident)
        self.invalid_doc_path = os.path.join(settings.SITE_ROOT, '%s_invalid.html' % self.ident)

        self.error_msg = 'Document Template HTML is invalid: %s.' % self.errors

        if settings.DEBUG is True:
            self.error_msg += 'The Comparison Docs are found at: %s and %s' % (self.valid_doc_path, self.invalid_doc_path,)

            valid_doc = open(self.valid_doc_path, 'wb')
            valid_doc.write(self.document.encode('utf-8'))
            valid_doc.close()

            invalid_doc = open(self.invalid_doc_path, 'wb')
            invalid_doc.write(self.html.encode('utf-8'))
            invalid_doc.close()

    def is_valid(self):
        is_valid = False
        if self.html is not None:
            self.document, self.errors = tidy_document(self.html, \
                                                options={
                                                    'numeric-entities':1
                                                    ,"output-xhtml": 1
                                                    ,'new-inline-tags': ''
                                                    } \
                                            )
            is_valid = len(self.errors) == 0

            if is_valid == False:
                self.save_valid_doc()

        return is_valid


class BaseDocumentService(object):
    """ Service used to meddle with the document meta JSON structure """
    def __init__(self, document, **kwargs):
        self.document = document
        #@TODO fix this; meta_data should default to being {} and not have to be set
        if self.document.meta_data is None:
            self.document.meta_data = {}

    def get_meta(self):
        return self.document.meta.copy()


class DocumentSignerService(BaseDocumentService):
    """ To be used for increment/decrement the signers count of a document """
    def reset(self):
        self.document.meta_data['num_signed'] = 0
        self.document.meta_data['signers'] = []
        self.document.save()

    def increment(self, signature):
        """ Save the number of signers, save the signature_id for uniqueness """
        meta = self.get_meta()
        signers = meta.get('signers', [])
        num_signed = meta.get('num_signed', 0)

        if signature.is_signed == True and signature.pk not in signers:
            signers.append(signature.pk)

        self.document.meta_data['num_signed'] = len(signers)
        self.document.meta_data['signers'] = signers
        self.document.save()

    def decrement(self, signature):
        meta = self.get_meta()
        signers = meta.get('signers', [])

        signers = filter(lambda i: i != signature.pk, signers)

        self.document.meta_data['num_signed'] = len(signers)
        self.document.meta_data['signers'] = signers
        self.document.save()


class DocumentInviteeService(BaseDocumentService):
    """ To be used for increment/decrement the signature invitee count of a document """
    def reset(self):
        self.document.meta_data['num_invited'] = 0
        self.document.meta_data['invitees'] = []
        self.document.save()

    def increment(self, signature):
        """ Save the number of invitees, save the signature_id for uniqueness """
        meta = self.get_meta()
        invitees = meta.get('invitees', [])
        num_invited = meta.get('num_invited', 0)

        if signature.pk is not None and signature.pk not in invitees:
            invitees.append(signature.pk)

        self.document.meta_data['num_invited'] = len(invitees)
        self.document.meta_data['invitees'] = invitees
        self.document.save()

    def decrement(self, signature):
        meta = self.get_meta()
        invitees = meta.get('invitees', [])

        invitees = filter(lambda i: i != signature.pk, invitees)

        self.document.meta_data['num_invited'] = len(invitees)
        self.document.meta_data['invitees'] = invitees
        self.document.save()


class DocumentCloneService(BaseDocumentService):
    """ To be used for the document cloning process """
    pass
