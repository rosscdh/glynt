# -*- coding: utf-8 -*-
# signals to handle the sending of signature invitations, when a new DocumentSignature model is created
from django.db.models.signals import post_save
from django.dispatch import receiver

from glynt.apps.sign.models import DocumentSignature
from glynt.apps.sign.tasks import send_signature_invite_email
import datetime

@receiver(post_save, sender=DocumentSignature)
def save_document_signature_signal(sender, **kwargs):
  # send an email to the invited person
  send_signature_invite_email.delay(document=sender.document, date_invited=datetime.datetime.now(), key_hash=sender.key_hash, **sender.meta)