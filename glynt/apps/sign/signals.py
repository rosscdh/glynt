# -*- coding: utf-8 -*-
# signals to handle the sending of signature invitations, when a new DocumentSignature model is created
from django.db.models.signals import post_save
from django.dispatch import receiver

from glynt.apps.sign.models import DocumentSignature
from glynt.apps.sign.tasks import send_signature_invite_email, send_signature_acquired_email


@receiver(post_save, sender=DocumentSignature)
def save_document_signature_signal(sender, **kwargs):
    # send an email to the invited person
    signature = kwargs['instance']
    document = signature.document

    meta_data = dict([(str(k), v) for k, v in signature.meta_data.items()])
    if signature.is_signed == True:
        document.increment_num_signed(signature.id)
        try:
          send_signature_acquired_email.delay(document=signature.document, date_invited=signature.date_invited, key_hash=signature.key_hash, **meta_data)
        except:
          send_signature_acquired_email(document=signature.document, date_invited=signature.date_invited, key_hash=signature.key_hash, **meta_data)

    else:
        document.increment_num_invited(signature.id)
        try:
          send_signature_invite_email.delay(document=signature.document, date_invited=signature.date_invited, key_hash=signature.key_hash, **meta_data)
        except:
          send_signature_invite_email(document=signature.document, date_invited=signature.date_invited, key_hash=signature.key_hash, **meta_data)

