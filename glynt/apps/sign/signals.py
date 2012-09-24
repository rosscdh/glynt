# -*- coding: utf-8 -*-
# signals to handle the sending of signature invitations, when a new DocumentSignature model is created
from django.db.models.signals import post_save
from django.dispatch import receiver

from glynt.apps.sign.models import DocumentSignature
from glynt.apps.sign.tasks import send_signature_invite_email, send_signature_acquired_email
import datetime

@receiver(post_save, sender=DocumentSignature)
def save_document_signature_signal(sender, **kwargs):
  # send an email to the invited person
  is_new = kwargs['created']

  signature = kwargs['instance']
  document = signature.document

  if signature.is_signed == True:

    try:
      send_signature_acquired_email.delay(document=signature.document, date_invited=signature.date_invited, key_hash=signature.key_hash, **signature.meta_data)
    except:
      send_signature_acquired_email(document=signature.document, date_invited=signature.date_invited, key_hash=signature.key_hash, **signature.meta_data)

  else:
    # Newly created document send invites
    # TODO abstract into another signal?
    if is_new:
      try:
        send_signature_invite_email.delay(document=signature.document, date_invited=signature.date_invited, key_hash=signature.key_hash, **signature.meta_data)
      except:
        send_signature_invite_email(document=signature.document, date_invited=signature.date_invited, key_hash=signature.key_hash, **signature.meta_data)