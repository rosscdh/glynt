# -*- coding: utf-8 -*-
import os
from django.conf import settings
from tidylib import tidy_document


class HtmlValidatorService(object):
    def __init__(self, html):
        self.html = html
        self.errors = None
        self.document = None
        self.valid_doc_path = None

    def save_valid_doc(self):
        self.valid_doc_path = os.path.join(settings.SITE_ROOT, 'valid_doc_template.html')
        valid_doc = open(self.valid_doc_path, 'wb')
        valid_doc.write(self.document.encode('utf-8'))
        valid_doc.close()

    def is_valid(self):
        is_valid = False
        if self.html is not None:
            self.document, self.errors = tidy_document(self.html, \
                                                options={'numeric-entities':1, "output-xhtml": 1} \
                                            )
            is_valid = len(self.errors) == 0

            if is_valid == False:
                self.save_valid_doc()

        return is_valid


class BaseDocumentService(object):
    def __init__(self, document, **kwargs):
        self.document = document

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
