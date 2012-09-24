# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from glynt.apps.document.models import ClientCreatedDocument
from glynt.apps.document.tasks import document_created
import datetime

@receiver(post_save, sender=ClientCreatedDocument)
def save_document_signal(sender, **kwargs):
    is_created = kwargs['created']
    document = kwargs['instance']

    if is_created:
        try:
          document_created.delay(document=document)
        except:
          document_created(document=document)


# @receiver(post_delete, sender=ClientCreatedDocument)
# def delete_document_signature_signal(sender, **kwargs):
#     document = kwargs['instance']
# 
#     try:
#       document_created.delay(document=document)
#     except:
#       document_created(document=document)
