# -*- coding: utf-8 -*-
""" Set of signals to handle when comments are posted and assigning notifications to the user """
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.models import LogEntry

from threadedcomments.models import ThreadedComment

from notifications import notify

from glynt.apps.utils import generate_unique_slug

from glynt.apps.todo import TODO_STATUS, TODO_STATUS_ACTION, FEEDBACK_STATUS

from glynt.apps.todo.tasks import delete_attachment
from glynt.apps.todo.models import ToDo, Attachment, FeedbackRequest
from glynt.apps.todo.services import (CrocdocAttachmentService, ToDoStatusService,
                                      ToDoAttachmentFeedbackRequestStatusService)
from glynt.apps.project.models import Project, ProjectLawyer

from actstream import action
from actstream.models import Action

from bunch import Bunch

import logging
logger = logging.getLogger('django.request')


def get_todo_info_object(todo):
    return {
        'instance': {
            'pk': todo.pk,
            'slug': todo.slug,
            'name': todo.name,
            'category': todo.category,
            'project': {'pk': todo.project.pk},
            'display_status': todo.display_status,
            'status': todo.status,
            'is_deleted': todo.is_deleted,
            'uri': todo.get_absolute_url(),
        }
    }


def is_sort_order_update(**kwargs):
    update_fields = kwargs.get('update_fields', frozenset())

    # if we have a specific update that is the sort_position changed update
    # then do nothing
    if type(update_fields) is frozenset and len(update_fields) == 1 and 'sort_position' in update_fields:
        # Do absolutely nothing
        return True
    return False

def is_data_field_update(**kwargs):
    update_fields = kwargs.get('update_fields', frozenset())

    # if we have a specific update that is the sort_position changed update
    # then do nothing
    if type(update_fields) is frozenset and len(update_fields) == 1 and 'data' in update_fields:
        # Do absolutely nothing
        return True
    return False


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

            todo = attachment.todo
            todostatus_service = ToDoStatusService(todo_item=todo)
            todostatus_service.process()

            # increment the attachment count
            todo.num_attachments_plus()

            verb = u'{name} uploaded an attachment: "{filename}" on the checklist item {todo} for {project}'.format(name=attachment.uploaded_by.get_full_name(), filename=attachment.filename, todo=attachment.todo, project=attachment.project).encode('utf-8')
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

    if not isinstance(sender, LogEntry):

        if attachment:
            try:
                todo = attachment.todo
                # decrement num_attachments
                todo.num_attachments_minus()  # increment the attachment count
            except:
                logger.info('todo does not exist for on_attachment_deleted')

            delete_attachment(is_new=is_new, attachment=attachment, **kwargs)

            try:
                verb = u'{name} deleted attachment: "{filename}" on the checklist item {todo} for {project}'.format(name=attachment.uploaded_by.get_full_name(), filename=attachment.filename, todo=attachment.todo, project=attachment.project).encode('utf-8')
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

"""
Comment Events
"""


