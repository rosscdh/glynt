class BaseDocumentService(object):
    def __init__(self, document, **kwargs):
        self.document = document


class DocumentSignerService(BaseDocumentService):
    """ To be used for increment/decrement the signers count of a document """
    def increment(self, signature):
        """ Save the number of signers, save the signature_id for uniqueness """
        meta = self.document.meta.copy()
        if 'signers' not in meta:
          meta['signers'] = []

        if signature.pk not in meta['signers']:
          meta['signers'].append(signature.pk)

        if 'num_signed' not in meta:
          meta['num_signed'] = 0

        meta['num_signed'] = len(meta['signers'])

        self.document.meta_data = meta
        self.document.save()

    def decrement(self, signature):
        self.document.meta_data['signers'] = filter(lambda i: i != signature.pk, self.document.meta_data['signers'])
        self.document.meta_data['num_signed'] = len(self.document.meta_data['signers'])
        self.document.save()


class DocumentInviteeService(BaseDocumentService):
    """ To be used for increment/decrement the signature invitee count of a document """
    def get_meta(self):
        return self.document.meta.copy()

    def increment(self, signature):
        """ Save the number of invitees, save the signature_id for uniqueness """
        meta = self.get_meta()
        invitees = meta.get('invitees', [])
        num_invited = meta.get('num_invited', 0)

        if signature.pk not in invitees:
            invitees.append(signature.pk)

        meta['num_invited'] = len(invitees)
        meta['invitees'] = invitees

        self.document.meta_data = meta
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
