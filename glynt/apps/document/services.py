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
    def increment(self, signature):
        """ Save the number of invitees, save the signature_id for uniqueness """
        meta = self.document.meta.copy()

        if 'invitees' not in meta:
          meta['invitees'] = []

        if signature.pk not in meta['invitees']:
          meta['invitees'].append(signature.pk)

        if 'num_invited' not in meta:
          meta['num_invited'] = 0

        meta['num_invited'] = len(meta['invitees'])

        self.document.meta_data = meta
        self.document.save()

    def decrement(self, signature):
        self.document.meta_data['invitees'] = filter(lambda i: i != signature.pk, self.document.meta_data['invitees'])
        self.document.meta_data['num_invited'] = len(self.document.meta_data['invitees'])
        self.document.save()


class DocumentCloneService(BaseDocumentService):
    """ To be used for the document cloning process """
    pass
