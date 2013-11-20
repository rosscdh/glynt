# -*- coding: utf-8 -*-
"""
Feedback Request Change Events
"""
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed

from actstream import action

from glynt.apps.todo import FEEDBACK_STATUS
from glynt.apps.todo.models import FeedbackRequest

from glynt.apps.todo.services import ToDoAttachmentFeedbackRequestStatusService

import logging
logger = logging.getLogger('django.request')


@receiver(m2m_changed, sender=FeedbackRequest.assigned_to.through, dispatch_uid='feedbackrequest.created')
def feedbackrequest_created(sender, **kwargs):
    # please note the pk_set check here
    # this is required in order to catch the m2m model change
    # so we get access to the assigned_to.all() object
    if kwargs.get('action') == 'post_add' and kwargs.get('pk_set') is not None:
        #is_new = kwargs.get('created', False)
        feedbackrequest = kwargs.get('instance')

        assigned = {'from': feedbackrequest.assigned_by.pk, 'to': [t.pk for t in feedbackrequest.assigned_to.all()]}

        if feedbackrequest and feedbackrequest.status == FEEDBACK_STATUS.open:
            assigned_to = feedbackrequest.primary_assigned_to.get_full_name()
            verb = '{assigned_by} requested feedback from {assigned_to} on checklist item {todo} for {project}'.format(assigned_by=feedbackrequest.assigned_by.get_full_name(), assigned_to=assigned_to, todo=feedbackrequest.attachment.todo, project=feedbackrequest.attachment.project)
            action.send(feedbackrequest.assigned_by,
                        verb=verb,
                        action_object=feedbackrequest.attachment,
                        target=feedbackrequest.attachment.todo,
                        content=feedbackrequest.comment,
                        detail_statement='for attachment "{attachment}" - "{todo}" is {status}<br/>'.format(attachment=feedbackrequest.attachment.filename, todo=feedbackrequest.attachment.todo.name, status=feedbackrequest.attachment.todo.display_status),
                        attachment=feedbackrequest.attachment.filename,
                        todo=feedbackrequest.attachment.todo.name,
                        status=feedbackrequest.attachment.todo.display_status,
                        assigned=assigned,
                        event='feedbackrequest.opened')

        if feedbackrequest and feedbackrequest.status == FEEDBACK_STATUS.closed:
            verb = '{assigned_by} closed the feedback request that was assigned to them on checklist item {todo} for {project}'.format(assigned_by=feedbackrequest.assigned_by.get_full_name(), todo=feedbackrequest.attachment.todo, project=feedbackrequest.attachment.project)
            action.send(feedbackrequest.assigned_by,
                        verb=verb,
                        action_object=feedbackrequest.attachment,
                        target=feedbackrequest.attachment.todo,
                        content=feedbackrequest.comment,
                        detail_statement='for attachment "{attachment}" - "{todo}" is {status}'.format(attachment=feedbackrequest.attachment.filename, todo=feedbackrequest.attachment.todo.name, status=feedbackrequest.attachment.todo.display_status),
                        attachment=feedbackrequest.attachment.filename,
                        todo=feedbackrequest.attachment.todo.name,
                        status=feedbackrequest.attachment.todo.display_status,
                        assigned=assigned,
                        event='feedbackrequest.closed')

        if feedbackrequest and feedbackrequest.status == FEEDBACK_STATUS.cancelled:
            verb = '{assigned_by} cancelled their feedback request on checklist item {todo} for {project}'.format(assigned_by=feedbackrequest.assigned_by.get_full_name(), todo=feedbackrequest.attachment.todo, project=feedbackrequest.attachment.project)
            action.send(feedbackrequest.assigned_by,
                        verb=verb,
                        action_object=feedbackrequest.attachment,
                        target=feedbackrequest.attachment.todo,
                        content=feedbackrequest.comment,
                        detail_statement='for attachment "{attachment}" - "{todo}" is {status}'.format(attachment=feedbackrequest.attachment.filename, todo=feedbackrequest.attachment.todo.name, status=feedbackrequest.attachment.todo.display_status),
                        attachment=feedbackrequest.attachment.filename,
                        todo=feedbackrequest.attachment.todo.name,
                        status=feedbackrequest.attachment.todo.display_status,
                        assigned=assigned,
                        event='feedbackrequest.cancelled')


@receiver(post_save, sender=FeedbackRequest, dispatch_uid='feedbackrequest.status_change')
def feedbackrequest_status_change(sender, **kwargs):
    feedback_request = kwargs.get('instance')
    logger.debug('Starting ToDoAttachmentFeedbackRequestStatusService todo.status: {status}'.format(status=feedback_request.attachment.todo.display_status))
    service = ToDoAttachmentFeedbackRequestStatusService(feedback_request=feedback_request)
    service.process()
