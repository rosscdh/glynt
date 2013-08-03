# -*- coding: utf-8 -*-
""" Set of signals to handle when comments are posted and assigning notifications to the user """
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.admin.models import LogEntry

# from notifications import notify
# from notifications.models import Notification

from .tasks import delete_attachment
from .models import Attachment
from .services import CrocdocAttachmentService

from django.contrib.auth.models import User
from actstream import action

import logging
logger = logging.getLogger('django.request')


@receiver(post_save, sender=Attachment, dispatch_uid='todo.attachment.created')
def on_attachment_created(sender, **kwargs):
    """
    Handle Creation of attachments
    """
    if not isinstance(sender, LogEntry):
        is_new = kwargs.get('created', False)
        attachment = kwargs.get('instance')

        if attachment and is_new:
            crocdoc_service = CrocdocAttachmentService(attachment=attachment)
            crocdoc_service.process()

            action.send(User.objects.get(pk=1), 
                        verb='Uploaded Attachment', 
                        action_object=attachment, 
                        target=attachment.todo,
                        attachment_name=attachment.filename)


@receiver(post_delete, sender=Attachment, dispatch_uid='todo.attachment.deleted')
def on_attachment_deleted(sender, **kwargs):
    """
    Handle Deletions of attachments
    """
    if not isinstance(sender, LogEntry):
        is_new = kwargs.get('created', False)
        attachment = kwargs.get('instance', None)

        if attachment:
            try:
                delete_attachment.delay(is_new=is_new, attachment=attachment)
            except Exception as e:
                logger.error('Could not call delete_attachment via celery: {exception}'.format(exception=e))
                delete_attachment(is_new=is_new, attachment=attachment, **kwargs)

        action.send(User.objects.get(pk=1), 
                    verb='Deleted Attachment', 
                    action_object=attachment, 
                    target=attachment.todo,
                    attachment_name=attachment.filename)

