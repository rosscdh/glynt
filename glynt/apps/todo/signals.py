# -*- coding: utf-8 -*-
""" Set of signals to handle when comments are posted and assigning notifications to the user """
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, m2m_changed

from django.contrib.admin.models import LogEntry

from threadedcomments.models import ThreadedComment

from bunch import Bunch

from glynt.apps.todo import FEEDBACK_STATUS

from .tasks import delete_attachment
from .models import Attachment, FeedbackRequest
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


@receiver(m2m_changed, sender=FeedbackRequest.assigned_to.through, dispatch_uid='feedbackrequest.created')
def feedbackrequest_created(sender, **kwargs):
    # please note the pk_set check here
    # this is required in order to catch the m2m model change 
    # so we get access to the assigned_to.all() object
    if kwargs.get('action') == 'post_add' and kwargs.get('pk_set') is not None:
        #is_new = kwargs.get('created', False)
        feedbackrequest = kwargs.get('instance')

        if feedbackrequest and feedbackrequest.status == FEEDBACK_STATUS.open:
            verb = 'requested feedback from {assigned_to}'.format(assigned_to=', '.join([u.get_full_name() for u in feedbackrequest.assigned_to.all()]))
            action.send(feedbackrequest.assigned_by,
                        verb=verb,
                        action_object=feedbackrequest.attachment,
                        target=feedbackrequest.attachment.todo,
                        content='for attachment "{attachment}"'.format(attachment=feedbackrequest.attachment.filename))

        if feedbackrequest and feedbackrequest.status == FEEDBACK_STATUS.responded:
            verb = 'provided feedback to {assigned_by} on {attachment}'.format(assigned_by=feedbackrequest.assigned_by, attachment=feedbackrequest.attachment.filename)
            action.send(feedbackrequest.assigned_by,
                        verb=verb,
                        action_object=feedbackrequest.attachment,
                        target=feedbackrequest.attachment.todo,
                        content='for attachment "{attachment}"'.format(attachment=feedbackrequest.attachment.filename),
                        assigned_to=feedbackrequest.assigned_by)

        if feedbackrequest and feedbackrequest.status == FEEDBACK_STATUS.closed:
            verb = 'closed the feedback request assigned to them'
            action.send(feedbackrequest.assigned_by,
                        verb=verb,
                        action_object=feedbackrequest.attachment,
                        target=feedbackrequest.attachment.todo,
                        content='for attachment "{attachment}"'.format(attachment=feedbackrequest.attachment.filename))


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
