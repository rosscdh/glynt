# -*- coding: utf-8 -*-
""" Set of signals to handle when comments are posted and assigning notifications to the user """
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.admin.models import LogEntry

from threadedcomments.models import ThreadedComment

from bunch import Bunch

from .tasks import delete_attachment
from .models import Attachment
from .services import CrocdocAttachmentService

from glynt.apps.services.pusher import PusherPublisherService

from actstream import action
from actstream.models import Action

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


@receiver(post_save, sender=ThreadedComment, dispatch_uid='todo.comment.created')
def on_comment_created(sender, **kwargs):
    """
    Handle Creation of attachments
    """
    logger.debug('GOT IT {type}'.format(type=type(sender)))
    if not isinstance(sender, LogEntry):
        is_new = kwargs.get('created', False)
        comment = kwargs.get('instance')

        if comment and is_new:
            verb = 'Commented on Checklist Item'
            action.send(comment.user,
                        verb=verb,
                        action_object=comment,
                        target=comment.content_object,
                        content=comment.comment)


@receiver(post_save, sender=Action, dispatch_uid='action.created')
def on_action_created(sender, **kwargs):
    """
    Handle Creation of attachments
    """
    if not isinstance(sender, LogEntry):
        is_new = kwargs.get('created', False)

        action = kwargs.get('instance')
        target = action.target

        if hasattr(target, 'pusher_id'):
            if action and is_new:
                pusher_service = PusherPublisherService(channel=target.pusher_id, event='action.created')

                user_name = action.actor.get_full_name()

                info_object = Bunch(name=user_name,
                                        verb=action.verb,
                                        target_name=unicode(action),
                                        timestamp='',
                                        content=action.data.get('content', ''))

                pusher_service.process(label=action.verb, comment=action.verb, **info_object)
