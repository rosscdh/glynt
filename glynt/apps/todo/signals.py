# -*- coding: utf-8 -*-
""" Set of signals to handle when comments are posted and assigning notifications to the user """
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed

from django.contrib.admin.models import LogEntry

from threadedcomments.models import ThreadedComment

from glynt.apps.todo import TODO_STATUS_ACTION, FEEDBACK_STATUS

from .tasks import delete_attachment
from .models import ToDo, Attachment, FeedbackRequest
from .services import CrocdocAttachmentService, ToDoStatusService, ToDoAttachmentFeedbackRequestStatusService

from glynt.apps.services.email import NewActionEmailService
from glynt.apps.services.pusher import PusherPublisherService

from actstream import action
from actstream.models import Action

from bunch import Bunch

import logging
logger = logging.getLogger('django.request')


"""
Attachment handler events
"""
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

            todostatus_service = ToDoStatusService(todo_item=attachment.todo)
            todostatus_service.process()


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

"""
Comment Events
"""
@receiver(post_save, sender=ThreadedComment, dispatch_uid='todo.comment.created')
def on_comment_created(sender, **kwargs):
    """
    Handle Creation of attachments
    """
    if not isinstance(sender, LogEntry):
        is_new = kwargs.get('created', False)
        comment = kwargs.get('instance')

        if comment and is_new:
            verb = '{name} commented on a checklist item'.format(name=comment.user.get_full_name())
            todo = comment.content_object
            action.send(comment.user,
                        verb=verb,
                        action_object=comment,
                        target=todo,
                        content=comment.comment)

            todostatus_service = ToDoStatusService(todo_item=todo)
            todostatus_service.process()

"""
Feedback Request Change Events
"""
@receiver(m2m_changed, sender=FeedbackRequest.assigned_to.through, dispatch_uid='feedbackrequest.created')
def feedbackrequest_created(sender, **kwargs):
    # please note the pk_set check here
    # this is required in order to catch the m2m model change 
    # so we get access to the assigned_to.all() object
    if kwargs.get('action') == 'post_add' and kwargs.get('pk_set') is not None:
        #is_new = kwargs.get('created', False)
        feedbackrequest = kwargs.get('instance')

        if feedbackrequest and feedbackrequest.status == FEEDBACK_STATUS.open:
            verb = '{assigned_by} requested feedback from {assigned_to}'.format(assigned_by=feedbackrequest.assigned_by.get_full_name(), assigned_to=', '.join([u.get_full_name() for u in feedbackrequest.assigned_to.all()]))
            action.send(feedbackrequest.assigned_by,
                        verb=verb,
                        action_object=feedbackrequest.attachment,
                        target=feedbackrequest.attachment.todo,
                        content=feedbackrequest.comment,
                        detail_statement='for attachment "{attachment}" - "{todo}" is {status}<br/>'.format(attachment=feedbackrequest.attachment.filename, todo=feedbackrequest.attachment.todo.name, status=feedbackrequest.attachment.todo.display_status),
                        attachment=feedbackrequest.attachment.filename,
                        todo=feedbackrequest.attachment.todo.name,
                        status=feedbackrequest.attachment.todo.display_status)

        # if feedbackrequest and feedbackrequest.status == FEEDBACK_STATUS.responded:
        #     verb = 'provided feedback to {assigned_by} on {attachment}'.format(assigned_by=feedbackrequest.assigned_by, attachment=feedbackrequest.attachment.filename)
        #     action.send(feedbackrequest.assigned_by,
        #                 verb=verb,
        #                 action_object=feedbackrequest.attachment,
        #                 target=feedbackrequest.attachment.todo,
        #                 content='for attachment "{attachment}" - "{todo}" is {status}'.format(attachment=feedbackrequest.attachment.filename, todo=feedbackrequest.attachment.todo.name, status=feedbackrequest.attachment.todo.display_status),
        #                 assigned_to=feedbackrequest.assigned_by)

        if feedbackrequest and feedbackrequest.status == FEEDBACK_STATUS.closed:
            verb = '{assigned_by} closed the feedback request assigned to them'.format(assigned_by=feedbackrequest.assigned_by.get_full_name(), )
            action.send(feedbackrequest.assigned_by,
                        verb=verb,
                        action_object=feedbackrequest.attachment,
                        target=feedbackrequest.attachment.todo,
                        content=feedbackrequest.comment,
                        detail_statement='for attachment "{attachment}" - "{todo}" is {status}'.format(attachment=feedbackrequest.attachment.filename, todo=feedbackrequest.attachment.todo.name, status=feedbackrequest.attachment.todo.display_status),
                        attachment=feedbackrequest.attachment.filename,
                        todo=feedbackrequest.attachment.todo.name,
                        status=feedbackrequest.attachment.todo.display_status)


@receiver(post_save, sender=FeedbackRequest, dispatch_uid='feedbackrequest.status_change')
def feedbackrequest_status_change(sender, **kwargs):
    feedback_request = kwargs.get('instance')
    logger.debug('Starting ToDoAttachmentFeedbackRequestStatusService todo.status: {status}'.format(status=feedback_request.attachment.todo.display_status))
    service = ToDoAttachmentFeedbackRequestStatusService(feedback_request=feedback_request)
    service.process()


@receiver(pre_save, sender=ToDo, dispatch_uid='todo.status_change')
def todo_item_status_change(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.pk is not None:

        if instance.user is not None:

            # we have an existing item
            prev_instance = ToDo.objects.get(pk=instance.pk)

            if prev_instance.status != instance.status:

                event_action = TODO_STATUS_ACTION[instance.status]
                verb = '{user} {action} {name}'.format(name=instance.name, action=event_action, user=instance.user.get_full_name())

                action.send(instance.user,
                            verb=verb,
                            action_object=instance,
                            target=instance,
                            content=None,
                            instance_status=instance.status,
                            instance_dispay_status=instance.display_status,
                            event_action=event_action,
                            event='todo.status_change')


"""
Action Created Events - which is involked everytime action.send is called
@PRIMARY HANDLER
"""
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

                event = action.data.get('event', 'action.created')

                pusher_service = PusherPublisherService(channel=target.pusher_id, event=event)

                user_name = action.actor.get_full_name()
                user_email = action.actor.email

                info_object = Bunch(name=user_name,
                                        verb=action.verb,
                                        target_name=unicode(action),
                                        timestamp='',
                                        **action.data)

                pusher_service.process(label=action.verb, comment=action.verb, **info_object)

                recipients = None
                url = None

                if type(action.target) == ToDo:
                    logger.debug('action.target is a ToDo object')
                    recipients = action.target.project.notification_recipients()
                    url = action.target.get_absolute_url()

                if recipients:
                    logger.debug('recipients: {recipients}'.format(recipients=recipients))
                    email = NewActionEmailService(subject=action.verb, from_name=user_name, from_email=user_email, recipients=recipients)
                    email.send(url=url, message=action.verb)