@receiver(post_save, sender=ThreadedComment, dispatch_uid='todo.comment.created')
def on_comment_created(sender, **kwargs):
    """
    Handle Creation of attachments
    @TODO: This needs to be abstracted!
    @CODESMELL
    """
    if not isinstance(sender, LogEntry):
        send = False
        is_new = kwargs.get('created', False)
        comment = kwargs.get('instance')
        extra = {}

        if comment and is_new:
            content_object_type = type(comment.content_object)
            logger.debug('New Comment on object type: {content_object_type}'.format(content_object_type=content_object_type))

            # If its a comment on a ToDo Object
            if content_object_type == ToDo:
                send = True
                target = todo = comment.content_object
                event = 'todo.comment.created'
                verb = u'{name} commented on checklist item {todo} for {project}'.format(name=comment.user.get_full_name(), project=todo.project, todo=todo.name).encode('utf-8')

                # update the ToDo Status as its been interacted with
                todostatus_service = ToDoStatusService(todo_item=todo)
                todostatus_service.process()

            elif content_object_type == Project:
                send = True
                target = project = comment.content_object
                event = 'project.comment.created'
                verb = u'{name} commented on the {project} project'.format(name=comment.user.get_full_name(), project=project).encode('utf-8')
                extra.update({
                    'url': comment.absolute_deeplink_url()  # append url to the comment deeplink
                })

            elif content_object_type == ProjectLawyer:
                send = True
                target = comment_target = comment.content_object
                event = 'project.lawyer_engage.comment.created'
                verb = u'{name} commented on the Lawyer Engagement conversation for {project}'.format(name=comment.user.get_full_name(), project=comment_target.project).encode('utf-8')

                # notify the lawyer (used for discussion counts)
                if comment.user.profile.is_customer:
                    recipient = comment.content_object.lawyer.user
                else:
                    recipient = comment.content_object.project.customer.user
                # send notification
                notify.send(comment.user, recipient=recipient, verb=u'added to discussion', action_object=comment_target.project,
                    description=comment.comment, target=comment_target.project, project_action='added_discussion_item', project_pk=comment_target.project.pk, creating_user_pk=comment.user.pk)

        if send is True:
            logger.debug(u'send action: {event} {verb} content: {content}'.format(event=event, verb=verb, content=comment.comment).encode('utf-8'))
            action.send(comment.user,
                        verb=verb,
                        action_object=comment,
                        target=target,
                        content=comment.comment,
                        event=event,
                        **extra)

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

        assigned = {'from': feedbackrequest.assigned_by.pk, 'to': [t.pk for t in feedbackrequest.assigned_to.all()]}

        if feedbackrequest and feedbackrequest.status == FEEDBACK_STATUS.open:
            assigned_to = feedbackrequest.primary_assigned_to.get_full_name()
            verb = u'{assigned_by} requested feedback from {assigned_to} on checklist item {todo} for {project}'.format(assigned_by=feedbackrequest.assigned_by.get_full_name(), assigned_to=assigned_to, todo=feedbackrequest.attachment.todo, project=feedbackrequest.attachment.project).encode('utf-8')
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


@receiver(post_save, sender=ProjectLawyer, dispatch_uid='projectlawyer.assigned')
def projectlawyer_assigned(sender, **kwargs):
    """
    On save of a ProjectLawyer instance where the status is ASSIGNED
    Set all the todos.user of that project to the lawyer
    excluding those todos that already have a user
    """
    instance = kwargs.get('instance')

    if instance.status == ProjectLawyer._LAWYER_STATUS.assigned:
        logger.info('Assigned Lawyer: {lawyer} to Project: {project}'.format(lawyer=instance.lawyer, project=instance.project))
        instance.project.todo_set.filter(user=None).update(user=instance.lawyer.user)


@receiver(post_delete, sender=ProjectLawyer, dispatch_uid='projectlawyer.delete')
def projectlawyer_deleted(sender, **kwargs):
    """
    On delete of a ProjectLawyer instance
    Set all the todos.user of that project to None
    where those todos.user == instance.lawyer
    """
    instance = kwargs.get('instance')
    try:
        logger.info('Deleted Lawyer: {lawyer} to Project: {project}'.format(lawyer=instance.lawyer, project=instance.project))
        instance.project.todo_set.filter(user=instance.lawyer.user).update(user=None)
    except:
        pass


@receiver(post_save, sender=ToDo, dispatch_uid='todo.item_crud')
def todo_item_crud(sender, **kwargs):
    from glynt.apps.services.pusher import PusherPublisherService

    is_new = kwargs.get('created', False)
    instance = kwargs.get('instance')

    if is_sort_order_update(**kwargs) is False and is_data_field_update(**kwargs) is False:

        info_object = get_todo_info_object(todo=instance)
        pusher_service = PusherPublisherService(channel=instance.project.pusher_id, event='todo.post_save')

        if is_new is True:
            pusher_service.event = 'todo.is_new'
            comment = label = 'Created new item "{name}"'.format(name=instance.name)

        elif instance.is_deleted is True:
            pusher_service.event = 'todo.is_deleted'
            comment = label = 'Deleted "{name}"'.format(name=instance.name)

        else:
            pusher_service.event = 'todo.is_updated'
            comment = label = 'Updated "{name}"'.format(name=instance.name)

        pusher_service.process(label=label, comment=comment, **info_object)


