# -*- coding: utf-8 -*-


class BaseDocumentService(object):
    def __init__(self, document, **kwargs):
        self.document = document

    def get_meta(self):
        return self.document.meta.copy()


class DocumentSignerService(BaseDocumentService):
    """ To be used for increment/decrement the signers count of a document """
    def increment(self, signature):
        """ Save the number of signers, save the signature_id for uniqueness """
        meta = self.get_meta()
        signers = meta.get('signers', [])
        num_signed = meta.get('num_signed', 0)

        if signature.pk not in signers:
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
    def increment(self, signature):
        """ Save the number of invitees, save the signature_id for uniqueness """
        meta = self.get_meta()
        invitees = meta.get('invitees', [])
        num_invited = meta.get('num_invited', 0)

        if signature.pk not in invitees:
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
