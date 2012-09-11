# -*- coding: utf-8 -*-
# signals to handle the sending of signature invitations, when a new DocumentSignature model is created
from django.db.models.signals import post_save
from django.dispatch import receiver

from glynt.apps.sign.models import DocumentSignature
from glynt.apps.sign.tasks import send_signature_invite_email


@receiver(post_save, sender=DocumentSignature)
def send_signature_invite_handler(sender, **kwargs):
    send_signature_invite_email.delay(sender)