@receiver(pre_save, sender=ToDo, dispatch_uid='todo.status_change')
def todo_item_status_change(sender, **kwargs):
    instance = kwargs.get('instance')

    if instance.pk is None:

        # ensure the slug is present
        if instance.slug in [None, '']:
            instance.slug = generate_unique_slug(instance=instance)

            # @BUSINESSRULE ensure we have a sort_position
            if not instance.sort_position:
                instance.sort_position = instance.project.todo_set.all().count() + 1

            # @BUSINESSRULE ensure we have a sort_position_by_cat
            if not instance.sort_position_by_cat:
                instance.sort_position_by_cat = instance.sort_position

    else:

        if instance.user is not None:

            # we have an existing item
            prev_instance = ToDo.objects.get(pk=instance.pk)

            if prev_instance.status != instance.status:

                event_action = TODO_STATUS_ACTION[instance.status]
                verb = '{user} {action} the checklist item "{name}"'.format(name=instance.name, action=event_action, user=instance.user.get_full_name())

                action.send(instance.user,
                            verb=verb,
                            action_object=instance,
                            target=instance,
                            content=None,
                            event_action=event_action,
                            event='todo.status_change',
                            **get_todo_info_object(todo=instance))

                if instance.status in [TODO_STATUS.closed, TODO_STATUS.resolved]:
                    """
                    @BUSINESS RULE Update the FeedbackRequest objects that are currently open to closed
                    """
                    FeedbackRequest.objects.close_by_todo(todo=instance)


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
        from glynt.apps.services.email import NewActionEmailService
        from glynt.apps.services.pusher import PusherPublisherService

        is_new = kwargs.get('created', False)
        action = kwargs.get('instance')
        target = action.target

        if action and is_new:

            event = action.data.get('event', 'action.created')

            user_name = action.actor.get_full_name()
            user_email = action.actor.email

            info_object = Bunch(name=user_name,
                                verb=action.verb,
                                target_name=unicode(action),
                                timestamp='',
                                **action.data)

            # if the target has a project attached to it
            if hasattr(target, 'pusher_id'):
                if hasattr(target, 'project'):
                    # send the same event to the project channel
                    # so that the other project channel subscribers
                    # can hear it
                    channels = [target.project.pusher_id, target.pusher_id]
                    pusher_service = PusherPublisherService(channel=channels, event=event)
                else:
                    pusher_service = PusherPublisherService(channel=target.pusher_id, event=event)

                pusher_service.process(label=action.verb, comment=action.verb, **info_object)

            recipients = None
            url = None

            target_type = type(target)

            if target_type == Project:
                logger.debug('action.target is a Project object')
                project = target
                recipients = project.notification_recipients()
                url = action.data.get('url', project.get_absolute_url())

            elif target_type == ProjectLawyer:
                logger.debug('action.target is a ProjectLawyer object')
                project = target.project
                recipients = target.notification_recipients()
                url = action.data.get('url', project.get_absolute_url()) # @TODO need to change this to be the actual engagement element link and write a js trigger to show the modal

            elif target_type == ToDo:
                logger.debug('action.target is a ToDo object')
                project = action.target.project
                recipients = project.notification_recipients()
                url = action.data.get('url', target.get_absolute_url())  # get the todos absolute url

            if recipients:
                logger.debug('recipients: {recipients}'.format(recipients=recipients))

                email = NewActionEmailService(
                    verb=event,
                    from_name=user_name,
                    from_email=user_email,
                    recipients=recipients,
                    actor=action.actor,
                    target=target,
                    project=project,
                    **action.data  # append kwargs sent in via: https://django-activity-stream.readthedocs.org/en/latest/data.html
                )
                email.send(url=url, message=action.verb)
