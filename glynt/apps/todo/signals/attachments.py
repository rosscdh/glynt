# -*- coding: utf-8 -*-
"""
Attachment handler events
"""
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from glynt.apps.todo.models import Attachment
from glynt.apps.todo.services import CrocdocAttachmentService, ToDoStatusService

from actstream import action

import logging
logger = logging.getLogger('django.request')


@receiver(post_save, sender=Attachment, dispatch_uid='todo.attachment.created')
def on_attachment_created(sender, **kwargs):
    """
    Handle Creation of attachments
    """
    if sender.__class__.__name__ != 'LogEntry':
        is_new = kwargs.get('created', False)
        attachment = kwargs.get('instance')

        if attachment and is_new:
            crocdoc_service = CrocdocAttachmentService(attachment=attachment)
            crocdoc_service.process()

            todo = attachment.todo
            todostatus_service = ToDoStatusService(todo_item=todo)
            todostatus_service.process()

            # increment the attachment count
            todo.num_attachments_plus()

            verb = '{name} uploaded an attachment: "{filename}" on the checklist item {todo} for {project}'.format(name=attachment.uploaded_by.get_full_name(), filename=attachment.filename, todo=attachment.todo, project=attachment.project)
            action.send(attachment.uploaded_by,
                        verb=verb,
                        action_object=attachment,
                        target=attachment.todo,
                        content=verb,
                        attachment=attachment.filename,
                        todo=attachment.todo.name,
                        status=attachment.todo.display_status,
                        event='todo.attachment.created')


@receiver(post_delete, sender=Attachment, dispatch_uid='todo.attachment.deleted')
def on_attachment_deleted(sender, **kwargs):
    """
    Handle Deletions of attachments
    """
    is_new = kwargs.get('created', False)
    attachment = kwargs.get('instance', None)

    if sender.__name__ != 'LogEntry':

        if attachment:
            try:
                todo = attachment.todo
                # decrement num_attachments
                todo.num_attachments_minus()  # increment the attachment count
            except:
                logger.info('todo does not exist for on_attachment_deleted')

            delete_attachment(is_new=is_new, attachment=attachment, **kwargs)

            try:
                verb = '{name} deleted attachment: "{filename}" on the checklist item {todo} for {project}'.format(name=attachment.uploaded_by.get_full_name(), filename=attachment.filename, todo=attachment.todo, project=attachment.project)
                action.send(attachment.uploaded_by,
                            verb=verb,
                            action_object=attachment,
                            target=attachment.todo,
                            content=verb,
                            attachment=attachment.filename,
                            todo=attachment.todo.name,
                            status=attachment.todo.display_status,
                            event='todo.attachment.deleted')
            except ObjectDoesNotExist:
                pass