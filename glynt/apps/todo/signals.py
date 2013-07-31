# -*- coding: utf-8 -*-
""" Set of signals to handle when comments are posted and assigning notifications to the user """
from django.dispatch import receiver
from django.db.models.signals import post_save

# from notifications import notify
# from notifications.models import Notification

from .models import Attachment
from .services import CrocdocAttachmentService

import logging
logger = logging.getLogger('django.request')


@receiver(post_save, sender=Attachment, dispatch_uid='todo.attachment.created')
def on_attachment_created(sender, **kwargs):
    """
    Handle new Project
    """
    is_new = kwargs.get('created')
    attachment = kwargs.get('instance')

    if attachment:
        upload_service = CrocdocAttachmentService(attachment=attachment)
        upload_service.process()
