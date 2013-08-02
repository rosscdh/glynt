# -*- coding: utf-8 -*-
""" Set of signals to handle when comments are posted and assigning notifications to the user """
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

# from notifications import notify
# from notifications.models import Notification

from .tasks import delete_attachment
from .models import Attachment
from .services import CrocdocAttachmentService

import logging
logger = logging.getLogger('django.request')


@receiver(post_save, sender=Attachment, dispatch_uid='todo.attachment.created')
def on_attachment_created(sender, **kwargs):
    """
    Handle Creation of attachments
    """
    #is_new = kwargs.get('created')
    attachment = kwargs.get('instance')

    if attachment:
        crocdoc_service = CrocdocAttachmentService(attachment=attachment)
        crocdoc_service.process()


@receiver(post_delete, sender=Attachment, dispatch_uid='todo.attachment.deleted')
def on_attachment_deleted(sender, **kwargs):
    """
    Handle Deletions of attachments
    """
    is_new = kwargs.get('created', False)
    attachment = kwargs.get('instance', None)

    if attachment:
        try:
            delete_attachment.delay(is_new=is_new, attachment=attachment)
        except Exception as e:
            logger.error('Could not call delete_attachment via celery: {exception}'.format(exception=e))
            delete_attachment(is_new=is_new, attachment=attachment, **kwargs)

